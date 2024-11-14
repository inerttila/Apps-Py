from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

# Function to remove products with 'Price not available'
def filter_valid_products(names, prices):
    # Create a new list where we only keep valid products with price
    valid_names_prices = [(name, price) for name, price in zip(names, prices) if price != 'Price not available']
    return valid_names_prices

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc., depending on your browser
driver.get('https://skaitech.al/en/store/')

# Scroll down to load content, waiting for 3 seconds each time
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the new content
    time.sleep(3)
    # Check if the page height has increased
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # No new content loaded
        break
    last_height = new_height

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # Close the browser

product_names = []
product_prices = []

# Extract product names and prices
for product in soup.select('li.product'):
    name_element = product.select_one('span a[title]')
    price_element = product.select_one('.woocommerce-Price-amount.amount')
    
    if name_element:
        name = name_element.get_text(strip=True)  # Extract and clean the text
        product_names.append(name)
    
        # If the price element exists, extract the price, else append a placeholder text
        if price_element:
            price = price_element.get_text(strip=True)
            product_prices.append(price)
        else:
            # If no price exists, append 'Price not available'
            product_prices.append('Price not available')

# Filter out products with 'Price not available'
valid_products = filter_valid_products(product_names, product_prices)

# Write the valid products (with prices) to a text file
with open('All_Skaitech.txt', 'w') as f:
    for name, price in valid_products:
        f.write(f"{name} - {price}\n")

print(f"Extracted {len(valid_products)} valid product names and prices and saved to All_Skaitech.txt.")
