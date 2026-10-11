---
name: htmx-interaction-diagnosis
description: Reproduce and diagnose htmx button, form, and HTML-response failures. Use when asked to debug or investigate why an hx-get button does nothing, an htmx form submits but its result stays empty, or a response arrives without a swap. Also use for an initial investigation plan when running tests is deferred, even if the likely cause seems obvious. Exclude conceptual explanations of htmx attributes, visual styling, and interactions that do not use htmx.
---

# Diagnose an htmx interaction

Produce a minimal reproduction and an evidence-backed diagnosis in a real htmx checkout. For an execution request, read [references/reproduction.md](references/reproduction.md) before setup or tests; it supplies exact commands and the native fixture pattern. For an outline-only request, use the decision branches below and respect the requested pause before execution.

## Establish the case

- Record the checkout commit, reported HTML, trigger, expected result, and actual result. If these are insufficient to reproduce, ask for the specific missing input instead of inventing a cause. Label any constructed scenario as constructed.
- Inspect the working-tree status and relevant existing tests before edits. Keep the case in a new `test/attributes/week3-*.js` or `test/core/week3-*.js` file; do not overwrite existing tests or change library defaults to make a case pass.
- Use the supplied checkout's `src/htmx.js` and native Mocha/Chai/Sinon utilities. Replace external services with a deterministic fake response. Retain the reported status, response headers, and HTML when they affect the failure.

## Reproduce before diagnosing

1. Run the closest existing test file as a baseline. A browser launch, dependency, or server failure is an environment failure, not evidence of an htmx defect.
2. Reduce the HTML to the trigger, target, and response while preserving inherited attributes and relevant DOM relationships. Run an assertion of the user's expected behavior. Save the failing output and original fixture before modifying it.
3. Observe request count, HTTP status, relevant htmx error events, and resulting DOM. Test the leading hypothesis with one controlled change.

## Choose the next step from evidence

- **No request:** check script initialization, trigger wiring, and target resolution first. An `htmx:targetError` can abort before any request. Verify the target against the actual DOM; distinguish a missing target from a selector syntax error.
- **Request fails:** distinguish transport failure from an HTTP error response. Inspect response handling and documented behavior before expecting an error response to swap. Do not treat every non-200 status as identical.
- **Response arrives but DOM is wrong:** inspect effective `hx-target`, `hx-swap`, `hx-select`, inherited values, and response headers. Verify the returned fragment rather than assuming it matches the requested region. Distinguish the normal swap from out-of-band updates: `hx-swap="none"` does not imply no request or no DOM updates anywhere.
- **Minimal case passes:** report non-reproduction and the removed factors to reintroduce; do not assert a root cause or silently change the expected result.
- **Documented behavior explains the result:** classify it as an application configuration or expectation issue. Call it a possible library defect only when a minimal test contradicts a documented guarantee on the recorded version.

## Verify and report

After reproducing, propose the smallest change supported by the observation. Apply it to the local reproduction when authorized; preserve both original and corrected versions. Move the intentionally failing test file itself out of `test/attributes/` or `test/core/` into an evidence directory before the final run. Copying a snapshot is insufficient if the failing original remains discoverable. Keep only corrected cases active; do not weaken the original assertion or count an intentional failure as a passing suite. Run the corrected case and the adjacent existing tests. If library source is changed, also run `npm test`; do not patch library source merely to fix a caller's HTML.

Verify file/line citations against this checkout, and use runner output rather than remembered counts. Report: reproduction steps and commit; exact commands and exit results; observed requests/events/DOM; hypothesis and controlled change; classification; before/after results; and any specific missing evidence. Do not claim tests passed without running them, fabricate an upstream issue, or publish a PR as part of diagnosis.
