import time
from selenium.common import NoSuchElementException
from dotenv import load_dotenv

from download_files import ParseDownloads

load_dotenv()

CHECK_INTERVAL = 600

def main():
    while True:
        try:
            ParseDownloads.start_downloads()

            time.sleep(CHECK_INTERVAL)
        except NoSuchElementException:
            print("Element not found. Skipping this iteration.")
            continue

if __name__ == "__main__":
    main()
