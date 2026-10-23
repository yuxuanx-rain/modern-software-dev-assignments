# Working in Day.js

Day.js is an immutable JavaScript date/time library with opt-in plugins and locales.
This checkout develops the library; it is not a web app and has no dev server.

## Map
- `src/index.js` implements the factory and `Dayjs` class; `src/constant.js` and
  `src/utils.js` support it. Core setters clone rather than mutate the input.
- `src/plugin/<name>/index.js` exports a plugin receiving options, the class,
  and the factory. Register it with `dayjs.extend(...)` before testing its API.
- `src/locale/` contains editable locale definitions. Plugin tests live in
  `test/plugin/<name>.test.js`; core tests are in `test/`.
- `types/index.d.ts` and `types/plugin/*.d.ts` are declaration sources. Public API
  changes may require matching declarations. `build/` contains editable build
  scripts, not generated bundles.

## Commands (from the repository root)
Use Node.js and npm; CI selects Node LTS and runs `npm install`, lint, and tests.
For this lockfile, install reproducibly with `npm ci`.

```sh
npm run lint
./node_modules/.bin/jest test/plugin/isLeapYear.test.js --runInBand --coverage=false
TZ=UTC npm test
npm run build
npm run babel
node -e "const dayjs = require('./dayjs.min.js'); console.log(dayjs('2024-02-29').format('YYYY-MM-DD'))"
```

Replace the focused test path for your change. Focused tests disable coverage
because Jest otherwise collects coverage across `src/**/*`. `npm test` is the
full gate: it runs core/plugin timezone tests under several `TZ` values, then
the suite with 100% global line coverage. Use `TZ=UTC npm test`: the final stage
inherits the host timezone, and unpinned Los Angeles runs fail date/DST cases.
The earlier stages still select their own timezones. A focused pass is not a
full-suite pass.
`npm run build` produces UMD bundles and runs the size check; `npm run babel`
produces ESM output. The Node example requires the UMD build first; importing
the package root before building points at a missing `dayjs.min.js`.
On Node 24, if the size check reports `ERR_OSSL_EVP_UNSUPPORTED`, rerun as
`NODE_OPTIONS=--openssl-legacy-provider npm run build` (per-command only).

## Editing and checks
- Follow `.editorconfig` (two spaces, LF) and `.eslintrc.json`: Airbnb base,
  single-quoted imports, no semicolons or trailing commas. `npm run prettier`
  formats documentation Markdown only; it does not format JavaScript.
- Tests use Jest `it`/`test` and `expect`. Import the local source (`../../src`
  from plugin tests), not the installed `dayjs` package. Mirror neighboring
  plugin tests and reset MockDate when a test freezes time.
- For a small change, run its focused test and `npm run lint`; report whether
  the full `npm test` gate was also run and any failures separately.
- Edit `src/` and `types/`, not generated root `plugin/`, `locale/`, `esm/`,
  `dayjs.min.js`, `index.d.ts`, or `locale.json`. Do not commit `coverage/` or
  `node_modules/`. Preserve `package-lock.json` unless dependencies change.
