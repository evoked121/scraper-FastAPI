
# -*- coding:utf-8 -*-
import time
from pyquery import PyQuery
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright



js ="""
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
"""



async def get():
    async with async_playwright() as async_p:
        port = 7890
        p = async_p.start()
        browser = p.firefox.launch(
            headless=False,
        )
        page = browser.new_page()

        page.add_init_script(js)
        url = 'https://www.expedia.com/Hotel-Search?adults=2&allowPreAppliedFilters=true&children=&d1=2024-04-20&d2=2024-04-24&destination=Bellevue%2C%20Washington%2C%20United%20States%20of%20America&endDate=2024-04-24&latLong=47.610378%2C-122.200676&mapBounds=&pwaDialog=&regionId=6434&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2024-04-20&theme=&useRewards=true&userIntent='

    
        page.goto(url)
        page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        page.wait_for_load_state('load')
        time.sleep(2)
        content = page.content()
        doc = PyQuery(content)
        n = 0
        lst = []
        for div in doc('div.uitk-spacing.uitk-spacing-margin-blockstart-three').items():
            #img_url = div('div.uitk-gallery-carousel-item-prev img.uitk-image-media').attr('src')
            name = div('h3.uitk-heading').text()
            location = div('div.uitk-text.uitk-text-spacing-half.truncate-lines-2.uitk-type-300.uitk-text-default-theme').text()
            
            total = div('div[data-test-id="price-summary-message-line"] > div.uitk-text-default-theme').text()[:-22]
            #score = div('span.uitk-badge-base-text').text().replace('Ad','').strip()
            #if len(score) > 10:
                #continue
            if name == "" or location=="" or total=="":
                continue
            item = {'name':name,"location":location,'price':total}
            n +=1
            lst.append(item)
            if n >= 10:
                break
        return lst

