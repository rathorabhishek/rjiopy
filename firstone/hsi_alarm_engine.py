import pymongo
from pymongo import MongoClient
import math


myclient = MongoClient("mongodb://localhost:27017/")
db = myclient.epc
col = db.lte_circ_kpi

eventid=201907071005
eventidl=201906251045

select_criteria={'$and':[{'event_id':eventid}]}
select_crit={'event_id':{ '$in': [201906251045,201907081950]} }

aggrecation_criteria=[{ '$match': {'$and': [{ 'event_id': eventid} ]}}, { '$group': { '_id' :'PANINDIA_'+str(eventid)+'',
                    ' total_den' : { '$sum': "$total_den" } ,
		            'total_num' : { '$sum' : "$total_num" } ,
		            'total_num_exception' : { '$sum': "$total_num_exception" } ,
		            'total_sgw_exception' : { '$sum': "$total_sgw_exception" } ,
		            'total_vlr_reg' : { '$sum': "$total_vlr_reg" } ,
		             'total_vlr_dereg' : { '$sum': "$total_vlr_dereg" } ,
		             'total_vlr' : { '$sum': "$total_vlr" } ,
		              'sgw_throughput_5min' : {'$sum': "$sgw_throughput_5min" } ,
		              'sgw_throughput_v4_5min' : { '$sum': "$sgw_throughput_v4_5min" } ,
		              'sgw_throughput_v6_5min' : { '$sum': "$sgw_throughput_v6_5min" } ,
		              'sgw_volume_5min' : { '$sum': "$sgw_volume_5min" } ,
                    'ims_apn_ipv4_util' : { '$sum': "$ims_apn_ipv4_util" } ,
                    'ims_apn_ipv4_total' : { '$sum': "$ims_apn_ipv4_total" },
                    'ims_apn_ipv6_util' : { '$sum': "$ims_apn_ipv6_util" },
                    'ims_apn_ipv6_total' : { '$sum': "$ims_apn_ipv6_total" },
		            'jionet_apn_ipv4_util' : { '$sum': "$jionet_apn_ipv4_util" },
                    'jionet_apn_ipv4_total' : { '$sum': "$jionet_apn_ipv4_total" },
                    'jionet_apn_ipv6_util' : { '$sum': "$jionet_apn_ipv6_util   " },
		            'jionet_apn_ipv6_total' : {'$sum': "$jionet_apn_ipv6_total   " },
                    'vEPC_session_est_succ_rt_nom' : { '$sum': "$vEPC_session_est_succ_rt_nom" },
                    'vEPC_session_est_succ_rt_denom' : { '$sum': "$vEPC_session_est_succ_rt_denom" },
         'vEPC_session_mo_succ_rt_nom' : { '$sum': "$vEPC_session_mo_succ_rt_nom" },
        'vEPC_session_mo_succ_rt_denom' : { '$sum': "$vEPC_session_mo_succ_rt_denom" }}}]

#data=col.find(select_crit)
data_aggre = col.aggregate(aggrecation_criteria)
# from here i can insert  eventiid
for x in data_aggre:
    print(x)
    x['event_id'] = eventid
    x['circle'] = 'PANINDIA'
    #print(type(x))
    #col.remove({'_id': 'null'})
    col.remove({'_id' : 'PANINDIA1_'+str(eventid)+''})
    col.insert(x)
