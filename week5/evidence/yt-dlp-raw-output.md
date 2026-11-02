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
