# htmx reproduction reference

Run commands from the htmx checkout. First inspect repository instructions and scripts: commands here were verified on commit `fa978b24e75fb03c137bf2cdae4fef0e711cf8a1` (2.0.11). Recheck them on another version.

## Setup and commands

```sh
git status --short
git rev-parse HEAD
node --version
npm --version
npm ci
npx playwright install chromium
```

Use Node 20 or later. If the user already supplies `PLAYWRIGHT_BROWSERS_PATH`, retain it consistently for installation and tests. If npm's default cache is unwritable, use a writable temporary cache, for example `npm ci --cache /tmp/htmx-npm-cache`. Resolve environment failures before interpreting behavioral tests.

Choose the closest test file rather than assuming every report is a target problem. Examples:

```sh
npx web-test-runner --files test/attributes/hx-target.js --browsers chromium --playwright
npx web-test-runner --files test/attributes/week3-repro.js --browsers chromium --playwright
npx web-test-runner --files test/attributes/hx-target.js test/attributes/week3-repro.js --browsers chromium --playwright
npm run lint
```

For response handling, inspect `test/core/ajax.js` and select the closest tests after reading them. Run `npm test` if changing library source. The native runner uses `web-test-runner.config.mjs`, loads `src/htmx.js`, and supplies Mocha, Chai, Sinon, and `test/util/util.js`.

## Minimal native fixture

Create a new case file; substitute the *reported* HTML and response behavior. This skeleton illustrates a successful swap, not a ready-made diagnosis:

```javascript
describe('Local interaction reproduction', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })
  it('shows the expected result', function() {
    this.server.respondWith('GET', '/fragment', [200, { 'Content-Type': 'text/html' }, 'Loaded'])
    var target = make('<div id="result">Empty</div>')
    var button = make('<button hx-get="/fragment" hx-target="#result">Load</button>')
    button.click()
    this.server.respond()
    this.server.requests.length.should.equal(1)
    target.textContent.should.equal('Loaded')
  })
})
```

`make()` inserts and processes fixture elements. Attach event listeners before clicking and remove them during cleanup. Preserve failing logs before corrections. After recording the failure, move the failing test file itself outside `test/attributes/**/*.js` and `test/core/**/*.js`; copying it to evidence while leaving the original under `test/` still breaks discovery. For example, for a newly created reproduction:

```sh
mkdir -p reproduction-evidence
mv test/attributes/week3-repro.js reproduction-evidence/original.js
# Write the corrected case back to test/attributes/week3-repro.js, then run it.
```

Preserve the failure log and archived assertion unchanged; keep only the corrected case active for final checks. Unexpected console errors require investigation; an expected error event in a deliberately broken fixture is evidence, not automatically a failed test run.

## Local reproduction only

Do not call live write endpoints when a fake response suffices. Do not change global error-response handling to resolve one local case without investigating its effect. Keep unrelated files and existing tests intact.
