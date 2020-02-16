import urllib
from pymongo import MongoClient
import datetime
from datetime import timedelta
import sys
import csv
import  ast

conStr = """mongodb://{0}:{1}@127.0.0.1:27018/jio?authMechanism=SCRAM-SHA-1""".format("rjiladmin", urllib.quote("TestServer@123"))
myclient= MongoClient(conStr)
db = myclient.jio

Current_date="201911131050"
Crntdate=datetime.datetime.strptime(Current_date, '%Y%m%d%H%M')
Cmpdate= Crntdate -timedelta(1)
long_crnt_dt=Crntdate.strftime('%Y%m%d%H%M')
long_Cmpdate= Cmpdate.strftime('%Y%m%d%H%M')
projection_crit={"event_id":1 ,"circle":1, "total_num":1 ,"total_den":1 ,"sgw_throughput_5min":1,"nodes":1,"PCRF":1,"OCS":1,"asr_w_inroamers_nom":1,"asr_w_inroamers_denom":1}

col = db.lte_cir_kpi
select_crit={'event_id':long(Current_date)}
selectCmpCrit={'event_id':long(long_Cmpdate)}
col_circle=db.lte_cir_alrm_engine
col_node = db.lte_node_alrm_engine
col_circle.remove({"event_id":long_crnt_dt})
col_node.remove({"event_id":long_crnt_dt})

data_aggre = col.find(select_crit ,projection_crit)
asr=0
thput=0
node_asr=0
node_thput=0

with open('circle.csv',mode='wb') as cirfile:
    wr = csv.writer(cirfile, delimiter=',')
    wr.writerow(['circle','event_id','asr','sgw_throughput_5min_gbps',"PCRF","OCS",'avg_sgw_throughput_5min_gbps','flag',"asr_w_inroamers_nom","asr_w_inroamers_denom"])

    with open('node.csv', mode='wb') as nodefile:
        wr_node = csv.writer(nodefile, delimiter=',')
        wr_node.writerow(['circle', 'event_id', 'node','asr','sgw_throughput_5min_gbps','PCRF','OCS','avg_sgw_throughput_5min_gbps','flag',"asr_w_inroamers_nom","asr_w_inroamers_denom"])
        for x_cur in data_aggre:
            #print(x_cur)
            try:
                asr = 100 * (float(x_cur["total_num"]) / float(x_cur["total_den"]))
            except Exception as ex:
                print(ex.message)
                asr = 0
            try:
                thput = float(x_cur["sgw_throughput_5min"] * 8) / (300 * 1024 * 1024)
            except Exception as ex:
                print(ex.message)
                thput = 0

            wr.writerow([x_cur["circle"], long(x_cur["event_id"]), asr, thput,x_cur["PCRF"],x_cur["OCS"],'','0',x_cur["asr_w_inroamers_nom"],x_cur["asr_w_inroamers_denom"]])

            for z in x_cur["nodes"]:
                if (str(z["node"]).__contains__('mme')):
                    try:
                        node_asr = 0
                        node_thput = 0
                        node_asr = 100 * (float(z["total_num"]) / float(z["total_den"]))
                    except Exception as ex:
                        print(ex.message)
                        node_asr = 0

                if (str(z["node"]).__contains__('sae') or str(z["node"]).__contains__('vfgwu') or str(
                        z["node"]).__contains__('vfgwc')):
                    try:
                        node_asr = 0
                        node_thput = 0
                        node_thput = float(z["sgw_throughput_5min"] * 8) / (300 * 1024 * 1024)
                    except Exception as ex:
                        print(ex.message)
                        node_thput = 0

                wr_node.writerow([z["circle"], long(x_cur["event_id"]),z["node"], node_asr,node_thput,z["PCRF"],z["OCS"],'','0',z["asr_w_inroamers_nom"],z["asr_w_inroamers_denom"]])


cir_csvfile= open('circle.csv','r')
node_csvfile=open('node.csv','r')
circ_read=csv.DictReader(cir_csvfile)
node_read=csv.DictReader(node_csvfile)

csv_cir_header={'circle':str,'event_id': long,'asr':float,'sgw_throughput_5min_gbps':float,'PCRF':eval,'OCS':eval,'avg_sgw_throughput_5min_gbps':str,'flag':int,"asr_w_inroamers_nom":eval,"asr_w_inroamers_denom":eval}


for line in circ_read:
    row={}
    for key,value in csv_cir_header.items():
        row[key]= value(line[key])
    col_circle.insert(row)


sys.exit(0)

csv_node_header={'circle':str,'event_id':long,'node':str,'asr':float,'sgw_throughput_5min_gbps':float,'PCRF':hash(),'OCS':hash(),'avg_sgw_throughput_5min_gbps':float,'flag':int,"asr_w_inroamers_nom":{},"asr_w_inroamers_denom":{}}
for line in node_read:
    row={}
    for column in csv_node_header:
        row[column]= line[column]
    col_node.insert(row)



def cir_avg_kpi_preparation(event_id,event_id_avg):

    cols_cir=db.lte_cir_alrm_engine
    data_cur=cols_cir.find({'event_id':event_id})
    data_prev=cols_cir.find({'event_id':event_id_avg})
    list_data_cur=list(data_cur)
    list_data_prev=list(data_prev)

    for x_cur in list_data_cur:
        for x_prev in list_data_prev:

            if(str(x_cur["circle"])== str(x_prev["circle"])):

                cur_thput=(x_cur["sgw_throughput_5min_gbps"])
                pre_avg_thput= (x_prev["avg_sgw_throughput_5min_gbps"])
                if cur_thput=="":
                    cur_thput=0.0
                if pre_avg_thput =="":
                    pre_avg_thput=0.0

                priv_day_avg=float(pre_avg_thput) - float(pre_avg_thput)*12/100
                if(cur_thput <priv_day_avg ):

                    #update last value
                    cols_cir.update({"circle": str(x_cur["circle"]),"event_id":event_id},
                                    {"$set": {"avg_sgw_throughput_5min_gbps": x_prev["avg_sgw_throughput_5min_gbps"],"flag":"1"}})

                else:

                    final_value = (float(x_cur["sgw_throughput_5min_gbps"]) + float(x_prev["avg_sgw_throughput_5min_gbps"]))/2
                    cols_cir.update({"circle": str(x_cur["circle"]), "event_id": event_id},
                                    {"$set": {"avg_sgw_throughput_5min_gbps": final_value ,"flag":"0"}})


def node_avg_kpi_preparation(event_id, event_id_avg):
    cols_node = db.lte_node_alrm_engine
    data_cur_node = cols_node.find({'event_id': event_id})
    data_pre_node = cols_node.find({'event_id': event_id_avg})
    list_data_cur_node = list(data_cur_node)
    list_data_prev_node = list(data_pre_node)

    for x_cur in list_data_cur_node:
        for x_prev in list_data_prev_node:

            if (str(x_cur["node"]) == str(x_prev["node"])):
                #print(x_cur["node"], x_cur["sgw_throughput_5min_gbps"], x_prev["sgw_throughput_5min_gbps"])
                cur_thput=0.0
                pre_avg_thput=0.0
                if x_cur["sgw_throughput_5min_gbps"]== "":
                    cur_thput=0.0
                else:
                   cur_thput = float(x_cur["sgw_throughput_5min_gbps"])

                if x_prev["avg_sgw_throughput_5min_gbps"]=="":
                    pre_avg_thput=0.0

                else:
                    pre_avg_thput=float(x_prev["avg_sgw_throughput_5min_gbps"])

                   #pre_avg_thput = float(x_prev["avg_sgw_throughput_5min_gbps"])

                priv_day_avg = pre_avg_thput - (pre_avg_thput) * 12 / 100
                if (cur_thput < priv_day_avg):

                    # update last value
                    update_formation=""

                    cols_node.update({"node": str(x_cur["node"]), "event_id": event_id},
                                    {"$set": {"avg_sgw_throughput_5min_gbps": x_prev["avg_sgw_throughput_5min_gbps"],
                                              "flag": "1"}})
                    print('you are here ')

                else:

                    final_value = (cur_thput + pre_avg_thput) / 2
                    print(final_value)
                    cols_node.update({"node": str(x_cur["node"]), "event_id": event_id},{"$set": {"avg_sgw_throughput_5min_gbps": final_value, "flag": "0"}})




cir_avg_kpi_preparation(Current_date,long_Cmpdate)
node_avg_kpi_preparation(Current_date,long_Cmpdate)
