// Run with: node verify.cjs /path/to/htmx /path/to/evidence
const path = require('node:path')
const fs = require('node:fs')
const assert = require('node:assert/strict')
const { chromium } = require(path.join(process.argv[2], 'node_modules/playwright'))
;(async () => {
  const browser = await chromium.launch({ headless: true })
  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 850 }, deviceScaleFactor: 1 })
    const requests = []
    page.on('request', request => { if (request.url().endsWith('/weather')) requests.push(request.url()) })
    await page.goto('http://127.0.0.1:19363')
    await page.click('#working')
    await page.waitForFunction(() => document.querySelector('#working-result').textContent.includes('Sunny'))
    await page.click('#broken')
    await page.waitForFunction(() => window.trace.some(x => x.event === 'htmx:targetError'))
    const desktop = await page.evaluate(() => ({
      working: document.querySelector('#working-result').textContent,
      broken: document.querySelector('#broken-result').textContent,
      trace: window.trace,
      overflow: document.documentElement.scrollWidth > innerWidth
    }))
    assert.match(desktop.working, /Sunny/)
    assert.equal(desktop.broken, '还没有查询')
    assert.equal(requests.length, 1)
    assert.equal(desktop.trace.filter(x => x.source === 'broken' && x.event === 'htmx:beforeRequest').length, 0)
    assert.equal(desktop.overflow, false)
    await page.screenshot({ path: path.join(process.argv[3], 'demo-desktop.png'), fullPage: true })
    await page.setViewportSize({ width: 390, height: 844 })
    await page.goto('http://127.0.0.1:19363')
    await page.click('#working')
    await page.waitForFunction(() => document.querySelector('#working-result').textContent.includes('Sunny'))
    await page.click('#broken')
    await page.waitForFunction(() => window.trace.some(x => x.event === 'htmx:targetError'))
    const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)
    assert.equal(mobileOverflow, false)
    await page.screenshot({ path: path.join(process.argv[3], 'demo-mobile.png'), fullPage: true })
    fs.writeFileSync(path.join(process.argv[3], 'demo-verification.json'), JSON.stringify({ desktop, weatherRequestsOnDesktop: 1, mobileOverflow, checksPassed: true }, null, 2) + '\n')
    console.log('Desktop and mobile: working request updates result; missing target emits targetError without a request; no horizontal overflow.')
  } finally { await browser.close() }
})().catch(error => { console.error(error); process.exitCode = 1 })
