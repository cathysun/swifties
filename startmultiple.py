import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set the URL of the page to scrape
urls = [
    "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1543880&ticketClasses=1524&seatTypes=&listingQty=",
    "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1544068&ticketClasses=1524&seatTypes=&listingQty=",
]

# Set the time between scrapes (in seconds)
scrape_interval = 300  # 5 minutes

# Define a function to scrape the page and return the lowest price
def scrape_price(url, driver):
    driver.get(url)
    price_elements = driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
    prices = [float(p.text.replace(",", "").replace("$", "")) for p in price_elements]
    lowest_price = min(prices)
    return lowest_price

# Start scraping the pages and storing the data
data = []
while True:
    with Service('./chromedriver') as service:
        driver = webdriver.Chrome(service=service)
        prices = []
        for url in urls:
            price = scrape_price(url, driver)
            prices.append(price)
            print(f"Scraped price ${price:.2f} from {url}")
        lowest_price = min(prices)
        data.append({"price": lowest_price, "time": time.time()})
        print(f"Lowest price: ${lowest_price:.2f}")
        with open("ticket_prices_multiple.json", "w") as f:
            json.dump(data, f)
        driver.quit()
        time.sleep(scrape_interval)
