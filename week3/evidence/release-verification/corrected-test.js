// Constructed scenario: hx-swap="none" with hx-swap-oob response
// Root cause: hx-swap="none" skips the primary target swap (src/htmx.js:1796-1797)
//   while OOB swaps still execute (src/htmx.js:1985).
// Fix: use hx-swap="innerHTML" (or omit hx-swap to accept the default) so the
//   primary response body is written to #result.
describe('week3 – hx-swap=none with oob response (corrected)', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })

  // Verified documented behavior: hx-swap="none" suppresses the main swap;
  // OOB swap on #status still runs.
  it('with hx-swap=none: result stays unchanged, status oob-swaps to Ready', function() {
    this.server.respondWith(
      'GET', '/fragment',
      [200, { 'Content-Type': 'text/html' },
        'Loaded<span id="status" hx-swap-oob="innerHTML">Ready</span>']
    )

    var result = make('<div id="result">Empty</div>')
    var status = make('<div id="status">Waiting</div>')
    var button = make('<button hx-get="/fragment" hx-target="#result" hx-swap="none">Load</button>')

    button.click()
    this.server.respond()

    this.server.requests.length.should.equal(1)
    result.textContent.should.equal('Empty') // main swap suppressed by hx-swap="none"
    status.textContent.should.equal('Ready') // OOB swap still fires
  })

  // Corrected: change hx-swap="none" -> hx-swap="innerHTML" so the primary
  // response body is written to #result, while OOB still updates #status.
  it('with hx-swap=innerHTML: result shows Loaded and status oob-swaps to Ready', function() {
    this.server.respondWith(
      'GET', '/fragment',
      [200, { 'Content-Type': 'text/html' },
        'Loaded<span id="status" hx-swap-oob="innerHTML">Ready</span>']
    )

    var result = make('<div id="result">Empty</div>')
    var status = make('<div id="status">Waiting</div>')
    // Fix: hx-swap="innerHTML" (was hx-swap="none")
    var button = make('<button hx-get="/fragment" hx-target="#result" hx-swap="innerHTML">Load</button>')

    button.click()
    this.server.respond()

    this.server.requests.length.should.equal(1)
    result.textContent.should.equal('Loaded')
    status.textContent.should.equal('Ready')
  })
})
