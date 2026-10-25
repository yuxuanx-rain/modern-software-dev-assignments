# Week 4 requirements audit

Sources: current upstream `week4/assignment.md` and `week4/writeup.md`, rechecked 2026-10-25. This checklist tracks evidence, not a promised grade.

| Requirement | Evidence / assessment |
|---|---|
| Unfamiliar open-source project not authored by the student | Day.js, an instructor-listed project authored upstream by iamkun and contributors; selected for this assignment. |
| Fork the project | Public GitHub fork `yuxuanx-rain/dayjs`, shown in evidence/fork-created.png. |
| Explore with an agent | Codex-assisted file inspection and execution, described honestly in writeup Part I. |
| Exact build and run commands | AGENTS command block; writeup table; successful compatibility build, ESM build, smoke logs. No invented application server. |
| Exact test and lint commands | Focused Jest, full UTC-prefixed npm test, npm run lint; recorded outputs and exits. |
| Major directories, entry points, relationships | AGENTS Map and writeup Part I; core, plugins, locales, tests, declarations, tooling, CI. |
| Unstated conventions and naming | Local source imports, dayjs.extend registration, matching plugin test/type paths, Jest idiom, MockDate cleanup, cloning behavior. |
| Generated/vendored/off-limits content | Source/output distinction from .gitignore and build scripts; lockfile preserved; no node_modules, coverage, or generated artifacts in change. |
| Root AGENTS.md or CLAUDE.md | AGENTS.md in Day.js root; neither file was present in the baseline clone. |
| All five required file areas | Project description, architecture, commands, conventions, guardrails all covered. |
| Wrong-but-plausible command/directory warning | No dev server; package-root import requires build; build/ is editable; prettier only handles docs Markdown. |
| Repository-specific content, concise | 415 words. Operational paths, scripts, coverage, timezone behavior, and output boundaries; no general etiquette or full API tutorial. |
| Two actual small tasks with file in place | Task 1 existing tests/lint and full-gate investigation; Task 2 three meaningful added tests. Configuration was explicitly read before task execution. |
| Report observed agent behavior honestly | Writeup records commands, paths, conventions, initial failures, and actual passes; identifies Codex as executor and same-conversation trials. |
| One grounded improvement | UTC prefix based on six unpinned failures disappearing on unchanged baseline; initial config and both outputs retained. |
| Template: project/fork and file choice | Writeup opening fields. |
| Template: six exploration rows | All six rows filled with project-specific findings. |
| Template: agent questions and direct reading | The method section records the real multi-round discussion, agent file inspection/execution, student questions, edge-case reasoning, and inclusion decision; it does not invent student terminal or source-reading activity. |
| Template: deliberately omitted material and hardest inclusion choice | Writeup Part II answers both with reasons. |
| Template: two-task table and one proposed change | Writeup Part III completes both. |
| Deliverables together under week4/ | AGENTS.md, writeup.md (including fork link), evidence; byte-identical configuration copy. |
| No remaining template placeholders | Search performed on authored Markdown; no unfilled template fields. |
| All changes published to remote | Day.js remote configuration and test file match the validated local versions. The final course files are published under week4/; verify their bytes against the local deliverables after upload. See FINAL_REVIEW.md and the final handoff for the publication result. |
| Add mihail911, isaackann, vdaita as collaborators on assignment repo | Not verified: GitHub settings/access currently requires password re-authentication (Confirm access). No permission changes were made during this audit. |
| Submit via Gradescope | Not submitted by this task. A Gradescope receipt is required before this gate can be marked complete. |

The assignment explicitly permits agent-assisted exploration. It does not prescribe student-only terminal commands, a minimum amount of manual source reading, fresh sessions, or a controlled experiment. The writeup template does ask which work the agent did and what was read directly; the writeup answers this without inventing personal actions. Same-conversation execution is disclosed briefly and does not itself contradict the two-task requirement.
