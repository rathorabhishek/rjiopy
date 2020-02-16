import mysql.connector
import mysql
import sys

query =""" select  role SubDomain, `Status`, count(role) Count from epc.hsi_handover_tracker  
             where status != 'Closed' group by role,status order by role;  """


cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307' ,database='epc')
cursor = cnx.cursor()
cursor.execute(query)

html_start = "<html> <body> " \
                   "<p>This is an Auto Mail</p> <br> " \
                   "<h3><u> Handover Portal Status Count(Open/Acknowledge) : </u> </h3>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> Role </th>  <th style='color:black'> Status </th>     " \
                   " <th style='color:black'> Status Count</th> </tr> "

concats_ho_mail = " "

for tup in cursor:
    mailstr1_ho_mail = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>"  "<td>" + str(tup[1]) + "</td>" "<td>" + str(tup[2]) + "</td>  </tr>"
    concats_ho_mail = concats_ho_mail + mailstr1_ho_mail

finish_ho_mail = "</table> <br> <br> "
cursor.close()
cnx.close()

finish_html = "</body></html>"

print(html_start + concats_ho_mail + finish_html)

