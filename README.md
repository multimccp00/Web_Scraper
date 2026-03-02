# Web Scraper for Car Jockey

This repository contains a web-scraping bot currently in development as part of a larger project called **Car Jockey**.

## Purpose
The goal is to gather pricing information for various car models and submodels from online sources (currently Standvirtual) and store it in a local file or a database. The collected data will feed into Car Jockey, which will present aggregated price data to users.

## Contents
- `fromScratch.py` and `fromScratch_teste.py` – Python scripts handling the scraping logic.
- `puppet.js` – a Node/Puppeteer stub not presently in use.
- `data/` – directory for output JSON/CSV files (ignored by Git via `.gitignore`).
- `package.json` – Node project metadata (for the Puppeteer stub).

## Notes
- The scraper is still under development; functionality and selectors may change as the target site evolves.
- Data is intended to be saved locally or pushed to a database for later analysis by Car Jockey.

Feel free to explore or contribute as the bot matures!