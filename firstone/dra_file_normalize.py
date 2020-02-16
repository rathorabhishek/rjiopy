import mysql_help
import sys

class file_normaliz:
    def dra_ha_mystate(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        strbuilder = "insert into epc.tbl_dra_ha_mystat(draname,service,statu) values("
        for x in filex:
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            service = x.strip().split('-->')[1].split(' ')[1].strip()
            status= x.strip().split('-->')[1].split(' ')[2].strip()
            strbuilder = strbuilder + '\'' + dra + '\','
            strbuilder = strbuilder + '\'' + service + '\','
            strbuilder = strbuilder + '\'' + status + '\'),('
        filex.close()
        print(strbuilder[0:len(strbuilder) - 2])
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)

    def dra_sys_check(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        strbuilder = "insert into epc.tbl_dra_sys_check(draname,class,statu) values("
        for x in filex:
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            clas= x.strip().split('-->')[1].split('...')[0].strip()
            status=x.strip().split('-->')[1].split('...')[1].strip()
            print(dra +  '  ' + clas + '    '+ status)
            strbuilder = strbuilder + '\'' + dra + '\','
            strbuilder = strbuilder + '\'' + clas + '\','
            strbuilder = strbuilder + '\'' + status + '\'),('

        filex.close()
        print(strbuilder[0:len(strbuilder) - 2])
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)

    def dra_state(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        strbuilder = "insert into epc.tbl_dra_stat(draname,severity,alarmname) values("
        for x in filex:
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            almsev= x.strip().split(' ')[2].strip().replace('\'','')

            if(x.strip().split(' ')[2].strip()=='**' or x.strip().split(' ')[2].strip()=='*C'):
                almname = x.strip().split(',')[0].strip().split('-->')[1][18:len(x.strip().split(',')[0].strip().split('-->')[1])].replace('\'','')
                strbuilder = strbuilder + '\'' + dra + '\','
                strbuilder = strbuilder + '\'' + almsev + '\','
                strbuilder = strbuilder + '\'' + almname + '\'),('

        filex.close()
        print(strbuilder[0:len(strbuilder) - 2])
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)


    def disk_check(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        strbuilder = "insert into epc.tbl_dra_diskcheck(draname,mountname,disusage) values("
        for x in filex:
            if not x.__contains__('Mounted on=Use'):
                dra = x.strip().split('-->')[0].split('_')[1].strip()
                path = x.strip().split('-->')[1].split('=')[0].strip()
                usg = x.strip().split('-->')[1].split('=')[1].strip()
                strbuilder = strbuilder + '\'' + dra + '\','
                strbuilder = strbuilder + '\'' + path + '\','
                strbuilder = strbuilder + '' + usg + '),('

        filex.close()
        print(strbuilder[0:len(strbuilder) - 2])
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)



    def dra_ntpq(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        strbuilder = "insert into epc.tbl_dra_ntpq(draname,delay) values("
        for x in filex:
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            delay= x.strip().split(' ')[9].strip()
            print(dra)
            print (delay)
            #sys.exit(0)
            strbuilder = strbuilder + '\'' + dra + '\','
            strbuilder = strbuilder + '' + delay + '),('
        filex.close()
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)


    def dra_alrmmgr(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        print(filex)
        strbuilder = "insert into epc.tbl_dra_alrmmngr(draname,AlarmText) values("
        for x in filex:
            print(x)
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            delay= x.strip().split('-->')[-1].strip()
            print(dra)
            print (delay)
            #sys.exit(0)
            strbuilder = strbuilder + '\'' + dra + '\','
            strbuilder = strbuilder + '\'' + delay + '\'),('
        filex.close()
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)


    def dra_nestat(self,path,hostmysql,usrmysql,pwdmysql,dbmysql):
        filex = open(path, 'r')
        print(filex)
        strbuilder = "insert into epc.tbl_pcrf_nestat(draname,rxErr,rxDrp,txErr,txDrp) values("
        for x in filex:
            #print(x)
            dra = x.strip().split('-->')[0].split('_')[1].strip()
            rxErr= x.strip().split('-->')[-1].split('|')[0].split(':')[1]
            rxDrp = x.strip().split('-->')[-1].split('|')[1].split(':')[1]
            txErr = x.strip().split('-->')[-1].split('|')[2].split(':')[1]
            txDrp = x.strip().split('-->')[-1].split('|')[3].split(':')[1]
            print(rxErr + ':' + rxDrp + ':' + txErr + ':' + txDrp)
            strbuilder = strbuilder + '\'' + dra + '\','
            strbuilder = strbuilder + '\'' + rxErr + '\','
            strbuilder = strbuilder + '\'' + rxDrp + '\','
            strbuilder = strbuilder + '\'' + txErr + '\','
            strbuilder = strbuilder + '\'' + txDrp + '\'),('
        filex.close()
        query_final = strbuilder[0:len(strbuilder) - 2]
        mc = mysql_help.mysqlhelp()
        mc.myssqlexecutequery(hostmysql, usrmysql, pwdmysql, dbmysql, query_final)



user = 'root'
password = 'root'
host = 'localhost'
database = 'epc'
path_ntpq = "dra_ntpq.txt"
path_ra_state= "dra_ra_stat.txt"
path_dra_syscheck ="dra_syscheck.txt"
path_dra_ha_stat= "dra_ha_mystat.txt"
path_disk_check="dra_diskcheck.txt"
path_alrm_mgr ="C:\\mylog\\dra\\healthcheck\\dra_alarmgr.txt"
path_ne_stat="C:\\mylog\\pcrf_hc\\pcrf_netstat.txt"
mc_file = file_normaliz()
#mc_file.dra_ha_mystate(path_dra_ha_stat,host,user,password,database)
#mc_file.dra_sys_check(path_dra_syscheck,host,user,password,database)
#mc_file.dra_state(path_ra_state,host,user,password,database)
#mc_file.dra_ntpq(path_ntpq,host,user,password,database)
#mc_file.dra_alrmmgr(path_alrm_mgr,host,user,password,database)
mc_file.dra_nestat(path_ne_stat,host,user,password,database)
