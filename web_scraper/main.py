from driver_setup import setup_driver
from login import login
from scraper import scrape_data
from logger_config import logging

# Create a logger object
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("[INFO] Starting scraper.")
    print("[INFO] Starting scraper.")
    driver = setup_driver()

    try:
        login(driver)
        scrape_data(driver)
    finally:
        driver.quit()
        logger.info("[INFO] Selenium driver closed.")
        print("[INFO] Selenium driver closed.")
