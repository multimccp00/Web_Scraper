const puppeteer = require('puppeteer');

async function scrapePage(pageNumber) {
  const browser = await puppeteer.launch({
    headless: false, // Run in non-headless mode to avoid detection (optional)
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();

  // Set a random User-Agent for each session to avoid detection
  const userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
  ];
  const randomUserAgent = userAgents[Math.floor(Math.random() * userAgents.length)];
  await page.setUserAgent(randomUserAgent);

  // Open the target URL
  const url = `https://suchen.mobile.de/fahrzeuge/search.html?dam=false&isSearchRequest=true&od=up&ref=srpNextPage&s=Car&sb=rel&vc=Car&pageNumber=${pageNumber}`;
  await page.goto(url, { waitUntil: 'networkidle2' });

  // Wait for listings to appear on the page
  await page.waitForSelector('div.K0qQI');

  // Scroll down to load more listings
  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });
  await page.waitForTimeout(2000);  // Wait for listings to load

  // Scrape the listings data
  const listings = await page.evaluate(() => {
    const data = [];
    const items = document.querySelectorAll('div.K0qQI'); // Adjust selector if necessary
    
    items.forEach(item => {
      const title = item.querySelector('.vehicle-title') ? item.querySelector('.vehicle-title').innerText : '';
      const price = item.querySelector('.price-block__price') ? item.querySelector('.price-block__price').innerText : '';
      const year = item.querySelector('.year') ? item.querySelector('.year').innerText : '';
      const km = item.querySelector('.km') ? item.querySelector('.km').innerText : '';

      data.push({ title, price, year, km });
    });

    return data;
  });

  // Log the scraped listings to the console
  console.log(listings);

  // Save the data to a file (optional)
  const fs = require('fs');
  fs.writeFileSync('listings.json', JSON.stringify(listings, null, 2));

  await browser.close();
}

// Scrape the first page
scrapePage(1).catch(console.error);
