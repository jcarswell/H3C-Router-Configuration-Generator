#!/bin/python
import sys
import csv
import config

def main():
    
    int_csv = None
    bgp_csv = None
    vrf_csv = None
    routes_csv = None
    acl_csv = None
    obj_csv = None
    config = 'config.txt'

    for x in len(sys.argv + 1):
        opt = sys.argv[x].lower()
        arg = sys.argv[x+1]
        if opt == "--interface":
            int_csv = arg
        elif opt == "--bgp":
            bgp_csv = arg
        elif opt == "--vrf":
            vrf_csv = arg
        elif opt == "--routes":
            routes_csv = arg
        elif opt == "--acls":
            acl_int = arg
        elif opt == "--obj":
            obj_csv == arg
        elif opt == "--out":
            config = arg

    with open(config, 'a+') as c:
        if vrf_csv != None:
            vrfCfg(c,crf_csv)
        if obj_csv != None:
            objCfg(c,acl_cfg)
        if acl_csv != None:
            aclCfg(c,acl_cfg)
        if int_csv != None:
            intCfg(c,int_csv)
        if bgp_csv != None:
            bgpCfg(c,bgp_csv)
        if routes_csv != None:
            routesCfg(c,routes_csv)

def intCfg(config,csv_file):
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:
            pass

def vrfCfg(config,csv_file):
    pass

def objCfg(config,csv_file):
    pass

def bgpCfg(config,csv_file):
    pass

def routesCfg(config,csv_file):
    pass

def aclCfg(config,csv_file):
    acl4s = {}
    acl6s = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if csv_data[row]["ipv"] == '4':
                if csv_data[row]["name"] in acl4s:
                    acl4s[csv_data[row]["name"]].add(csv_data[row])
                else:
                    acl4s[csv_data[row]["name"]] = Acl(csv_data[row]["name"])
                    acl4s[csv_data[row]["name"]].add(csv_data[row])
            elif csv_data[row]["ipv"] == '6':
                if csv_data[row]["name"] in acl6s:
                    acl6s[csv_data[row]["name"]].add(csv_data[row])
                else:
                    acl64s[csv_data[row]["name"]] = Acl(csv_data[row]["name"])
                    acl6s[csv_data[row]["name"]].add(csv_data[row])
        for acl in acl4s:
            acl4s[acl].output(config)

        for acl in acl6s:
            acl6s[acl].output(config)

