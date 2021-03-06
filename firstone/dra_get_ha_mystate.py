path= 'C:/mylog/dra/healthcheck/2019-08-06.txt'
list_dra_log=[]
with open(path) as f:
    lines = f.readlines()
    for line in lines:
        list_dra_log.append(line.strip())

ra_stat_key=[]
ra_state_value=[]
total_len = len(list_dra_log)

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
    for i in range(strtloop, endloop):
        hostname = list_dra_log[strtloop + 1][len('HOSTNAME:'):len(list_dra_log[i + 1])]
        if(str(list_dra_log[i]).__contains__('DbReplication') or str(list_dra_log[i]).__contains__('pSbr status')  or
               str(list_dra_log[i]).__contains__('psbsesstion') or  str(list_dra_log[i]).__contains__('pSbrBBaseRep') or
               str(list_dra_log[i]).__contains__('pSbrBBaseRepl') or str(list_dra_log[i]).__contains__('pSbrBindingRes') or
               str(list_dra_log[i]).__contains__('PSBR_B_Proc') or str(list_dra_log[i]).__contains__('pSbrSBaseRepl') or
               str(list_dra_log[i]).__contains__('pSbrSessionRes') or str(list_dra_log[i]).__contains__('PSBR_S_Proc')):
            ra_stat_key.append(str(i)+'_'+hostname)
            ra_state_value.append(list_dra_log[i])



loop(0, 0 ,'cmd--ha.mystate--start-','cmd--ha.mystate--end-')
di = dict(zip(ra_stat_key, ra_state_value))
filex = open('C:\\mylog\\dra\\healthcheck\\dra_ha_mystat.txt','w+')
for key,value in di.items():
    print(key,value)
    filex.write(key + ' --> ' + value)
    filex.write('\n')

filex.close()