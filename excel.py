# import the modules
from pymysql import*
import xlwt
import pandas.io.sql as sql
import time

from sqlalchemy import true


def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec

second = sleep_time(0,0,5)
while true:
    time.sleep(second)
    con = connect(user="rfidwebapp",password="rfid12345",host="localhost",database="rfid")
    df = sql.read_sql('select * from user',con)
    print(df)
    df.to_excel('rfid.xls')

    dg=sql.read_sql('select * from attendance',con)
    print(dg)
    dg.to_excel('rfid1.xls')

    dh=sql.read_sql('select * from profiles',con)
    print(dh)
    dh.to_excel('rfid2.xls')

# export the data into the excel sheet


