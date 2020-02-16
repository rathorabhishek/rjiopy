import mysql.connector
import pymongo
import sys
from pymongo import InsertOne
import os

# getting data from pymongo  and inserting into mysql table .
# print(os.stat('C:\\Users\\abhishek.rathor\\Downloads\\HSI-2019-06-07.xlsx').st_size/(1024*1024))

#filesizemb = os.stat('C:\\Users\\abhishek.rathor\\Downloads\\HSI-2019-06-07.xlsx').st_size / (1024 * 1024)
#if filesizemb > 5:
#    print("Message file size is greater than 5")
#else:
#    print("ok ..yu can send your message")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["epc"]
mycollection =mydb.cms_hypervisor_list
print(mycollection)
print('you are in')
sys.exit()
print('ok read')




#getting data inot mysql table ,then inserting data into mongodb .

query_final =" SELECT * FROM epc.cms_hypervisor_list where date_format(dttime,'%Y-%m-%d') = date_format(date_sub(now() ,interval 18 day),'%Y-%m-%d') "\
              " and circle = 'MAH' and state !='State';"
cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='epc')
cnx.autocommit=True
try:
   if cnx.is_connected():
       print('connected to localhost')
       cursor = cnx.cursor()
       # cursor.execute(query_final)
       print(query_final)
       cursor.execute(query_final)
       result=cursor.fetchall()
       for res in result:
           print(res)
       cursor.close()
       cnx.close()
       print("successfully executed")
except NameError as ex:
    print(ex)
    cnx.close()