# Week 4 final review — 2026-10-25

Sources: instructor [assignment](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/assignment.md) and [writeup template](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/writeup.md), re-read for this review.

## Content requirements

| Requirement | Evidence | Result |
|---|---|---|
| Eligible unfamiliar repository and fork | Instructor-listed Day.js; public yuxuanx-rain/dayjs fork; baseline commit recorded | Pass |
| Accurate build/test/lint/run commands | writeup Part I; package scripts, CI, and successful command logs | Pass |
| Structure, entry points, conventions, off-limits files | writeup's six exploration rows; AGENTS Map and Editing sections | Pass |
| Root agent file with all five areas | Project description, architecture, commands, conventions, guardrails | Pass |
| Specific and concise agent context | 415 words; actual paths, commands, testing conventions, generated-output boundary | Pass |
| Avoid generic padding and README repetition | No API tutorial, generic etiquette, exhaustive plugin list, or machine-specific paths | Pass |
| Warn about plausible mistakes | No app server; source/output distinction; build/ is tooling; package-root import needs build; prettier only formats docs | Pass |
| Two tasks with configuration present | Existing test/check task; three added leap-year test cases; commands, patch, and outputs retained | Pass |
| Honest report of behavior and one grounded improvement | Original failure retained; UTC rerun; initial configuration; actual conventions followed | Pass |
| Complete writeup template | Repo/file fields; six findings; exploration method; omission/inclusion reflections; two-task table; improvement | Pass |
| Student-agent interaction accurately represented | Real multi-round selection, questions, rubric review, edge-case discussion, and inclusion decision; actual inspection/execution attributed to Codex | Pass |
| Deliverables under week4/ | AGENTS.md, writeup.md, fork link, detailed checklist, and execution evidence | Pass |
| No unfilled placeholders or broken local writeup links | artifact-checks.json and prose whitespace check | Pass |
| Preserve unrelated code/dependencies/generated files | Day.js diff from baseline contains only AGENTS.md and test/plugin/isLeapYear.test.js | Pass |

The detailed item-by-item map is in [REQUIREMENTS_CHECKLIST.md](REQUIREMENTS_CHECKLIST.md). These results assess evidence against the stated rubric; the instructor assigns the grade.

## Fresh verification of the published Day.js source

Remote `dev` commit: `421ff708a9989e4f6a3ba2eaedfea44c9c19cd0f`.

| Check | Result | Evidence |
|---|---|---|
| Focused isLeapYear tests | 4 passed | [log](evidence/final-focused.log) |
| ESLint | exit 0 | [log](evidence/final-lint.log) |
| Full UTC gate | 93 suites / 797 tests passed; 100% line coverage | [log](evidence/final-full-tests.log) |
| UMD build with documented Node 24 fallback | exit 0 | [log](evidence/final-build.log) |
| ESM build | exit 0 | [log](evidence/final-esm.log) |
| Built-library smoke example | prints 2024-02-29 | [log](evidence/final-smoke.log) |

See [commands and exits](evidence/final-checks.json) and [artifact checks / hashes](evidence/artifact-checks.json). Warnings from the existing toolchain are retained in the logs.

## Submission gates

- Day.js root configuration and test are published and byte-identical to the checked local versions.
- Course deliverables belong at [week4 on master](https://github.com/yuxuanx-rain/modern-software-dev-assignments/tree/master/week4). Final publication must be verified by fetching that tree and comparing file bytes, not by observing an upload spinner.
- Collaborators `mihail911`, `isaackann`, and `vdaita`: not verified in this audit. GitHub's settings/access page requires account re-authentication. Pending invitations must be distinguished from accepted access. No permissions were changed.
- Gradescope: this task has not submitted the assignment. A visible submission receipt is needed to mark this step complete.
