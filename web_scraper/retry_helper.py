from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from logger_config import logging

# Create a logger object
logger = logging.getLogger(__name__)



def retry_click(driver, xpath, attempts=3, sleep_time=2):
    for attempt in range(attempts):
        try:
            element = WebDriverWait(driver, 600).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            logger.info(f"[INFO] Element clicked successfully on attempt {attempt + 1}")
            print(f"[INFO] Element clicked successfully on attempt {attempt + 1}")
            return True
        except TimeoutException:
            logger.warning(
                f"[WARNING] Attempt {attempt + 1}/{attempts} - Unable to click element. Retrying..."
            )
            print(f"[WARNING] Attempt {attempt + 1}/{attempts} - Unable to click element. Retrying...")
            time.sleep(sleep_time)
    logger.error("[ERROR] Unable to click element after multiple attempts.")
    print("[ERROR] Unable to click element after multiple attempts.")
    return False


def retry_visibility_of_all_elements_located(
    driver, xpath, index, attempts=3, sleep_time=2
):
    for attempt in range(attempts):
        try:
            selection_options = WebDriverWait(driver, 600).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
            option = selection_options[index]
            option_text = option.text
            logger.info(f"[INFO] Selecting option: {option_text} on attempt {attempt + 1}")
            option.click()
            return option_text
        except TimeoutException:
            logger.warning(
                f"[WARNING] Attempt {attempt + 1}/{attempts} - Unable to click element. Retrying..."
            )
            print(f"[WARNING] Attempt {attempt + 1}/{attempts} - Unable to click element. Retrying...")
            time.sleep(sleep_time)
    logger.error("[ERROR] Unable to click element after multiple attempts.")
    print("[ERROR] Unable to click element after multiple attempts.")
    return False
