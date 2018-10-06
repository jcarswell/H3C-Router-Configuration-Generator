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

def intCfg(config,csvFile):
    with open(csvFile) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:

class Acl():
    rules = {}
    name = None
    acl_num = None

    def __init__(self,n,r=None):
        self.name = n
        self.acl_num = r
    
    def add(self,data):
        if type(acl) != 'dict':
            raise TypeError('data must be a dict')

        try:
            rule_num = int(data['num'])
        else:
            rule_num = 0
        except ValueError:
            rule_num = 0

        while true:
            if rule_num in self.rules:
                rule_num = rule_num + 5
            else:
                break
        self.rules[rule_num] = {}
        for x in data:
            if x == 'num' or 
                x == 'name' or 
                x == 'ipv':
                pass
            else:
                self.rules[rule_num] = {x:data[x]}


    def output(self,f):
        pass

class Acl6(Acl):
    def output(self,f):
        pass





