# Week 5 Write-up: Agent-Readiness Report

## Repositories chosen and method

I compared a compact date library, a large downloader CLI, and a production server. They differ in language, size, repository age, operating model, and whether service-oriented criteria fit their purpose. These are three deliberately contrasting cases, not a representative sample of open source.

Day.js is retained deliberately as the library case: comparing it with a CLI and a server lets me examine whether the same readiness checklist fits different kinds of software. This design supports a framework-applicability comparison. It cannot isolate language effects or establish a general project-quality ranking. Missing service instrumentation in Day.js must therefore be interpreted against its purpose, rather than treated automatically as a defect.

| Repository / purpose | Primary language | Size at evaluated commit | Repository created / latest commit | Maintenance evidence |
|---|---|---|---|---|
| [iamkun/dayjs](https://github.com/iamkun/dayjs) — Date/time library | JavaScript | 380 tracked files; 286 `.js` files / 18,827 physical lines | 2018-04-10 / 2026-09-15 | Individual-owned repository; package author is iamkun. This does **not** establish that there is only one maintainer. |
| [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) — Audio/video downloader CLI | Python | 1,235 tracked files; 1,124 `.py` files / 247,104 physical lines | 2020-10-26 / 2026-10-29 | Community organization with multiple named core maintainers; fork lineage predates this repository. |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) — HTTPS server platform | Go | 745 tracked files; 402 `.go` files / 131,440 physical lines | 2015-01-13 / 2026-11-01 | README identifies Caddy as a ZeroSSL project, an HID Global company; this establishes commercial backing, not a measured staffing budget. |

Size means all tracked primary-extension files, including tests, locale files and generated files if tracked; physical lines include comments and blanks. It is a consistent size proxy, not production SLOC, download size, or complexity. Creation dates come from saved public GitHub metadata; latest-commit dates come from Git. In particular, yt-dlp's 2020 creation date does not date all inherited youtube-dl code. Maintenance descriptions are supported by [Day.js package metadata](https://github.com/iamkun/dayjs/blob/436bde0bcded312781cbe45dc2b0ef079a36d8e3/package.json), [yt-dlp's maintainers list](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/Maintainers.md), and [Caddy's README](https://github.com/caddyserver/caddy/blob/1a870400e684156f240f8db6e225c980b4357a80/README.md), not inferred from GitHub owner type alone.

**Execution.** On November 1, 2026, I cloned each upstream default branch into a clean, separate directory and invoked Factory Droid **1.1.0**, `/readiness-report`, from its repository root. Day.js used the interactive CLI; yt-dlp and Caddy used `droid exec '/readiness-report'`. All used GPT-6.1 Sol with high reasoning. The two exec sessions initially stopped at permission checks for bounded collection/inspection commands and were resumed in the same sessions with `--auto medium`. Source/configuration changes and package/runtime installation were excluded. All reports were successfully stored in Factory. No upstream issues, comments, or pull requests were created.

Each clone was shallow (`--depth 1`). This limits historical attribution, AI-coauthorship detection, and documentation-freshness inference; I do not use those checks to establish actual historical adoption or document maintenance. The saved [repository manifest](evidence/repo-manifest.json) pins the exact commits. The [run record](evidence/run-record.json) records session/report IDs, tool versions, and limitations. This was one audit per commit, not repeated score selection.

**Version and scoring differences.** The assignment's reading describes 60+ criteria, eight pillars and gated maturity progression. The installed CLI supplied **84 criteria** and explicitly calculated levels from the overall non-skipped pass rate: L1 below 20%, L2 from 20% to below 40%, L3 from 40% to below 60%, L4 from 60% to below 80%, and L5 from 80% through 100%. I report its actual outputs rather than silently substituting the older 80%-per-level rule. Every detected application is the repository root, so every criterion denominator is 1. A null numerator is N/A or unavailable evidence, **not a failure**.

Factory's current documentation and raw reports also organize categories differently from the course template. The tables below transparently regroup unchanged criterion IDs into the **eight requested course pillars**, retaining Task Discovery and Product & Experimentation in two additional rows. This is an analyst mapping, not an assertion that Factory officially weights these ten rows. [comparison.json](evidence/comparison.json) lists the complete, non-overlapping mapping of all 84 IDs. Overall scores are calculated directly across criteria, never by averaging pillar percentages. Reproduce the tables with `python3 week5/recompute.py` from the assignment-repository root.

## Part I: Report Results

### Summary and what blocks the next level

| Repository | CLI maturity level | Passed / evaluated | Failed / skipped | Next-level boundary and remaining gap |
|---|---|---:|---:|---|
| Day.js | Level 2 | 21/59 = 35.59% | 38 / 25 | L3 starts at 40%; at least **3** current failures must become passes: 24/59 = 40.68%. |
| yt-dlp | Level 3 | 29/61 = 47.54% | 32 / 23 | L4 starts at 60%; at least **8** further passes: 37/61 = 60.66%. |
| Caddy | Level 4 | 41/68 = 60.29% | 27 / 16 | L5 starts at 80%; at least **14** further passes: 55/68 = 80.88%. |

Those gaps hold the current evaluated denominator fixed. In this CLI version there is **no individually mandatory blocking criterion**: every evaluated failure contributes equally, and any sufficient number of actual fixes can cross the next band. The complete candidate blockers are enumerated by ID in the failed-criteria table below. For example, Day.js's `build_cmd_doc`, `single_command_setup`, and `agents_md` are a possible three-pass set; documenting commands does not automatically prove that all three pass. Making a previously skipped criterion evaluable changes the denominator and requires recalculation. No proposed fix was implemented or rescored.

### Per-pillar score conventions

Each cell is **passes / evaluated criteria**, followed by percentage and the number of skipped criteria. Different N/A counts mean that these are not identical baskets of checks.

### Current Factory category scores

For completeness, these scores retain the current dashboard's nine-category membership, checked against the saved Caddy report in the Factory UI. The exact numerator/denominator ratios are recomputed from the original payloads; the dashboard rounds percentages to whole numbers. Its additional Mission Readiness view overlaps these criteria, so it is not counted as another pillar or added to the overall total.

| Current Factory category | Day.js | yt-dlp | Caddy |
|---|---:|---:|---:|
| Style & Validation | 6/11 (54.5%); 2 N/A | 5/12 (41.7%); 1 N/A | 8/12 (66.7%); 1 N/A |
| Build System | 4/10 (40.0%); 9 N/A | 5/9 (55.6%); 10 N/A | 5/9 (55.6%); 10 N/A |
| Testing | 5/9 (55.6%); 1 N/A | 6/9 (66.7%); 1 N/A | 7/9 (77.8%); 1 N/A |
| Documentation | 3/7 (42.9%); 1 N/A | 4/7 (57.1%); 1 N/A | 5/8 (62.5%); 0 N/A |
| Development Environment | 0/2 (0.0%); 3 N/A | 1/2 (50.0%); 3 N/A | 0/3 (0.0%); 2 N/A |
| Debugging & Observability | 1/9 (11.1%); 2 N/A | 1/9 (11.1%); 2 N/A | 7/11 (63.6%); 0 N/A |
| Security | 1/6 (16.7%); 6 N/A | 6/8 (75.0%); 4 N/A | 8/11 (72.7%); 1 N/A |
| Task Discovery | 1/3 (33.3%); 1 N/A | 1/3 (33.3%); 1 N/A | 1/3 (33.3%); 1 N/A |
| Product & Experimentation | 0/2 (0.0%); 0 N/A | 0/2 (0.0%); 0 N/A | 0/2 (0.0%); 0 N/A |

### Course-template regrouping

The eight course pillars and the two supplemental rows use the explicit mapping described above. In particular, code-quality checks move out of the current Style/Build groups into the course's separate Code Quality pillar. These rows should not be mistaken for unchanged dashboard category scores.

| Pillar | Day.js | yt-dlp | Caddy |
|---|---:|---:|---:|
| Style & Validation | 4/6 (66.7%); 0 N/A | 4/6 (66.7%); 0 N/A | 5/5 (100.0%); 1 N/A |
| Build System | 3/8 (37.5%); 8 N/A | 5/8 (62.5%); 8 N/A | 5/8 (62.5%); 8 N/A |
| Testing | 5/9 (55.6%); 1 N/A | 6/9 (66.7%); 1 N/A | 7/9 (77.8%); 1 N/A |
| Documentation | 3/7 (42.9%); 1 N/A | 4/7 (57.1%); 1 N/A | 5/8 (62.5%); 0 N/A |
| Dev Environment | 0/2 (0.0%); 3 N/A | 1/2 (50.0%); 3 N/A | 0/3 (0.0%); 2 N/A |
| Code Quality | 3/7 (42.9%); 3 N/A | 1/7 (14.3%); 3 N/A | 3/8 (37.5%); 2 N/A |
| Observability | 1/9 (11.1%); 2 N/A | 1/9 (11.1%); 2 N/A | 7/11 (63.6%); 0 N/A |
| Security & Governance | 1/6 (16.7%); 6 N/A | 6/8 (75.0%); 4 N/A | 8/11 (72.7%); 1 N/A |
| Task Discovery (additional) | 1/3 (33.3%); 1 N/A | 1/3 (33.3%); 1 N/A | 1/3 (33.3%); 1 N/A |
| Product & Experimentation (additional) | 0/2 (0.0%); 0 N/A | 0/2 (0.0%); 0 N/A | 0/2 (0.0%); 0 N/A |

### Failed criteria by pillar

Only actual zeroes appear here; all N/A rationales remain available in the raw reports and JSON payloads. Identifiers match the original Factory payloads exactly.

| Pillar | Day.js | yt-dlp | Caddy |
|---|---|---|---|
| Style & Validation | `type_check`, `strict_typing` | `type_check`, `strict_typing` | None |
| Build System | `build_cmd_doc`, `vcs_cli_tools`, `agentic_development`, `single_command_setup`, `feature_flag_infrastructure` | `vcs_cli_tools`, `agentic_development`, `feature_flag_infrastructure` | `vcs_cli_tools`, `agentic_development`, `feature_flag_infrastructure` |
| Testing | `unit_tests_runnable`, `test_performance_tracking`, `interactive_qa_exists`, `interactive_qa_runnable` | `test_performance_tracking`, `test_coverage_thresholds`, `test_naming_conventions` | `test_performance_tracking`, `test_coverage_thresholds` |
| Documentation | `agents_md`, `skills`, `service_flow_documented`, `agents_md_validation` | `agents_md`, `skills`, `agents_md_validation` | `skills`, `api_schema_docs`, `agents_md_validation` |
| Dev Environment | `devcontainer`, `env_template` | `devcontainer` | `devcontainer`, `env_template`, `database_schema` |
| Code Quality | `cyclomatic_complexity`, `duplicate_code_detection`, `tech_debt_tracking`, `unused_dependencies_detection` | `cyclomatic_complexity`, `large_file_detection`, `duplicate_code_detection`, `code_modularization`, `tech_debt_tracking`, `unused_dependencies_detection` | `cyclomatic_complexity`, `large_file_detection`, `tech_debt_tracking`, `n_plus_one_detection`, `unused_dependencies_detection` |
| Observability | `structured_logging`, `distributed_tracing`, `metrics_collection`, `error_tracking_contextualized`, `alerting_configured`, `runbooks_documented`, `deployment_observability`, `profiling_instrumentation` | `structured_logging`, `distributed_tracing`, `metrics_collection`, `error_tracking_contextualized`, `alerting_configured`, `runbooks_documented`, `deployment_observability`, `profiling_instrumentation` | `error_tracking_contextualized`, `alerting_configured`, `runbooks_documented`, `deployment_observability` |
| Security & Governance | `codeowners`, `dependency_update_automation`, `gitignore_comprehensive`, `log_scrubbing`, `min_release_age` | `codeowners`, `gitignore_comprehensive` | `codeowners`, `gitignore_comprehensive`, `min_release_age` |
| Task Discovery (additional) | `issue_labeling_system`, `pr_templates` | `issue_labeling_system`, `pr_templates` | `issue_labeling_system`, `pr_templates` |
| Product & Experimentation (additional) | `product_analytics_instrumentation`, `error_to_insight_pipeline` | `product_analytics_instrumentation`, `error_to_insight_pipeline` | `product_analytics_instrumentation`, `error_to_insight_pipeline` |

### The reports' own top remediation suggestions

These preserve the three action-item groups and their order from each report; they are not my prioritization.

| Repository | Factory recommendations, in returned order |
|---|---|
| Day.js | (1) Add AGENTS.md covering installation, supported Node, builds, environment and smoke interaction. (2) Add declaration type checks and unused-dependency checks to CI. (3) Configure dependency updates with minimum release age, and ignore secret-bearing environment files. |
| yt-dlp | (1) Add strict Python type checks, complexity limits and unused-dependency checks. (2) Add coverage thresholds, retained timing reports and explicit pytest discovery patterns. (3) Exclude environment secrets, add a PR testing-results section, and provide a Python 3.11+ devcontainer. |
| Caddy | (1) Strengthen CI with coverage thresholds, retained test timings, root-module tidy verification and complexity limits. (2) Document the environment contract, broaden environment-file exclusions and add a validated devcontainer. (3) Add API schemas, runbooks, CODEOWNERS, fuller PR-template sections and AGENTS.md validation. |

## Part II: Analysis

### Which pillars failed most?

Among the **eight course pillars**, Observability had the most observed failures: **20/29 evaluated checks failed** across the three repositories. Code Quality followed with **15/22**. By failure *rate*, Dev Environment was worst at **6/7**, but that is a much smaller denominator: mostly missing development containers, plus environment-contract or embedded-database documentation gaps. These are pooled criterion observations, not 29 independent repositories.

The failures were not uniform. Day.js and yt-dlp each passed only **1/9** observability checks; Caddy passed **7/11**, including structured logging, OpenTelemetry, Prometheus metrics, health checks, resilience mechanisms and profiling. Nevertheless, all three failed contextual error tracking, alerting, deployment observability and runbooks. All three also lacked demonstrated complexity limits, enforced debt tracking and unused-dependency detection. Conversely, basic linting and existing unit/integration tests were present in all three. The recurring pattern concerns additional enforcement and operating-feedback signals; it does not establish a universal absence of tests or linters, or that every missing signal deserves implementation.

Two additional signals failed in every repository: product analytics and an error-to-issue pipeline. They should not displace the eight-pillar comparison or be treated as equally urgent in all project types. Caddy's missing embedded-database schema and N+1 detector, Day.js's missing documented build path, and yt-dlp's missing enforced architectural boundaries are repository-specific findings.

These are patterns in Factory's recorded checks. For example, the Dev Environment failures establish missing checked-in containers or documentation, not that development is impossible. Likewise, an observability zero needs a task-specific justification before it becomes a recommended change.

### What explains the pattern, and what can this sample support?

**Project purpose is the strongest mechanism supported by the files.** A network server needs runtime logs, metrics, tracing and upstream health checks; Caddy implements those concrete mechanisms. A date library and a local downloader have different operational needs. That explains a plausible route to the observability gap without claiming that low telemetry scores prove those tools are unreliable. The source evidence supports the mechanism, not a causal effect size.

**Age does not track the scores monotonically.** Caddy (2015) is the oldest and scored highest, but the younger yt-dlp repository (2020) scored above Day.js (2018). This is insufficient evidence for a general older-is-better relationship. Fork ancestry further weakens creation date as a proxy for code age. These three cases cannot isolate age from project purpose, staffing or ecosystem.

**Size alone is also insufficient.** The largest snapshot by primary-language physical lines is yt-dlp (247,104), followed by Caddy (131,440) and Day.js (18,827); readiness does not increase monotonically with that measure. In particular, yt-dlp's many extractor modules coexist with a `code_modularization` failure because the criterion demands enforced boundaries. Having more code or visibly separated directories does not itself satisfy that check.

**Language contributes some mechanical differences, but language quality is not identified.** Go compilation supplies type checking, while the JavaScript and Python snapshots lacked configured static type-checking tasks. Go's separate `strict_typing` check was N/A. One repository per language cannot establish that Go projects generally outperform Python or JavaScript projects; repository purpose and maintenance model are completely entangled with language here.

**Maintenance model is a hypothesis, not a controlled comparison.** Caddy has documented commercial backing and stronger operational tooling. yt-dlp documents several community core maintainers and substantial release/security automation. Day.js has an individual-owned repository; that is not proof of single-maintainer governance. With no staffing, spending or contributor-concentration measurement, I cannot attribute the score gap to corporate ownership or conclude that community maintenance is inherently weaker.

### Separate repository evidence from limitations of this run

All three failed `vcs_cli_tools` because this auditing machine lacked authenticated `gh`/`glab`; that is an observer limitation. Other findings require the same distinction:

| Recorded observation | What this run supports | What it does not establish |
|---|---|---|
| Day.js test collection failed with uninstalled dependencies; its bundle was absent. | These commands did not work in the unprepared checkout. Its contributor documentation also lacks a complete install/build/interaction sequence, which can be checked independently in the files. | That correctly installed Day.js tests or its build are broken. |
| yt-dlp requires Python 3.11+; the audit used older interpreters. | Test execution was unverified in this environment. The repository already documents Hatch setup, environment activation and tests. | That contributors need a new container or lack an existing setup path. |
| Caddy's Go runtime was unavailable. | Test execution was unverified. Build/test instructions and CI can still be inspected statically. | That its test suite passes or fails locally. |
| yt-dlp and Caddy passed interactive QA through a documentation fallback. | The auditor accepted a documented interaction path. | That either application was actually started and exercised successfully. |
| History-sensitive checks used depth-one clones. | Current files and snapshot identity can be examined. | Reliable historical AI adoption or document modification dates. |

No full upstream test suite ran. To check how much these limitations affect the comparison, I calculate two sensitivities rather than rewriting the original scores. First, I restrict comparison to criteria evaluated in all three. Second, I exclude **the same six IDs from every repository**: `vcs_cli_tools`, `unit_tests_runnable`, `interactive_qa_runnable`, `devcontainer_runnable`, `agentic_development`, and `documentation_freshness`. This removes affected passes as well as failures, including documentation-fallback passes and shallow-history freshness passes. The exclusion rationale and exact retained IDs are recorded in [comparison.json](evidence/comparison.json).

| Comparison basis | Day.js | yt-dlp | Caddy |
|---|---:|---:|---:|
| Original Factory results | 21/59 (35.59%) | 29/61 (47.54%) | 41/68 (60.29%) |
| Criteria evaluated in all three | 19/55 (34.55%) | 25/55 (45.45%) | 31/55 (56.36%) |
| After excluding six observer/history-sensitive checks | 20/54 (37.04%) | 27/57 (47.37%) | 39/64 (60.94%) |
| Common criteria after those exclusions | 18/51 (35.29%) | 23/51 (45.10%) | 29/51 (56.86%) |

The ordering remains under these specified exclusions. On a shared basket, Caddy's lead over Day.js is smaller than in the original results. This supports discussing the direction of the recorded differences, but does not establish robustness to every scoring judgment or eliminate project-purpose confounding. These are analyst sensitivity calculations, not new Factory scores or maturity levels. Preparing supported toolchains and using complete history would still be necessary before making stronger execution or historical claims.

### Cheapest high-leverage fix, per repository

These are specific proposed changes, with expected mechanisms rather than measured improvements. I prioritize an evidenced repository gap, a small implementation surface, reuse of existing tooling, and a clear benefit to an agent's validation loop. There are no measured effort estimates, so these are justified priorities rather than proven global optima. They are not commitments to contribute upstream.

| Repository | The one change I would prioritize | Why this change over the report's first recommendation |
|---|---|---|
| Day.js | Add a concise, verified **fresh-clone verification recipe to CONTRIBUTING.md**, covering the supported Node environment, locked install, existing lint/build/ESM commands, one focused test and one built-library interaction. | Existing scripts and a lockfile already exist; the missing connection is how a fresh contributor gets from clone to a usable target. This addresses the observed missing-build and setup documentation and the absent bundle encountered by the audit. Factory first recommends a broader AGENTS.md. I would establish the tested canonical recipe first so an agent file can reference maintained instructions instead of becoming a second, potentially drifting command source. A recipe is not proof that the current uninstalled test collector passes. |
| yt-dlp | Have maintainers add **retained per-test timing/results to the existing core-test CI job**, rather than create another development environment. | The snapshot already documents Hatch and configures its environments; the audit's unsupported Python is insufficient evidence that a container is the best fix. In contrast, the report's `test_performance_tracking` failure is supported by the current workflow: it runs pytest through `devscripts/run_tests.py` without retained timing reports. One workflow change could pass `--durations=10` and a JUnit output path through the existing `--pytest-args` option, then retain the report on failure as well as success. This reuses an existing CI runtime and test job, gives agents/reviewers test names, outcomes and timings, and helps identify costly validation paths. I prioritize that bounded feedback improvement over Factory's first, broader recommendation to introduce strict typing, complexity limits and dependency analysis. Actual time savings remain unmeasured. Its no-AI contribution policy still requires human-maintainer ownership; this is a tooling proposal, not authorization for upstream agent contributions. |
| Caddy | Add a **root-module [`go mod tidy -diff`](https://go.dev/ref/mod#go-mod-tidy) CI check**, using the supported Go version. | The report found that AGENTS.md recommends tidy while release preparation checks a generated build module, leaving no equivalent root-module unused-dependency gate. One small check gives immediate feedback when an agent adds or removes imports and dependencies. Factory's first recommendation bundles this with coverage thresholds, timing and complexity limits; I would extract this existing, documented check first. It needs less threshold design and calibration than imposing new coverage/complexity policy, while guarding a concrete agent failure mode. |

The yt-dlp priority is grounded in its pinned [existing Hatch instructions](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/CONTRIBUTING.md#developer-instructions), [core-test workflow](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/.github/workflows/quick-test.yml), and [pytest argument forwarding](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/devscripts/run_tests.py). Pytest documents both [duration reporting](https://docs.pytest.org/en/stable/how-to/usage.html#profiling-test-execution-duration) and [JUnit XML output](https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files). These establish that the proposed mechanism is available; they do not show that the workflow change was implemented or tested.

No single proposed change is claimed to cross the maturity boundary. For Caddy especially, moving from 41/68 to 55/68 requires substantially more than this one check. The priority is reducing predictable friction per unit of implementation effort, not maximizing checklist count.

### Where the framework falls short

1. **Repository purpose and permission to use agents are separate axes.** Day.js is penalized for missing production tracing, alerting, runbooks and feature flags although it is an embedded library. A lack of centrally collected product analytics can also be a privacy/design choice. More significantly, yt-dlp explicitly bans AI contributions in its checked-in policy; its absent AGENTS.md and agentic-development evidence are partly intentional. Technical scaffolding cannot establish organizational permission. A better report would show a project-type applicability profile and a separate contribution-policy gate before recommending autonomous work.

2. **The audit mixes repository properties with the observer's environment.** Missing authenticated VCS tools is true of this run, not proof of deficient upstream tooling. Missing installed dependencies is distinct from broken tests; missing Go is distinct from a working or failing Go test suite. Documentation-fallback passes should be visibly distinguished from executed passes. Likewise, a depth-one clone cannot support conclusions about historical agent adoption, and `git log` in a shallow snapshot can misattribute inherited documents to the boundary commit. Those limitations are retained here instead of rewritten into facts about the projects.

3. **Existence heuristics can reward the wrong thing or miss ecosystem conventions.** Day.js passed `large_file_detection` because of a bundled-output size budget, although that does not detect oversized source files; the same budget also earns `heavy_dependency_detection`. Conversely, yt-dlp failed test naming despite having conventional `test_*.py` files, because the check demanded explicit configuration/documentation rather than accepting pytest's convention. Caddy's embedded persistence also triggered schema/N+1 expectations closer to database applications. These findings need contextual review before becoming remediation tickets.

4. **A maturity label is coarse and version-dependent.** The live CLI uses equal-weight global bands, while the assigned article describes gated progression. Caddy sits just above 60%: changing one current pass to a failure would produce **40/68 = 58.82%**, dropping it a level without a broad architectural regression. Several cheap documentation checks can also compensate numerically for a consequential missing control. I would report raw criteria, verified execution status and sensitive boundary cases alongside the level, and retain the CLI version when comparing later runs.

The defensible conclusion is limited: in these three snapshots, basic lint/test configuration was more consistently evidenced than additional code-quality enforcement and the framework's operational-feedback signals. Missing development containers and environment documentation were also recorded, but this run did not establish that existing contributor setups were unusable. Caddy's stronger observability has a visible server-specific explanation, and the score ordering persists under the stated observer/history exclusions. Three confounded observations do not establish general effects of language, size, age or commercial backing, or a ranking of overall software quality.

## Raw report output

The complete human-readable responses below are original Factory outputs, not rewritten summaries. Exact structured payloads and successful storage receipts are also included, so every criterion and rationale can be inspected independently of my mapping.

### Day.js

[Exact report payload](evidence/dayjs-report.json) · [Raw output file](evidence/dayjs-raw-output.md) · [Factory storage receipt](evidence/dayjs-receipt.json)

<details>
<summary>Complete original Day.js output</summary>

# Level
**Level 2, 35.59% readiness.** Passed 21 of 59 evaluated criteria; 38 failed and 25 were skipped.

Evaluated `dev` at `436bde0`. Report stored successfully. Source and configuration were unchanged.

# Applications
1. `.` - Day.js, a JavaScript date/time library with TypeScript declarations, plugins, and locales.

# Criteria
Skipped scores use `null/1` and are excluded from scoring.

**Style & Validation**
- Linter: 1/1 - ESLint with Airbnb rules runs in CI.
- Type checking: 0/1 - Declarations exist, but no configured type-check task.
- Formatter: 1/1 - Prettier configuration and documentation-formatting command exist.
- Pre-commit hooks: 1/1 - Commits trigger linting.
- Strict typing: 0/1 - No strict checking configuration.
- Naming consistency: 1/1 - Inherited Airbnb naming rules.
- Cyclomatic complexity: 0/1 - No complexity threshold configured.
- Large-file detection: 1/1 - CI enforces the built bundle’s size limit.
- Dead-code detection: 1/1 - Inherited ESLint unused-variable checks.
- Duplicate-code detection: 0/1 - No duplication scanner.
- Code modularization: null/1 - Skipped for this compact, single-package library.
- Technical-debt tracking: 0/1 - No enforced TODO tracking or debt process.
- N+1 detection: null/1 - No database or ORM.

**Build System**
- Build command documentation: 0/1 - Build scripts are not documented in contributor instructions.
- Pinned dependencies: 1/1 - Committed `package-lock.json`.
- VCS CLI tools: 0/1 - GitHub and GitLab CLIs are unavailable.
- Automated PR review: null/1 - Requires authenticated remote evidence.
- Agentic development: 0/1 - No agent workflow or available co-authorship evidence.
- Fast CI feedback: null/1 - Remote CI timing unavailable.
- Build-performance tracking: null/1 - No deliberate tracking; remote evidence unavailable.
- Deployment frequency: null/1 - Remote release history unavailable.
- Single-command setup: 0/1 - No fresh-clone development sequence documented.
- Feature flags: 0/1 - No feature-flag infrastructure.
- Release-note automation: 1/1 - Semantic-release generates the changelog.
- Progressive rollout: null/1 - Not an infrastructure repository.
- Rollback automation: null/1 - Not an infrastructure repository.
- Monorepo tooling: null/1 - Single-package repository.
- Heavy-dependency detection: 1/1 - Bundle-size budget enforced.
- Unused-dependency detection: 0/1 - No configured checker.
- Version-drift detection: null/1 - Only one build package.
- Release automation: 1/1 - Automated releases on `master`; evaluated branch is `dev`.
- Dead-feature-flag detection: null/1 - No feature-flag infrastructure.

**Testing**
- Unit tests exist: 1/1 - Core, plugin, locale, and regression tests.
- Integration tests exist: 1/1 - Browser bundle and cross-plugin coverage.
- Unit tests runnable: 0/1 - `npx --no-install jest --listTests` exited 1 because dependencies are absent. No tests ran.
- Test-performance tracking: 0/1 - No retained timing reports or analytics.
- Flaky-test detection: null/1 - No local tooling; remote evidence unavailable.
- Coverage thresholds: 1/1 - CI enforces 100% line coverage.
- Test naming: 1/1 - Explicit Jest filename pattern.
- Test isolation: 1/1 - Jest uses isolated environments and default workers.
- Interactive QA documented: 0/1 - No complete repository-local setup and interaction path.
- Interactive QA runnable: 0/1 - Library interaction failed because `dayjs.min.js` is absent.

**Documentation**
- `AGENTS.md`: 0/1 - Missing.
- README: 1/1 - Installation and usage examples exist.
- Automated documentation: 1/1 - Changelog generation configured.
- Skills: 0/1 - No repository-local skills.
- Documentation freshness: 1/1 - Core documentation updated September 15, 2026.
- API schemas: null/1 - No HTTP or GraphQL service.
- Architecture documentation: 0/1 - No architecture diagrams or dependency-flow documentation.
- `AGENTS.md` validation: 0/1 - Instructions and validation are absent.
- Runbooks: 0/1 - No incident-response documentation or pointers.
- Issue templates: 1/1 - Structured bug-report template.
- Issue labeling: 0/1 - No evidenced priority, type, and area taxonomy.
- Backlog health: null/1 - Authenticated remote access unavailable.
- PR templates: 0/1 - Missing.

**Dev Environment**
- Devcontainer: 0/1 - No configuration.
- Environment template: 0/1 - No template or documented environment requirements.
- Local services setup: null/1 - No external runtime services required.
- Database schema: null/1 - No database.
- Devcontainer runnable: null/1 - CLI unavailable.
- Comprehensive gitignore: 0/1 - Generated files are excluded, but `.env` variants are not.

**Debugging & Observability**
- Structured logging: 0/1 - No structured logger.
- Distributed tracing: 0/1 - No tracing instrumentation.
- Metrics collection: 0/1 - No application telemetry.
- Code-quality metrics: 1/1 - Coverage collection and conditional Codecov upload.
- Contextual error tracking: 0/1 - No error-tracking integration.
- Alerting: 0/1 - No alert definitions.
- Deployment observability: 0/1 - No deployment-impact dashboards or notifications.
- Health checks: null/1 - Library, not a deployed service.
- Circuit breakers: null/1 - No external-service calls.
- Profiling: 0/1 - No configured profiling tools.
- Log scrubbing: 0/1 - No redaction or scrubbing mechanism.
- Product analytics: 0/1 - No instrumentation.
- Error-to-insight pipeline: 0/1 - No error-to-issue automation.

**Security**
- Branch protection: null/1 - Authenticated admin verification unavailable.
- Secret scanning: null/1 - No local scanner; native settings unverifiable.
- CODEOWNERS: 0/1 - Missing.
- Automated security review: null/1 - No local assessment workflow; remote evidence unavailable.
- Dependency updates: 0/1 - No Dependabot or Renovate configuration.
- DAST: null/1 - Not a deployed web service.
- PII handling: null/1 - No personal-data collection identified.
- Privacy compliance: null/1 - No end-user data collection.
- Secrets management: 1/1 - CI uses GitHub Actions secrets.
- Minimum release age: 0/1 - No dependency-update waiting period.

# Action Items
- Add `AGENTS.md` documenting dependency installation, supported Node version, build commands, environment requirements, and a verifiable library smoke interaction.
- Add CI type checking for declarations and unused-dependency detection.
- Configure dependency-update automation with a minimum release age, and ignore secret-bearing `.env` files.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Fiamkun%2Fdayjs

</details>

### yt-dlp

[Exact report payload](evidence/yt-dlp-report.json) · [Raw output file](evidence/yt-dlp-raw-output.md) · [Factory storage receipt](evidence/yt-dlp-receipt.json)

<details>
<summary>Complete original yt-dlp output</summary>

# Level
Level 3

**47.54%**, 29 passed, 32 failed, 23 skipped. All 84 criteria were validated and stored.

Runtime verification was blocked by missing Python 3.11+. No tests executed, packages installed, or source/configuration changed. Remote checks were limited by unavailable `gh`/`glab`; Git history is shallow.

The repository explicitly prohibits AI-authored contributions. This score does not override that policy.

# Applications
1. `.` - Python audio/video downloader CLI and embeddable library.

# Criteria
`null/1` means skipped and excluded from scoring.

**Style & Validation**
- `lint_config`: 1/1 - Ruff configured and enforced in CI.
- `type_check`: 0/1 - No Python static type checker configured.
- `formatter`: 1/1 - autopep8 configured and checked in CI.
- `pre_commit_hooks`: 1/1 - Ruff and formatting hooks provided.
- `strict_typing`: 0/1 - No strict type-checking configuration.
- `naming_consistency`: 1/1 - Ruff naming rules and documented extractor conventions.
- `cyclomatic_complexity`: 0/1 - No complexity analyzer or thresholds.
- `large_file_detection`: 0/1 - No file-size limits or equivalent checks.
- `dead_code_detection`: 1/1 - Ruff detects unused imports and variables.
- `duplicate_code_detection`: 0/1 - No duplication detector.
- `code_modularization`: 0/1 - Package boundaries lack automated enforcement.
- `tech_debt_tracking`: 0/1 - TODO formatting exists, but tracking and issue-link enforcement do not.
- `n_plus_one_detection`: null/1 - No application database or ORM.
- `unused_dependencies_detection`: 0/1 - No declared-dependency usage checks.

**Build System**
- `build_cmd_doc`: 1/1 - README documents compilation and packaging commands.
- `deps_pinned`: 1/1 - Committed lockfile and hashed, pinned requirements.
- `vcs_cli_tools`: 0/1 - Neither `gh` nor `glab` installed.
- `automated_pr_review`: null/1 - Requires unavailable authenticated CLI access.
- `agentic_development`: 0/1 - No active agent evidence; contributions explicitly prohibited.
- `fast_ci_feedback`: null/1 - Actual PR check durations unavailable.
- `build_performance_tracking`: null/1 - No verified performance tracking or remote timing access.
- `deployment_frequency`: null/1 - Actual successful release frequency unverified.
- `single_command_setup`: 1/1 - Hatch setup and direct source execution documented.
- `feature_flag_infrastructure`: 0/1 - No rollout-oriented feature flag system.
- `release_notes_automation`: 1/1 - Release workflows generate changelogs and notes.
- `progressive_rollout`: null/1 - Not an infrastructure repository.
- `rollback_automation`: null/1 - Not an infrastructure repository.
- `monorepo_tooling`: null/1 - Single root application.
- `heavy_dependency_detection`: null/1 - Python CLI, not a frontend bundle.
- `version_drift_detection`: null/1 - Single build package/module.
- `release_automation`: 1/1 - Automated GitHub/PyPI release workflows.
- `dead_feature_flag_detection`: null/1 - No feature flag infrastructure.

**Testing**
- `unit_tests_exist`: 1/1 - Extensive existing unit tests under `test/`.
- `integration_tests_exist`: 1/1 - HTTP downloader, networking, and subprocess integration tests.
- `unit_tests_runnable`: null/1 - Bounded collection of `test/test_cache.py` exited 4 at the unsupported-Python guard.
- `test_performance_tracking`: 0/1 - No retained timing reports or test analytics.
- `flaky_test_detection`: 1/1 - CI retries and explicit flaky-test exclusion.
- `test_coverage_thresholds`: 0/1 - No coverage gate; coverage command explicitly unimplemented.
- `test_naming_conventions`: 0/1 - Consistent files, but no explicit discovery patterns or documented file-naming rule.
- `test_isolation`: 1/1 - Hatch configures randomization and parallel-test tooling.
- `interactive_qa_exists`: 1/1 - Complete documented source-launch and offline CLI interactions.
- `interactive_qa_runnable`: 1/1 - Documentation fallback applied; actual launch failed on unsupported Python.

**Documentation**
- `agents_md`: 0/1 - No root `AGENTS.md`.
- `readme`: 1/1 - Comprehensive installation, usage, and build documentation.
- `automated_doc_generation`: 1/1 - README help, supported sites, templates, and manpages generated.
- `skills`: 0/1 - No repository-local skill definitions.
- `documentation_freshness`: 1/1 - Local history lists key documentation within 180 days; shallow-history caveat.
- `api_schema_docs`: null/1 - CLI consumes APIs but exposes no service API.
- `service_flow_documented`: 1/1 - External APIs and endpoint configuration documented.
- `agents_md_validation`: 0/1 - No agent instructions or validation automation.
- `runbooks_documented`: 0/1 - No operational runbook pointers found.
- `issue_templates`: 1/1 - Structured bug, feature, and site-request templates.
- `issue_labeling_system`: 0/1 - Complete priority/type/area taxonomy not established.
- `backlog_health`: null/1 - Live issue sample unavailable.
- `pr_templates`: 0/1 - Template lacks a testing-performed section.

**Dev Environment**
- `devcontainer`: 0/1 - No development-container configuration.
- `env_template`: 1/1 - Environment variables and defaults documented.
- `local_services_setup`: null/1 - No required local service stack.
- `database_schema`: null/1 - No application-owned database.
- `devcontainer_runnable`: null/1 - Devcontainer CLI unavailable.

**Debugging & Observability**
- `structured_logging`: 0/1 - Logger adapter exists, but no dedicated logging module or logging dependency.
- `distributed_tracing`: 0/1 - No application-wide trace/request propagation.
- `metrics_collection`: 0/1 - No configured metrics collection system.
- `code_quality_metrics`: null/1 - No qualifying local metrics tracking; remote analyses unverified.
- `error_tracking_contextualized`: 0/1 - No contextualized error-tracking integration.
- `alerting_configured`: 0/1 - No operational alerting rules.
- `deployment_observability`: 0/1 - No deploy-impact dashboards or notifications.
- `health_checks`: null/1 - CLI/library, not a continuously deployed service.
- `circuit_breakers`: 1/1 - Retry management supports exponential backoff.
- `profiling_instrumentation`: 0/1 - No configured profiler or profiling workflow.
- `product_analytics_instrumentation`: 0/1 - No product-usage analytics.
- `error_to_insight_pipeline`: 0/1 - No error-to-issue automation.

**Security**
- `branch_protection`: null/1 - Permissions and protection settings unverified.
- `secret_scanning`: null/1 - No local scanner; native scanning status inaccessible.
- `codeowners`: 0/1 - No `CODEOWNERS`.
- `automated_security_review`: 1/1 - CodeQL workflows publish security findings.
- `dependency_update_automation`: 1/1 - Custom dependency bot evidenced by generated metadata and recorded update PRs.
- `gitignore_comprehensive`: 0/1 - Missing `.env` secret-file exclusions.
- `dast_scanning`: null/1 - Not a deployed web service.
- `pii_handling`: 1/1 - Personal-metadata warnings, cleanup, and credential-handling guidance.
- `privacy_compliance`: null/1 - No centralized end-user collection service.
- `secrets_management`: 1/1 - GitHub Actions secrets and protected credential-file guidance.
- `log_scrubbing`: 1/1 - Usernames and passwords masked in configuration logs.
- `min_release_age`: 1/1 - Seven-day dependency delay configured, with explicit exemptions.

# Action Items
- Add strict Python type checking, complexity limits, and unused-dependency checks to CI.
- Implement coverage thresholds, retained test-timing reports, and explicit pytest discovery patterns.
- Exclude `.env` secrets, add a PR testing-results section, and provide a Python 3.11+ devcontainer.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Fyt-dlp%2Fyt-dlp

</details>

### Caddy

[Exact report payload](evidence/caddy-report.json) · [Raw output file](evidence/caddy-raw-output.md) · [Factory storage receipt](evidence/caddy-receipt.json)

<details>
<summary>Complete original Caddy output</summary>

# Level
Level 4, **60.29%**.

41 passed, 27 failed, 16 skipped. All 84 criteria validated and stored.

Go and authenticated VCS CLIs were unavailable. No tests ran, no packages were installed, and no source or configuration files changed. `null/1` means skipped and excluded from scoring.

# Applications
1. **.** - Caddy HTTPS server, CLI, and extensible Go server platform. Primary language: Go.

# Criteria

**Style & Validation**
- `lint_config`: 1/1 - golangci-lint configured and invoked by CI.
- `type_check`: 1/1 - Go compilation provides static type checking.
- `formatter`: 1/1 - gofmt, gofumpt, goimports, and gci configured.
- `pre_commit_hooks`: 1/1 - Security, lint, formatting, and whitespace hooks configured.
- `strict_typing`: null/1 - Go has no separate stricter typing mode.
- `naming_consistency`: 1/1 - AGENTS.md specifies naming conventions.
- `cyclomatic_complexity`: 0/1 - No enabled complexity threshold.
- `large_file_detection`: 0/1 - No file-size or line-count guard.
- `dead_code_detection`: 1/1 - staticcheck and unused enabled.
- `duplicate_code_detection`: 1/1 - dupl enabled with scoped exclusions.
- `code_modularization`: 1/1 - Go `internal/` packages enforce boundaries.
- `tech_debt_tracking`: 0/1 - No enforced TODO tracking or debt-management process.

**Build System**
- `build_cmd_doc`: 1/1 - README.md and AGENTS.md document builds.
- `deps_pinned`: 1/1 - Fixed Go dependency versions and committed checksums.
- `vcs_cli_tools`: 0/1 - Neither gh nor glab is installed.
- `automated_pr_review`: null/1 - Authenticated CLI unavailable.
- `agentic_development`: 0/1 - No strong active-agent evidence; history is shallow.
- `fast_ci_feedback`: null/1 - Actual PR check durations unavailable.
- `build_performance_tracking`: null/1 - No explicit tracking evidence or authenticated access.
- `deployment_frequency`: null/1 - Release/deployment history unavailable.
- `single_command_setup`: 1/1 - Short documented build/run and integration-harness paths.
- `feature_flag_infrastructure`: 0/1 - No managed feature-flag system.
- `release_notes_automation`: 1/1 - GoReleaser and release proposals generate changelogs.
- `progressive_rollout`: null/1 - Not a deployment-infrastructure repository.
- `rollback_automation`: null/1 - No managed deployment environment.
- `monorepo_tooling`: null/1 - Single application.
- `heavy_dependency_detection`: null/1 - Non-bundled Go server/CLI.
- `unused_dependencies_detection`: 0/1 - No root-module tidy verification in CI.
- `version_drift_detection`: null/1 - Only one build module.
- `release_automation`: 1/1 - Automated packaging, signing, and publishing workflows.
- `dead_feature_flag_detection`: null/1 - Feature-flag prerequisite absent.

**Testing**
- `unit_tests_exist`: 1/1 - Extensive Go unit tests.
- `integration_tests_exist`: 1/1 - Dedicated server integration harness and tests.
- `unit_tests_runnable`: null/1 - Go runtime unavailable; no tests executed.
- `test_performance_tracking`: 0/1 - No deliberate duration reporting or trend tracking.
- `flaky_test_detection`: 1/1 - s390x CI job configures failed-test retries.
- `test_coverage_thresholds`: 0/1 - Coverage measured, but no minimum enforced.
- `test_naming_conventions`: 1/1 - Go test naming conventions enforced.
- `test_isolation`: 1/1 - Parallel tests, temporary directories, and cleanup patterns.
- `interactive_qa_exists`: 1/1 - Documented harness starts Caddy and checks HTTP responses.
- `interactive_qa_runnable`: 1/1 - Documentation fallback accepted; no live execution claimed.

**Documentation**
- `agents_md`: 1/1 - Substantial root agent instructions.
- `readme`: 1/1 - Requirements, installation, build, and usage guidance.
- `automated_doc_generation`: 1/1 - Release tooling generates manual pages.
- `skills`: 0/1 - No repository-local valid skills.
- `documentation_freshness`: 1/1 - Requested history check finds recent docs; shallow-history caveat.
- `api_schema_docs`: 0/1 - No OpenAPI, Swagger, or GraphQL schema.
- `service_flow_documented`: 1/1 - Modules, configuration flow, and certificate providers documented.
- `agents_md_validation`: 0/1 - No automated accuracy validation.
- `runbooks_documented`: 0/1 - No operational incident-response runbook pointer.
- `issue_templates`: 1/1 - Structured issue form exists.
- `issue_labeling_system`: 0/1 - Priority/type/area taxonomy not evidenced.
- `backlog_health`: null/1 - Authenticated issue inspection unavailable.
- `pr_templates`: 0/1 - Disclosure template lacks description and testing sections.

**Dev Environment**
- `devcontainer`: 0/1 - No devcontainer configuration.
- `env_template`: 0/1 - No environment template or explicit environment contract.
- `local_services_setup`: null/1 - Local HTTP target needs no external services.
- `database_schema`: 0/1 - ACME bbolt record schema not defined locally.
- `devcontainer_runnable`: null/1 - Devcontainer CLI unavailable.
- `n_plus_one_detection`: 0/1 - Embedded persistence exists without lookup-amplification analysis.

**Debugging & Observability**
- `structured_logging`: 1/1 - Zap and dedicated logging modules.
- `distributed_tracing`: 1/1 - OpenTelemetry trace propagation and log correlation.
- `metrics_collection`: 1/1 - Prometheus instrumentation.
- `code_quality_metrics`: 1/1 - CI generates coverage profiles.
- `error_tracking_contextualized`: 0/1 - No contextual error-tracking integration.
- `alerting_configured`: 0/1 - No configured alert rules or incident notifications.
- `deployment_observability`: 0/1 - No deployment-impact dashboard pointers.
- `health_checks`: 1/1 - Active and passive upstream health checks.
- `circuit_breakers`: 1/1 - Failure suppression, recovery, and resilience hooks.
- `profiling_instrumentation`: 1/1 - Admin pprof and trace endpoints.
- `product_analytics_instrumentation`: 0/1 - No product-usage analytics integration.
- `error_to_insight_pipeline`: 0/1 - No error-to-issue automation.

**Security**
- `branch_protection`: null/1 - Authenticated admin inspection unavailable.
- `secret_scanning`: 1/1 - Gitleaks pre-commit hook configured.
- `codeowners`: 0/1 - No CODEOWNERS file.
- `automated_security_review`: 1/1 - Dependency-review comments, vulnerability checks, and SARIF reports.
- `dependency_update_automation`: 1/1 - Dependabot configured; live PR activity unverified.
- `gitignore_comprehensive`: 0/1 - `.env` exclusions cover only one specific directory.
- `dast_scanning`: 1/1 - CI includes custom live-endpoint security regressions.
- `pii_handling`: 1/1 - IP masking and sensitive-field filtering.
- `privacy_compliance`: 1/1 - Privacy-by-design logging minimization mechanisms.
- `secrets_management`: 1/1 - Workflows use GitHub Actions secrets.
- `log_scrubbing`: 1/1 - Redaction, hashing, deletion, and credential suppression.
- `min_release_age`: 0/1 - Monthly updates do not enforce dependency release age.

# Action Items
- Strengthen CI with coverage thresholds, retained test timings, root-module tidy verification, and complexity limits.
- Document the environment contract, broaden `.env` exclusions, and add a validated devcontainer.
- Add API schemas, operational runbooks, CODEOWNERS, complete PR-template sections, and AGENTS.md validation.

---
View the full report: https://app.factory.ai/analytics/readiness/https%3A%2F%2Fgithub.com%2Fcaddyserver%2Fcaddy

</details>

## Source and reproduction notes

- [Assignment requirements](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week5/assignment.md); [assigned framework article](https://factory.com/news/agent-readiness); [current CLI report documentation](https://docs.factory.com/agent-readiness/readiness-report); [current framework overview](https://docs.factory.com/agent-readiness/overview).
- Relevant pinned source checks: [Day.js contributing instructions](https://github.com/iamkun/dayjs/blob/436bde0bcded312781cbe45dc2b0ef079a36d8e3/CONTRIBUTING.md), [Day.js package scripts](https://github.com/iamkun/dayjs/blob/436bde0bcded312781cbe45dc2b0ef079a36d8e3/package.json), [yt-dlp contributor instructions and policy](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/CONTRIBUTING.md), [yt-dlp runtime, dependencies and test settings](https://github.com/yt-dlp/yt-dlp/blob/b77c9304e1c4220cca450c583491904daf8455af/pyproject.toml), [Caddy contributor/agent instructions](https://github.com/caddyserver/caddy/blob/1a870400e684156f240f8db6e225c980b4357a80/AGENTS.md), [Caddy CI](https://github.com/caddyserver/caddy/blob/1a870400e684156f240f8db6e225c980b4357a80/.github/workflows/ci.yml), [Caddy lint configuration](https://github.com/caddyserver/caddy/blob/1a870400e684156f240f8db6e225c980b4357a80/.golangci.yml).
- Original JSON, raw outputs, run metadata and mapping are in `week5/evidence/`. `recompute.py` validates 84 unique criterion IDs, one-app denominators and legal skips, then recalculates rates and tables. [checksums.json](evidence/checksums.json) fingerprints the evidence.
- AI assistance: Droid generated the three audits; Codex assisted with evidence extraction, arithmetic, comparison and drafting. No claim is made that these reports independently verify every upstream setting, that proposed fixes were implemented, or that any full suite passed.
