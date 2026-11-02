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
