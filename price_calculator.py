import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class ParseDownloads:
    @staticmethod
    def start_downloads(search_url):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service("C:\\Users\\alvis\\Downloads\\chromedriver-win64\\chromedriver.exe"), options=options)

        downloaded_songs = set()

        try:
            while True:
                driver.get(search_url)
                wait = WebDriverWait(driver, 60)
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(8)

                table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-striped.table-row-dashed.align-middle.gs-0.gy-3.my-0')))
                rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

                if not rows:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(8)
                    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

                    if not rows:
                        button = driver.find_element(By.ID, 'view_songs_load_more')
                        button.click()
                        time.sleep(12)
                        continue 

                for row in rows:
                    try:
                        name_element = row.find_element(By.CSS_SELECTOR, '.text-gray-800.fw-bold.text-hover-primary.mb-0.fs-4')
                        song_name = name_element.text.strip()

                        if song_name in downloaded_songs:
                            print(f"{song_name} has already been downloaded.")
                            continue

                        download_button = row.find_element(By.CSS_SELECTOR, '.btn.btn-sm.btn-outline.btn-outline-dashed.mb-2')
                        download_button.click()

                        downloaded_songs.add(song_name)
                        print(f"Started downloading: {song_name}")

                        time.sleep(8)

                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue

                time.sleep(5)

        finally:
            driver.quit()
            print('Selenium driver has been closed')
