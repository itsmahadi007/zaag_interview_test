from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Maximize window to handle dynamic elements better
    driver = webdriver.Chrome(options=options)
    print("[INFO] Selenium driver set up successfully.")
    return driver



# def setup_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(options=chrome_options)
#     print("[INFO] Selenium driver set up successfully.")
#     return driver