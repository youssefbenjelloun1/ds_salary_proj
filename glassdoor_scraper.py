# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 17:51:25 2021

@author: Youssef
"""

  
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 12:39:46 2020
@author: Jen butt
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import pandas as pd
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

#from selenium.webdriver.common.touch_actions import TouchActions
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.actions import Actions

def get_jobs(keyword, location, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1920, 1080)


    driver.get('https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&sc.keyword=&locT=&locId=&jobType=')
    
    #Uses first variable in function to input job title
    search = driver.find_element_by_id("KeywordSearch")
    search.send_keys(keyword)
    
    #Uses second variable in function to input Location.  Use 'City,State Abbreviation'
    search = driver.find_element_by_id("LocationSearch").clear()
    search = driver.find_element_by_id("LocationSearch")
    search.send_keys(location)
    search.send_keys(Keys.RETURN)
    
    #Test for the "Sign Up" prompt and get rid of it.
    time.sleep(slp_time)
    
    try:
                driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass
    
    time.sleep(.1)
    
    try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
    except NoSuchElementException:
        pass
    
    #changes 'posted' dropdown to 'Last Week'
    driver.find_element_by_id('filter_fromAge').click()
    time.sleep(5)
    driver.find_element_by_xpath('.//ul[@class="css-1dv4b0s ew8xong0"]//li[@value="7"]').click()
   
    
    
    jobs = []
    
    time.sleep(5)
    # Auto-accepts cookies
    try:
        driver.find_element_by_css_selector('[id="onetrust-accept-btn-handler"]').click()  # clicking to the X.
    except NoSuchElementException:
        pass
    time.sleep(.1)

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
       
        time.sleep(5)
        
        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
      
        
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
        
            #touchactions = TouchActions(driver)
            #touchactions.tap(job_button).perform()
            #ActionChains(driver).move_to_element(job_button).click().perform()
            
          
            #webdriver.ActionChains(driver).move_to_element(job_button).perform()
            #actions.moveToElement(job_button).click().perform();
            #driver.execute_script("arguments[0].scrollIntoView();", job_button)
            driver.execute_script("arguments[0].click();", job_button)  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[1]').text
                    location = driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[3]').text
                    job_title = driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[2]').text
                    job_description = driver.find_element_by_xpath('//*[@id="Details"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[4]').text

            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[1]/span').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1


            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
               

                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.