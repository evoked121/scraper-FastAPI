from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service




website = 'https://www.expedia.com/Hotel-Search?adults=2&allowPreAppliedFilters=true&children=&d1=2024-04-20&d2=2024-04-24&destination=Bellevue%2C%20Washington%2C%20United%20States%20of%20America&endDate=2024-04-24&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2024-04-20&theme=&useRewards=true&userIntent='
options = webdriver.ChromeOptions()
options.add_argument("--headless")

options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
driver = webdriver.Chrome(options=options)
with open('/Users/haoranwang/Documents/stealth.min.js/stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})

driver.get(website)

first_ten_hotels = []
first_ten_locations = []
first_ten_price = []

hotel_count = location_count = price_count = 0

res = []

all_hotels = driver.find_elements(By.XPATH, value='//*[@class="uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start"]')
all_locations = driver.find_elements(By.XPATH, value='//*[@class="uitk-text uitk-text-spacing-half truncate-lines-2 uitk-type-300 uitk-text-default-theme"]')
all_price = driver.find_elements(By.XPATH, value='//*[@class="uitk-text uitk-type-end uitk-type-200 uitk-text-default-theme"]')
for price in all_price:
    if price_count>=20:
        break
    price_count += 1
    first_ten_price.append(price.text)

for hotel in all_hotels:
    if hotel_count>=10:
        break
    hotel_count += 1
    first_ten_hotels.append(hotel.text)

for location in all_locations:
    if location_count>=10:
        break
    location_count += 1
    first_ten_locations.append(location.text)

for i in range(location_count):
    p = first_ten_price[2*i]
    name = first_ten_hotels[i]
    loc = first_ten_locations[i]
    entity = {"name":name, "location":loc, "price":p}
    res.append(entity)

print(first_ten_hotels)
print(first_ten_price)


driver.quit()