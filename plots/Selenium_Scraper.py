from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time


class SeleniumScraper:
    def __init__(self):
        self.url = 'https://www.doh.wa.gov/Emergencies/Coronavirus'
        self.county_data = None

    def load(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get('https://www.doh.wa.gov/Emergencies/Coronavirus')
        time.sleep(3)

        src = driver.find_element_by_tag_name(name='html')
        soup_selector = BeautifulSoup(driver.page_source, 'lxml')

        # Beautiful Soup grabs the HTML table on the page
        table = soup_selector.find_all('table')[4]

        # Giving the HTML table to pandas to put in a dataframe object
        df_list = pd.read_html(str(table), header=1)
        df = df_list[0]
        df2 = df.iloc[0:15, 0:3]
        print(df2)

        driver.close()

        # MATCH DATA SCHEMA
        # ==================
        self.county_data = {}
        for index, row in df.iterrows():
            key = row['County']
            cfg = {
                'Confirmed_Cases': row['Positive/Confirmed Cases'],
                'Deaths': row['Deaths'],
            }

            self.county_data[key] = cfg

        return self.county_data