// Constructed scenario: hx-swap="none" with hx-swap-oob response
// Reported: result stays Empty even though response body contains "Loaded"
describe('week3 – hx-swap=none with oob response (constructed reproduction)', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })

  it('result region shows Loaded and status region shows Ready after clicking Load', function() {
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

    // Both assertions must hold per the reported expectation
    result.textContent.should.equal('Loaded')
    status.textContent.should.equal('Ready')
  })
})
