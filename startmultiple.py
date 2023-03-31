import json
import subprocess
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Set the URL of the page to scrape
urls = [
    "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1543880&ticketClasses=1524&seatTypes=&listingQty=",
    "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1544068&ticketClasses=1524&seatTypes=&listingQty=",
]

# Define a function to scrape the page and return the lowest price
def scrape_price(url):
    driver.get(url)
    price_elements = driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
    prices = [float(p.text.replace(",", "").replace("$", "")) for p in price_elements]
    lowest_price = min(prices)
    return lowest_price

# Scrape the pages and store the data
prices = []
for url in urls:
    price = scrape_price(url)
    prices.append(price)
    print(f"Scraped price ${price:.2f} from {url}")

lowest_price = min(prices)
data = [{"price": lowest_price, "time": time.time()}]

print(f"Lowest price: ${lowest_price:.2f}")
with open("ticket_prices_multiple.json", "w") as f:
    json.dump(data, f)

driver.quit()
