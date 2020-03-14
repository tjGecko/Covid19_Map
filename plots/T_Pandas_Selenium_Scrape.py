from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time


driver = webdriver.Chrome()
driver.implicitly_wait(30)
# time.sleep(5) #extra time to let all JS on site load
driver.get('https://www.doh.wa.gov/Emergencies/Coronavirus')
time.sleep(3)

# src = driver.page_source
src = driver.find_element_by_tag_name(name='html')
soup_selector = BeautifulSoup(driver.page_source, 'lxml')

# Beautiful Soup grabs the HTML table on the page
# tables = soup_level2.find_all('table')
table = soup_selector.find_all('table')[4]

# for table in tables:
#     print(table)

# Giving the HTML table to pandas to put in a dataframe object
df_list = pd.read_html(str(table), header=1)
df = df_list[0]
df2 = df.iloc[0:15, 0:3]
print(df2)

driver.close()