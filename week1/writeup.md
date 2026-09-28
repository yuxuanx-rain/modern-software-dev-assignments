# Week 1 Write-up

## Evidence convention

R1–R15 are the 15 successful `POST /v1/messages?beta=true` flows in capture order. R1 is an auxiliary title-generation request with no tools; R2–R15 are the coding-agent conversation. Within a request, M0, M1, etc. are zero-based indices in `messages`, and C0, C1, etc. are zero-based content-block indices. The private `session.flows` and downloaded request-body JSON stay outside this repository.

## Part I: Capture

**Setup (reproducible on this Mac):**

```text
Claude Code:       2.1.163 (claude --version)
mitmproxy:         11.0.2 (mitmweb --version)
scratch repo:      a separate local Git repo, scratch-agent, beside this assignment repo
trace test Python: 3.10.7 (python3 --version)
capture path:      /private/tmp/cs146s-session-success.flows (outside all Git repos)
retained copy:     ~/Downloads/cs146s-week1-session.flows (outside all Git repos)
```

I installed mitmproxy in the isolated `/private/tmp/cs146s-mitm-venv` environment. Its `mitmweb` binary was `/private/tmp/cs146s-mitm-venv/bin/mitmweb`; with that environment's `bin` directory on `PATH`, I ran the following from `/private/tmp`:

```bash
mitmweb --listen-host 127.0.0.1 --listen-port 58888 \
  --web-host 127.0.0.1 --web-port 8081 --no-web-open-browser \
  --mode reverse:https://api.anthropic.com \
  -w /private/tmp/cs146s-session-success.flows
```

The extra `--no-web-open-browser` only suppressed automatic browser launch. I later opened `http://127.0.0.1:8081`, selected a successful `POST /v1/messages` flow, and downloaded its request body as valid JSON to `~/Downloads/cs146s-week1-request-r2.json`. Before the run, `scratch-agent/.claude/settings.json` contained:

```json
{"env":{"ANTHROPIC_BASE_URL":"http://127.0.0.1:58888","ENABLE_TOOL_SEARCH":"true"}}
```

The scratch repo's baseline commit contained `ledger.py`, `report.py`, and `tests/test_refunds.py`. `normalize_transaction` accepted only `kind == "sale"` and raised `ValueError("unsupported transaction kind")` otherwise. `daily_net_revenue` simply added normalized amounts. The two prewritten tests required a positive-input refund of `4.50` to retain its kind and to reduce a same-day sale of `12.00` to net revenue of `7.50`. Thus `python3 -m unittest discover -s tests -v` failed on both tests before Claude edited anything.

I launched a fresh Claude Code session in that repo and asked it to create and update an explicit task list, run that exact test command before editing, implement refund support in `ledger.py` and `report.py` while keeping `Decimal` precision and rejecting nonpositive amounts, then rerun the full test command. The prompt also limited work to the scratch repo and prohibited reading credentials or outside files (R2 M0/C4). The proxy recorded **15 successful POSTs**, including the auxiliary title request. Afterward I stopped mitmweb and deleted the project-level settings file. I retained a private local copy of the flow, which can be reopened with `mitmweb -r ~/Downloads/cs146s-week1-session.flows`.

| Requirement | Evidence |
|---|---|
| Touched at least two files | `Edit` changed `ledger.py` at R10 M15/C0 and `report.py` at R12 M19/C0. |
| Failed at least once | Baseline `Bash` test call at R6 M7/C2 returned exit code 1 and two errors at R6 M8/C1; the rerun passed at R14 M24/C0. |
| Long enough to plan | `ToolSearch` loaded `TaskCreate` at R5 M5/C2; R6 M7/C1 created task 1, and R8 M11/C2–C4 created the remaining tasks. |
| My own repo | `scratch-agent` was initialized as a separate local Git repo; the assignment repo was only used for this write-up. R2 `system[2]` identifies the scratch repo as the working directory and says it is a Git repository. |

**Sanitization.** The excerpts below omit HTTP headers entirely. I do not quote the `userEmail` reminder, account identifiers, or absolute home-directory paths. The error quote is a contiguous, path-free span of the test result; I omitted the surrounding stack trace because it contains local paths. If quoting a path were necessary, I would replace it visibly with `[REDACTED: local path]`. Neither the raw flow nor the downloaded request body is in this Git repo.

## Part II: System Prompt Annotation

**a. Structure.** R2 `system` is a three-block array; there are no `role: "system"` messages in R2–R15. `system[0]` carries a Claude Code billing/version marker, `system[1]` identifies the SDK agent, and `system[2]` is the operative prompt. Its major sections are in this order. The placement explanations are my reading of the design, not observed proof that each rule changed Claude's behavior:

| Section of `system[2]` | Behavior bought; failure prevented | Why this placement helps |
|---|---|---|
| Opening safety and URL rules | Sets authorization boundaries; limits harmful assistance and invented links. | Puts global limits before repository instructions can be interpreted as permission. |
| `System` | Explains output visibility, permission prompts, hooks, tool results, and compression; guards against treating tool output as trusted instructions or repeating a denied action. | Defines the runtime's rules before telling the agent how to work. |
| `Doing tasks` | Converts requests into repository work while limiting unnecessary features and validation; guards against answer-only responses and scope creep. | Establishes the normal work pattern before the narrower action gates. |
| `Executing actions with care` | Gates destructive and shared-state actions by reversibility and authorization; guards against lost work or unwanted publication. | Qualifies the preceding bias to act before tool execution guidance begins. |
| `Using your tools` | Prefers dedicated tools, task tracking, and ordered dependent calls; guards against indiscriminate shell edits and stale plans. | Turns the work policy into concrete tool choices after the permission boundaries are set. |
| `Tone and style` and `Text output` | Keeps updates short and gives file locations; guards against silent work, verbose narration, and unsupported summaries. | Applies to how the already defined work and tool results are reported. |
| `Session-specific guidance` | Chooses when agents or skills fit; guards against excess delegation for a small known-file task. | Refines the general tool rules with session-specific options. |
| `auto memory` | Separates durable facts from ephemeral task state; guards against storing transient code details as personal memory. | Adds persistence rules after ordinary task behavior. |
| `Environment` and `Context management` | Supplies working directory, Git snapshot, OS, shell, model, and compaction behavior; guards against wrong-repo actions and premature stopping. | Places variable machine and session facts at the end, where they can be read under the earlier rules. |

The order moves from general limits to work method, then to the concrete machine and repository. That lets later environment facts be interpreted under the earlier safety and scope rules.

**b. Tone and verbosity.** R2 `system[2]`, `Tone and style` says “Your responses should be short and concise.” Its `Text output` section says “End-of-turn summary: one or two sentences.” These short controls defend against long process narration crowding out the result. The same section asks for an update before the first tool call and at key moments, defending against an agent that works invisibly. Spending prompt tokens on this is plausible because response length and update timing recur on every task, not just this refund exercise.

**c. When not to act.** R2 `system[2]` says “Don't implement until the user agrees” for exploratory proposals, limiting premature edits. Its `Executing actions with care` section says to “check with the user before proceeding” on hard-to-reverse or shared-system actions; this protects local work and shared state. The opening rule says “Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes.” That is a separate refusal gate, rather than a request to ask permission. The `Doing tasks` section restricts extra features and speculative validation. Together these address user-intent ambiguity, action impact, harmful intent, and scope.

**d. Environment context.** R2 `system[2]` → `Environment` gives the scratch working directory, Git-repository status, macOS/Darwin, zsh, and model ID. Its final Git snapshot gives branch `main`, clean status, and recent commits, while explicitly warning that the snapshot will not update during the conversation. The user prompt and capability notices live in R2 M0, not in a `role: "system"` message. This split gives the agent machine facts once while carrying changing session information in the message history.

**e. `<system-reminder>`.** Actual reminder tags occur in `messages`, not as standalone `system` blocks: R2 M0/C0 lists 20 deferred tool names and explains `ToolSearch`; R2 M0/C3 carries date/account context (not quoted here). A later reminder is embedded in the `Read` tool result at R5 M4/C2: it adds 50 deferred MCP tool names as servers finish connecting. Thus the tags both provide capability discovery and inject session context. Putting them in messages or tool results lets the runtime update availability mid-conversation, rather than freezing a tool list at session start. The system block itself explains that reminders may appear in messages or tool results, but the observed tags in this capture are in those two message locations.

## Part III: Tool Design Annotation

**Inventory.** Counts are unique names across the directly supplied `tools` array and the deferred names listed in reminders. “Deferred MCP” means named and searchable, with no schema loaded into the direct `tools` array. The 50 newly announced MCP names were not used in this coding task.

| Request | Direct built-in | Direct MCP | Deferred built-in | Deferred MCP | **Unique total** |
|---|---:|---:|---:|---:|---:|
| R2, first coding request | 11 | 0 | 20 | 0 | **31** |
| R5, after `TaskCreate` loads and MCP announcement | 12 | 0 | 19 | 50 | **81** |
| R7–R15, after `TaskUpdate` loads | 13 | 0 | 18 | 50 | **81** |

R1 is an auxiliary title-generation request with **0 tools**, not the first coding request. R5 M5/C2 requests `select:TaskCreate`; R5 M6 reports it loaded and R5's direct schema list has grown to 12. R7 M9/C2 requests `TaskUpdate`; from R7 onward the list contains 13 direct schemas. Separately, the reminder appended to the R5 M4/C2 `Read` result announces 50 MCP-provided searchable names as connections complete; this is availability, not evidence that Claude invoked them.

**Two deliberately different tools:** `Edit` changes a file; `TaskCreate` creates orchestration state. Both schemas set `additionalProperties: false`.

| | `Edit` (R2 `tools`) | `TaskCreate` (R5 `tools`) |
|---|---|---|
| Relevant schema | `{file_path: string, old_string: string, new_string: string, replace_all?: boolean=false}` | `{subject: string, description: string, activeForm?: string, metadata?: object}` |
| Required, optional, and why | Exact target path and before/after strings are required so a replacement is reviewable. `replace_all` is optional and defaults false to avoid broad changes. | `subject` and `description` are required to make a task actionable. Spinner text and metadata are optional presentation/extension fields. |
| Description's defensive detail | “The edit will FAIL if `old_string` is not unique” and a prior read is required. This anticipates ambiguous replacements and hallucinated file contents. | “NOTE that you should not use this tool if there is only one trivial task to do.” This anticipates agents creating busywork task lists merely because the tool exists. |
| Deliberately does not do | It does not search, choose the target, run tests, or commit. The agent must use `Read`, deliberate matching, then another tool to verify. | It does not implement work or advance status by itself; creation starts `pending`. `TaskUpdate` and actual file/test tools are separate responsibilities. |

I chose these two because `Edit` constrains a risky file mutation through exact matching, while `TaskCreate` constrains workflow overhead through its usage guidance. Their schemas show different boundaries: one acts on code, and the other records work for later tools to advance.

## Part IV: Behavioral Analysis

**a. Error recovery — [OBSERVED].** R6 M7/C2 calls `Bash` to run the baseline suite. R6 M8/C1 returns, verbatim in part:

```text
Exit code 1
test_normalizes_refund (test_refunds.RefundTests) ... ERROR
test_refund_reduces_daily_revenue (test_refunds.RefundTests) ... ERROR
```

The same tool result contains `ValueError: unsupported transaction kind` twice. At R7 M9/C1 the agent identifies the cause as rejecting `kind == "refund"`; at R8 M11 it creates tasks for the two code changes and verification. It then edits `ledger.py` (R10 M15/C0) and `report.py` (R12 M19/C0), reruns the suite (R14 M23/C0), and sees both tests `ok` (R14 M24/C0). Recovery takes **eight subsequent assistant turns**—M9, M11, M13, M15, M17, M19, M21, and M23—from the failed result to the passing result; M25 closes the final task afterward.

**b. Planning — [OBSERVED].** It is a combination of explicit instruction and tool support. R2 M0/C4 asks for a plan; R2 `system[2]` → `Using your tools` directs use of `TaskCreate`. Claude says it will plan at R5 M5/C1, loads `TaskCreate` at R5 M5/C2, creates task 1 at R6 M7/C1, and creates tasks 2–4 at R8 M11/C2–C4. The trace does not establish that planning would have happened without either prompt instruction.

**c. Plans and task state — [OBSERVED].** `TaskCreate`'s R5 tool description says new tasks start `pending`; its results confirm creation and give IDs, but do not echo the status (R6 M8/C0; R8 M12/C1–C3). `TaskUpdate` calls set task 1 to `completed` at R8 M11/C1, task 2 to `in_progress` at R9 M13/C0, and advance tasks 2–4 through R15 M25/C0. The next request's `messages` retain each assistant `tool_use` with its requested status and a `tool_result` acknowledgment; R10 M13/C0 and M14/C0 show that pair for task 2. The acknowledgment says only that the status was updated, not what the new status is. No complete task-list snapshot appears on every turn in this trace, so I cannot claim one was supplied.

**d. Subagents — [INFERRED].** No `Agent` call appears in R2–R15. R2's `Agent` schema requires `description` and `prompt`, optionally accepts `subagent_type`, `model`, `run_in_background`, and `isolation`; R2 M0/C1 lists available agent types. Its description recommends delegation for open-ended work across a codebase and says the agent returns one result message to the parent, which then checks edits and relays a summary. This small, known-file task used direct `Read`/`Edit` calls, so no actual subagent input or output can be reported.

**e. Context management — [OBSERVED].** The main request grows from one `messages` entry at R2 to 27 at R15. Earlier assistant `tool_use` blocks and user `tool_result` blocks are retained: the R6 failure at M8 is still present in R15. The main `system[2]` text remains the same length (26,771 characters); the small billing marker changes, and the direct tool list grows 11 → 12 → 13 as schemas load. R2 includes `context_management` settings and the system prompt describes eventual summarization, but no summary replacing earlier turns is visible in this short trace. I therefore observed accumulation and tool-schema loading, not an actual compaction event.

## Part V: Reflection

**Two decisions I would copy.** First, the explicit `TaskCreate`/`TaskUpdate` lifecycle made the failure, both edits, and verification separate visible steps. It reduced the chance of declaring success immediately after a patch. Second, `Edit` requires an exact match after a read and rejects an ambiguous `old_string`; that narrows the blast radius of automated changes.

**One decision I would change.** The agent's first `find` searched every file under the scratch root (R3 M1/C2), including `.git` and the proxy settings path. A broad scan helps orient an agent in an unfamiliar repository, but here `git ls-files` or a scoped file listing would have supplied the needed map with less noise and less chance of pulling private configuration into context. The agent did not read a credential in this trace.

**Day-to-day steering change.** I will give coding agents a reproducible failing command, a narrow file scope, and explicit pass criteria up front. In this session that made the error-recovery sequence inspectable: initial failure, targeted edits, and the same test command passing afterward.

## Submission checks

- All template placeholders filled.
- Quoted excerpts reviewed for credentials, authorization headers, account identifiers, and local paths.
- Raw captures and downloaded request JSON remain outside the assignment Git repository.
- The temporary `ANTHROPIC_BASE_URL` project setting was removed after capture.
