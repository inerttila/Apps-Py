from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc., depending on your browser
driver.get('https://3dskai.com/en/shop/')

# Initialize an empty list to store product info (name and price)
product_info = []

# Loop through pagination pages
while True:
    # Wait for the page to load
    time.sleep(3)
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Loop through each product element
    for product in soup.select('span a[title]'):
        # Extract the product name
        name = product.get_text(strip=True)
        
        # Find the nearest price element for the product
        price_tag = product.find_next(class_="woocommerce-Price-amount amount")
        
        # Only add products that have a valid price
        if price_tag:
            price = price_tag.get_text(strip=True)
            product_info.append((name, price))

    # Try to find the "Next" button and click it to go to the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')  # Update this selector to match the "Next" button
        next_button.click()
    except NoSuchElementException:
        # Break the loop if there is no "Next" button (end of pagination)
        break

# Close the browser
driver.quit()

# Write the product names and prices to a text file
with open('3DSKAI_Products_with_Prices.txt', 'w') as f:
    for name, price in product_info:
        f.write(f"{name}: {price}\n")

print(f"Extracted {len(product_info)} products with prices and saved to 3DSKAI_Products_with_Prices.txt.")
