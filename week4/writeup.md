# Week 4 Write-up

**Repo chosen and link to fork:** [yuxuanx-rain/dayjs](https://github.com/yuxuanx-rain/dayjs), forked from iamkun/dayjs.

**Baseline:** `dev` at [`436bde0bcded312781cbe45dc2b0ef079a36d8e3`](https://github.com/iamkun/dayjs/tree/436bde0bcded312781cbe45dc2b0ef079a36d8e3).

**File written:** [`AGENTS.md`](https://github.com/yuxuanx-rain/dayjs/blob/dev/AGENTS.md) at the root of the Day.js fork; an identical submission copy is beside this writeup. Neither AGENTS.md nor CLAUDE.md existed in the cloned project before this work. The final file is 415 words, approximately one page.

## Part I: Exploration

| | Finding |
|---|---|
| Build / run | Run commands from the Day.js root. `npm ci` installs the lockfile reproducibly. `npm run build` builds UMD output and runs the size check; on the verified Node 24 environment, use `NODE_OPTIONS=--openssl-legacy-provider npm run build` if the size check reports `ERR_OSSL_EVP_UNSUPPORTED`. `npm run babel` creates ESM output. This is a library, with no application server or start script. After building, `node -e "const dayjs = require('./dayjs.min.js'); console.log(dayjs('2024-02-29').format('YYYY-MM-DD'))"` prints `2024-02-29`. |
| Test | Jest 22 and Babel load local ES6 source. Focused command: `./node_modules/.bin/jest test/plugin/isLeapYear.test.js --runInBand --coverage=false`. The official `npm test` runs core/plugin timezone tests in multiple zones, then the full suite with 100% global line coverage. Use `TZ=UTC npm test` to make the final stage reproducible; each explicitly configured timezone stage still runs in its designated zone. |
| Lint / format | `npm run lint` runs ESLint over `src/* test/* build/*`. `.eslintrc.json` extends Airbnb base and disables semicolons and trailing commas. `.editorconfig` specifies two-space indentation and LF. `npm run prettier` formats only documentation Markdown, not JavaScript. |
| Key directories and entry points | `src/index.js`: factory/class; `src/constant.js` and `src/utils.js`: support; `src/plugin/<name>/index.js`: extensions; `src/locale/`: locale sources; `test/`: core/plugin/locale tests; `types/`: editable declarations; `build/index.js`, `build/rollup.config.js`, and `build/esm.js`: tooling. CI is in `.github/workflows/check.yml` and `lint-test.yml`. |
| Unstated conventions | Plugin tests import `../../src` and the local plugin, then register it with `dayjs.extend`. Tests use Jest `it`/`test` and `expect`; the leap-year test has MockDate setup/reset hooks. Plugin APIs have corresponding declarations under `types/plugin/`. Core setters clone, although opt-in plugins such as badMutable intentionally change behavior. |
| Off-limits (generated, vendored) | `.gitignore` and build scripts distinguish editable `src/plugin/`, `src/locale/`, and `types/` from generated root `plugin/`, `locale/`, `esm/`, `dayjs.min.js`, `index.d.ts`, and `locale.json`. `build/` is editable tooling. Do not hand-edit or commit `node_modules/` or `coverage/`. Preserve the lockfile for this documentation/test-only change. |

**How you figured it out — what you asked the agent, what you had to read yourself:**

I developed the configuration through multiple rounds of research and discussion with Codex. The conversation began with interpreting the assignment and its rubric, then choosing a repository that would support concrete exploration and two manageable trial tasks. After discussing Day.js's structure, available checks, and suitability, I selected it and asked Codex to begin the repository exploration.

Codex performed the source inspection and terminal execution. The exploration examined `package.json`, the contribution and style files, CI workflows, `.gitignore`, build scripts, and the isLeapYear implementation, tests, and type declaration. These direct checks established which commands the project actually uses, how plugin tests load local source, and which directories contain generated output. Execution also exposed a host-timezone issue in the full test command and a Node 24 compatibility issue in the build toolchain.

The initial results were followed by further discussion and revision. I asked for a requirement-by-requirement audit and then a guided explanation of the repository and configuration. We worked through the difference between implementation files, tests, and agent instructions. In discussing the leap-year tests, I identified century-year cases as edge cases that catch the oversimplified assumption that every year divisible by four is a leap year. We also reviewed the five required areas of the agent file and considered which details would be useful enough to justify taking up context space.

One concrete decision from that review was to retain the conditional Node 24 build workaround. Codex explained the tradeoff between keeping the file short and preserving an actionable fix for a failure observed during execution, and I agreed to keep it. The final configuration reflects the repository findings, trial results, and these follow-up discussions. My role included selecting the repository, asking follow-up questions, evaluating the edge-case rationale, and reviewing inclusion decisions; Codex carried out the file inspection, edits, and command runs.

**Initial exploration and trial environment (2026-10-22):** macOS, Node v24.16.0, npm 11.13.0; host timezone America/Los_Angeles. The initial install hit a pre-existing npm-cache permission error. `npm ci --cache /tmp/cs146s-week4-npm-cache --no-audit --no-fund` succeeded with 1,794 packages. This isolated cache avoided modifying the user's existing cache.

- Baseline lint passed and the original focused plugin test passed (1 test).
- Unpinned `npm test` exited 1. The final stage had 90 passing/3 failing suites and 788 passing/6 failing tests, in localizedFormat, dayOfYear, and timezone. Earlier explicit timezone stages passed. No test or production source changes had been made.
- On that same baseline, `TZ=UTC npm test` exited 0: 93 suites and 794 tests passed. This observation motivated the configuration revision below.
- Plain `npm run build` failed in the size-check toolchain with `ERR_OSSL_EVP_UNSUPPORTED`. `NODE_OPTIONS=--openssl-legacy-provider npm run build` exited 0. Size-limit reported 2.79 KB against 2.99 KB; the separate gzip-size CLI printed 3.04 kB. These are the tools' reported values.
- `npm run babel` and the built-library Node example exited 0.

Logs are in [evidence/](evidence/). No dependency, production source, or build-tool changes were needed.

## Part II: The File

**Anything deliberately left out, and why:** The full API tutorial, contributor etiquette, issue counts, exhaustive plugin lists, and generic advice such as “write clean code” do not help an agent choose the right command or file. Machine-specific paths and the local npm-cache workaround also do not transfer to other checkouts. Detailed exploration logs belong in the writeup/evidence instead of every agent context.

**The hardest call on what to include:** Balancing concise instructions against useful exceptions. During the guided review, we considered keeping the Node 24 compatibility workaround only in the writeup. I agreed to retain it in AGENTS.md because an actual build encountered the specific error and the conditional command resolved it; another agent can act on it without reading the execution history. It is a per-command fallback, not a dependency change or permanent Node setting. The file also distinguishes focused tests from the full gate so that brevity does not encourage an exaggerated success claim.

## Part III: Trying It Out

Both tasks were executed by Codex with the root `AGENTS.md` present and explicitly read. They ran in the same conversation; the observations below report actual command use, edits, and results. The later guided discussion informed the final review and wording, while the trial commands and outputs below were already recorded during execution.

| # | Task | Did the agent use the commands and conventions? |
|---|---|---|
| 1 | With the initial file present, run the existing isLeapYear test and lint, then investigate the full gate. | Yes. The exact focused command passed 1 test; npm run lint exited 0. The full gate's failures were retained and reported. Inspecting the host timezone and repeating with UTC produced 794 passing tests. Evidence: [focused test](evidence/task1-test.log), [lint](evidence/task1-lint.log), [unpinned full run](evidence/full-test.log), and [UTC baseline](evidence/full-test-utc-baseline.log). |
| 2 | Add meaningful leap-year boundary and non-mutation tests; verify them. | Yes. Added 3 it cases in test/plugin/isLeapYear.test.js, retaining local imports, dayjs.extend, MockDate hooks, indentation, and no semicolons. Cases cover ordinary 1996/2023, century exceptions 1900/2400, and the unchanged value/date of 2024-02-29. The focused run passed 4 tests; lint passed; TZ=UTC npm test passed 93 suites/797 tests with 100% line coverage. No production code, declarations, generated artifacts, or lockfile changes were included in the committed diff. Evidence: [exact patch](evidence/task2.patch), [focused tests](evidence/task2-test.log), [lint](evidence/task2-lint.log), and [full suite](evidence/task2-full-test.log). |

**One thing to change after watching the file get used:** Make the full-gate timezone explicit. The initial file said npm test, leaving its final Jest stage dependent on the machine timezone. Six failures under Los Angeles disappeared with TZ=UTC on unchanged source/tests. The final file therefore specifies TZ=UTC npm test and explains that the scripted timezone matrix remains intact. [The initial configuration](evidence/AGENTS.initial.md) preserves the version before that improvement.

## Final reproducibility check (2026-10-25)

A fresh clone of the published Day.js fork was checked after the final prose review. Its root configuration and isLeapYear test were byte-identical to the local versions used above. Locked dependency installation succeeded; focused tests passed 4/4, lint passed, and the UTC-prefixed full gate passed 93 suites/797 tests with 100% line coverage. The conditional Node 24 UMD build, ESM build, and smoke example also exited 0. The smoke example printed `2024-02-29`. This is an additional reproducibility check, not a replacement for the two original trials.

See the [commands and exit codes](evidence/final-checks.json), [full test output](evidence/final-full-tests.log), and [artifact consistency checks](evidence/artifact-checks.json).

## Submission artifacts

- Root configuration in the [Day.js fork](https://github.com/yuxuanx-rain/dayjs/blob/dev/AGENTS.md), with the same file under `week4/AGENTS.md` in the assignment repository.
- This completed writeup, the two-task patch, initial configuration, command logs, and environment record under `week4/`.
- A requirement-by-requirement audit is included in `REQUIREMENTS_CHECKLIST.md`. Publication, collaborator verification, and Gradescope submission are tracked separately from local content validation.
