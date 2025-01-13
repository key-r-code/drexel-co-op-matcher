from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import os


class dragonScraper:
    def __init__(self):
        safari_options = webdriver.SafariOptions()
        safari_options.add_argument("--enable-automatic-inspection")
        self.driver = webdriver.Safari(options=safari_options)

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--enable-automatic-inspection")
        # self.driver = webdriver.Chrome(options=chrome_options)

        # firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--enable-automatic-inspection")
        # self.driver = webdriver.Firefox(options=firefox_options)

        self.wait = WebDriverWait(self.driver, 20)
        self.driver.set_window_size(1440, 900)


    def login_to_banner(self, username, password):
        """Connects to Drexel Banner"""
        try:
            print("Connecting to DrexelBanner...")
            self.driver.get('https://connect.drexel.edu')
            time.sleep(3)

            # Find and click the sign in button
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='SIGN IN']")))
            sign_in_button.click()
        
            time.sleep(3)  

            # Enter drexel userID
            username_input = self.wait.until(EC.presence_of_element_located((By.ID, "i0116")))
            username_input.send_keys(username + "@drexel.edu")  

            # Click next and navigate to the password page
            next_button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
            next_button.click()

            time.sleep(3)

            # Enter password
            password_input = self.wait.until(EC.presence_of_element_located((By.ID, "i0118")))
            password_input.send_keys(password)

            # Click Sign in button
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
            sign_in_button.click()
            
            print("Waiting for 2FA approval...")
            bannerweb_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-primary[href*='bannersso.drexel.edu']")))
            print("2FA approved, continuing...")
            bannerweb_button.click()

            time.sleep(3)

        except TimeoutException:
            self.driver.quit()
            return False

    def grab_job_postings(self, operating_sys, majors):
        """Navigates to job listing portal"""
        try:
            # navigate to SCDC services page
            scdc_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='P_CMCMnu']")))
            scdc_link.click()

            time.sleep(3)

            # navigate to job portal
            job_portal_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='P_StudentJobSearchStud']")))
            job_portal_link.click()

            time.sleep(3)

            # selecting from multi-select menu
            major_select = self.wait.until(EC.presence_of_element_located((By.ID, "i_a_cmajs_id")))
            

            actions = ActionChains(self.driver)

            # Hold down Command key (for Mac) or Control key (for Windows)
            if operating_sys == 'Windows': 
                actions.key_down(Keys.CONTROL)
            elif operating_sys == 'Mac':
                actions.key_down(Keys.COMMAND)

            # Select each major from list
            for option in major_select.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") in majors:
                    option.click()
            
            # Release key
            if operating_sys == 'Windows':
                actions.key_up(Keys.CONTROL)
            elif operating_sys == 'Mac':
                actions.key_up(Keys.COMMAND)

            actions.perform()

            search_button = self.driver.find_element(By.XPATH, '//input[@value="Search"]')
            search_button.click()

            time.sleep(3)

        except TimeoutError:
            self.driver.quit()
            return False

    def grab_past_interviews(self):
        """Navigates to Request Interviews Phase List"""
        
        try:
           # navigate to SCDC services page
           scdc_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='P_CMCMnu']")))
           scdc_link.click()

           time.sleep(3)
           
           # navigate to interview page
           interview_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='P_StudentRequestMaintStud']")))
           interview_link.click()

           time.sleep(3)

           # display all interviews
           display_all_interviews = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='P_StudentReqMaintSignupIntrv']")))
           display_all_interviews.click()

           # wait until heading appears
           self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'List All Interview Requests in Signup for Interviews Phase')]")))

        except TimeoutException:
            self.driver.quit()
            return False
       
    def scrape_each_posting(self, index):
        print("Starting to scrape posting")
        try:
            html_directory = "job_htmls1"
            os.makedirs(html_directory, exist_ok=True)
            html_content = self.driver.page_source
            print("Got HTML content")

            with open(f"{html_directory}/job_{str(index + 1)}.html", "w", encoding='utf-8') as f:
                f.write(html_content)
            print(f"Saved page_{str(index + 1)}.html")
            
        except Exception as e:
            print(f"Error in scrape_each_posting: {e}")

    def scrape_all_postings(self):
        while True:
            # Get records info from the text
            records_text = self.driver.find_element(By.CLASS_NAME, "centeraligntext").text
            start_record = int(records_text.split("to")[0].split()[-1])
            end_record = int(records_text.split("to")[1].split()[0])
            total_records = int(records_text.split("of")[1].split()[0])
            records_per_page = end_record - start_record + 1
            
            total_pages = -(-total_records // records_per_page)  
            current_page = -(-end_record // records_per_page)
            
            print(f"Processing page {current_page} of {total_pages} (Total records: {total_records})")
            
            # Get all job links on current page
            job_links = self.driver.find_elements(By.XPATH, "//a[.//span[contains(@class, 'strongtext')]]")
            print(f"Found {len(job_links)} jobs on this page")
        
            for i, job in enumerate(job_links):
                try:
                    job.click()
                    print(f"Clicked job {i + 1}")
                    time.sleep(2)
                
                    global_index = (current_page - 1) * records_per_page + i
                    self.scrape_each_posting(global_index)

                    time.sleep(2)

                    self.driver.back()
                    print(f"Returned to main page")
                    
                except Exception as e:
                    print(f"Error processing job {i + 1}: {str(e)}")
                    continue
            
            if current_page >= total_pages:
                print("Reached last page")
                break
                
            try:
                next_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img[name='Arrow-Next']"))
                )
                next_button.click()
                time.sleep(2)
                    
            except Exception as e:
                print(f"Error navigating to next page: {str(e)}")
                break