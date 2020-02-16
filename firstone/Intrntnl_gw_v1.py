#!/bin/python
from __future__ import print_function
import os
import sys
import urllib
from pymongo import MongoClient
#from RJILLib import GetConnectionString

#event_id = long(sys.argv[1])
event_id = long(201912022055)

conStr="""mongodb://{0}:{1}@127.0.0.1:27018/jio?authMechanism=SCRAM-SHA-1""".format("rjiladmin", urllib.quote("TestServer@123"))
myclient= MongoClient(conStr)

#myclient = MongoClient("mongodb://localhost:27017/")
db = myclient.jio
col = db.lte_circ_kpi_intnl
col.remove({ "event_id" : event_id})
# connection for localhost
path="C:/mylog/sgsn_mme_thput/201912022055/"
csm_circle_map = {}
with open(path+"hosts.txt", "r") as hFile:
    for n in hFile.readlines():
        n = n.strip().split("|")
        if(n[4]=="MUM" or n[4]=="KA" ):
            csm_circle_map[n[0]] = n[5]

print(csm_circle_map)

node_circle_map = {}
circl_dict={"KA":5,"MU":16}

#sys.exit(0)

with open(path+"nodes.txt", "r") as nodesFile:
    for n in nodesFile.readlines():
        n = n.strip().split("\t")
        if(n[3]=="mu1saeX003" or n[3]=="mu1saeX004" or n[3]=="ka1saeX003"):
            circl_t = n[3][0:2].upper()
            # to check if filename and element start from different first 2 char
            if (circl_t == "PU"):
                circl_t = "PB"
            if n[0] in csm_circle_map:
                if n[1] == "sgw_pgw":
                    ty = "sgw"
                else:
                    ty = "mme"
                node_circle_map[n[3]] = {"node": n[3], "circle": circl_t, "type": ty,
                                         "csm_id": int(circl_dict[circl_t]),
                                         "version": int((n[4].split('_')[0]).replace("v", ""))}


for node in node_circle_map:
    # print(node)
    n = node_circle_map[node]

    n["intl_sgw_throughput_5min"] = long(0)
    fl = n["circle"] + "." + n["type"] + "." + str(n["csm_id"]) + ".csv"

    #print(fl)
    with open(path+fl) as f:

        for ln in f.readlines():
            ln = ln.strip().split("|")
            if ln[0] != node:
                continue

            # here collect parameter
            op = ln[1].replace("#!TOT:", "").split(":")

            if n["type"] == "sgw" and op[0] == "331":
                if(op[2]=="126" or op[2]=="3001" or op[2]=="3501"):
                    op = ln[1].split(" ")
                    print(op[8])
                    print(op[12])
                    n["intl_sgw_throughput_5min"] += (long(op[8]) + long(op[12]))/(100*1024)





    #print(n)
#print(n["intenational_sgw_throughput_v4_5min"])

#sys.exit(0)



circle_collection = {}
for i in node_circle_map:
    n = node_circle_map[i]

    if n["circle"] not in circle_collection:
        circle_collection[n["circle"]] = {}
        c = circle_collection[n["circle"]]
        c["circle"] = n["circle"]
        c["event_id"] = event_id


        c["intl_sgw_throughput_5min"] = long(0)
        c["nodes"] = []

    c = circle_collection[n["circle"]]
    c["intl_sgw_throughput_5min"] += n["intl_sgw_throughput_5min"]



    c["nodes"].append(n)

for c in circle_collection:
    print(circle_collection[c])
    col.insert(circle_collection[c])