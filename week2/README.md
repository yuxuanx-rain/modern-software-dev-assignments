# Drive Document Assistant

A local stdio MCP server that searches Google Doc titles, reads text and previews
then applies one exact text replacement. The OAuth developer project and the
Google account granting access can be different: API access follows the latter
account's existing file permissions.

## Setup

From the repository root, using Python 3.12:

```sh
python3 -m venv week2/.venv
week2/.venv/bin/python -m pip install -r week2/requirements.txt
cp week2/.env.example week2/.env
chmod 600 week2/.env
```

Enable Google Drive API and Google Docs API in your Google Cloud project. Create
a Desktop app OAuth client, configure the consent screen and add the intended
Google account as a test user. Workspace administrators can restrict third-party
apps. Put client credentials in the ignored `.env`, never in a committed file.
Set an absolute private token path; list only explicitly approved document IDs in
`GOOGLE_WRITE_DOCUMENT_IDS`. An empty allowlist disables all document writes.

Authorize explicitly, choosing the account that has the desired file access:

```sh
week2/.venv/bin/python week2/auth.py
```

If the server uses an external env/cache path, run authorization with those same
values and its installed interpreter, for example:

```sh
GOOGLE_ENV_FILE=/absolute/private/credentials.env GOOGLE_TOKEN_PATH=/absolute/private/token.json /absolute/venv/bin/python week2/auth.py
```

Start the server with this single command:

```sh
week2/.venv/bin/python week2/server.py
```

The server speaks MCP on stdin/stdout; use an MCP client to interact with it.
Copy `.mcp.json.example` into your client's real configuration, replace its
absolute paths and document ID placeholders, and keep that real file ignored.
Claude Code can load it using `--mcp-config /absolute/private/config.json`.

On this machine the Desktop directory is managed by iCloud, and dependency reads
stalled there. The verified demonstrations used an equivalent virtual environment
at `/private/tmp/cs146s-week2-venv`, installed from this same requirements file,
with source still in `week2/`. Private env/token files and bytecode cache were also
kept outside iCloud. The demonstrated start command was:

```sh
/private/tmp/cs146s-week2-venv/bin/python week2/server.py
```

The example config's interpreter path should point to your own installed virtual
environment. Temporary runtime directories may need recreation after reboot.

## Workflow and boundaries

1. `search_documents` returns `doc_id`, title, edit capability and pagination.
2. `read_document(doc_id)` returns text, `tab_id` and revision information.
3. `preview_document_update` requires an allowlisted document and exactly one
   occurrence of the old text in the selected tab. Show its before/after to the user.
4. After approval, `apply_document_update(preview_id)` checks the revision and
   performs the replacement and compares the entire selected tab's text with the
   expected result. Previews expire after ten minutes and are single use.
   An explicit request can already authorize the exact change; a redundant
   confirmation pause is not required. The preview step itself remains mandatory.

Title search is not semantic full-text search. `shared_with_me` is not an inventory
of organizational Shared Drives. This version does not enumerate Shared Drives;
the selected metadata scope does not permit that endpoint. Accessible-file search
requests inclusion of shared-drive files, but no organizational Shared Drive file
has been verified live. Text extraction covers paragraphs and table cells, not
images, comments, headers/footers or formatting. Only native Google Docs are supported.

Token refresh is silent. Invalid/revoked credentials return `AUTH_REQUIRED`; run
the explicit auth command yourself. A tool call never opens an authorization
browser. Errors identify whether retry is appropriate. An uncertain write outcome
requires a read to inspect the result, never a blind retry.

Scopes: `drive.metadata.readonly` for title/ID/access metadata;
`documents` for reading and updating native Google Docs. Google has no dedicated
read-plus-update Docs scope excluding deletion; this server exposes no document
deletion tool and limits writes locally to the configured allowlist.
Google's narrower `drive.file` alternative grants access only to files created or
selected/opened with this app, rather than arbitrary existing Docs returned by
account-wide title search. A Picker-based per-file product would use that alternative;
this project deliberately searches and reads existing account-accessible Docs.
The local write allowlist is an application restriction, not an OAuth per-file grant.

## Tests

```sh
week2/.venv/bin/python -m pytest week2/test_protocol.py week2/test_oauth.py -q
```

Tests use synthetic documents through MCP, including a real stdio subprocess.
They do not prove live OAuth or real Google mutations; those require separate
demonstration evidence in the write-up.
