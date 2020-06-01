#!/usr/bin/env python
# coding: utf-8

import mysql.connector as mariadb
from selenium.webdriver import PhantomJS
import time
import datetime
import sys

config = {
  'database': 'destimate',
  'host': 'localhost',
  'user': 'root',
  'password': 'root',
}
conn = mariadb.connect(**config)
cur = conn.cursor()

url = 'https://www.assetapex.com/nifty-pe-ratio-chart/'

driver = PhantomJS("phantomjs.exe")
driver.maximize_window()
driver.get(url)
time.sleep(2)

scrape_date = datetime.date.today()
print(scrape_date)

tr = driver.find_element_by_xpath('//*[@id="tablepress-4"]/tbody/tr')
tds = tr.find_elements_by_tag_name('td')

pe = tds[1].text
pb = tds[2].text
dividend_yield = tds[3].text

cur.execute("select * from PE_PB_dividend_yield_data where scrape_date='" + str(scrape_date) + "';")
x = cur.fetchall()

print(len(x))
if len(x) >= 1:
    sys.exit(0)
else:
    cur.execute("INSERT INTO PE_PB_dividend_yield_data(scrape_date,PE,PB,dividend_yeild) VALUES ('" + str(scrape_date) + "'," + str(pe) + "," + str(pb) + "," + str(dividend_yield) + ")")
    conn.commit()
print("Record inserted ")
# In[ ]:




