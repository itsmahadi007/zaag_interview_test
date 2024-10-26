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
        handle_dialogs(driver)
        root_folders = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "table tbody tr td a")
            )
        )
        print(f"[INFO] Found {len(root_folders)} folders.")

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
                try:
                    print(
                        f"[INFO] Thread Execption processing root folder at index {index}"
                    )
                except:
                    pass
                    
            finally:
                thread_driver.quit()

        num_threads = min(
            4, len(list_of_folders)
        )

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_index = {
                executor.submit(process_folder_thread, index): index
                for index in range(len(list_of_folders))
            }

            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    future.result()
                except Exception as e:
                    print(
                        f"[ERROR] Exception in thread for folder index {root_folders[index].text}: {str(e)}"
                    )

        print("[INFO] All folders processed.")

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

        def process_sub_folder_thread(index, thread_root_folder_index):
            thread_sub_driver = setup_driver()
            try:
                login(thread_sub_driver)
                handle_dialogs(thread_sub_driver)
                thread_root_folders = WebDriverWait(thread_sub_driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr td a"))
                )
                folder = thread_root_folders[thread_root_folder_index]
                print(f"[INFO] Thread processing root folder: {folder.text} - Thread Index: {thread_root_folder_index}")
                folder.click()
                time.sleep(3)
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
                print(f"[INFO] Thread processing folder at index {index}: {str(e)}")
            finally:
                thread_sub_driver.quit()

        num_sub_threads = min(5, len(sub_folders))

        with ThreadPoolExecutor(max_workers=num_sub_threads) as sub_executor:
            futures = [sub_executor.submit(process_sub_folder_thread, i, root_folder_index) for i in range(len(sub_folders))]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"[ERROR] Exception in thread: {str(e)}")

        print(f"[INFO] Finished processing folder: {folder.text}")
        return True

    except Exception as e:
        print(f"[ERROR] Error processing folder '{folder.text}': {str(e)}")