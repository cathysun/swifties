import json
import time
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set the URL to scrape
url = "https://www.stubhub.com/taylor-swift-santa-clara-tickets-7-28-2023/event/151197002/?quantity=2&sections=1544070&ticketClasses=1524&seatTypes=&listingQty="

# Set the concert time as a datetime object in the Pacific Timezone
concert_time = datetime(2023, 7, 28, 18, 30, tzinfo=timezone(-timedelta(hours=7)))

# Initialize the web driver
driver = webdriver.Chrome()

while True:
    # Open the URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Find the ticket price element using text-based XPath
    price_element = driver.find_element(By.XPATH, "//div[contains(text(), 'each')]/preceding-sibling::div")

    # Extract the price as a float value
    price_str = price_element.text.replace("$", "").replace(",", "")
    price = float(price_str)

    # Calculate the time until the concert in seconds
    time_until_concert = int((concert_time - datetime.now(timezone.utc)).total_seconds())

    # Create a dictionary to store the price and time data
    data = {"time_until_concert": time_until_concert, "price": price}

    # Write the data to a JSON file
    with open("ticket_prices.json", "a") as file:
        file.write(json.dumps(data) + "\n")

    # Wait for 5 minutes before running the script again
    time.sleep(5 * 60)

# Close the web driver
driver.quit()
