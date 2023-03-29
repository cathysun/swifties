import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the web driver
driver = webdriver.Chrome()

# Set the URL of the page to scrape
url = "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1544070&ticketClasses=1524&seatTypes=&listingQty="

# Set the time between scrapes (in seconds)
scrape_interval = 60

# Define a function to scrape the page and return the price
def scrape_price():
    driver.get(url)
    price_element = driver.find_element(By.XPATH, "//div[contains(text(), 'each')]/preceding-sibling::div")
    price_text = price_element.text.replace(",", "").replace("$", "")
    return float(price_text)

# Start scraping the page and storing the data
data = []
while True:
    price = scrape_price()
    scrape_time = time.time()
    data.append({
        "time": scrape_time,
        "price": price
    })
    with open("ticket_prices.json", "w") as f:
        json.dump(data, f)
    print(f"Scraped price ${price:.2f} at {scrape_time:.0f}")
    time.sleep(scrape_interval)
