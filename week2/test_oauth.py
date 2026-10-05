"""Boundary tests with synthetic tokens and HTTP responses, never real secrets."""
import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from google.auth.exceptions import RefreshError, TransportError
from google.oauth2.credentials import Credentials

from drive_api import APIError, GoogleAPI


def utc_naive():
    # Google-auth compares against naive UTC internally.
    return datetime.now(timezone.utc).replace(tzinfo=None)


def configured(monkeypatch, tmp_path):
    monkeypatch.setenv('GOOGLE_TOKEN_PATH', str(tmp_path / 'token.json'))
    monkeypatch.setenv('GOOGLE_ENV_FILE', str(tmp_path / 'missing.env'))
    api = GoogleAPI()
    api.credentials = Credentials('synthetic', refresh_token='synthetic-refresh',
        token_uri='https://oauth2.googleapis.com/token', client_id='synthetic-id',
        client_secret='synthetic-secret', expiry=utc_naive() - timedelta(seconds=10))
    return api


def test_expired_token_refresh_is_cached_privately(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    calls = []
    def refresh(self, request):
        calls.append(True)
        self.token = 'synthetic-new'
        self.expiry = utc_naive() + timedelta(hours=1)
    monkeypatch.setattr(Credentials, 'refresh', refresh)
    assert api._token() == 'synthetic-new'
    assert api._token() == 'synthetic-new'
    assert len(calls) == 1
    assert json.loads(api.cache.read_text())['token'] == 'synthetic-new'
    assert api.cache.stat().st_mode & 0o777 == 0o600


def test_revoked_token_returns_actionable_error(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    def refresh(self, request):
        raise RefreshError('synthetic-invalid-grant')
    monkeypatch.setattr(Credentials, 'refresh', refresh)
    with pytest.raises(APIError) as caught:
        api._token()
    assert caught.value.payload['error'] == 'AUTH_REQUIRED'
    assert not caught.value.payload['retryable']
    assert 'explicitly' in caught.value.payload['next_step']
    assert api.credentials is None


def test_refresh_network_failure_does_not_demand_login(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    def refresh(self, request):
        raise TransportError('synthetic-network-failure')
    monkeypatch.setattr(Credentials, 'refresh', refresh)
    with pytest.raises(APIError) as caught:
        api._token()
    assert caught.value.payload['error'] == 'AUTH_NETWORK_ERROR'
    assert caught.value.payload['retryable']
    assert api.credentials is not None


def test_query_escapes_quotes_and_backslashes(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    captured = {}
    def request(method, path, *, params=None):
        captured.update(params)
        return {'files': []}
    monkeypatch.setattr(api, 'request', request)
    api.search("O'Brien\\notes", 'accessible', None, 10, None)
    assert "O\\'Brien\\\\notes" in captured['q']


def test_transient_refresh_error_is_retryable(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    def refresh(self, request):
        raise RefreshError('synthetic-provider-unavailable', retryable=True)
    monkeypatch.setattr(Credentials, 'refresh', refresh)
    with pytest.raises(APIError) as caught:
        api._token()
    assert caught.value.payload['error'] == 'AUTH_NETWORK_ERROR'
    assert caught.value.payload['retryable']
    assert api.credentials is not None


def test_second_401_clears_memory_and_reloads_new_authorization(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    tokens = []
    def refresh(self, request):
        self.expiry = utc_naive() + timedelta(hours=1)
    monkeypatch.setattr(Credentials, 'refresh', refresh)
    def response(method, url, **kwargs):
        tokens.append(kwargs['headers']['Authorization'])
        return httpx.Response(401 if len(tokens) <= 2 else 200, json={'title':'Reauthorized'})
    monkeypatch.setattr(api.http, 'request', response)
    with pytest.raises(APIError) as caught:
        api.document('doc1')
    assert caught.value.payload['error'] == 'AUTH_REQUIRED'
    assert api.credentials is None
    monkeypatch.setenv('GOOGLE_CLIENT_ID', 'synthetic-id')
    monkeypatch.setenv('GOOGLE_CLIENT_SECRET', 'synthetic-secret')
    renewed = Credentials('synthetic-renewed', refresh_token='synthetic-refresh',
        token_uri='https://oauth2.googleapis.com/token', client_id='synthetic-id',
        client_secret='synthetic-secret', expiry=utc_naive() + timedelta(hours=1))
    api.cache.write_text(renewed.to_json())
    assert api.document('doc1')['title'] == 'Reauthorized'
    assert tokens == ['Bearer synthetic', 'Bearer synthetic', 'Bearer synthetic-renewed']


def test_rate_limit_returns_delay_and_retry_advice(monkeypatch, tmp_path):
    api = configured(monkeypatch, tmp_path)
    monkeypatch.setattr(api, '_token', lambda **kwargs:'synthetic')
    monkeypatch.setattr(api.http, 'request', lambda *a, **k: httpx.Response(
        429, headers={'Retry-After':'42'}, json={'error':{'message':'private-provider-body'}}))
    with pytest.raises(APIError) as caught:
        api.document('doc1')
    assert caught.value.payload['error'] == 'RATE_LIMITED'
    assert caught.value.payload['retry_after_seconds'] == 42
    assert caught.value.payload['retryable']
    assert 'private-provider-body' not in json.dumps(caught.value.payload)


@pytest.mark.parametrize('method,expected,retryable', [
    ('GET', 'NETWORK_ERROR', True), ('POST', 'WRITE_OUTCOME_UNKNOWN', False)])
def test_uncertain_write_is_not_retryable(monkeypatch, tmp_path, method, expected, retryable):
    api = configured(monkeypatch, tmp_path)
    monkeypatch.setattr(api, '_token', lambda **kwargs: 'synthetic')
    def fail(*args, **kwargs):
        raise httpx.ReadTimeout('synthetic')
    monkeypatch.setattr(api.http, 'request', fail)
    with pytest.raises(APIError) as caught:
        api.request(method, 'documents/doc1')
    assert caught.value.payload['error'] == expected
    assert caught.value.payload['retryable'] is retryable
