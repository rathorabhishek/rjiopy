import  mysql.connector

query_free_m = """select name,total, free, 100*(cast(Free as signed)/cast(Total as signed)) as freeRatio   from epc.lcs_free_m
                   where 100*(cast(Free as signed)/cast(Total as signed)) <20 ;"""

query_disk_space = """ select Name, Filesystem, Mounted_on,Used_Per
                        from epc.lcs_diskspace where cast(replace(Used_Per,'%','') as unsigned) >80 ;   """


query_systemcheck = """ select Name, replace(replace(Replace(status1,'Status : [1;31m',''),'(local)',''),'status : [1;31m','') Stat
                      from epc.lcs_systemcheck where status1 not like '%up%' and status1 not like '%sysstatus%';  """



cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307')

cursor_free_m = cnx.cursor()
cursor_free_m.execute(query_free_m)

mailstr_freem = "<html> <body> " \
                   "<p>This is an Auto Mail  <br> " \
                   "<h3><u> LCS   HEALTH CHECK : Free Memory (less Than 20 Percent)   </u></h3> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> Name </th>  <th style='color:black'> Total Memory(KiB) </th>     " \
                   "<th style='color:black'> Free Memory(KiB)</th> <th style='color:black'> Free Memory(%) </th> " \
                   "</tr> "

concats_freem = ""

for s in cursor_free_m:
    mailstr1_freem = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
        "</tr>"
    concats_freem = concats_freem + mailstr1_freem
finish_sys = "</table> <br> <br> "
cursor_free_m.close()



mailstr_diskcheck = "<h3><u>LCS  HEALTH CHECK : DISK CHECK  ANALYSIS > 80 Percent </u></h3> <br>" \
                    "<table border ='1'> " \
                    "<tr align='center'> " \
                    "<th> Named </th>  <th style='color:black'> FileSystem </th>     " \
                    "<th style='color:black'> Mounted on</th> <th style='color:black'> Diks_Use_Percentage </th> " \
                    "</tr> "
cursor_disk_usgae = cnx.cursor()
cursor_disk_usgae.execute(query_disk_space)
concat_disk_check = ""
for s in cursor_disk_usgae:
    mailstr_diskusage = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>" + str(s[2]) + "</td>" + "<td>" + str(
            s[3]) + "</td>" \
        "</tr>"
    concat_disk_check = concat_disk_check + mailstr_diskusage

finish_disk_check = "</table> <br> <br> "




mailstr_systemcheck ="<h3><u>LCS  HEALTH CHECK : SYSTEM HEALTHCHECK(SERVER/DB) </u></h3> <br>" \
                    "<table border ='1'> " \
                    "<tr align='center'> " \
                    "<th> Named </th>  <th style='color:black'> Status </th>     " \
                    "</tr> "


cursor_syscheck = cnx.cursor()
cursor_syscheck.execute(query_systemcheck)
concat_syscheck = ""
for s in cursor_syscheck:
    mailstr_syscheck = \
        "<tr align=\"center\">" \
        "<td>" + str(s[0]) + "</td>" + "<td>" + str(s[1]) + "</td>" + "<td>"\
        "</tr>"
    concat_syscheck = concat_syscheck + mailstr_syscheck

finish_syscheck = "</table> <br> <br> "


finish_html = "</body></html>"

print(mailstr_freem  +  concats_freem + finish_sys + mailstr_diskcheck + concat_disk_check + finish_disk_check + mailstr_systemcheck +  concat_syscheck + finish_syscheck +   finish_html )