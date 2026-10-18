from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];Q=R/'analysis/qa';Q.mkdir(exist_ok=True)
report={'desktop':[],'mobile':[],'errors':[]}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto((R/'presentation/index.html').as_uri());page.wait_for_timeout(700)
    assert page.locator('.slide').count()==13
    for n in range(1,14):
        page.evaluate(f'show({n-1})');page.wait_for_timeout(1600)
        overflow=page.locator('.slide.active').evaluate('s=>({x:s.scrollWidth-s.clientWidth,y:s.scrollHeight-s.clientHeight})')
        report['desktop'].append({'slide':n,'overflow':overflow})
        page.screenshot(path=str(Q/f'web_{n:02}.png'))
    page.evaluate('show(4)');page.keyboard.press('ArrowRight');assert page.locator('#page').inner_text()=='06 / 13'
    page.locator('#notes').click();assert page.locator('#dialog').evaluate('d=>d.open');page.locator('#close').click()
    page.locator('#sources').click();assert page.locator('.source-item').count()>0;page.locator('#close').click()
    page.locator('#disclosure').click();assert page.locator('.drow').count()==6;page.locator('#close').click()
    page.evaluate('show(4)');page.locator('#motion').click();page.wait_for_timeout(1200)
    video=page.locator('video').evaluate('v=>({ready:v.readyState,duration:v.duration,width:v.videoWidth,error:v.error?.message??null})')
    report['video']=video;assert video['ready']>=2 and not video['error'];page.locator('#close').click()
    page.locator('#fullscreen').click();page.wait_for_timeout(300);report['fullscreen']=page.evaluate('!!document.fullscreenElement');assert report['fullscreen'];page.evaluate('document.exitFullscreen()')
    phone=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    phone.goto((R/'presentation/index.html').as_uri())
    for n in range(1,14):
        phone.evaluate(f'show({n-1})');phone.wait_for_timeout(80)
        x=phone.evaluate('document.documentElement.scrollWidth-innerWidth');report['mobile'].append({'slide':n,'page_horizontal_overflow':x});assert x<=1
    phone.evaluate('show(4)');phone.wait_for_timeout(1700);phone.screenshot(path=str(Q/'mobile_prices.png'))
    assert not report['errors'],report['errors']
    assert all(r['overflow']['x']<=1 and r['overflow']['y']<=1 for r in report['desktop']),report['desktop']
    browser.close()
(Q/'browser_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('13 desktop + 13 mobile slides, navigation, notes, sources, matrix, video and fullscreen passed')
