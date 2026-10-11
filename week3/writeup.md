# Week 3: Author a Skill

## Part I — Workflow

**Workflow:** minimal reproduction and diagnosis of broken htmx interactions.

**Target repository:** [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx), checked out at `fa978b24e75fb03c137bf2cdae4fef0e711cf8a1` (htmx 2.0.11).

This workflow is useful whenever an htmx button or form does not update its intended page region. The input is a reported interaction, its HTML and response behavior, and its expected and actual results. The output is a small runnable reproduction, observations, an evidence-backed classification, and a verified local correction when appropriate.

The procedure is repeatable across weather buttons, search results, signup forms, and other fragment updates. It includes real decisions: whether the report is complete, whether a request is issued, whether its response permits a swap, and whether the cause is application configuration, an expectation mismatch, or a possible library defect. These branches determine the next investigation; this is not a wrapper around one fixed command.

### First execution before authoring

Codex assisted with the first execution before the new skill was written or installed. The case was a **constructed configuration error**, not a discovered htmx defect: a weather button targeted `#missing-result`, while its intended result element had id `weather-result`.

The existing target suite passed **17/17**. The minimal reproduction then failed its expected-result assertion: the panel remained `Not queried` instead of displaying `Sunny 22C`. The browser emitted `htmx:targetError`. Inspection of `getTarget()` and `issueAjaxRequest()` showed that this failure occurs before sending a request. Changing only the selector to `#weather-result` made the original assertion pass **1/1**. A separate real-HTTP demonstration confirmed that the missing-target button issued no weather request, while the correctly configured button issued one request and updated its panel.

This run informed the skill's no-request branch and its requirement to distinguish observations from hypotheses. Full procedure, commands, environment recovery, and before/after logs: [manual-run.md](evidence/manual-run.md), [failing fixture](evidence/manual-target-repro.js), [corrected fixture](evidence/manual-target-fixed.js), [baseline](evidence/manual-baseline.log), [failure](evidence/manual-failing.log), and [correction](evidence/manual-fixed.log).

## Part II — Skill

The deliverable is [htmx-interaction-diagnosis/SKILL.md](htmx-interaction-diagnosis/SKILL.md), with one supporting [reproduction reference](htmx-interaction-diagnosis/references/reproduction.md).

- **Trigger description:** names broken htmx button/form/response interactions in ordinary user language. It excludes conceptual explanations, styling, and non-htmx JavaScript interactions.
- **Encoded judgment:** branches on request issuance, response handling, and DOM updates; requires documented behavior before classifying a library defect; handles incomplete reports and non-reproduction explicitly.
- **Exact commands:** the reference provides repository inspection, dependency installation, Chromium setup, targeted native test execution, linting, and when to run the complete test command.
- **Lean body:** the entrypoint contains decisions and reporting requirements; setup commands and the native fixture pattern live in the linked reference. No external skill is required to execute this workflow.
- **Boundaries:** preserve failing evidence and expected behavior, make a controlled change, keep unrelated work intact, and use fake local responses rather than live write endpoints. Do not fabricate an upstream bug or publish a PR during diagnosis.

### Discovery and reproduction

Agent selected for behavioral testing: Claude Code 2.1.163. A local project symlink places the skill at the location Claude Code discovers:

```sh
# From a fresh assignment checkout:
git clone https://github.com/bigskysoftware/htmx.git ../htmx-week3-lab
git -C ../htmx-week3-lab checkout fa978b24e75fb03c137bf2cdae4fef0e711cf8a1
HTMX_REPO="$(cd ../htmx-week3-lab && pwd)"
mkdir -p "$HTMX_REPO/.claude/skills"
ln -s "$PWD/week3/htmx-interaction-diagnosis" \
  "$HTMX_REPO/.claude/skills/htmx-interaction-diagnosis"
cd "$HTMX_REPO"
claude
```

The full skill remains in `week3/`; the local discovery link is not a substitute for the submitted files. Normal automatic invocation is enabled. The frontmatter and naming passed the skill-creator validator. The local reproduction passed repository linting.

The design was checked against the [Agent Skills specification](https://agentskills.io/specification) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills). The assignment's sample [triage](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md) and [TDD](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) skills were inspected during refinement for reference-file organization and evidence-first testing; their unrelated tracker actions and approval conventions were not copied.

## Part III — Behavioral testing

Trigger testing was performed using Claude Code 2.1.163 with its configured default model, `claude-sonnet-4-6`, after authorization to use the public/generated test payload. The final four cases all matched their expected invocation behavior.

### Trigger tests

The exact prompts and expected outcomes are saved in [trigger-prompts.json](evidence/trigger-prompts.json). Each was run in a fresh Claude Code session without explicitly naming the skill. Successful triggering means an actual `Skill` tool invocation for `htmx-interaction-diagnosis` in the recorded transcript, not merely a plausible answer or a textual claim.

| Case | Prompt focus | Expected | Observed |
|---|---|---|---|
| 1 | `hx-get` button does nothing; reproduce and diagnose | Invoke | Invoked once; completed ([transcript](evidence/trigger-1.json)) |
| 2 | Form returns an HTML validation message but panel stays empty | Invoke | Invoked once; completed ([transcript](evidence/trigger-2.json)) |
| 3 | Response arrives but htmx does not swap | Invoke | Invoked once; completed ([transcript](evidence/trigger-3.json)) |
| Near-miss | Explain `hx-target` versus `hx-swap` | Do not invoke | No Skill invocation; explanation completed ([transcript](evidence/near-miss.json)) |

The trigger prompts restrict actions to planning; the separate end-to-end run tests execution. The initial harness exposed only the `Skill` tool. Case 1 invoked the skill repeatedly while trying to access its reference and finished with an error; case 2 answered directly without invoking the skill. Cases 3 and the near-miss selected correctly. These outcomes are retained in the [initial/final results](evidence/trigger-results.json) and initial transcripts.

The description was refined to include investigation outlines when execution is deferred, including apparently obvious causes, and made the reference necessary only for execution. The final harness exposed `Skill`, `Read`, `Grep`, and `Glob`, while keeping commands and editing unavailable. The **same four prompts** were rerun. All three positive cases invoked the skill exactly once and completed; the near-miss did not invoke it. This is observed behavior in these sessions, not a claim that every future prompt will route perfectly.

Example invocation command, from the htmx checkout:

```sh
claude -p '<exact prompt from evidence/trigger-prompts.json>' \
  --setting-sources project --strict-mcp-config \
  --tools Skill,Read,Grep,Glob --allowedTools Skill,Read,Grep,Glob \
  --permission-mode dontAsk --no-session-persistence \
  --output-format stream-json --verbose
```

The evidence transcripts omit telemetry and replace local absolute paths with named placeholders; actual tool calls and visible answers remain. Text logs have ANSI controls and trailing whitespace removed, preserving test observations and results.

### End-to-end test

The separate constructed execution case reports an unchanged panel after a response with HTTP 204. Its [exact prompt](evidence/end-to-end-prompt.txt) specifies input, response, expectation, local execution permission, and evidence retention, without giving the diagnosis or correction. It exercises a different branch from the missing-target first execution.

Claude automatically invoked `htmx-interaction-diagnosis` and completed the run. It inspected source, documentation, and native tests; created a fake-server browser fixture; and diagnosed a **server response contract / expectation error**, not an htmx defect. The native fixture sent one request with status 204 and retained `Empty` in the target. The assertion expecting `Loaded.` failed. Changing only the fake response status to 200 produced `Loaded.` and passed, without changing the library or its global settings.

| Execution | Actual result | Evidence |
|---|---|---|
| Pre-existing local interaction baseline | 1 passed; exit 0 | [baseline](evidence/end-to-end/baseline.log) |
| Original 204 reproduction | 1 observation passed, 1 expected-result assertion failed; exit 1 | [original fixture](evidence/end-to-end/week3-204-repro-original.js), [actual output](evidence/end-to-end/original-failing.log) |
| Corrected 200 reproduction | 1 passed; exit 0 | [corrected fixture](evidence/end-to-end/week3-204-repro-corrected.js), [actual output](evidence/end-to-end/corrected.log) |
| Agent's combined run, including the intentional failing snapshot | 107 passed, 1 intentional failure, 1 skipped; exit 1 | [actual output](evidence/end-to-end/agent-adjacent-with-intentional-failure.log) |
| Final independent check, after archiving that snapshot outside active test discovery | **106 passed, 0 failed, 1 skipped; exit 0** | [final adjacent output](evidence/end-to-end/final-adjacent.log) |
| Final repository lint | Passed; exit 0 | [lint output](evidence/final-lint.log) |

The final adjacent check included `hx-get.js`, `hx-target.js`, `test/core/ajax.js`, and the passing local fixtures. The skipped test is reported rather than counted as passed. The failing snapshot remains available as evidence, but is not left inside the active test glob. No tracked htmx source or existing tests were changed.

The [full execution transcript](evidence/end-to-end.json) retains actual tool calls and outputs. Browser logs linked above were extracted from the recorded tool results, rather than reconstructed from the agent's final prose. The agent's complete run finished successfully in about 137 seconds. Execution exposed the read tools plus `Bash`, `Write`, and `Edit`, with project settings, no MCP servers, and instructions limiting access to public/generated experiment files and prohibiting network or publication actions.

The decision differed from the first run: the missing-target case stopped **before** a request; this case sent a request but the documented 204 response rule suppressed swapping. The skill therefore exercised two diagnostic branches instead of repeating one selector correction.

### Final review and another execution

A clean-checkout review found two weaknesses: the agent copied the failing fixture as evidence but left its original in the active test glob, and its report overstated `hx-swap="none"` as preventing all DOM changes. The skill was tightened to require moving the failing original out of discovery and to distinguish primary swaps from out-of-band updates. The description used in the passing trigger tests was unchanged.

The final skill was then automatically invoked once in another clean checkout at the same htmx commit. The [constructed prompt](evidence/release-verification/prompt.txt) supplied a response containing both primary content and an `hx-swap-oob` status update. The original expected-result assertion failed (**0 passed, 1 failed**): one request was sent, the primary region remained `Empty`, and the status region became `Ready`. Changing only `hx-swap` to `innerHTML` made the primary region show `Loaded` while retaining the status update. The corrected fixture passed **2/2**; adjacent tests passed **68/68**. The original failing fixture was genuinely moved outside active test discovery.

An independent full Chromium run of all **51** discovered test files passed **870 tests, with 0 failures and 3 skips** ([output](evidence/release-verification/full-suite.log)). Repository lint initially found four formatting errors in the generated fixture; formatting was corrected and lint then exited 0 ([initial](evidence/release-verification/lint-initial.log), [final](evidence/release-verification/lint.log)). No tracked library source or existing tests changed. The full browser run was performed before that formatting-only cleanup; the assertions and behavior were unchanged.

Evidence: [final execution transcript](evidence/release-verification/transcript.json), [actual commands and output links](evidence/release-verification/commands.json), [original fixture](evidence/release-verification/original-failing-test.js), [corrected fixture](evidence/release-verification/corrected-test.js), and [review summary](evidence/release-verification/review-summary.json). The earlier review transcript and its actual outputs are retained in [final-review](evidence/final-review/transcript.json). Claims here follow runner results and fixture observations; the transcript's broad statement that OOB updates "always" execute is not a guarantee for every possible configuration.

### Clickable learning demonstration

The supplementary demo uses the checked-out `src/htmx.js`, a local HTTP server, and fixed weather fixture data. It is an explanation aid, not a replacement for the agent tests.

```sh
python3 week3/demo/server.py --repo "$HTMX_REPO" --port 19363
# Open http://127.0.0.1:19363
```

Desktop and mobile browser verification passed. See [observations](evidence/demo-verification.json), [desktop screenshot](evidence/demo-desktop.png), and [mobile screenshot](evidence/demo-mobile.png).

## Requirement check

| Requirement | Evidence |
|---|---|
| Real open-source target | Named htmx repository and recorded commit |
| Repeatable workflow with a genuine decision | Request/response/DOM diagnostic branches |
| Execute before authoring | Pre-skill manual run and before/after browser outputs |
| Agent Skills format and discoverable installation | Validated frontmatter; real Claude discovery and invocation |
| Useful trigger description and encoded judgment | Final skill, refinement record, and behavioral transcripts |
| Exact commands and concise entrypoint | Linked reproduction reference |
| Three positive prompts and one near-miss, with actual outcomes | Four final transcripts and retained initial outcomes |
| End-to-end execution | Full agent transcript, fixtures, and actual browser outputs |
| Skill directory and completed writeup in `week3/` | This directory |

Submission additionally requires the pushed assignment repository, collaborators `mihail911`, `isaackann`, and `vdaita`, and Gradescope submission. These administrative steps are tracked separately from the completed workflow and skill tests.
