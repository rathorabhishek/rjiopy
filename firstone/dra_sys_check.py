import sys
path= 'C:\\mylog\\dra\\healthcheck\\2019-09-24.txt'
list_dra_log=[]
sys.setrecursionlimit(1500)
with open(path) as f:
    lines = f.readlines()
    for line in lines:
        list_dra_log.append(line.strip())

ra_stat_key=[]
ra_state_value=[]
#list_dra_log = sorted(list_dra_log)
total_len = len(list_dra_log)
print(total_len)

def loop(index_start , index_end,startcommand, endcommand):
    try:
        if index_start == 0 and index_end==0:
            index_start1 = list_dra_log.index(startcommand, index_start)
            index_end1 = list_dra_log.index(endcommand, index_end)

            loop_read(index_start1,index_end1)
            loop(index_start1 , index_end1,startcommand, endcommand)

        else:
            index_start1 = list_dra_log.index(startcommand, index_start + 1)
            index_end1 = list_dra_log.index(endcommand, index_end + 1)
            loop_read(index_start1, index_end1)
            loop(index_start1, index_end1,startcommand, endcommand)

    except Exception as ex:
        print(ex)

def loop_read(strtloop ,endloop):
    hostname = list_dra_log[strtloop + 1][len('HOSTNAME:'):len(list_dra_log[strtloop + 1])]
    for i in range(strtloop, endloop):
        if(list_dra_log[i]=='Running modules in class disk...' or list_dra_log[i]=='Running modules in class hardware...' or
                   list_dra_log[i] == 'Running modules in class net...' or list_dra_log[i]=='Running modules in class proc...' or
                   list_dra_log[i] == 'Running modules in class system...' or list_dra_log[i]=='Running modules in class upgrade...' ):
            values = list_dra_log[i] + list_dra_log[i + 1]

            ra_stat_key.append(str(i)+'_'+ hostname)
            ra_state_value.append(values)

loop(0, 0 ,'cmd--syscheck--start-','cmd--syscheck--end-')
filex = open('C:\\mylog\\dra\\healthcheck\\dra_syscheck.txt','w+')
di = dict(zip(ra_stat_key, ra_state_value))

for key,value in di.items():
    print(key,value)
    filex.write(key + ' --> '+ value)
    filex.write('\n')
filex.close()
