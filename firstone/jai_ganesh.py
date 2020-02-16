import os
import mysql.connector
import openpyxl
from openpyxl import workbook
import time

try:
    template = "C:\\mylog\\temip\\template\Template.xlsx"
    workbk = openpyxl.load_workbook(template)

    try:

        cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='esi_alarm_dump')
        print('connected to localhost')

        cursor = cnx.cursor()
        query = "select * from temip_ocwise_alarm_static "
        cursor.execute(query)
        worksht = workbk["OCWise Alarm Count"]
        # list1 = list(listx)
        # print(len(listx))
        i = 1
        for s in cursor:
            i = i + 1
            worksht["A" + str(i)] = str(s[0])
            worksht["B" + str(i)] = str(s[1])
            worksht["C" + str(i)] = int(s[2])
            # worksht["C" + str(i)].number_format='0.00E+00'
            worksht["D" + str(i)] = int(s[3])
            worksht["E" + str(i)] = int(s[4])

            print(',' + s[0], ',' + s[1], ',' + s[2], ',' + s[3])

        cursor_raw = cnx.cursor()
        query_raw = "SELECT * FROM temip_alarm_log_tmp "
        worksht = workbk["Data"]
        j = 1
        for x in cursor_raw:
            j = j + 1
            # worksht["A" + str(i)] = str(x[0])
            # worksht["B" + str(i)] = str(x[1])
            # worksht["C" + str(i)] = str(x[2])
            # worksht["D" + str(i)] = str(x[3])
            # worksht["E" + str(i)] = str(x[4])
            # worksht["F" + str(i)] = str(x[5])
            # worksht["J" + str(i)] = str(x[6])

        cnx.close()

    except mysql.connector.Error as ex:
        print(ex)
    finally:
        cnx.close()

    workbk.save("C:\\mylog\\temip\\template\\Hi.xlsx")
    workbk.close()
except NameError as ex:
    print(ex)

