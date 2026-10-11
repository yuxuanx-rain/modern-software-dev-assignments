/*
 * CORRECTED reproduction — change HTTP 204 → 200 so the swap happens
 *
 * Fix: the server must return HTTP 200 (or any 2xx other than 204) when it
 * wants htmx to swap the response body into the target element.
 * HTTP 204 No Content is documented to suppress the swap by design.
 *
 * No htmx source or global config was changed.
 */
describe('Week 3 – 204 swap suppression (corrected, 200 response)', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })

  it('HTTP 200 body IS swapped into #result', function() {
    // Correction: return 200 instead of 204
    this.server.respondWith('GET', '/fragment', function(xhr) {
      xhr.respond(200, { 'Content-Type': 'text/html' }, 'Loaded.')
    })

    var target = make('<div id="result">Empty</div>')
    var button = make('<button hx-get="/fragment" hx-target="#result">Load</button>')

    button.click()
    this.server.respond()

    this.server.requests.length.should.equal(1)
    target.textContent.should.equal('Loaded.')
  })
})
