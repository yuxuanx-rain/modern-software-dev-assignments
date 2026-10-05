"""Google API boundary: private OAuth cache and actionable, sanitized errors."""
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError, TransportError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/documents',
]
BASE = Path(__file__).resolve().parent


def load_environment():
    load_dotenv(os.environ.get('GOOGLE_ENV_FILE', str(BASE / '.env')), override=False)


class APIError(Exception):
    def __init__(self, code, message, next_step, retryable=False, **details):
        self.payload = dict(error=code, message=message, retryable=retryable,
                            next_step=next_step, **details)
        super().__init__(message)


def save_private(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class GoogleAPI:
    def __init__(self):
        load_environment()
        self.credentials = None
        self.cache = Path(os.environ.get('GOOGLE_TOKEN_PATH', str(BASE / '.private/token.json')))
        self.write_ids = frozenset(filter(None, os.environ.get('GOOGLE_WRITE_DOCUMENT_IDS', '').split(',')))
        self.http = httpx.Client(timeout=30.0, follow_redirects=False)

    def _auth_error(self):
        return APIError('AUTH_REQUIRED', 'Google authorization needs renewal.',
                        "Run week2/auth.py explicitly with this server's Python environment, GOOGLE_ENV_FILE and GOOGLE_TOKEN_PATH (see README), then retry. Tools never open a browser.")

    def _token(self, force=False):
        if self.credentials is None:
            try:
                raw = json.loads(self.cache.read_text())
                # Accept the standalone feasibility probe cache once; then save standard format.
                info = dict(raw, client_id=os.environ['GOOGLE_CLIENT_ID'],
                            client_secret=os.environ['GOOGLE_CLIENT_SECRET'])
                if 'token' not in info:
                    info['token'] = info.get('access_token')
                    info['expiry'] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat().replace('+00:00', 'Z')
                self.credentials = Credentials.from_authorized_user_info(info, scopes=SCOPES)
            except (OSError, ValueError, KeyError):
                raise self._auth_error() from None
        if force or not self.credentials.valid:
            try:
                self.credentials.refresh(Request())
                save_private(self.cache, self.credentials.to_json())
            except TransportError:
                raise APIError('AUTH_NETWORK_ERROR', 'Cannot reach Google to refresh authorization.',
                               'Check connectivity, then retry; a new login is not yet required.', True) from None
            except RefreshError as error:
                if error.retryable:
                    raise APIError('AUTH_NETWORK_ERROR', 'Google temporarily could not refresh authorization.',
                                   'Wait and retry; a new login is not yet required.', True) from None
                self.credentials = None
                raise self._auth_error() from None
            except OSError:
                raise APIError('CACHE_ERROR', 'Cannot save the refreshed private token.',
                               'Check GOOGLE_TOKEN_PATH directory permissions; do not paste tokens into chat.') from None
        return self.credentials.token

    def request(self, method, path, *, params=None, body=None):
        base = 'https://docs.googleapis.com/v1/' if path.startswith('documents') else 'https://www.googleapis.com/drive/v3/'
        for attempt in range(2):
            token = self._token(force=attempt == 1)
            try:
                response = self.http.request(method, base + path, params=params, json=body,
                                             headers={'Authorization': 'Bearer ' + token})
            except httpx.RequestError:
                if method != 'GET':
                    raise APIError('WRITE_OUTCOME_UNKNOWN', 'The write response was lost.',
                                   'Read the document to inspect the outcome. Do not automatically retry this write.') from None
                raise APIError('NETWORK_ERROR', 'Google could not be reached.',
                               'Retry the read after checking connectivity.', True) from None
            if response.status_code == 401 and attempt == 0:
                continue
            if response.is_success:
                return response.json()
            try:
                error = response.json().get('error', {})
                reasons = [item.get('reason') for item in error.get('errors', [])]
                status = error.get('status', '')
            except (ValueError, AttributeError):
                reasons, status = [], ''
            if response.status_code == 401:
                self.credentials = None
                raise self._auth_error()
            if response.status_code == 429 or any(r in ('rateLimitExceeded', 'userRateLimitExceeded') for r in reasons):
                delay = response.headers.get('Retry-After', '30')
                raise APIError('RATE_LIMITED', 'Google rate limit reached.',
                               'Wait for retry_after_seconds, then retry the read or re-preview the write.',
                               True, retry_after_seconds=int(delay) if delay.isdigit() else 30)
            if response.status_code == 403 and 'insufficientPermissions' in reasons:
                raise APIError('INSUFFICIENT_SCOPE', 'The authorized scopes do not permit this request.',
                               'Check the documented scopes; do not retry unchanged or silently expand authorization.')
            if response.status_code in (403, 404):
                raise APIError('NOT_FOUND_OR_NO_ACCESS', 'Document not found or this account lacks access.',
                               'Use search_documents to obtain a visible doc_id. Check the account and sharing; this error alone does not distinguish a missing file from denied access.',
                               source_tool='search_documents',
                               possible_causes=['missing_file', 'wrong_account', 'insufficient_file_permission'])
            if response.status_code == 400 and method != 'GET':
                raise APIError('REVISION_CONFLICT_OR_INVALID_WRITE', 'Google rejected the guarded write.',
                               'Read the document and create a fresh preview; do not reuse this preview.')
            if response.status_code >= 500:
                raise APIError('GOOGLE_UNAVAILABLE' if method == 'GET' else 'WRITE_OUTCOME_UNKNOWN',
                               'Google returned a server error.',
                               'Retry the read later.' if method == 'GET' else 'Read to inspect outcome before considering another write.',
                               method == 'GET')
            raise APIError('API_REJECTED', 'Google rejected this request.',
                           'Check arguments and API enablement before retrying.', http_status=response.status_code,
                           google_status=status)
        raise self._auth_error()

    def search(self, keyword, scope, folder_id, page_size, page_token):
        escape = lambda text: text.replace(chr(92), chr(92) * 2).replace("'", chr(92) + "'")
        query = "trashed = false and mimeType = 'application/vnd.google-apps.document'"
        if keyword:
            query += " and name contains '" + escape(keyword) + "'"
        if scope == 'shared_with_me':
            query += ' and sharedWithMe = true'
        elif scope == 'owned_by_me':
            query += " and 'me' in owners"
        if folder_id:
            query += " and '" + escape(folder_id) + "' in parents"
        params = dict(q=query, pageSize=page_size,
                      fields='files(id,name,mimeType,modifiedTime,webViewLink,driveId,capabilities(canEdit)),nextPageToken,incompleteSearch',
                      supportsAllDrives='true', includeItemsFromAllDrives='true', orderBy='modifiedTime desc')
        if page_token:
            params['pageToken'] = page_token
        raw = self.request('GET', 'files', params=params)
        return dict(documents=[dict(doc_id=f['id'], title=f['name'], modified_time=f.get('modifiedTime'),
                         url=f.get('webViewLink'), drive_id=f.get('driveId'), can_edit=f.get('capabilities', {}).get('canEdit', False))
                        for f in raw.get('files', [])], next_page_token=raw.get('nextPageToken'),
                    incomplete_search=raw.get('incompleteSearch', False))

    def document(self, doc_id):
        return self.request('GET', 'documents/' + doc_id, params={'includeTabsContent': 'true'})

    def apply(self, doc_id, tab_id, old, new, revision):
        return self.request('POST', 'documents/' + doc_id + ':batchUpdate', body={
            'writeControl': {'requiredRevisionId': revision},
            'requests': [{'replaceAllText': {'containsText': {'text': old, 'matchCase': True},
                                           'replaceText': new, 'tabsCriteria': {'tabIds': [tab_id]}}}]})
