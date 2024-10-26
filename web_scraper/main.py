from driver_setup import setup_driver
from login import login
from scraper_v2 import scrape_data

if __name__ == "__main__":
    print("[INFO] Starting scraper.")
    driver = setup_driver()

    try:
        login(driver)
        scrape_data(driver)
    finally:
        driver.quit()
        print("[INFO] Selenium driver closed.")