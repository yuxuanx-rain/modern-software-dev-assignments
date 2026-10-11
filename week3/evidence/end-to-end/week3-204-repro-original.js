/*
 * ORIGINAL failing reproduction — HTTP 204 swap suppression
 *
 * Constructed scenario:
 *   HTML     : <div id="result">Empty</div>
 *              <button hx-get="/fragment" hx-target="#result">Load</button>
 *   Response : HTTP 204, Content-Type: text/html, body: "Loaded."
 *   Expected : #result textContent === "Loaded."
 *   Actual   : #result textContent === "Empty"  (assertion FAILS — reproduces the bug)
 *
 * Classification: application configuration / expectation error.
 *   htmx.config.responseHandling has { code:'204', swap:false } as its first rule
 *   (src/htmx.js line 265).  HTTP 204 No Content is explicitly documented to
 *   suppress the swap.  The fix belongs at the server, not in htmx.
 */
describe('Week 3 – 204 swap suppression (original, FAILING assertion)', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })

  it('HTTP 204 body is NOT swapped into #result (expected behavior assertion fails)', function() {
    // Fake server mirrors the reported behaviour exactly: 204 + body
    this.server.respondWith('GET', '/fragment', function(xhr) {
      xhr.respond(204, { 'Content-Type': 'text/html' }, 'Loaded.')
    })

    var target = make('<div id="result">Empty</div>')
    var button = make('<button hx-get="/fragment" hx-target="#result">Load</button>')

    button.click()
    this.server.respond()

    // One request was sent
    this.server.requests.length.should.equal(1)
    // The swap did NOT happen because 204 → swap:false in responseHandling
    // This assertion documents the ACTUAL outcome (not swapped).
    target.textContent.should.equal('Empty')   // passes – panel stays Empty
  })

  it('SHOWS THE BUG: asserting "Loaded." on a 204 response fails', function() {
    this.server.respondWith('GET', '/fragment', function(xhr) {
      xhr.respond(204, { 'Content-Type': 'text/html' }, 'Loaded.')
    })

    var target = make('<div id="result">Empty</div>')
    var button = make('<button hx-get="/fragment" hx-target="#result">Load</button>')

    button.click()
    this.server.respond()

    // This assertion FAILS intentionally – it states what the user expected
    // but htmx's documented 204 rule prevents the swap from happening.
    target.textContent.should.equal('Loaded.')
  })
})
