import csv
import mysql.connector as mariadb
from datetime import datetime
import sys

config = {
  'database': 'destimate',
  'host': 'localhost',
  'user': 'root',
  'password': 'root',
}

conn = mariadb.connect(**config)
cur = conn.cursor()

file = open("NSE_PE_PB_Dividend_yield_1999_to_2020.csv", mode="r")
reader = csv.DictReader(file)

for row in reader:
    dat = datetime.strptime(row.get("Date"), '%d-%b-%Y')
    dat = dat.date()
    print(row.get("P/E"))
    print(row.get("P/B"))
    print(row.get("Div Yield"))

    cur.execute("select * from PE_PB_dividend_yield_data where scrape_date='" + str(dat) + "';")
    x = cur.fetchall()

    if len(x) >= 1:
        print("Already exist")
        continue
    else:
        cur.execute("INSERT INTO PE_PB_dividend_yield_data(scrape_date,PE,PB,dividend_yeild) VALUES ('" + str(dat) + "'," + str(row.get("P/E")) + "," + str(row.get("P/B")) + "," + str(row.get("Div Yield")) + ")")
        conn.commit()
        print("Record inserted ")