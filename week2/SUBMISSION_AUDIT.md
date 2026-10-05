# Week 2 pre-submission audit — October 4, 2026

Implementation and evidence checks pass after the corrections below. Commit/push
and Gradescope submission are still pending at this pre-commit audit. Collaborator
status has been verified as described below. This audit
does not predict or guarantee the instructor's score.

## Authorities and work-process rules

- [Current assignment](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week2/assignment.md)
  and [writeup template](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week2/writeup.md).
  Upstream master was checked live: `1f9eedda85eaeddac97fd9871cdfffc1ed644421`,
  already incorporated in this checkout. No new assignment update is missing.
- [Staff AI policy](https://edstem.org/us/courses/106077/discussion/8328490): AI
  assistance is allowed; the student must understand and be able to defend the work.
  This report discloses Codex assistance and separates actual observations from
  synthetic tests. There is no Week 2 page limit in the checked assignment/template.
- [Repo setup guide](https://edstem.org/us/courses/106077/discussion/8303053) and
  [specific fork clarification](https://edstem.org/us/courses/106077/discussion/8320070):
  the staff approved course-repository forks. This student uses `origin` for the
  course and `fork` for the student repository; the destination, rather than the
  arbitrary remote name, matters. Preserve Week 1; push only to `fork`.
- [Staff write-brake clarification](https://edstem.org/us/courses/106077/discussion/8346895):
  an effective dry-run/preview is a brake; an already authorized operation does not
  require a redundant confirmation pause. This server always requires a preview
  token before applying a change and honors an explicit user's existing approval.
- [Assignment 2 announcement](https://edstem.org/us/courses/106077/discussion/8321771)
  and actual Gradescope dashboard: due **October 4, 2026, 11:59 PM Pacific Time**.
  A displayed late-submission window is not treated as an automatic penalty waiver.
- The implementation plan and preliminary OAuth feasibility test preceded server
  implementation. The MCP Git reference was reviewed during development. No
  applicable `AGENTS.md` was found in the repository or its parent directories.
  Shared Drive enumeration is outside the selected product scope and is not a
  required rubric item.

## Rubric checklist

| Requirement | Finding and concrete evidence |
|---|---|
| OAuth 2.0 third-party API | Stanford Google authorization; `auth.py`, `drive_api.py`, `evidence/oauth-feasibility.json` |
| At least three composing tools | Four tools: search → doc ID → read → tab ID → preview → preview ID → apply; protocol-chain test |
| Real state mutation | Actual approved test Doc replacement plus readback in `evidence/live-protocol-transcript.json`; distinct from mock tests |
| Code in week2, stdio, one start command | `server.py` stdio entry; README primary command and demonstrated equivalent interpreter; real stdio subprocess checks |
| Constraints in schemas | Literals, length/range/pattern constraints, additionalProperties=false, strict validation; invalid enum/empty input/range/type/unknown-argument tests |
| Shaped output | Selected metadata and bounded tab text; raw provider payloads are not forwarded |
| Structured actionable errors | JSON ToolError; retry advice distinguishes bad IDs, authorization, rate limits, read failures and uncertain writes; real bad-ID Claude recovery |
| Chaining docstrings and FastMCP instructions | State the preceding tool supplying each ID, workflow and document-content trust boundary |
| Write brake and annotations | Read-only annotations; preview/apply; allowlist; exact match; ten-minute expiry; single-use token; revision guard |
| Authorization-code exchange | Explicit browser CLI with PKCE; real exchange evidence, not a manually pasted bearer token |
| Cached tokens and silent refresh | Private atomic cache; live preliminary refresh; expiration/refresh-cache tests |
| Minimal justified scopes | Metadata read-only plus Docs read/write; writeup explains necessity and why per-file drive.file does not cover arbitrary existing Doc search/read |
| No secrets, env from first feature commit | Env-based source, placeholder examples, ignored actual config/cache; no feature commit yet; actual credential scan has zero matches |
| Mid-session token death | No tool browser launch; revoked-token error, transient-refresh retry classification, 401 refresh-once/reset and same-process new-cache recovery tests |
| Claude Code/Cursor integration | Claude Code CLI with the actual ignored config; placeholder `.mcp.json.example` ready for commit |
| Real chained agent transcript | Prompt, arguments, linked tool results and response in `evidence/claude-read-transcript.json`; final-source rerun in `evidence/final-claude-read-transcript.json` |
| Failure and recovery | Real provoked bad ID → actionable error → search → valid read; original and improved transcripts preserved |
| Change after observed misuse | Writeup explains added source_tool/possible_causes and clarified ID/access contract; post-change recovery trace |
| MCP protocol test | FastMCP client and actual stdio subprocess, not only direct function calls |
| Completed writeup and required files | All four Parts completed; no template placeholder remains; code/examples/tests/evidence under week2 |

## Corrections from this final review

1. Compare the entire selected tab with the expected replacement result. Merely
   finding the new text could falsely pass when it already occurred elsewhere.
   Mismatch returns an explicit status and inspection instructions. Tests include
   deletion, new text containing the old text, and a misleading provider response.
2. Treat retryable Google refresh errors as temporary failures rather than forcing
   another login. Clear stale credentials after a second 401 so explicit external
   reauthorization can recover in the same server process.
3. Enforce schema types without coercion and reject undeclared arguments in the
   published schemas. Tests verify both behavior and advertised constraints.
4. Clarify the narrower drive.file alternative, existing-approval handling, final
   evidence filenames and code references in the report and README.

## Final verification

- **22 tests passed**, including an independent clean source-copy run. That copy
  contained no real `.mcp.json`, env/token files or local virtual environment. It
  used the already verified dependency environment; a new online dependency
  installation was not repeated. Two upstream Authlib deprecation warnings remain.
- `pip check`: no broken requirements.
- Final real stdio search/read/preview: passed; document unchanged; bad-ID recovery
  fields verified. Recorded in `evidence/final-audit-protocol.json`.
- Final real Claude search/read: passed with actual linked MCP events; no write.
- Exact current Google credential values absent from candidate source/evidence;
  JSON evidence parses; real config/env/cache/venv ignored; `git diff --check` passes.
- Week 1 diff against submitted commit
  `55e77ce65edcba5118789d63e0a821719c20e816` is empty. That commit is still the
  student's remote master, so Week 2 has not accidentally been submitted.

## Delivery steps that must still be verified

1. Access/invitations verified for **mihail911, isaackann, vdaita**. The current
   Gradescope Q1 lists two names; the assignment and setup guide list three, so
   satisfy the three-name requirement. The authenticated settings page became
   available and showed isaackann as
   an accepted collaborator and mihail911/vdaita as pending invitations. Both
   remaining recipients must accept themselves. No duplicate invites were sent;
   no passwords were read or stored. See `evidence/collaborator-status.json`.
2. Commit all intended code, examples, tests and evidence, inspecting the actual
   staged content for secrets. Push `master` to the student's **fork**. Confirm the
   new full SHA is present on the remote. The current merge HEAD is not the final
   grading commit because the implementation is still uncommitted.
3. Actual Gradescope Assignment 2 has Q1 repository URL and Q2 full commit SHA from
   `git rev-parse HEAD`. Fill those only after push verification, then verify the
   submitted confirmation. Nothing was entered or submitted during this audit.
4. Removing configuration, deleting tokens and revoking access are optional. No
   automatic cleanup has been performed; it would prevent further live checks.
