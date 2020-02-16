import os
import cms
import datetime
import sys
import logging
import math



dirpath='C:\\mylog\\gw_healthcheck\\t'
#dirpath = sys.argv[1]
logging.basicConfig(filename=dirpath+'/error.log', filemode='w',format='%(name)s - %(levelname)s - %(message)s')

from datetime import timedelta

yest = datetime.date.today() - timedelta(1)
cms_call = cms.test()

def rtrv_pkg_info(filename, sgwname):

    with open(filename.replace(sgwname + '.log', 'pckg_info.txt'), 'a+') as fw:
        try:
            data_rtrv_pckg_info = cms_call.data_pars(filename, 'RTRV-PKG-INF', ';')
            for line in data_rtrv_pckg_info:
                line = ' '.join(line.split())
                print(line)
                if str(line).__contains__(sgwname) and str(line).__contains__(str(yest.strftime('%Y%m%d053300'))):
                    fw.writelines(sgwname + ',' +  str(line).replace(' ',',') + '\n')
            del data_rtrv_pckg_info[:]
        except Exception as ex:
            logging.error(sgwname+ ':Command :RTRV-PKG-INF--->'+ ex.message)
    fw.close()

def sub_rtrv_port_status(filename, sgw_name):
    
    with open(filename.replace(sgw_name + '.log', 'Rtrv_Port_St.txt'), 'a+') as fw:
        listtt = []
        try:
            data_rtrv_port_st = cms_call.data_pars(filename, 'RTRV-PORT-STS', ';')
            for x in data_rtrv_port_st:
                if (str(x).__contains__('ENABLE') or str(x).__contains__('DISABLE')):
                    if (str(x[0:5]).strip().__contains__('LE')):
                        listtt.append(
                            str(x[0:5]).strip() + ',' + str(x[14:15]).strip() + ',' + str(x[17:19]).strip() + ',' + str(
                                x[24:30]).strip() + ',' + str(x[34:40]).strip() + ',' +
                            str(x[43:49]).strip() + ',' + str(x[43:49]).strip() + ',' + str(x[80:105]).strip())

                    if (str(x[0:1]).strip() == '1' or str(x[0:1]).strip() == '2' or str(x[0:1]).strip() == '3' or str(
                            x[0:1]).strip() == '4' or str(x[0:1]).strip() == '5'
                        or str(x[0:1]).strip() == '6' or str(x[0:1]).strip() == '7' or str(
                        x[0:1]).strip() == '8' or str(
                        x[0:1]).strip() == '9'):
                        listtt.append(
                            str(x[0:1]).strip() + ',' + str(x[3:6]).strip() + ',' + str(x[10:17]).strip() + ',' + str(
                                x[20:27]).strip() + ',' + str(x[29:36]).strip() + ',' + str(x[66:76]).strip())

            final_list = []
            stri = ""
            for i in range(0, len(listtt) - 1):
                if listtt[i][0:2] == 'LE':
                    final_list.append(listtt[i])
                    stri = listtt[i][0:5]
                if listtt[i][0:2] != 'LE':
                    final_list.append(stri + ',' + listtt[i])
            for z in final_list:
                fw.writelines(sgw_name + ',' + z + '\n')
            del data_rtrv_port_st[:]
        except Exception as ex:
            logging.error(sgw_name+ ':Command :RTRV-PORT-STS--->'+ex.message)
    fw.close()


def RTRV_NODE_STS(filename, sgwname):
    with open(filename.replace(sgwname + '.log', 'Rtrv_Node_St.txt'), 'a+') as fw:
        try:
            data_rtrv_node_st = cms_call.data_pars(filename, 'RTRV-NODE-STS', ';')
            for x in data_rtrv_node_st:
                if ((str(x).__contains__('ENABLE') or str(x).__contains__('DISABLE')) and (
                        not str(x).__contains__('TOTAL'))):
                    fw.writelines(sgwname + ',' + x[0:6] + ',' + x[15:16] + ',' + x[21:23] + ',' + x[24:32] + ',' + x[41:47] + ',' + x[50:56] + ',' + x[60:66] + '\n')
            del data_rtrv_node_st[:]
        except Exception as ex:
            logging.error(sgwname+ ':Command :RTRV-NODE-STS--->'+ex.message)

    fw.close()


def sub_rtrv_load(filename, sgwname):
    with open(filename.replace(sgwname + '.log', 'Rtrv_load_St.txt'), 'a+') as fw:
        listtt = []
        try:
            data_rtrv_load = cms_call.data_pars(filename, 'RTRV-LOAD-STS', ';')
            for x in data_rtrv_load:
                if (str(x).__contains__('AUTO')):
                    if (str(x[0:5]).strip().__contains__('LE')):
                        listtt.append(str(x[0:5]).strip() + ',' + str(x[47:58]).strip() + ',' + str(x[60:75]).strip())
                    if (str(x[0:1]).strip() == '1'):
                        listtt.append(str(x[30:35]).strip() + ',' + str(x[35:60]).strip())
            final_list = []
            for i in range(0, len(listtt) - 1):
                if listtt[i][0:2] == 'LE' and listtt[i + 1][0:2] == 'LE':
                    final_list.append(listtt[i] + ',NA,NA')
                if listtt[i + 1][0:2] != 'LE':
                    final_list.append(listtt[i] + ',' + listtt[i + 1])
            for z in final_list:
                fw.writelines(sgwname + ',' + z + '\n')

            del data_rtrv_load[:]
        except Exception as ex:
            logging.error(sgwname+ ':Command :RTRV-LOAD-STS--->'+ex.message)

    fw.close()



def rtrv_peak_kbps(filename,sgwname):
    with open(filename.replace(sgwname + '.log', 'peak_kbps.txt'),'a+') as fw:
        try:
            i = 0
            data_rtrv_peak_kbps = cms_call.data_pars(filename, 'RTRV-MEAS-PUD:ITEM=PKT,SDT=', ';')
            for line in data_rtrv_peak_kbps:
                i = i + 1
                line = ' '.join(line.split())

                if str(line).__contains__("TOTAL"):

                    line2 = data_rtrv_peak_kbps[i + 2]
                    line2 = ' '.join(line2.split())
                    tot_lag_imb = float(line2.split(' ')[3]) + float(line.split(' ')[5])
                    fw.writelines(sgwname + ',' + str(tot_lag_imb) + '\n')
                    print(tot_lag_imb)
            del data_rtrv_peak_kbps[:]
        except Exception as ex:
            logging.error(sgwname + ':Command :RTRV-MEAS-PUD:ITEM=PKT,SDT' +ex.message)
    fw.close()


def rtrv_lag_wise_thput_imbalance_4(filename,sgwname):
    with open(filename.replace(sgwname + '.log', 'thput_imbalance_sgw.txt'),'a+') as fw:
        try:
            i = 0
            data_rtrv_thput_imblance = cms_call.data_pars(filename, 'RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=1125,EDT=1125,INTV=DAY,PORT=4', ';')
            for line in data_rtrv_thput_imblance:
                i = i + 1
                line = ' '.join(line.split())
                # print(line)
                if str(line).__contains__("LENA0") or str(line).__contains__('LENA1') or str(line).__contains__('LENA2') or str(line).__contains__('LENA3'):
                    #print(line.split(' ')[5])
                    print(line)
                    line_v4_rx = data_rtrv_thput_imblance[i]
                    line_v4_rx = ' '.join(line_v4_rx.split())
                    line_v6_rx = data_rtrv_thput_imblance[i+4]
                    line_v6_rx = ' '.join(line_v6_rx.split())
                    print(line_v4_rx.split(' ')[4])
                    print(line_v6_rx.split(' ')[4])
                    tot_lag_imb =   0
                    fw.writelines(sgwname + ',4,' + str(line.split(' ')[0])+ ',' + line_v4_rx.split(' ')[4]+',' + line_v6_rx.split(' ')[4]   + '\n')
                    # print(line)
            del data_rtrv_thput_imblance[:]
        except Exception as ex:
            logging.error(sgwname + ':Command :RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=' +ex.message)
    fw.close()


def rtrv_lag_wise_thput_imbalance_5(filename,sgwname):
    with open(filename.replace(sgwname + '.log', 'thput_imbalance_sgw.txt'),'a+') as fw:
        try:
            i = 0
            data_rtrv_thput_imblance = cms_call.data_pars(filename, 'RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=1125,EDT=1125,INTV=DAY,PORT=5', ';')
            for line in data_rtrv_thput_imblance:
                i = i + 1
                line = ' '.join(line.split())
                # print(line)
                if str(line).__contains__("LENA0") or str(line).__contains__('LENA1') or str(line).__contains__('LENA2') or str(line).__contains__('LENA3'):
                    #print(line.split(' ')[5])
                    print(line)
                    line_v4_rx = data_rtrv_thput_imblance[i]
                    line_v4_rx = ' '.join(line_v4_rx.split())
                    line_v6_rx = data_rtrv_thput_imblance[i+4]
                    line_v6_rx = ' '.join(line_v6_rx.split())
                    print(line_v4_rx.split(' ')[4])
                    print(line_v6_rx.split(' ')[4])
                    tot_lag_imb =   0
                    fw.writelines(sgwname + ',5,' + str(line.split(' ')[0])+ ',' + line_v4_rx.split(' ')[4]+',' + line_v6_rx.split(' ')[4]   + '\n')
                    # print(line)
            del data_rtrv_thput_imblance[:]
        except Exception as ex:
            logging.error(sgwname + ':Command :RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=' +ex.message)
    fw.close()


def rtrv_lag_wise_thput_imbalance_6(filename,sgwname):
    with open(filename.replace(sgwname + '.log', 'thput_imbalance_sgw.txt'),'a+') as fw:
        try:
            i = 0
            data_rtrv_thput_imblance = cms_call.data_pars(filename, 'RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=1125,EDT=1125,INTV=DAY,PORT=6', ';')
            for line in data_rtrv_thput_imblance:
                i = i + 1
                line = ' '.join(line.split())
                # print(line)
                if str(line).__contains__("LENA0") or str(line).__contains__('LENA1') or str(line).__contains__('LENA2') or str(line).__contains__('LENA3'):
                    #print(line.split(' ')[5])
                    print(line)
                    line_v4_rx = data_rtrv_thput_imblance[i]
                    line_v4_rx = ' '.join(line_v4_rx.split())
                    line_v6_rx = data_rtrv_thput_imblance[i+4]
                    line_v6_rx = ' '.join(line_v6_rx.split())
                    print(line_v4_rx.split(' ')[4])
                    print(line_v6_rx.split(' ')[4])
                    tot_lag_imb =   0
                    fw.writelines(sgwname + ',6,' + str(line.split(' ')[0])+ ',' + line_v4_rx.split(' ')[4]+',' + line_v6_rx.split(' ')[4]   + '\n')
                    # print(line)
            del data_rtrv_thput_imblance[:]
        except Exception as ex:
            logging.error(sgwname + ':Command :RTRV-MEAS-PPORT:ITEM=PKT,TYPE=DETAIL,SDT=' +ex.message)
    fw.close()

dir = os.listdir(dirpath)
for file in dir:
    if ((not file.__contains__('mme')) and (not os.stat(dirpath + '/' + file).st_size == 0) and file.__contains__(
            '.log') and (not file.__contains__('vfgwu'))  and (not file.__contains__('vfigu')) and (not file.__contains__('Rsae'))  ):
        # print(dirpath + '/' + file)
        #rtrv_pkg_info(dirpath + '/' + file, file.replace('.log', ''))
        #rtrv_peak_kbps(dirpath + '\\' + file, file.replace('.log', ''))
        rtrv_lag_wise_thput_imbalance_4(dirpath + '\\' + file, file.replace('.log', ''))
        rtrv_lag_wise_thput_imbalance_5(dirpath + '\\' + file, file.replace('.log', ''))
        rtrv_lag_wise_thput_imbalance_6(dirpath + '\\' + file, file.replace('.log', ''))
        #sub_rtrv_port_status(dirpath + '/' + file, file.replace('.log', ''))
        #RTRV_NODE_STS(dirpath + '/' + file, file.replace('.log', ''))
        #sub_rtrv_load(dirpath + '/' + file, file.replace('.log', ''))