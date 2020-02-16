#!/bin/python
from __future__ import print_function
import os
import sys
import urllib
from pymongo import MongoClient
import mysql.connector

#from RJILLib import GetConnectionString


#event_id = long(sys.argv[1])
event_id = long(201912101425)
path="C:/mylog/sgsn_mme_thput/201912121230/"
#mongo32jio = GetConnectionString.GetConnectionString().GetServer('mongo32jio')
#conStr = "mongodb://{0}:{1}@{2}/{3}?authMechanism=SCRAM-SHA-1".format(mongo32jio["user"],mongo32jio["password"], mongo32jio["host"],mongo32jio["db"])


conStr="""mongodb://{0}:{1}@127.0.0.1:27018/jio?authMechanism=SCRAM-SHA-1""".format("rjiladmin", urllib.quote("TestServer@123"))
client = MongoClient(conStr)
db = client.jio
col = db.lte_circ_kpi_intnl
col.remove({ "event_id" : event_id})

csm_circle_map = {}
with open(path+"hosts.txt", "r") as hFile:
    for n in hFile.readlines():
        n = n.strip().split("|")
        if(n[4]=="MUM" or n[4]=="KA" ):
            csm_circle_map[n[0]] = n[5]

#print(csm_circle_map)

node_circle_map = {}
circl_dict={"KA":5,"MU":16}

#sys.exit(0)

with open(path+"nodes.txt", "r") as nodesFile:
    for n in nodesFile.readlines():
        n = n.strip().split("\t")
        if(n[3]=="mu1saeX003" or n[3]=="mu1saeX004" or n[3]=="ka1saeX003" or n[3]=="ka1saeX012"):
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
    n["intl_sgw_throughput_5min_volte"] = long(0)
    n["intl_sgw_throughput_5min_vowifi"] = long(0)
    n["intnl_sgw_session_count"] = long(0)
    n["total_sgw_exception"] = 0
    n["PCRF"] = {}
    n["OCS"] = {}

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
                #data apn
                if(op[2]=="126" or op[2]=="3001" or op[2]=="3501" ):
                    op = ln[1].split(" ")
                   
                    print(op[0].split(':')[2])
                    n["intl_sgw_throughput_5min"] += (long(op[8]) + long(op[12]))/(100*1024)
                # volte apn
                if(op[2]=="28"):
                    op = ln[1].split(" ")
                    n["intl_sgw_throughput_5min_volte"] += (long(op[8]) + long(op[12]))/(100*1024)
                # vowifi APN
                if (op[2] == "25" or op[2] == "30"):
                    op = ln[1].split(" ")
                    n["intl_sgw_throughput_5min_vowifi"] += (long(op[8]) + long(op[12]))/(100*1024)


            elif n["type"] == "sgw" and op[0] == "179":
                if op[4] not in n["PCRF"]:
                    n["PCRF"][op[4]] = 0

                n["PCRF"][op[4]] += int(op[7])

                if "0:5030:" in ln[1]:
                    n["total_sgw_exception"] += int(op[7])


            elif n["type"] == "sgw" and op[0] == "182":
                if op[4] not in n["OCS"]:
                    n["OCS"][op[4]] = 0

                n["OCS"][op[4]] += int(op[7])

                if "0:5030:" in ln[1]:
                    n["total_sgw_exception"] += int(op[7])

            elif n["type"] =="sgw" and op[0] =="800":
                if(op[2]=="126" or op[2]=="3001" or op[2]=="3501"):
                    op = ln[1].split(" ")
                    print(node+ "_800= " + op[12] )
                    n["intnl_sgw_session_count"] += long(op[12])





circle_collection = {}
for i in node_circle_map:
    n = node_circle_map[i]

    if n["circle"] not in circle_collection:
        circle_collection[n["circle"]] = {}
        c = circle_collection[n["circle"]]
        c["circle"] = n["circle"]
        c["event_id"] = event_id

        c["total_sgw_exception"] = 0
        c["intl_sgw_throughput_5min"] = long(0)
        c["intl_sgw_throughput_5min_volte"] = long(0)
        c["intl_sgw_throughput_5min_vowifi"] = long(0)
        c["intnl_sgw_session_count"] = long(0)
        c["PCRF"] = {}
        c["OCS"] = {}

        c["nodes"] = []

    c = circle_collection[n["circle"]]
    c["total_sgw_exception"] += n["total_sgw_exception"]
    c["intl_sgw_throughput_5min"] += n["intl_sgw_throughput_5min"]
    c["intl_sgw_throughput_5min_volte"]  += n["intl_sgw_throughput_5min_volte"]
    c["intl_sgw_throughput_5min_vowifi"]   += n["intl_sgw_throughput_5min_vowifi"]
    c["intnl_sgw_session_count"] +=n["intnl_sgw_session_count"]

    for k in ["PCRF", "OCS"]:
        for cc in n[k]:
            if cc not in c[k]:
                c[k][cc] = 0
            c[k][cc] += n[k][cc]

    c["nodes"].append(n)

for c in circle_collection:
    print(circle_collection[c])
    col.insert(circle_collection[c])