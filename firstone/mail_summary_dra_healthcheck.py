import mysql.connector
import sys


query_sys_check = """select
location, dra_node, server_role, ip, draname, class, status
from (SELECT
b.location ,b.dra_node ,b.server_role,b.ip,a.draname, a.class,a.statu as status
FROM epc.tbl_dra_sys_check a left join epc.tbl_dra2 b
on  a.draname =b.hostname order by draname)a
where status != 'OK'"""

query_ha_stat = """select
location, dra_node, server_role, ip, draname, service, `Status`
from (select b.location ,b.dra_node ,b.server_role,b.ip,a.draname, a.service, a.statu as Status
from epc.tbl_dra_ha_mystat a left join  epc.tbl_dra2 b
on  a.draname =b.hostname
order by draname)dt where `status` like '%oos%'"""

query_disk_usgage = """select
location, dra_node, server_role, ip, draname, Mount, disusage from
(select
b.location ,b.dra_node ,b.server_role,b.ip,
a.draname, a.mountname as Mount , a.disusage from epc.tbl_dra_diskcheck a
left join epc.tbl_dra2 b
on  a.draname =b.hostname order by draname )dt where disusage > 90"""

cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307')

cursor_sys_check = cnx.cursor()
cursor_sys_check.execute(query_sys_check)

mailstr_syscheck = "<html> <body> " \
                   "<p>This is an Auto Mail <br> For Critical , Major Alarm and Packet offset delay ,Kindly refer attached Excel WorkBook </br> </p> <br> " \
                   "<h3><u> DRA SYSTEM  HEALTH CHECK : SYS CHECK  ANALYSIS   </u></h3> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> LOCATION </th> <th style='color:black'>DRA NODE</th> <th style='color:black'> Server Role</th> <th style='color:black'> DRA IP </th>     " \
                   "<th style='color:black'> DRA NAME</th> <th style='color:black'> CLASS </th> <th style='color:black'>STATUS </th>     " \
                   "</tr> "
concats_syscheck = ""

for s in cursor_sys_check:
    mailstr1_syschek = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
                    "<td>" + str(s[4]) + "</td>" + "<td>" + str(s[5]) + "</td>" + "<td>" + str(s[6]) + "</td>" + \
        "</tr>"
    concats_syscheck = concats_syscheck + mailstr1_syschek
finish_sys = "</table> <br> <br> "
cursor_sys_check.close()

mailstr_ha_stat = "<h3><u>DRA SYSTEM  HEALTH CHECK : HA STAT  ANALYSIS(Out of Service Node) </u></h3> <br>" \
                  "<table border ='1'> " \
                  "<tr align='center'> " \
                  "<th> LOCATION </th> <th style='color:black'>DRA NODE</th> <th style='color:black'> Server Role</th> <th style='color:black'> DRA IP </th>     " \
                  "<th style='color:black'> DRA NAME</th> <th style='color:black'> Service </th> <th style='color:black'>Status </th>     " \
                  "</tr> "
concat_ha_stat = ""

cursor_ha_stat = cnx.cursor()
cursor_ha_stat.execute(query_ha_stat)
for s in cursor_ha_stat:
    mailstr1 = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
                    "<td>" + str(s[4]) + "</td>" + "<td>" + str(s[5]) + "</td>" + "<td>" + str(s[6]) + "</td>" + \
        "</tr>"
    concat_ha_stat = concat_ha_stat + mailstr1

cursor_ha_stat.close()
finish_ha_stat = "</table> <br> <br> "

mailstr_diskcheck = "<h1><u>DRA SYSTEM  HEALTH CHECK : DISK CHECK  ANALYSIS > 90 Percent </u></h1> <br>" \
                    "<table border ='1'> " \
                    "<tr align='center'> " \
                    "<th> LOCATION </th> <th style='color:black'>DRA NODE</th> <th style='color:black'> Server Role</th> <th style='color:black'> DRA IP </th>     " \
                    "<th style='color:black'> DRA NAME</th> <th style='color:black'> MountName </th> <th style='color:black'>DiskUsage </th>     " \
                    "</tr> "
cursor_disk_usgae = cnx.cursor()
cursor_disk_usgae.execute(query_disk_usgage)
concat_disk_check = ""
for s in cursor_disk_usgae:
    mailstr_diskusage = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
                    "<td>" + str(s[4]) + "</td>" + "<td>" + str(s[5]) + "</td>" + "<td>" + str(s[6]) + "</td>" + \
        "</tr>"
    concat_disk_check = concat_disk_check + mailstr_diskusage

finish_disk_check = "</table> <br> <br> "


finish_html = "</body></html>"
print(mailstr_syscheck + concats_syscheck + finish_sys + mailstr_diskcheck +
      concat_disk_check + finish_disk_check + mailstr_ha_stat + concat_ha_stat + finish_ha_stat + finish_html)




