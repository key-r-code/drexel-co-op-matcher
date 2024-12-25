from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import toml


class dragonScraper:
       
   def __init__(self):
       safari_options = webdriver.SafariOptions()
       safari_options.add_argument("--enable-automatic-inspection")
       
       self.driver = webdriver.Safari(options=safari_options)
       self.wait = WebDriverWait(self.driver, 20)
       self.driver.set_window_size(1440, 900)

   def grab_interview(self, username, password):

       try:
           print("Connecting to DrexelOne...")
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
           print("Login failed")
           self.driver.quit()
           return False
       
   def scrape_each_posting(self, index):
    print("Starting to scrape posting")
    try:
        html_directory = "job_htmls"
        os.makedirs(html_directory, exist_ok=True)
        html_content = self.driver.page_source
        print("Got HTML content")

        with open(f"{html_directory}/job_{str(index + 1)}.html", "w", encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved page_{str(index + 1)}.html")
            
    except Exception as e:
        print(f"Error in scrape_each_posting: {e}")

   def scrape_all_postings(self):

    job_links = self.driver.find_elements(By.XPATH, "//a[.//span[contains(@class, 'strongtext')]]")
    print(f"Found {len(job_links)} jobs on this page")
    
    for i, job in enumerate(job_links):
        try:
            job.click()
            print(f"Clicked job {i + 1}")

            time.sleep(2)
        
            self.scrape_each_posting(i)

            time.sleep(2)

            self.driver.back()
            print(f"Returned to main page")
            
        except Exception as e:
            print(f"Error processing job {i + 1}: {str(e)}")
            continue
       
    













            
       
