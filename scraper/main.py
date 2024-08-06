from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import time
from pyquery import PyQuery
from playwright.sync_api import sync_playwright

js ="""
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
"""

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    parent: str
    room: str
    location: str
    start: str
    end: str

def getDesUrl(location_list):
    des_url = ""
    total_length = len(location_list)
    for i in range(total_length):
        lst = location_list[i].split(" ")
        lst = lst[1:] if lst[0]=="" else lst
        length = len(lst)
        des = ""
        for j in range(length):
            if j==length-1 and i==total_length-1:
                des += lst[j]
            elif j==length-1:
                des += lst[j]+"%2C%20"
            else:
                des += lst[j]+"%20"
        des_url += des
    return des_url

def getAdult(people):
    res = ""
    length = len(people)
    for i in range(length):
        if i==length-1:
            res += people[i]
        else:
            res += people[i]+"%2C"
    return res

class ExpediaCarwl:
    def __init__(self):
        self.port = 7890
        p = sync_playwright().start()
        self.browser = p.firefox.launch(
            headless=False,
        )
        self.page = self.browser.new_page()

        self.page.add_init_script(js)


    def get_page(self,url):
        self.page.goto(url)
        self.page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        self.page.wait_for_load_state('load')
        time.sleep(2)
        content = self.page.content()
        doc = PyQuery(content)
        n = 0
        lst = []
        for div in doc('div.uitk-spacing.uitk-spacing-margin-blockstart-three').items():
            #img_url = div('div.uitk-gallery-carousel-item-prev img.uitk-image-media').attr('src')
            name = div('h3.uitk-heading').text()
            if name == "":
                continue
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

@app.post("/items")
def read_item(item: Item):
    new_url = 'https://www.expedia.com/Hotel-Search?adults={parent}&allowPreAppliedFilters=true&children=&d1={start}&d2={end}&destination={location}&endDate={end}&rooms={room}&semdtl=&sort=RECOMMENDED&startDate={start}&theme=&useRewards=true&userIntent='
    #url = 'https://www.expedia.com/Hotel-Search?adults=2&allowPreAppliedFilters=true&children=&d1=2024-04-20&d2=2024-04-24&destination=Bellevue%2C%20Washington%2C%20United%20States%20of%20America&endDate=2024-04-24&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2024-04-20&theme=&useRewards=true&userIntent='
    location = item.location.split(",")
    start = item.start
    end = item.end
    parent = item.parent.split(",")
    room = item.room
    location = getDesUrl(location)
    parent = getAdult(parent)
    app = ExpediaCarwl()
    final_url = new_url.format(location=location, parent=parent, start=start, end=end, room=room)
    print(final_url)
    data = app.get_page(final_url)
    app.browser.close()

    return {"message": data}