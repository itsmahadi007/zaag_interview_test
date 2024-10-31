from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

from dotenv import load_dotenv
from logger_config import logging

# Create a logger object
logger = logging.getLogger(__name__)


def login(driver):
    driver.get("https://app.cosmosid.com/search")
    logger.info("[INFO] Navigating to CosmosID login page.")

    time.sleep(2)  # Wait for page to load

    # Handle announcement dialog if it appears
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//button[contains(text(), 'Close') or contains(text(), 'Dismiss') or contains(text(), 'OK')]"))).click()
        logger.info("[INFO] Announcement dialog closed.")
    except:
        logger.info("[INFO] No announcement dialog found.")

    load_dotenv()

    # Handle login form
    try:
        email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='username' or @placeholder='Email address']")))
        email_field.send_keys(os.getenv("EMAIL"))
        logger.info("[INFO] Email entered.")
        print("[INFO] Email entered.")
        password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='password' or @name='password' or @placeholder='Password']")))
        password_field.send_keys(os.getenv("PASSWORD"))
        logger.info("[INFO] Password entered.")
        print("[INFO] Password entered.")

        # Click login button
        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sign-in-form--submit")))
        login_button.click()
        logger.info("[INFO] Login button clicked.")
        print("[INFO] Login button clicked.")
    except Exception as e:
        logger.error("[ERROR] Error during login:", str(e))
        print("[ERROR] Error during login:", str(e))

    time.sleep(5)  # Wait for login to complete