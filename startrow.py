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

# Define a function to scrape the page and return all prices and their corresponding row numbers
def scrape_prices_and_rows(url):
    driver.get(url)
    price_elements = driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
    row_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Row:')]")
    prices = [float(p.text.replace(",", "").replace("$", "")) for p in price_elements]
    rows = [int(r.text.split("Row:")[1].strip()) for r in row_elements]
    return prices, rows

# Scrape the pages and store the data
lowest_price_10 = None
lowest_row_10 = None
lowest_price_11 = None
lowest_row_11 = None
for url in urls:
    prices, rows = scrape_prices_and_rows(url)
    for i in range(len(prices)):
        price = prices[i]
        row = rows[i]
        print(f"Scraped price ${price:.2f} and row {row} from {url}")
        if row <= 10:
            if lowest_price_10 is None or price < lowest_price_10:
                lowest_price_10 = price
                lowest_row_10 = row
        else:
            if lowest_price_11 is None or price < lowest_price_11:
                lowest_price_11 = price
                lowest_row_11 = row

current_time = time.time()

# Load the existing data from the JSON file and append the new data

try:
    with open("ticket_prices_rows.json", "r") as f:
        data = json.load(f)
except json.decoder.JSONDecodeError:
    data = []

data.append({
    "lowest_price_10_or_lower": {
        "price": lowest_price_10,
        "row": lowest_row_10
    },
    "lowest_price_11_or_higher": {
        "price": lowest_price_11,
        "row": lowest_row_11
    },
    "time": current_time
})

print(f"Lowest price for rows 10 or lower: ${lowest_price_10:.2f} for row {lowest_row_10}")
print(f"Lowest price for rows 11 or higher: ${lowest_price_11:.2f} for row {lowest_row_11}")
with open("ticket_prices_rows.json", "w") as f:
    json.dump(data, f)

driver.quit()
