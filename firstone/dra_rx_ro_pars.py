import sys
import os
import re

list_rx=[]
list_ro=[]

def rx_interface(path,filename):

    with open(path+'/'+filename,'r') as fl:
        location = filename.split('_')[0]
        pdrtype = filename.split('_')[1].replace('.log','')
        for x in fl:
            if x.strip().__contains__('_rx_'):
                #print(x.strip().split(','))
                dt=x.strip().split(',')[0]
                col=x.strip().split(',')[1]
                cir=col[0:2].upper()
                if(cir == 'MB'):
                    cir='MU'
                txans3xx=x.strip().split(',')[2]
                txans4xx=x.strip().split(',')[3]
                txans5xx=x.strip().split(',')[4]
                txansloclnode=x.strip().split(',')[5]
                if txans3xx == 'n/a':
                    txans3xx =0
                if txans4xx == 'n/a':
                    txans4xx=0
                if txans5xx == 'n/a':
                    txans5xx = 0
                if txansloclnode == 'n/a':
                    txansloclnode =0
                list_rx.append("" + str(dt) + "," + str(location) + "," + str(cir) + "," + str(pdrtype) + "," + str(col) + "," + str(txans3xx) + "," + str(txans4xx) + "," + str(txans5xx) + "," + str(txansloclnode) + "\n")



def ro_interface(path,filename):

    pattern='[0-9]'
    dra_type = re.sub(pattern,'',filename.replace('.txt','')[-6:])
    if dra_type ==  'DRDRA':
        with open(path + '/' + filename, 'r') as fl:
            location = filename.split('_')[0]
            pdrtype = filename.split('_')[1].replace('.txt', '')
            for x in fl:
                if x.strip().__contains__('dri0tas')  or  x.strip().__contains__('dri1tas')  or x.strip().__contains__('Ro0') or x.strip().__contains__('btas') :
                    # print(x.strip().split(','))
                    dt = x.strip().split(',')[0]
                    col = x.strip().split(',')[1]
                    cir = col[0:2].upper()
                    if (cir == 'MB'):
                        cir = 'MU'
                    txans3xx = x.strip().split(',')[2]
                    txans4xx = x.strip().split(',')[3]
                    txans5xx = x.strip().split(',')[4]
                    txansloclnode = x.strip().split(',')[5]
                    if txans3xx == 'n/a':
                        txans3xx = 0
                    if txans4xx == 'n/a':
                        txans4xx = 0
                    if txans5xx == 'n/a':
                        txans5xx = 0
                    if txansloclnode == 'n/a':
                        txansloclnode = 0
                    list_ro.append("" + str(dt) + "," + str(location) + "," + str(cir) + "," + str(pdrtype) + "," + str(
                        col) + "," + str(txans3xx) + "," + str(txans4xx) + "," + str(txans5xx) + "," + str(
                        txansloclnode) + "\n")

    if dra_type == 'OCDRA':
        with open(path + '/' + filename, 'r') as fl:
            location = filename.split('_')[0]
            pdrtype = filename.split('_')[1].replace('.txt', '')
            for x in fl:
                if x.strip().__contains__('i0tasn')  or  x.strip().__contains__('i1tasn')  or x.strip().__contains__('ctaspmvro') or x.strip().__contains__('btas') or x.strip().__contains__('ctas') :
                    # print(x.strip().split(','))
                    dt = x.strip().split(',')[0]
                    col = x.strip().split(',')[1]
                    cir = col[0:2].upper()
                    if (cir == 'MB'):
                        cir = 'MU'
                    txans3xx = x.strip().split(',')[2]
                    txans4xx = x.strip().split(',')[3]
                    txans5xx = x.strip().split(',')[4]
                    txansloclnode = x.strip().split(',')[5]
                    if txans3xx == 'n/a':
                        txans3xx = 0
                    if txans4xx == 'n/a':
                        txans4xx = 0
                    if txans5xx == 'n/a':
                        txans5xx = 0
                    if txansloclnode == 'n/a':
                        txansloclnode = 0
                    list_ro.append("" + str(dt) + "," + str(location) + "," + str(cir) + "," + str(pdrtype) + "," + str(
                        col) + "," + str(txans3xx) + "," + str(txans4xx) + "," + str(txans5xx) + "," + str(
                        txansloclnode) + "\n")





dir_path = "C:/mylog/dra_rx_ro/20191024"
filedetail = os.listdir(dir_path)
for filename in filedetail:
    if filename.__contains__('.log') and os.stat(dir_path + '\\' + filename).st_size > 10240:
        rx_interface(dir_path,filename)

    if filename.__contains__('.txt')    and os.stat(dir_path + '\\' + filename).st_size > 10240:
        ro_interface(dir_path,filename)


with open('C:/Users/abhishek.rathor/Desktop/erics/TBL_DRA/rx.csv', 'a+') as fw:
    fw.writelines('date,location,circle,dra_node,collection,TxAnswer3xxx,TxAnswer4xxx,TxAnswer5xxx,txansloclnode\n')
    for line in list_rx:
        print(str(line).strip())
        fw.writelines(str(line).strip()+'\n' )



with open('C:/Users/abhishek.rathor/Desktop/erics/TBL_DRA/ro.csv', 'a+') as fw:
    fw.writelines('date,location,circle,dra_node,collection,TxAnswer3xxx,TxAnswer4xxx,TxAnswer5xxx,txansloclnode\n')
    for line in list_ro:
        print(str(line).strip())
        fw.writelines(str(line).strip()+'\n' )




