# #!/usr/bin/env python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Start the browser and login with standard_user
def login (user, password):
    print ('Starting the browser...')

    options = ChromeOptions()
    if os.getenv("SELENIUM_HEADLESS") == "TRUE":
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    # if os.getenv("SELENIUM_HEADLESS") == "TRUE":
    #     driver.Manage().Timeouts().ImplicitlyWait(TimeSpan.FromSeconds(5));

    print('Browser started successfully.')
    print("Navigating to the demo page to login...")
    driver.get('https://www.saucedemo.com/')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    print("Login successful.")

    return driver


def add_products_to_cart(driver):
    inventory_container = driver.find_element_by_css_selector("div[id='inventory_container']")
    items_list = inventory_container.find_elements_by_css_selector("div[class='inventory_item']")
    print("Adding products to cart...")
    for item in items_list:
        # item.find_element_by_css_selector("button[class='btn_inventory']").click()
        item.find_element_by_tag_name("button").click()
    print("Finished adding products to cart.")


def test_all_products_in_cart(driver):
    print("Testing all products were added to cart...")
    text = driver.find_element_by_css_selector("span[class='shopping_cart_badge']").text
    assert text == "6"
    print("All products successfully added to cart!")


if __name__ == "__main__":
    driver = login('standard_user', 'secret_sauce')
    add_products_to_cart(driver)
    test_all_products_in_cart(driver)
    driver.quit()
