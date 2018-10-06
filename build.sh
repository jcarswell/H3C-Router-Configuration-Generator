#!/bin/python
import sys
import csv

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
        elif opt == "--obj"
            obj_csv == arg
        elif opt == "--out"
            config = arg

    with open(config, 'a+') as c:
        if int_csv != None:
            intCfg(c,int_csv)
        elif bgp_csv != None:
            bgpCfg(c,bgp_csv)
        elif vrf_csv != None:
            vrfCfg(c,crf_csv)
        elif routes_csv != none:
            routesCfg(c,routes_csv)
        elif acl_csv != None:
            aclCfg(c,acl_cfg)
        elif obj_csv != None:
            objCfg(c,acl_cfg)


