from dragonScraper import dragonScraper


if __name__ == "__main__":

    scraper = dragonScraper()
    scraper.grab_interview(USER, PASSWORD)

    scraper.scrape_all_postings()