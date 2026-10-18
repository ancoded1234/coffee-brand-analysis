from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1280,'height':900})
    page.goto('https://app.passorder.co.kr/normal/279ece8e-612f-452c-8da2-d5422c4525fc/menus',wait_until='domcontentloaded')
    page.wait_for_timeout(4000)
    page.get_by_text('아메리카노',exact=True).first.click()
    page.wait_for_timeout(2000)
    (R/'data/raw/ten_menu_options.txt').write_text(page.locator('body').inner_text(),encoding='utf-8')
    page.screenshot(path=str(R/'data/raw/ten_menu_options.png'))
    print(page.locator('body').inner_text()[-7500:])
    browser.close()
