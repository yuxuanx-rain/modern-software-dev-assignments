# Execution evidence

Exploration and trial execution used Node v24.16.0 and npm 11.13.0 on macOS.
All commands below ran at the root of the Day.js checkout. Command output is
preserved in the named logs; exit codes below were observed by the calling shell.

| Log | Command | Exit |
|---|---|---|
| install.log | npm ci --cache /tmp/cs146s-week4-npm-cache --no-audit --no-fund | 0 |
| baseline-lint.log | npm run lint | 0 |
| baseline-plugin.log | ./node_modules/.bin/jest test/plugin/isLeapYear.test.js --runInBand --coverage=false | 0 |
| task1-test.log | ./node_modules/.bin/jest test/plugin/isLeapYear.test.js --runInBand --coverage=false | 0 |
| task1-lint.log | npm run lint | 0 |
| full-test.log | npm test | 1 |
| full-test-utc-baseline.log | TZ=UTC npm test | 0 |
| build.log | npm run build | 1 |
| build-compat.log | NODE_OPTIONS=--openssl-legacy-provider npm run build | 0 |
| esm-build.log | npm run babel | 0 |
| smoke.log | node -e "const dayjs = require('./dayjs.min.js'); console.log(dayjs('2024-02-29').format('YYYY-MM-DD'))" | 0 |
| task2-test.log | ./node_modules/.bin/jest test/plugin/isLeapYear.test.js --runInBand --coverage=false | 0 |
| task2-lint.log | npm run lint | 0 |
| task2-full-test.log | TZ=UTC npm test | 0 |

AGENTS.initial.md is the file used for the first trial. The final file adds the
UTC full-gate command and the observed Node 24 build workaround. task2.patch
contains the exact three test cases added in the second trial. environment.json
records the unpinned environment. fork-created.png records the created GitHub fork.

Both trials were performed by Codex in the same conversation; these logs do not
represent independent agent sessions or student terminal activity.

## Final verification on 2026-10-25

The published Day.js `dev` files were downloaded into a fresh temporary checkout.
Its AGENTS.md and isLeapYear test were byte-compared with the local deliverables.
The final verification commands and observed exits are recorded in
[final-checks.json](final-checks.json); corresponding outputs are
[focused tests](final-focused.log), [lint](final-lint.log),
[full tests](final-full-tests.log), [UMD build](final-build.log),
[ESM build](final-esm.log), and [smoke example](final-smoke.log).

[artifact-checks.json](artifact-checks.json) records structural checks and hashes.
The requirement mapping and unresolved submission gates are documented in
[FINAL_REVIEW.md](../FINAL_REVIEW.md).
