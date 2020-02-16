import cms
import sys
import os
import datetime
from datetime import timedelta


yest = datetime.date.today() - timedelta(1)
cms_call = cms.test()

def data_disk_util_status(path,filename):
    with open(path + '\\df_h.txt', 'a+') as fw:
        data_disk_space = cms_call.data_pars(path+'\\'+filename, '--df -h start', '--df -h end')
        for line in data_disk_space:
            print(line)
            line = ' '.join(line.split())
            if str(line).__contains__('/'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')
        del data_disk_space[:]
    fw.close()


def data_free_memory(path,filename):
    with open(path + '\\free_m.txt', 'a+') as fw:
        data_free_mem = cms_call.data_pars(path+'\\'+filename, '--free -m start', '--free -m end')
        for line in data_free_mem:
            line = ' '.join(line.split())
            if str(line).__contains__('Mem'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')

        del data_free_mem[:]
    fw.close()


def system_status(path,filename):
    with open(path + '\\ss.txt', 'a+') as fw:
        try:
            data_ss = cms_call.data_pars(path + '\\' + filename, '--sysstatus start', '--- Alarms:')
            for line in data_ss:
                stringbuilder = ''
                line = ' '.join(line.split())
                lcsname=""
                #if str(line).__contains__('@'):
                #    lcsname= str(line).split('@')[1]
                #    print(lcsname)
                #    stringbuilder =  stringbuilder + lcsname
                if str(line).__contains__('Status') or str(line).__contains__('status'):
                    fw.writelines(filename.replace('.log', '') + ',' + str(line).replace('','').replace('[1;32m','').replace('[0m','').replace('[0m',''))
                    fw.writelines('\n')
            del data_ss[:]
        except Exception as ex:
            print(ex)


    fw.close()




dir_path = "C:\\mylog\\lcs_hc\\2019-11-20"
filedetail = os.listdir(dir_path)
for filename in filedetail:
    if filename.__contains__('.log') and  os.stat(dir_path+'\\'+filename).st_size > 102:
        print(filename +':' + str( os.stat(dir_path+'\\'+filename).st_size))
        data_disk_util_status(dir_path,filename)
        data_free_memory(dir_path, filename)
        system_status(dir_path,filename)
