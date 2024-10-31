from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from logger_config import logging

# Create a logger object
logger = logging.getLogger(__name__)


# With UI
# def setup_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument('--start-maximized')  # Maximize window to handle dynamic elements better
#     driver = webdriver.Chrome(options=options)
#     logger.info("Selenium driver set up successfully.")
#     print("[INFO] Selenium driver set up successfully.")
#     return driver


# Without UI
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    logger.info("Selenium driver set up successfully.")
    print("[INFO] Selenium driver set up successfully.")
    return driver