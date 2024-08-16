import time

from selenium.common import NoSuchElementException

from query_builder import QueryBuilder
from price_calculator import ParseDownloads

query_builder = QueryBuilder()

PRICE_FILE = "songs_downloaded.json"
CHECK_INTERVAL = 600

SEARCH_URL = 'https://rhythmverse.co/songfiles/game/rb3xbox'

def main():
    while True:
        try:
            ParseDownloads.start_downloads(SEARCH_URL)

            time.sleep(CHECK_INTERVAL)
        except NoSuchElementException:
            print("Element not found. Skipping this iteration.")
            continue

if __name__ == "__main__":
    main()
