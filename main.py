from dragonScraper import dragonScraper


if __name__ == "__main__":

    scraper = dragonScraper()

    # add login details
    scraper.login_to_banner(username='', password='')

    # choose operating system (Mac/Windows)
    operating_sys = 'Mac'

    # select majors, see majors.json for full code list
    majors = ["CO-COMP", "CO-DS", "EN-COM", "EN-ELEC"]
    
    scraper.grab_job_postings(operating_sys=operating_sys, majors=majors)
    scraper.scrape_all_postings()