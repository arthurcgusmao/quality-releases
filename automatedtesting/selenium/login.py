# #!/usr/bin/env python
import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('selenium-results.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logger = setup_custom_logger("selenium")


# Start the browser and login with standard_user
def login (user, password):
    logger.info('Starting the browser...')

    options = ChromeOptions()
    if os.getenv("SELENIUM_HEADLESS") == "TRUE":
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    # if os.getenv("SELENIUM_HEADLESS") == "TRUE":
    #     driver.Manage().Timeouts().ImplicitlyWait(TimeSpan.FromSeconds(5));

    logger.info('Browser started successfully.')
    logger.info("Navigating to the demo page to login...")
    driver.get('https://www.saucedemo.com/')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    logger.info(f"Login successful with user {user}")

    return driver


def get_items_list(driver):
    inventory_container = driver.find_element_by_css_selector("div[id='inventory_container']")
    items_list = inventory_container.find_elements_by_css_selector("div[class='inventory_item']")
    return items_list

def get_item_name(item):
    return item.find_element_by_css_selector("div[class='inventory_item_name']").text



def add_products_to_cart(driver):
    items_list = get_items_list(driver)
    logger.info("Adding products to cart...")
    for item in items_list:
        item.find_element_by_tag_name("button").click()
        logger.info(f"Added product {get_item_name(item)} to cart.")
    logger.info("Finished adding products to cart.")


def test_all_products_in_cart(driver):
    logger.info("Testing all products were added to cart...")
    text = driver.find_element_by_css_selector("span[class='shopping_cart_badge']").text
    assert text == "6"
    logger.info("All products successfully added to cart!")


def remove_products_from_cart(driver):
    items_list = get_items_list(driver)
    logger.info("Removing products from cart...")
    for item in items_list:
        item.find_element_by_tag_name("button").click()
        logger.info(f"Removed product {get_item_name(item)} from cart.")
    logger.info("Finished removing products from cart.")


def test_no_products_in_cart(driver):
    logger.info("Testing all products were removed from cart...")
    try:
        text = driver.find_element_by_css_selector("span[class='shopping_cart_badge']")
    except NoSuchElementException:
        logger.info("All products successfully removed from cart!")



if __name__ == "__main__":
    driver = login('standard_user', 'secret_sauce')
    add_products_to_cart(driver)
    test_all_products_in_cart(driver)
    remove_products_from_cart(driver)
    test_no_products_in_cart(driver)
    driver.quit()
