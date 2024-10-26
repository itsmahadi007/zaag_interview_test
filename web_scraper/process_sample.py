import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.options import Options

def setup_custom_chrome_profile(download_dir):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    return chrome_options

def process_sample(driver, sample, sub_folder_name, root_folder_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_download_dir = os.path.join(current_dir, 'downloads', root_folder_name, sub_folder_name)
    
    from handle_dialogs import handle_dialogs
    from navigation_utils import refresh_and_validate

    try:
        handle_dialogs(driver)  # Handle dialogs if any appear
        sample.click()
        time.sleep(2)  # Allow time for the sample page to load

        # Ensure we're not stuck on a "data:," page
        if driver.current_url.startswith("data:,"):
            print(
                "[WARNING] Page URL turned into 'data:,' likely indicating an issue. Refreshing the page."
            )
            refresh_and_validate(driver)

        # Wait for the selection field to be clickable and click it to open the dropdown
        retry_attempts_selection_field_one = 5
        for i in range(retry_attempts_selection_field_one):
            try:
                time.sleep(1)
                selection_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[@id='analysis-select']")
                    )
                )

                selection_field.click()
                print("[INFO] Selection field dropdown opened.")
                break
            except Exception as e:
                print(
                    f"[WARNING] Attempt {i + 1} - Unable to click selection field. Retrying... Error: {str(e)}"
                )
                time.sleep(1)

        selection_options = WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//ul[@role='listbox']//li")
            )
        )
        print(f"[INFO] Found {len(selection_options)} selection options.")

        # Iterate through options
        for i in range(len(selection_options)):
            try:
                # Re-locate the selection options to avoid stale element reference
                selection_options = WebDriverWait(driver, 15).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, "//ul[@role='listbox']//li")
                    )
                )
                option = selection_options[i]
                option_text = option.text
                print(f"[INFO] Selecting option: {option_text}")
                option.click()
                time.sleep(1)  # Wait for the selection to be processed

                if option_text == "Bacteria":
                    print("[INFO] Bacteria selected.")
                    for_bacteria_sample(driver, base_download_dir, root_folder_name, sub_folder_name)
                    # Process further if Bacteria is selected (add your logic)
                else:
                    # Handle case where it is not Bacteria
                    print(f"[INFO] {option_text} selected.")
                    try:
                        # Create a unique folder for this download
                        unique_download_dir = os.path.join(base_download_dir, option_text)
                        os.makedirs(unique_download_dir, exist_ok=True)
                        
                        # Update Chrome download settings for this specific download
                        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                            "behavior": "allow",
                            "downloadPath": unique_download_dir
                        })

                        # Attempt to locate the "Export current results" button within the timeout period
                        export_button = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                "//button[contains(@class, 'MuiButton-root') and contains(., 'Export current results')]"
                            ))
                        )

                        # If the button is found, proceed to click it
                        if export_button.is_displayed() and export_button.is_enabled():
                            export_button.click()
                            print("[INFO] 'Export current results' button clicked.")
                            
                            # Wait for the file to appear in the unique folder
                            max_wait_time = 10  # Maximum wait time in seconds
                            start_time = time.time()
                            while time.time() - start_time < max_wait_time:
                                files = os.listdir(unique_download_dir)
                                if files:
                                    downloaded_file = os.path.join(unique_download_dir, files[0])
                                    break
                                time.sleep(0.5)
                            else:
                                print("[WARNING] Download timeout reached. No file detected.")
                                continue
                            
                            # Rename the downloaded file if needed
                            new_filename = f"{root_folder_name}__{sub_folder_name}__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                            new_file_path = os.path.join(unique_download_dir, new_filename)
                            os.rename(downloaded_file, new_file_path)
                            print(f"[INFO] File downloaded and renamed to: {new_file_path}")
                            
                        else:
                            print(f"[INFO] No data available. Creating an empty TSV file.")
                            new_filename = f"{root_folder_name}__{sub_folder_name}__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                            new_file_path = os.path.join(unique_download_dir, new_filename)
                            # Create an empty TSV file
                            with open(new_file_path, 'w') as f:
                                f.write('')  # Write an empty string to create a valid TSV file

                    except TimeoutException:

                        print(f"[INFO] Timed out waiting for export button to appear.")
                        new_filename = f"{root_folder_name}__{sub_folder_name}__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                        new_file_path = os.path.join(unique_download_dir, new_filename)
                        # Create an empty TSV file
                        with open(new_file_path, 'w') as f:
                            f.write('')  # Write an empty string to create a valid TSV file

                # Retry mechanism to open the selection field dropdown again
                if i == len(selection_options):
                    break
                
                retry_attempts = 3
                selection_field_opened = False

                for attempt in range(retry_attempts):
                    try:
                        time.sleep(2)
                        # Try to locate and click the selection field again
                        selection_field = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//div[@id='analysis-select']")
                            )
                        )
                        selection_field.click()
                        time.sleep(1)
                        print(
                            f"[INFO] Selection field dropdown opened successfully on attempt {attempt + 1}."
                        )
                        selection_field_opened = True
                        break  # Exit the retry loop if successful
                    except Exception as e:
                        print(
                            f"[WARNING] Attempt {attempt + 1} - Unable to click selection field. Retrying... Error: {str(e)}"
                        )
                        time.sleep(2)  # Pause before retrying

                if not selection_field_opened:
                    print(
                        "[ERROR] Unable to open selection field dropdown after multiple attempts. Moving to the next option."
                    )
            except Exception as e:
                print(f"[INFO] Finished Current Page")
        print(
            f"[INFO] Finished processing sample {sample.text}"
        )

    except Exception as e:
        try:
            print(f"[INFO] Exception processing sample.")
        except:
            pass



def for_bacteria_sample(driver, base_download_dir, root_folder_name, sub_folder_name):
    base_download_dir = os.path.join(base_download_dir, "Bacteria")
    # Retry mechanism for taxonomy switcher button
    taxonomy_switcher_clicked = False
    retry_count = 3
    switcher_ids = ["artifact-select-button-biom", "artifact-select-button-kepler-biom"]
    for attempt in range(retry_count):
        for switcher_id in switcher_ids:
            try:
                taxonomy_switcher_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, switcher_id))
                )
                taxonomy_switcher_btn.click()
                taxonomy_switcher_clicked = True
                print(
                    f"[INFO] Taxonomy switcher button with ID '{switcher_id}' clicked."
                )
                time.sleep(2)  # Allow the switcher to load
                break
            except TimeoutException:
                print(
                    f"[WARNING] Attempt {attempt + 1}/{retry_count} - Failed to click taxonomy switcher button with ID '{switcher_id}'. Retrying with next ID..."
                )
        if taxonomy_switcher_clicked:
            break
        time.sleep(2)  # Allow some time before retrying

    if not taxonomy_switcher_clicked:
        print(
            "[ERROR] Unable to click taxonomy switcher button after multiple attempts."
        )
        return

    # Initialize the variable to store the working index
    working_taxonomy_index = None

    # Try multiple attempts to locate and click the taxonomy options select label
    for attempt in [2, 1]:  # Trying index 2 first, then index 1 if necessary
        try:
            taxonomy_options_select_label = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"(//div[@id='artifact-options-select'])[{attempt}]")
                )
            )
            taxonomy_options_select_label.click()
            working_taxonomy_index = attempt  # Store the working index
            print(
                f"[INFO] Taxonomy options select label clicked using attempt index {attempt}."
            )
            break
        except TimeoutException:
            print(
                f"[WARNING] Attempt to click taxonomy level with index {attempt} failed. Trying next index..."
            )

    # If a working index was found, proceed with dropdown options
    if working_taxonomy_index is not None:
        # Wait for the dropdown options to be visible
        dropdown_options = WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//ul[@role='listbox']//li")
            )
        )
        print(f"[INFO] Found {len(dropdown_options)} dropdown options.")

        # Iterate through taxonomy levels
        for i in range(len(dropdown_options)):
            # for i in range(2):
            # Re-locate the dropdown options to avoid stale element reference
            dropdown_options = WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//ul[@role='listbox']//li")
                )
            )
            option = dropdown_options[i]
            option_text = option.text
            print(f"[INFO] Taxonomy option: {option.text}")
            option.click()
            time.sleep(1)  # Wait for the selection to be processed

            try:
                # Wait for the "Export current results" button to be clickable and click it
                unique_download_dir = os.path.join(base_download_dir, option_text)
                os.makedirs(unique_download_dir, exist_ok=True)
                # Update Chrome download settings for this specific download
                driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                    "behavior": "allow",
                            "downloadPath": unique_download_dir
                        })
                
                export_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@class, 'MuiButton-root') and contains(., 'Export current results')]",
                        )
                    )
                )
                
                # If the button is found, proceed to click it
                if export_button.is_displayed() and export_button.is_enabled():
                    export_button.click()
                    print("[INFO] 'Export current results' button clicked.")
                    
                    # Wait for the file to appear in the unique folder
                    max_wait_time = 10  # Maximum wait time in seconds
                    start_time = time.time()
                    while time.time() - start_time < max_wait_time:
                        files = os.listdir(unique_download_dir)
                        if files:
                            downloaded_file = os.path.join(unique_download_dir, files[0])
                            break
                        time.sleep(0.5)
                    else:
                        print("[WARNING] Download timeout reached. No file detected.")
                        continue
                    
                    # Rename the downloaded file if needed
                    new_filename = f"{root_folder_name}__{sub_folder_name}__Bacteria__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                    new_file_path = os.path.join(unique_download_dir, new_filename)
                    os.rename(downloaded_file, new_file_path)
                    print(f"[INFO] File downloaded and renamed to: {new_file_path}")
                    
                else:
                    print(f"[INFO] No data available. Creating an empty TSV file.")
                    new_filename = f"{root_folder_name}__{sub_folder_name}__Bacteria__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                    new_file_path = os.path.join(unique_download_dir, new_filename)
                    # Create an empty TSV file
                    with open(new_file_path, 'w') as f:
                        f.write('')  # Write an empty string to create a valid TSV file
                    print(f"[INFO] Empty TSV file created: {new_file_path}")
            except Exception as e:
                print(f"[ERROR] Export current results: {str(e)}")
                new_filename = f"{root_folder_name}__{sub_folder_name}__Bacteria__{option_text}__{time.strftime('%Y-%m-%d-%M-%S')}.tsv"
                new_file_path = os.path.join(unique_download_dir, new_filename)
                # Create an empty TSV file
                with open(new_file_path, 'w') as f:
                    f.write('')  # Write an empty string to create a valid TSV file
                print(f"[INFO] Empty TSV file created: {new_file_path}")

            if i == len(dropdown_options) - 1:
                break

            # Re-click the taxonomy options select label to open the dropdown again
            try:
                taxonomy_options_select_label = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"(//div[@id='artifact-options-select'])[{working_taxonomy_index}]",
                        )
                    )
                )
                taxonomy_options_select_label.click()
                print(
                    f"[INFO] Taxonomy options select label clicked again using stored index {working_taxonomy_index}."
                )
            except TimeoutException:
                print(
                    f"[ERROR] Unable to re-click taxonomy options select label using stored index {working_taxonomy_index}."
                )
    else:
        print(
            "[ERROR] No valid taxonomy options select label index found. Cannot proceed."
        )
