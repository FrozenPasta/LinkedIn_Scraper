from ast import keyword
import time
import os.path
from turtle import pos
import pandas as pd
import re
import information

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pandas import ExcelWriter

from selenium.common.exceptions import NoSuchElementException


PATH = "./chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)

#local_file = pd.read_csv('test.csv', index_col=0)

class LinkedInScraper:
    def __init__(self) -> None:
        pass

    def login(self, mail, password):

        actions = ActionChains(driver)

        driver.get("https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        driver.find_element(By.ID, 'username').send_keys(mail)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, "//*[@id='organic-div']/form/div[3]/button").click()
        time.sleep(1)

    def job_LinkedIn(self, keywords, location):
        driver.get("https://www.linkedin.com/jobs/")
        time.sleep(1)

        search_bars = driver.find_elements_by_class_name('jobs-search-box__text-input')
        time.sleep(1)
        search_keywords = search_bars[0]
        search_keywords.send_keys(keywords)
        time.sleep(1)

        search_location = search_bars[3]
        search_location.send_keys(location)

        driver.find_element(By.XPATH, "//*[@id='global-nav-search']/div/div[2]/button[1]").click()

        time.sleep(2)


    def run(self, email, password, keywords, location):
        """ 
        
        """
        self.login(email, password)
        self.job_LinkedIn(keywords, location)
        # scrolls a single page:
        #for page in range(2,8):

        for page in range(1,2):
            # get a list of all the listings elements's in the side bar
            list_items = driver.find_elements_by_class_name("occludable-update")

            for job in list_items:
                time.sleep(1)
                # executes JavaScript to scroll the div into view
                driver.execute_script("arguments[0].scrollIntoView();", job)
                job.click()
                time.sleep(1)
                resultat = []
                # get info:
                try:
                    [position, company, location] = job.text.split('\n')[:3]
                    currentUrl = driver.current_url
                    identifiantJob = re.findall('currentJobId=([0-9]{10})', currentUrl)
                    
                    details = driver.find_element(By.ID, "job-details").text

                    temp_result = {
                                    'Position ': position,
                                    'IdJob' : identifiantJob[0],
                                    'Company': company,
                                    'Location': location,
                                    #'Informations': details      
                    }
                    resultat.append(temp_result)
                except:
                    identifiantJob = re.findall('currentJobId=([0-9]{10})', currentUrl)
                    temp_result = {
                                    'IdJob' : identifiantJob[0],
                                    #'Informations': details      
                    }
                    resultat.append(temp_result)

            driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']").click()
            time.sleep(3)
            print("Fin de l'extraction")


        df = pd.DataFrame(resultat)
        local_file = df.to_csv("./LinkedInScraper.csv", index=True)
        print('Operation over')

if __name__ == "__main__":
    email = information.email
    password = information.password
    scraper = LinkedInScraper()
    keywords = "Summer"
    location = "Japon"

    scraper.run(email, password, keywords, location)









#   resultat_tech = []
#   resultat_fi = []    
#   series_tech = pd.Series(['Data' or 'Technology' or 'Developer'])
#     if (position.contains(series_tech)):
#         temp_technology_result = {'Position ': position,
#                         'IdJob' : identifiantJob,
#                         'Company': company,
#                         'Location': location,
#                         #'Informations': details      
#             }
#     elif (position.lower().contains("Finance" or "Investment" or "Sales" or "Trading" or "Management" or "Analyst" or "Banking" or "Market")):
#         temp_finance_result = {'Position ': position,
#                         'IdJob' : identifiantJob,
#                         'Company': company,
#                         'Location': location,
#                         #'Informations': details      
#             }
#     else:
#         temp_result = {'Position ': position,
#             'IdJob' : identifiantJob,
#             'Company': company,
#             'Location': location,
#             #'Informations': details  
#         }
#     resultat_tech.append(temp_technology_result)
#     resultat_fi.append(temp_finance_result)

# df_tech = pd.DataFrame(resultat_tech)
# df_fi = pd.DataFrame(resultat_fi)

# local_file_tech = df_tech.to_csv("./LinkedInScraperTechnology.csv", index=True)
# local_file_fi = df_fi.to_csv("./LinkedInScraperFinance.csv", index=True)

#https://medium.com/nerd-for-tech/linked-in-web-scraper-using-selenium-15189959b3ba