from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def get_driver():
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('useAutomationExtension', False)
    opt.add_argument('--disable-blink-features=AutomationControlled')
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined});""",
    })
    driver.implicitly_wait(10)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    driver.maximize_window()
    return driver

website = 'https://www.expedia.com/Hotel-Search?adults=2&allowPreAppliedFilters=true&children=&d1=2024-04-20&d2=2024-04-24&destination=Bellevue%2C%20Washington%2C%20United%20States%20of%20America&endDate=2024-04-24&latLong=47.610378%2C-122.200676&mapBounds=&pwaDialog=&regionId=6434&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2024-04-20&theme=&useRewards=true&userIntent='

driver = get_driver()
driver.get(website)

first_ten_hotels = []
first_ten_locations = []

scrolling = True
hotel_count = location_count = 0

while scrolling:
    if hotel_count>=10 and location_count>=10:
        scrolling = False
        break
    all_hotels = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start"]')))
    all_locations = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="uitk-text uitk-text-spacing-half truncate-lines-2 uitk-type-300 uitk-text-default-theme"]')))
    for hotel in all_hotels:
        hotel_count += 1
        first_ten_hotels.append(hotel.text)
    for location in all_locations:
        location_count += 1
        first_ten_locations.append(location.text)
    
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scrolling = False
            break
        else:
            last_height = new_height

print(first_ten_hotels)
print(first_ten_locations)
#
driver.quit()

