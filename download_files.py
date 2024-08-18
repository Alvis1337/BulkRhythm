import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from dotenv import load_dotenv

load_dotenv()

class ParseDownloads:
    download_folder_path = os.getenv('DOWNLOAD_FOLDER_PATH', os.path.join(os.getcwd(), 'downloads'))
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    prefs = {
        "download.default_directory": download_folder_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver_path = os.getenv('CHROMEDRIVER_PATH')
    downloaded_songs_file = os.getenv('DOWNLOAD_SONGS_FILE', 'downloaded_songs.json')
    search_url = os.getenv('SEARCH_URL')

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    @staticmethod
    def load_downloaded_songs(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return set(json.load(file))
        return set()

    @staticmethod
    def save_downloaded_songs(downloaded_songs, filename):
        with open(filename, 'w') as file:
            json.dump(list(downloaded_songs), file)

    @staticmethod        
    def load_page():
        ParseDownloads.driver.get(ParseDownloads.search_url)
        return WebDriverWait(ParseDownloads.driver, 60)

    @staticmethod
    def set_filters(wait):
        try:
            filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-dark.me-3.songs_view_filter_drawer')))
            filter_button.click()
            
            time.sleep(2)
            
            close_notice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.svg-icon.svg-icon-1')))
            close_notice.click()
            
            time.sleep(2)

            full_band_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.form-check-input')))
            full_band_toggle.click()
            
            time.sleep(2)

            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary.flex-grow-1.fw-semibold')))
            submit_button.click()

            time.sleep(5)
        except TimeoutException as e:
            print(f"Error setting filters: {e}")
        except ElementNotInteractableException as e:
            print(f"Element not interactable: {e}")

    @staticmethod
    def scroll_and_load_rows(wait):
        ParseDownloads.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)
        
        try:
            table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-striped.table-row-dashed.align-middle.gs-0.gy-3.my-0')))
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
            return rows
        except TimeoutException:
            print("No rows found after scrolling.")
            return []

    @staticmethod
    def start_downloads():
        downloaded_songs = ParseDownloads.load_downloaded_songs(ParseDownloads.downloaded_songs_file)
        wait = ParseDownloads.load_page()

        try:
            ParseDownloads.set_filters(wait)

            while True:
                rows = ParseDownloads.scroll_and_load_rows(wait)

                if not rows:
                    try:
                        load_more_button = wait.until(EC.element_to_be_clickable((By.ID, 'view_songs_load_more')))
                        load_more_button.click()
                        time.sleep(12)
                        continue
                    except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                        print("No more songs to load.")
                        break

                for row in rows:
                    try:
                        name_element = row.find_element(By.CSS_SELECTOR, '.text-gray-800.fw-bold.text-hover-primary.mb-0.fs-4')
                        song_name = name_element.text.strip()

                        if song_name in downloaded_songs:
                            print(f"{song_name} has already been downloaded.")
                            continue

                        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-sm.btn-outline.btn-outline-dashed.mb-2')))
                        ParseDownloads.driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                        download_button.click()

                        downloaded_songs.add(song_name)
                        ParseDownloads.save_downloaded_songs(downloaded_songs, ParseDownloads.downloaded_songs_file)
                        print(f"Started downloading: {song_name}")

                        time.sleep(8)

                    except (NoSuchElementException, ElementNotInteractableException) as e:
                        print(f"Error processing row: {e}")
                        continue

                time.sleep(5)

        except Exception as e:
            print(f"Error in main loop: {e}")

        finally:
            ParseDownloads.driver.quit()
            print('Selenium driver has been closed')

