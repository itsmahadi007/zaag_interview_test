from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logger_config import logging

# Create a logger object
logger = logging.getLogger(__name__)

def handle_dialogs(driver):
    logger.info("[INFO] Handling dialogs. Its random dialog. Waiting for dialog to be clickable. Timeout: 10 seconds. until it will show error, it no issue")
    print("[INFO] Handling dialogs. Its random dialog. Waiting for dialog to be clickable. Timeout: 10 seconds. until it will show error, it no issue")
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                   "//button[contains(text(), 'Close') or contains(text(), 'Dismiss') or contains(text(), 'OK')]"))).click()
        logger.info("[INFO] Dialog closed successfully.")
        print("[INFO] Dialog closed successfully.")
    except TimeoutException:
        logger.info("[INFO] No dialog found. It's no issue. Ignoring.")
        print("[INFO] No dialog found. It's no issue. Ignoring.")
