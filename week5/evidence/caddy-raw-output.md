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
