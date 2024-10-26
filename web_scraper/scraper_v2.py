from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
from handle_dialogs import handle_dialogs
from navigation_utils import refresh_and_validate
from process_sample import process_sample
from driver_setup import setup_driver
from login import login
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


def scrape_data(driver):
    try:
        handle_dialogs(driver)  # Handle dialogs if any appear
        # Locate folder names in the table
        root_folders = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "table tbody tr td a")
            )
        )
        print(f"[INFO] Found {len(root_folders)} folders.")

        # create a two dimensional list to store the folder names and the number of samples in each folder
        list_of_folders = [index for index in range(len(root_folders))]

        def process_folder_thread(index):
            thread_driver = setup_driver()
            try:
                login(thread_driver)
                handle_dialogs(thread_driver)
                folders = WebDriverWait(thread_driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "table tbody tr td a")
                    )
                )
                folder = folders[index]
                print(f"[INFO] Thread processing folder: {folder.text}")
                process_folder(thread_driver, folder, index)
            except Exception as e:
                print(
                    f"[ERROR] Thread error processing root folder at index {index}: {str(e)}"
                )
            finally:
                thread_driver.quit()

        # Define the number of threads to use
        num_threads = min(
            1, len(list_of_folders)
        )  # Use up to 6 threads or the number of folders, whichever is smaller

        # Use ThreadPoolExecutor to manage threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit tasks to the executor
            future_to_index = {
                executor.submit(process_folder_thread, index): index
                for index in list_of_folders
            }

            # Process completed tasks
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    future.result()
                except Exception as e:
                    print(
                        f"[ERROR] Exception in thread for folder index {root_folders[index].text}: {str(e)}"
                    )

        print("[INFO] All folders processed.")

        for index in range(len(folders)):
            try:
                # Re-locate the folder elements before each interaction
                folders = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "table tbody tr td a")
                    )
                )
                folder = folders[index]
                print(f"[INFO] Processing folder: {folder.text}")
                process_folder(driver, folder)

            except StaleElementReferenceException as e:
                print(
                    f"[WARNING] Stale element detected while processing folder: {str(e)}. Retrying folder identification."
                )
                refresh_and_validate(driver, "search")
                continue  # Retry locating folders
            except Exception as e:
                print(
                    f"[ERROR] Unable to process folder: {folder.text if folder else 'Unknown'}. Error: {str(e)}"
                )

    except Exception as e:
        print("[ERROR] Problem In Root Folder:", str(e))

def process_folder(driver, folder, root_folder_index):
    try:
        handle_dialogs(driver)
        folder.click()
        time.sleep(3)

        if driver.current_url.startswith("data:,"):
            refresh_and_validate(driver)

        sub_folders = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr td a"))
        )
        print(f"[INFO] Found {len(sub_folders)} Sub folders.")

        def process_sub_folder_thread(index):
            thread_sub_driver = setup_driver()
            try:
                login(thread_sub_driver)
                handle_dialogs(thread_sub_driver)
                folders = WebDriverWait(thread_sub_driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr td a"))
                )
                folder = folders[root_folder_index]
                print(f"[INFO] Thread processing root folder: {folder.text} - Thread Index: {index}")
                folder.click()
                if thread_sub_driver.current_url.startswith("data:,"):
                    refresh_and_validate(thread_sub_driver)
                
                threads_sub_folders = WebDriverWait(thread_sub_driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr td a"))
                )
                print(f"[INFO] Thread processing Sub folder: Found {len(threads_sub_folders)} - Current Sub Index: {index}")
                sample = threads_sub_folders[index]
                print(f"[INFO] Thread Processing sample: {sample.text} - Thread Index: {index}")
                process_sample(thread_sub_driver, sample)

            except Exception as e:
                print(f"[ERROR] Thread error processing folder at index {index}: {str(e)}")
            finally:
                thread_sub_driver.quit()

        # Increase the number of threads (adjust as needed)
        num_sub_threads = min(1, len(sub_folders))

        with ThreadPoolExecutor(max_workers=num_sub_threads) as sub_executor:
            futures = [sub_executor.submit(process_sub_folder_thread, i) for i in range(len(sub_folders))]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"[ERROR] Exception in thread: {str(e)}")

        print(f"[INFO] Finished processing folder: {folder.text}")

    except Exception as e:
        print(f"[ERROR] Error processing folder '{folder.text}': {str(e)}")