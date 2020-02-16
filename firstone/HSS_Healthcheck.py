import cms
import sys
import os
import time
cms_call = cms.test()



def data_ntpq_clock_sync(path,filename):
    with open(path+'\\ntpq.txt','a+') as fw:
        data_ntpq_clock_sync = cms_call.data_pars(path+'\\'+filename, 'ntpq -p', '------- Command --- End')
        for line in data_ntpq_clock_sync:
            line = ' '.join(line.split())
            if str(line).__contains__('x') or str(line).__contains__('*') or str(line).__contains__('+'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')

        del data_ntpq_clock_sync[:]
    fw.close()


def data_free_memory(path,filename):
    with open(path + '\\free_m.txt', 'a+') as fw:
        data_free_mem = cms_call.data_pars(path+'\\'+filename, 'free -m', '------- Command --- End')
        for line in data_free_mem:
            line = ' '.join(line.split())
            if str(line).__contains__('Mem'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')

        del data_free_mem[:]
    fw.close()


def data_disk_util_status(path,filename):
    with open(path + '\\df_h.txt', 'a+') as fw:
        data_disk_space = cms_call.data_pars(path+'\\'+filename, 'df -hk', '------- Command --- End')
        for line in data_disk_space:
            line = ' '.join(line.split())
            if str(line).__contains__('/'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')
        del data_disk_space[:]
    fw.close()


def disk_memory_status(path,filename):
    with open(path + '\\top.txt', 'a+') as fw:
        data_memory_status = cms_call.data_pars(path+'\\'+filename, 'top -b -n 1', '------- Command --- End')
        for line in data_memory_status:
            line = ' '.join(line.split())
            if str(line).__contains__('KiB Mem'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace('KiB Mem : ','').replace('free','').replace('used','').replace('buff/cache','').replace('+total','').strip())
                fw.writelines('\n')

        del data_memory_status[:]
    fw.close()



def data_process_usage(path,filename):
    with open(path + '\\sar.txt', 'a+') as fw:
        data_process_usage = cms_call.data_pars(path+'\\'+filename, 'sar 1 5', '------- Command --- End')
        for line in data_process_usage:
            line = ' '.join(line.split())
            if str(line).__contains__('all') and not str(line).__contains__('Average'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')
        del data_process_usage[:]
    fw.close()


def ntste_3868(path,filename):
    with open(path + '\\netstat_3868.txt', 'a+') as fw:
        data_ntste_3868 = cms_call.data_pars(path+'\\'+ filename, 'netstat -an | grep 3868', '------- Command --- End')
        for line in data_ntste_3868:
            line = ' '.join(line.split())
            if  (str(line).__contains__('sctp') or str(line).__contains__('tcp')) and  not str(line).__contains__('LISTEN'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')
        del data_ntste_3868[:]
    fw.close()


def ntste_30300(path,filename):
    with open(path + '\\netstat_30300.txt', 'a+') as fw:
        data_ntste_30300 = cms_call.data_pars(path+'\\'+ filename, 'netstat -an | grep 30300', '------- Command --- End')
        for line in data_ntste_30300:
            line = ' '.join(line.split())
            if (str(line).__contains__('sctp') or str(line).__contains__('tcp')) and  not str(line).__contains__('LISTEN'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')

        del data_ntste_30300[:]
    fw.close()



def ntste_16611(path,filename):
    with open(path + '\\netstat_16611.txt', 'a+') as fw:
        data_ntste_16611 = cms_call.data_pars(path+'\\'+filename, 'netstat -an | grep 16611', '------- Command --- End')
        for line in data_ntste_16611:
            line = ' '.join(line.split())
            if (str(line).__contains__('sctp') or str(line).__contains__('tcp')) and  not str(line).__contains__('LISTEN'):
                fw.writelines(filename.replace('.log','')+','+ str(line).replace(' ',','))
                fw.writelines('\n')

        del data_ntste_16611[:]
    fw.close()

# greet 20 percent of total free memory
# criteria shoud not be 80 percent for disk usage .
# sar idle should not be less than 90 percent .
# establishe
# free should be available  at least 20 percent
#  x and delay should not be greater than 2 .

dir_path = "C:\\mylog\\HC_Logs\\hss"
filedetail = os.listdir(dir_path)
for filename in filedetail:
    if filename.__contains__('.log') and  os.stat(dir_path+'\\'+filename).st_size > 10240:
        #print(filename +':' + str( os.stat(dir_path+'\\'+filename).st_size))
        disk_memory_status(dir_path,filename)
        data_ntpq_clock_sync(dir_path, filename)
        data_free_memory(dir_path,filename)
        data_disk_util_status(dir_path,filename)
        data_process_usage(dir_path,filename)
        ntste_3868(dir_path,filename)
        ntste_30300(dir_path,filename)
        ntste_16611(dir_path,filename)




# once log is written now times to insert into mysql and mongodb.


