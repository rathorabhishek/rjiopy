import mysql.connector
import mysql
import sys

#dt= sys.argv[1]
#print(dt)

gw_load="Select nodename, node, CPU0_load, MEM0_LOAD, CPU1_load, MEM1_LOAD from epc.tbl_gw_load_sts where cpu0_load > 40 or cpu1_load > 40 or mem0_load >80 or mem1_load >80;"

cnx = mysql.connector.connect(host='localhost', user='rjiladmin', password='TestServer@123', port='3307')
cursor_gw_load = cnx.cursor()
cursor_gw_load.execute(gw_load)

mailstr_gw_load = "<html> <body> " \
                   "<p>This is an Auto Mail</p> <br> " \
                   "<h3><u> SGW SYSTEM  HEALTH CHECK : </u>  </h3> <h4>  <br> CPU and  MEMORY Load: </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> SGW_Name </th>  <th style='color:black'> Node </th>     " \
                   "<th style='color:black'>CPU0_LOAD</th><th style='color:black'>MEM0_LOAD</th> <th style='color:black'>CPU1_LOAD</th> <th style='color:black'>MEM1_LOAD</th>" \
                   "</tr> "

concats_gw_load = " "

for tup in cursor_gw_load:
    mailstr1_gw_load = \
        "<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>"  "<td>" + str(tup[1]) + "</td>" "<td>" + str(tup[2]) + "</td>  <td>" + str(tup[3]) + "</td>  " \
        "<td>" + str(tup[4]) + "</td> <td>" + str(tup[5]) + "</td>   </tr>"
    concats_gw_load = concats_gw_load + mailstr1_gw_load
finish_gw_load = "</table> <br> <br> "
cursor_gw_load.close()

gw_avail_node = "SELECT Nodename, node, SHELF, SLOT, ACT_STS, ADM_STS, OPR_STS, SVC_STS FROM epc.tbl_gw_node_sts where OPR_sts !='ENABLE' and Act_sts != '-' AND ADM_STS !='-' AND SVC_STS !='-'  ;"
cursor_node_avail = cnx.cursor()
cursor_node_avail.execute(gw_avail_node)

concat_avail_node = " "

mailstr_avail_load = "<h4>  <br> Node Status : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> SGW_Name </th>  <th style='color:black'> Node  </th>     " \
                   "<th style='color:black'>SHELF</th> <th style='color:black'>SHELF</th> <th style='color:black'>SLOT</th><th style='color:black'>ACT_STATUS</th>" \
                     "<th style='color:black'>ADM_STATUS</th><th style='color:black'>OPR_STATUS</th><th style='color:black'>SVC_STATUS</th> " \
                   "</tr> "
for tup in cursor_node_avail:
    mailstr1_avail_load="<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>"  "<td>" + str(tup[1]) + "</td>" "<td>" + str(tup[2]) + "</td>  <td>" + str(tup[3]) + "</td>  " \
        "<td>" + str(tup[4]) + "</td> <td>" + str(tup[5]) + "</td><td>" + str(tup[6]) + "</td><td>" + str(tup[7]) + "</td>   </tr>"
    concat_avail_node=concat_avail_node + mailstr1_avail_load

finish_avail_load = "</table> <br> <br> "
cursor_node_avail.close()


pckge_info = " SELECT ems_alias FROM epc.cm_t_level3_head where type = 'sgw_pgw' and  ems_alias not like '%Rsae%' and ems_alias not in  (SELECT nodename FROM epc.tbl_gw_pckg_info); "
cursor_pckge_info = cnx.cursor()
cursor_pckge_info.execute(pckge_info)

mailstr_pckg_info = "<h4>  <br> Package Information(Absent) : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> SGW_Name </th>      " \
                    "</tr> "
concat_pckge_info=""

for tup in cursor_pckge_info:
    mailstr1_concat_pckge_info="<tr align=\"center\">" \
        "<td>" + str(tup[0]) + "</td>"  "<td>" \
        "</tr>"
    concat_pckge_info=concat_pckge_info + mailstr1_concat_pckge_info

finish_pckge_info = "</table> <br> <br> "
cursor_pckge_info.close()


port_status = " SELECT nodename, node, port, typ, act_stats, adm_status, opr_status, descr FROM epc.tbl_gw_port_sts where opr_status !='ENABLE';"
cursor_port_status = cnx.cursor()
cursor_port_status.execute(port_status)

mailstr_port_status="<h4>  <br> Port Status : </br> </h4> <br>" \
                   "<table border ='1'> " \
                   "<tr align='center'> " \
                   "<th> SGW_Name </th>  <th style='color:black'> Node  </th>     " \
                   "<th style='color:black'>Port</th> <th style='color:black'>Type</th> <th style='color:black'>Act_Status</th>" \
                     "<th style='color:black'>ADM_STATUS</th><th style='color:black'>OPR_STATUS</th><th style='color:black'>Description</th> " \
                   "</tr> "

concat_port_status =""

for tup in cursor_port_status:
    mailstr1_port_status = "<tr align=\"center\">" \
                          "<td>" + str(tup[0]) + "</td>"  "<td>" + str(tup[1]) + "</td>" "<td>" + str(tup[2]) + "</td>  <td>" + str(tup[3]) + "</td>  " \
                        "<td>" + str(tup[4]) + "</td> <td>" + str(tup[5]) + "</td><td>" + str(tup[6]) + "</td><td>" + str(tup[7]) + "</td>   </tr>"
    concat_port_status = concat_port_status + mailstr1_port_status

finish_port_status = "</table> <br> <br> "

finish_html = "</body></html>"

print(mailstr_gw_load + concats_gw_load + finish_gw_load + mailstr_avail_load +concat_avail_node + finish_avail_load+
      mailstr_pckg_info + concat_pckge_info + finish_pckge_info+ mailstr_port_status + concat_port_status+ finish_port_status+ finish_html )


