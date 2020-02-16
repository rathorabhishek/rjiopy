import mysql.connector
import sys


query_sys_check = """SELECT location , draname , IP , class ,statu as status
from
(select b.location ,a.draname, b.ip ,a.class,a.statu
from epc.tbl_pcrf_sys_check a left join  epc.tbl_pcrf2 b
on a.draname = b.hostname)a where statu != 'OK';"""



query_disk_usgage = """select location,DraName,IP,mountname Mount,disusage from
(SELECT b.location,a.draname,b.ip,a.mountname,a.disusage
FROM epc.tbl_pcrf_diskcheck a
left join epc.tbl_pcrf2 b on a.draname = b.hostname)a where disusage >90;"""

cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307')

cursor_sys_check = cnx.cursor()
cursor_sys_check.execute(query_sys_check)

mailstr_syscheck = "<html> <body> " \
                   "<p>This is an Auto Mail <br> For Packet offset delay and alarm detail ,Kindly refer attached Excel WorkBook </br> </p> <br> " \
                   "<h3><u> PCRF SYSTEM  HEALTH CHECK : SYS CHECK  ANALYSIS   </u></h3> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> LOCATION </th>  <th style='color:black'> DRA NAME </th>     " \
                   "<th style='color:black'> DRA IP</th> <th style='color:black'> CLASS </th> <th style='color:black'>STATUS </th>     " \
                   "</tr> "
concats_syscheck = ""

for s in cursor_sys_check:
    mailstr1_syschek = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
                    "<td>" + str(s[4])+"</td>" \
        "</tr>"
    concats_syscheck = concats_syscheck + mailstr1_syschek
finish_sys = "</table> <br> <br> "
cursor_sys_check.close()




mailstr_diskcheck = "<h3><u>PCRF SYSTEM  HEALTH CHECK : DISK CHECK  ANALYSIS > 90 Percent </u></h3> <br>" \
                    "<table border ='1'> " \
                    "<tr align='center'> " \
                    "<th> LOCATION </th>  <th style='color:black'> DRA NAME </th>     " \
                    "<th style='color:black'> DRA IP</th> <th style='color:black'> MountName </th> <th style='color:black'>DiskUsage </th>     " \
                    "</tr> "
cursor_disk_usgae = cnx.cursor()
cursor_disk_usgae.execute(query_disk_usgage)
concat_disk_check = ""
for s in cursor_disk_usgae:
    mailstr_diskusage = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
                    "<td>" + str(s[4]) + "</td>" \
        "</tr>"
    concat_disk_check = concat_disk_check + mailstr_diskusage

finish_disk_check = "</table> <br> <br> "






finish_html = "</body></html>"
print(mailstr_syscheck + concats_syscheck + finish_sys + mailstr_diskcheck +
      concat_disk_check + finish_disk_check + finish_html)




