/* Constructed application configuration error; not an upstream defect. */
describe('Week 3 manual target reproduction', function() {
  beforeEach(function() {
    this.server = sinon.fakeServer.create()
    clearWorkArea()
  })
  afterEach(function() {
    this.server.restore()
    clearWorkArea()
  })
  it('updates the weather result after clicking', function() {
    this.server.respondWith('GET', '/weather', 'Sunny 22C')
    var result = make('<div id="weather-result">Not queried</div>')
    var button = make('<button hx-get="/weather" hx-target="#missing-result">Check weather</button>')
    button.click()
    this.server.respond()
    result.textContent.should.equal('Sunny 22C')
  })
})
