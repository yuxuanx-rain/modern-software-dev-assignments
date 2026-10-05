# Week 2 Write-up

Development used Codex assistance; the demonstrations below used real Claude Code
and Google API responses. Synthetic tests are labeled separately. Course staff
allow AI assistance provided the student understands and can stand behind the work
([AI policy](https://edstem.org/us/courses/106077/discussion/8328490)).

## Part I: The Server

**API chosen, and why:** Google Drive metadata and Google Docs API. I use a
Stanford Google account and want to find shared documents and make targeted edits.
The personal-account OAuth developer project is separate from the Stanford account
that grants file access. Google continues to enforce that account's file permissions.

I read the reference MCP Git server implementation before writing this server.
This implementation uses FastMCP 2.14.5 and stdio, with four composing tools.

**How to run it**, after the setup and explicit authorization in `README.md`:
```sh
week2/.venv/bin/python week2/server.py
```
The actual demonstrations used `/private/tmp/cs146s-week2-venv/bin/python
week2/server.py`, with dependencies installed from the same requirements file.
This avoids iCloud on-demand dependency reads on this machine; source remains in
`week2/`. The real config points to that interpreter and private env/token files
outside iCloud. See the README for the runtime alternative.

| Tool | What it does | Read/Write | Composes with |
|---|---|---|---|
| search_documents | Native Doc title search, pagination and account/folder filters | Read | Returns doc_id for read_document |
| read_document | Bounded plain text, tab IDs and revision | Read | Returns doc_id and tab_id for preview |
| preview_document_update | Checks one exact replacement; stores ten-minute preview | Local state only | Returns preview_id for apply |
| apply_document_update | Consumes preview; guarded Google Docs replacement and readback | Real write | Uses preview_id; conflicts require another read/preview |

A live stdio MCP test performed the real write, not just a mock: it replaced the
feasibility-test sentence with “CS146S MCP protocol test: preview and guarded
document update succeeded.” Google reported one changed occurrence and readback
verified it. The test also reread before apply to confirm preview had not changed
the document. Full arguments/results: `evidence/live-protocol-transcript.json`.
This was developer-driven protocol verification, distinct from the agent transcript.

## Part II: Agent Ergonomics

| Decision | Where | Why |
|---|---|---|
| Schema constraints | server.py:14, server.py:150, server.py:216 | Document ID rejects URLs; tab ID allows Google's t.0 format; scope is a Literal; page size 1–50; bounded text/output; strict protocol validation rejects type coercion and additional arguments |
| Output shaping | drive_api.py:141, server.py:65 | Search keeps ID/title/edit capability/link/pagination, dropping raw API structure; read keeps tab text/IDs/revision, omitting images and formatting |
| Structured errors | drive_api.py:89, server.py:46 | MCP ToolError carries JSON with error/message/retryable/next_step; read network failures differ from uncertain writes; provider error bodies and secrets are not exposed |
| Chaining docstrings | server.py:180, server.py:192, server.py:206 | State which preceding tool supplies each ID, and that doc_id is not a URL |
| Write brake | server.py:83, server.py:114 | Explicit write allowlist, preview/apply split, expiry and single-use preview, current-revision check and Google's requiredRevisionId guard; exact full-tab readback prevents substring false positives |
| Cross-tool guidance | server.py:150 | Explain approval, conflicts, uncertain writes, account/scope boundaries and untrusted document text; an already authorized exact change need not prompt again |

**One thing changed after watching the agent misuse a tool:**
The controlled failure prompt deliberately asked the agent to use a made-up ID,
not one returned by search. It actually called
`read_document({"doc_id":"nonexistent-cs146s-test-document"})` and received a
non-retryable error. After observing that invalid-ID use, I changed the recovery
contract to return `source_tool: "search_documents"` and `possible_causes` directly
in the error data. I also clarified the read docstring: this error alone does not
prove deletion or an invalid ID. The initial run and post-improvement run are
`evidence/claude-failure-transcript.json` and
`evidence/claude-failure-after-improvement.json`. The latter verifies the new fields
and actual search/read recovery. This misuse was deliberately provoked, not an
unprompted mistake.

There was also a genuine discovery problem: the agent's first ToolSearch query
`{"query":"drive-docs read search document","max_results":5}` returned unrelated
tools such as TaskOutput and EnterPlanMode. It recovered with
`{"query":"+drive read_document search_documents","max_results":5}`. I strengthened
the first lines of all four docstrings with explicit “Google Drive” / “Google Docs”
provider labels to make discovery less ambiguous. This observation is preserved
in the initial failure transcript; better ranking is not guaranteed from one run.

Earlier startup experiments produced confident document claims without any actual
MCP tool_use/tool_result events. I rejected those runs as evidence, corrected the
client tool settings/runtime, and required real linked calls/results before accepting
a transcript. Those experiments are not presented as successful API interactions.

## Part III: OAuth

**Flow:** `auth.py:12` uses authorization code with PKCE and a localhost callback.
The CLI explicitly opens the browser; tools never invoke it. Private cache writes
are atomic and mode 0600 (`drive_api.py:32`). `drive_api.py:58` loads cached
credentials and silently refreshes expired access tokens. A 401 triggers one refresh
and retry; invalid/revoked refresh credentials return AUTH_REQUIRED. Refresh
transport failures return retryable AUTH_NETWORK_ERROR, avoiding needless sign-in.

The preliminary live Stanford check verified code exchange, refresh-token receipt,
silent refresh, shared-with-me metadata query and a created test Doc's write/readback.
The sanitized report is `evidence/oauth-feasibility.json`. Subsequent live protocol
and Claude calls used the cached authorization without another browser login.

**Scopes requested:**
- `drive.metadata.readonly`: search titles and return IDs, metadata and edit capability.
- `documents`: read native Docs and update text. Google has no narrow Docs
  read-plus-update scope excluding deletion. This server exposes no deletion tool;
  writes are limited to explicitly allowlisted documents.

I considered Google's narrower `drive.file` scope, which covers files created or
selected/opened with an app (for example through Google Picker). It would not let
this client read arbitrary existing Docs discovered by account-wide title search.
The `documents` scope is the Docs-specific write scope for that chosen workflow;
`drive` and `drive.readonly` would unnecessarily cover other file types and content.
The allowlist restricts this application's writes; it does not narrow Google's
OAuth consent grant. Sources: [Docs scopes](https://developers.google.com/workspace/docs/api/auth)
and [Drive per-file scope](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).

The metadata scope cannot call `drives.list` (live probe returned 403). Broader
`drive`/`drive.readonly` scopes were not added. `shared_with_me` is not organizational
Shared Drive enumeration; no actual organizational Shared Drive document is claimed
as tested. Title search requests inclusion of accessible shared-drive files, but
this is not a guarantee of complete coverage.

**Secrets:** client ID/secret come from environment variables or ignored env files.
This installation keeps private env/token files outside the repository. The root
`.gitignore` excludes the real project `.mcp.json`; `week2/.gitignore` excludes local
env/config, token/client downloads, private data, venv and Python caches. The env
and MCP examples contain placeholders. No live credentials are intended for commit.

**Token dies mid-session:** the MCP tool returns JSON as an error:
```json
{"error":"AUTH_REQUIRED","message":"Google authorization needs renewal.","retryable":false,"next_step":"Run week2/auth.py explicitly with this server's Python environment, GOOGLE_ENV_FILE and GOOGLE_TOKEN_PATH (see README), then retry. Tools never open a browser."}
```
Run the explicit auth CLI externally to recover. The synthetic revoked-token test
checks this path; the actual account's authorization was not revoked for testing.

## Part IV: Integration

**Registration config/client:** `.mcp.json.example` shows the interpreter, server
path and private env/cache paths. I loaded the ignored real project config with
Claude Code CLI 2.1.163 using `--mcp-config` and `--strict-mcp-config`.
Only this server was loaded. Native file-reading, editing, Bash and web tools were
disallowed during the successful demonstrations. Real calls/results and the final
responses are preserved; thinking, signatures and authentication metadata are omitted.

**End-to-end agent transcript:** full exact prompt and events are in
`evidence/claude-read-transcript.json`. Abbreviated display:
```text
Prompt: Find my Doc titled CS146S OAuth Feasibility Test owned by the authenticated
account; select only the approved test doc_id from search results, then read that
returned doc_id and report its actual sentence. Do not access other documents.

search_documents({"keyword":"CS146S OAuth Feasibility Test","scope":"owned_by_me"})
 -> documents[0].doc_id = 171pt4NrdDlZnOk7sqdxfYhMcgcV_Ja0_NdbmjOQLfDM
 -> title = CS146S OAuth Feasibility Test; can_edit = true
read_document({"doc_id":"171pt4NrdDlZnOk7sqdxfYhMcgcV_Ja0_NdbmjOQLfDM"})
 -> tab_id = t.0
 -> text = CS146S MCP protocol test: preview and guarded document update succeeded.
Agent answered using that actual sentence.
```

**A failure, handled:** deliberately requested a made-up document ID; complete
prompt/events are in `evidence/claude-failure-transcript.json`.
```text
read_document({"doc_id":"nonexistent-cs146s-test-document"})
 -> is_error = true
 -> error = NOT_FOUND_OR_NO_ACCESS; retryable = false
 -> next_step = search for a valid visible ID and check account/sharing
Agent did not retry the same ID.
search_documents({"keyword":"CS146S OAuth Feasibility Test","scope":"owned_by_me"})
 -> returned the approved test doc_id
read_document({"doc_id":"171pt4NrdDlZnOk7sqdxfYhMcgcV_Ja0_NdbmjOQLfDM"})
 -> success; actual sentence returned
```
The original transcript predates the additional machine-readable recovery fields;
the post-improvement run is `evidence/claude-failure-after-improvement.json`.

**Protocol-level tests:**
```sh
week2/.venv/bin/python -m pytest week2/test_protocol.py week2/test_oauth.py -q
```
The final local verification used the documented alternative interpreter and
returned **22 passed**. `test_protocol.py` covers discovery/schema constraints,
chained search/read/preview/apply, preview without write, replay refusal, revision
conflicts, ambiguity, allowlisting, preview expiry, exact readback (including deletion
and a replacement containing the old text), and a real stdio subprocess's missing-auth error.
Google responses in these automated tests are synthetic. `test_oauth.py` covers
private refresh caching, revoked credentials, refresh-network failures, query
escaping, rate-limit delay, transient refresh failures, clearing stale in-memory
credentials after repeated 401s and reloading an externally renewed cache in the same
process, and safe retry classification. Live evidence is separately labeled above.
The two warnings are upstream Authlib deprecations; tests did not fail.
Final-code live stdio search/read/preview and unchanged readback, without another
Google write, are recorded in `evidence/final-audit-protocol.json`.
The final-source Claude search/read rerun is in
`evidence/final-claude-read-transcript.json`. A separate clean source copy without
real client configuration, credentials or vendored dependencies also passed all
22 tests using the verified dependency environment. `pip check` reported no broken
requirements. See `SUBMISSION_AUDIT.md` for the requirement-to-evidence checklist.

## Submission

The staff explicitly confirmed that a course-repository fork is acceptable
([repo setup clarification](https://edstem.org/us/courses/106077/discussion/8320070)).
The current remotes are `origin` (course) and `fork` (student); pushes must target
`fork`, preserving the already submitted Week 1 work. Staff also clarified that
an effective preview/dry-run is a brake and already authorized writes need no
extra confirmation pause ([write brake clarification](https://edstem.org/us/courses/106077/discussion/8346895)).
Assignment 2 is due October 4, 2026, 11:59 PM Pacific Time, as verified on the
actual Gradescope assignment dashboard and in the
[staff announcement](https://edstem.org/us/courses/106077/discussion/8321771).

The implementation, examples, tests and demonstration evidence are complete.
The authenticated GitHub settings page showed `isaackann` as an accepted
collaborator and existing invitations for `mihail911` and `vdaita`, pending those
recipients' acceptance (`evidence/collaborator-status.json`). This does not claim
all three have accepted. Push the finalized commit to the assignment repository
and submit the repository URL plus the full `git rev-parse HEAD` hash on Gradescope.
Gradescope will be filled and submitted by the student; this write-up does not
claim that step has been performed.
Optional cleanup is to remove the client configuration and revoke/delete cached
authorization; no such cleanup has been performed automatically.
