from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc., depending on your browser
driver.get('https://skaitech.al/en/store/')

# Scroll down to load content dynamically
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for content to load
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # No new content loaded
        break
    last_height = new_height

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # Close the browser

# Extract product names and prices
product_info = []
for product in soup.select('span a[title]'):
    name = product.get_text(strip=True)
    # Find the nearest price element with the specific class
    price_tag = product.find_next(class_="woocommerce-Price-amount amount")
    price = price_tag.get_text(strip=True) if price_tag else "Price not found"
    product_info.append((name, price))

# Write the product information to a text file
with open('SKAITECH_products_with_prices.txt', 'w') as f:
    for name, price in product_info:
        f.write(f"{name}: {price}\n")

print(f"Extracted {len(product_info)} products with prices and saved to SKAITECH_products_with_prices.txt.")
