# rmp-uky-injector
This is the CS498 project repository at the University of Kentucky for:
- Lucas Mullins
- Quinton Saldana
- Kaleb Slone
- Keaton Martin

Repository overview:
- `scraper.py` : a script to collect RMP data
- `extension/` : directory for the chrome extension
    - `manifest.json` : extension manifest
    - `profs.csv` : professor dataset scraped from rmp, not necessarily complete
    - `scripts/`
        - `injector.js` : content script, main logic of extension
        - `papaparse.min.js` : minimized source code to <a href="papaparse.com">Papa Parse</a>
