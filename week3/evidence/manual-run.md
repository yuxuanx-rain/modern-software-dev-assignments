# First execution, before authoring the skill

The workflow was executed by Codex assisting the student, without the new skill installed. This is a constructed application configuration error, not a discovered upstream defect.

- Target: https://github.com/bigskysoftware/htmx
- Checkout: `fa978b24e75fb03c137bf2cdae4fef0e711cf8a1`; htmx 2.0.11.
- Runtime: Node v24.16.0; npm 11.13.0; Chromium installed by the locked Playwright dependency.
- Report: clicking a weather button should replace the result panel with `Sunny 22C`; it remains `Not queried`.
- Fixture: `manual-target-repro.js`, copied into `test/attributes/week3-target-repro.js` in the htmx checkout.

## Procedure and observations

1. Inspected `package.json`, `web-test-runner.config.mjs`, `test/util/util.js`, and existing `test/attributes/hx-target.js`.
2. Installed dependencies with `npm ci --cache /private/tmp/cs146s-week3-npm-cache --no-audit --no-fund`. A first install using the default npm cache failed with EACCES; switching the cache resolved the environment issue.
3. Installed Chromium using `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/cs146s-week3-browsers npx playwright install chromium`.
4. Ran the existing target tests: **17 passed, 0 failed**, exit 0. See `manual-baseline.log`.
5. Ran the constructed fixture: **0 passed, 1 failed**, exit 1. The assertion expected `Sunny 22C` but observed `Not queried`; the console emitted `htmx:targetError, #missing-result`. See `manual-failing.log`.
6. Inspected `getTarget()` and `issueAjaxRequest()` in `src/htmx.js`. A missing target is rejected before the request is issued. This challenged the initial assumption that a response might already have arrived.
7. Changed only `hx-target="#missing-result"` to `hx-target="#weather-result"` in the local fixture. The unchanged expected-result assertion then passed: **1 passed, 0 failed**, exit 0. See `manual-target-fixed.js` and `manual-fixed.log`.
8. Verified the clickable demo in desktop and mobile Chromium. The working button issued one weather request and updated its panel. The broken button emitted `htmx:targetError`, issued no request, and left its panel unchanged. Neither viewport overflowed horizontally. See `demo-verification.json` and screenshots.

## Exact test commands

From the htmx checkout, with the browser cache variable set:

```sh
npx web-test-runner --files test/attributes/hx-target.js --browsers chromium --playwright
npx web-test-runner --files test/attributes/week3-target-repro.js --browsers chromium --playwright
```

The second command was executed once before and once after the selector correction. The failing and corrected fixture snapshots are both retained.

## Judgment extracted for the skill

Observe requests, status, events, and DOM before choosing a cause. Missing-target errors belong to the no-request branch; do not assume every unchanged panel is a failed HTTP response. Diagnose the caller's configuration before altering library code. Use a controlled change with the original expectation intact.
