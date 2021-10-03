# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 23:45:07 2021

@author: oming
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

path = "D:\\Downloads\\chromedriver_win32\\chromedriver"
slp_time = 15
num_jobs = 50
keyword = "data engineer"

def get_jobs(keyword, num_jobs, path, slp_time, verbose=False):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + keyword + '&suggestCount=0&suggestChosen=false&clickSource=searchBox&locId=1147401&locT=C&locName=San%20Francisco%2C%20CA'
    # url = "https://www.glassdoor.co.in/profile/login_input.htm"
    url = "https://www.glassdoor.co.in/Job/san-francisco-data-engineer-jobs-SRCH_IL.0,13_IC1147401_KO14,27.htm"
    driver.get(url)
    jobs = []

    time.sleep(slp_time)
    

    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass
    except:
        pass

    try:
        driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
    except NoSuchElementException:
        pass

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
        
        
        # Going through each job in this page
        job_buttons = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul')  # jl for Job Listing. These are the buttons we're going to click.
        
        time.sleep(slp_time)
        # # job_buttons = JobResults.find_element_by_xpath('.//ul[contains(@class, "css-kgm6qi exy0tjh1")]')
        all_li = job_buttons.find_elements_by_tag_name("li")
        
        time.sleep(slp_time)
        for li in all_li:
            if len(jobs) >= num_jobs:
                break
            try:
                li.click()
                try:
                    driver.find_element_by_css_selector('[alt="Close"]').click()
                except StaleElementReferenceException:
                    li.click()
                except NoSuchElementException:
                    pass
            except ElementClickInterceptedException:
                try:
                    driver.find_element_by_css_selector('[alt="Close"]').click()
                    li.click()
                except NoSuchElementException:
                    pass

            time.sleep(2)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    job_title = driver.find_element_by_xpath('.//div[@class="css-1j389vi e1tk4kwz2"]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = li.find_element_by_xpath('.//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            try:
                try:
                    driver.find_element_by_xpath('.//div[@data-item="tab" and @data-tab-type="overview"]').click()

                except ElementClickInterceptedException:
                    try:
                        driver.find_element_by_css_selector('[alt="Close"]').click()
                    except NoSuchElementException:
                        pass

                try:
                    size = driver.find_element_by_xpath(
                    './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Size")]//following-sibling::*').text

                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath(
                        './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Founded")]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Type")]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath(
                        './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Industry")]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath(
                        './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Sector")]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath(
                        './/div[@id="EmpBasicInfo"]//div[1]//div[1]//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2" and contains(.//span, "Revenue")]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue})
                        # add job to jobs

        try:
            driver.find_element_by_xpath('.//li//a[@data-test="pagination-next"]').click()
        except ElementClickInterceptedException:
            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            print(
                "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.