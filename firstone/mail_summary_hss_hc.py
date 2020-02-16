import mysql.connector
import mysql
import sys

dt= sys.argv[1]

print(dt)

#hss memory status ........
hms="select gwname,total,free from epc.tbl_hss_mem_status where dt = '"+dt+"' and CAST(trim(total) AS UNSIGNED) /20 > CAST(trim(free) AS UNSIGNED)   "
print(hms)

#sys.exit(0)


cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307')
cursor_hms = cnx.cursor()
cursor_hms.execute(hms)


mailstr_hms = "<html> <body> " \
                   "<p>This is an Auto Mail</p> <br> " \
                   "<h3><u> HSS SYSTEM  HEALTH CHECK : </u>  </h3> <h4>  <br>  Memory status: </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Total Memory(KiB) </th>     " \
                   "<th style='color:black'>Free Memory(KiB)</th>" \
                   "</tr> "

concats_hms = " "

for tup in cursor_hms:
    mailstr1_hms = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td>" + "<td>" + str(tup[2]) + "</td></tr>"
    concats_hms = concats_hms + mailstr1_hms
finish_hms = "</table> <br> <br> "
cursor_hms.close()

#File system usage
fsu="select gwname,MOUNTNAME,used_blck_util from epc.tbl_hss_disk_util where dt = '"+dt+"' and cast(replace(used_blck_util,'%','') as UNSIGNED) > 80 "
cursor_fsu=cnx.cursor()
cursor_fsu.execute(fsu)
concat_fsu=""
mailstr_fsu= "<h4>  <br>  Disk Utlization > 80% : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> MountName  </th>     " \
                   "<th style='color:black'>Disk Util(%)</th>" \
                   "</tr> "

for tup in cursor_fsu:
    mailstr1_fsu = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td>" + "<td>" + str(tup[2]) + "</td></tr>"
    concat_fsu = concat_fsu + mailstr1_fsu
finish_fsu = "</table> <br> <br> "
cursor_fsu.close()


#Process Usage
pu="select gwname,per_idle from epc.tbl_hss_procss_usage where dt = '"+dt+"' and cast(per_idle as decimal) < 90"
cursor_pu=cnx.cursor()
cursor_pu.execute(pu)
concat_pu = ""
mailstr_pu = "<h4>  <br> Process Usage (IDLE % < 90) : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Idle(%) </th> </tr> "

for tup in cursor_pu:
    mailstr1_pu = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td></tr>"
    concat_pu = concat_pu + mailstr1_pu

finish_pu = "</table> <br> <br> "
cursor_pu.close()

# clock synchronization .
cs="select gwname,delay,offse1t,jitter from epc.tbl_hss_clock_synch where dt = '"+dt+"' and delay >2"
cursor_cs=cnx.cursor()
cursor_cs.execute(cs)
concat_cs = ""
mailstr_cs = "<h4>  <br> Clock Sync - NTPQ -P (Delay > 2Sec): </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Delay </th> <th style='color:black'> Offset </th> <th style='color:black'> Jitter </th></tr> "

for tup in cursor_cs:
    mailstr1_cs = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td>"  + "<td>" + str(tup[2]) + "</td>"   + "<td>" + str(tup[3]) + "</td></tr>"
    concat_cs = concat_cs + mailstr1_cs
finish_cs = "</table> <br> <br> "
cursor_cs.close()


# free memory check
fmm= "select gwname,total,free from epc.tbl_hss_free_memory where dt = '"+dt+"' and  CAST(total AS UNSIGNED) /20 > CAST(free AS UNSIGNED) "
cursor_fmm=cnx.cursor()
cursor_fmm.execute(fmm)
concat_fm=""
mailstr_fmm = "<h4>  <br> Free Memory Check - Free -m: </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Total </th> <th style='color:black'> Free </th></tr> "

for tup in cursor_fmm:
    mailstr1_fm = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td>" + "<td>" + str(tup[2]) + "</td></tr>"
    concat_fm = concat_fm + mailstr1_fm
finish_fm = "</table> <br> <br> "
cursor_fmm.close()


#diameter socket status
dss="select gwname,status1 from epc.ntstat_3868 where dt = '"+dt+"' and  status1 !='ESTABLISHED'"
cursor_dss=cnx.cursor()
cursor_dss.execute(dss)
concat_dss = ""

mailstr_dss = "<h4>  <br> Diameter Socket Status(netstat 3868) : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Status </th></tr> "


for tup in cursor_dss:
    mailstr1_dss = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td></tr>"
    concat_dss = concat_dss + mailstr1_dss

finish_dss = "</table> <br> <br> "
cursor_dss.close()


# soap trigger socket status
stss="select gwname,status1 from epc.ntstat_30300 where dt = '"+dt+"' and status1 !='ESTABLISHED' "
cursor_stss=cnx.cursor()
cursor_stss.execute(dss)
concat_stss = ""
mailstr_stss = "<h4>  <br> Soap Trigger Socket Status(netstat 30300): </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Status </th></tr> "

for tup in cursor_stss:
    mailstr1_stss = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td></tr>"
    concat_stss = concat_stss + mailstr1_stss

finish_stss = "</table> <br> <br> "
cursor_stss.close()


# LDAP connections
ldc="select gwname,status1 from epc.ntstat_16611 where dt = '"+dt+"' and status1 !='ESTABLISHED' "
cursor_ldc=cnx.cursor()
cursor_ldc.execute(dss)
concat_ldc = ""
mailstr_ldc = "<h4>  <br> LDAP connections(netstat 16611) : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> HSS </th>  <th style='color:black'> Status </th></tr> "

for tup in cursor_ldc:
    mailstr1_ldc = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>" + "<td>" + str(tup[1]) + "</td></tr>"
    concat_ldc = concat_ldc + mailstr1_ldc

finish_ldc = "</table> <br> <br> "
cursor_ldc.close()


finish_html = "</body></html>"
print(mailstr_hms + concats_hms+finish_hms+ mailstr_fsu + concat_fsu+ finish_fsu+ mailstr_pu + concat_pu + finish_pu +
       mailstr_cs + concat_cs + finish_cs + mailstr_fmm + concat_fm + finish_fm +  mailstr_dss + concat_dss + finish_dss +
       mailstr_stss + concat_stss + finish_stss + mailstr_ldc + concat_ldc + finish_ldc +  finish_html)


