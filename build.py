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
    ospfs = {}
    ospfv3s = {}
    interfaces = {}

    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:
            if csv_data[row]["Interface"] not in interfaces:
                interfaces[csv_data[row]["Interface"]] in config.Interface(
                        csv_data[row]["Interface"],csv_data[row])
            else:
                if csv_data[row]["dhcp-opts"] != None:
                    interfaces[csv_data[row]["Interface"]].add(
                            dhcp=csv_data[row]["dhcp-opts"])
                if csv_data[row]["dhcpv6-opts"] != None:
                    interfaces[csv_data[row]["Interface"]].add(
                            dhcpv6=csv_data[row]["dhcpv6-opts"])
            if csv_data[row]["OSPF-ID"] != None:
                if (csv_data[row]["OSPF-Area"] != None and 
                        csv_data[row]["OSPF-Area"] not in ospfs):
                    ospfs[csv_data[row]["OSPF-ID"]] = config.ospf(
                        csv_data[row]["OSPF-ID"],
                        csv_data[row]["OSPF-router-id"])
                    if csv_data[row]["OSPF-Silent"] != None:
                        ospfs[csv_data[row]["OSPF-ID"]].silent_int.append(
                                csv_data[row]["Interface"])
                if (csv_data[row]["OSPFv3-Area"] != None and 
                        csv_data[row]["OSPFv3-Area"] not in ospfv3s):
                    ospfv3s[csv_data[row]["OSPFv3-ID"]] = config.ospf(
                        csv_data[row]["OSPF-ID"],
                        csv_data[row]["OSPF-router-id"])
                    if csv_data[row]["OSPFv3-Silent"] != None:
                        ospfv3s[csv_data[row]["OSPF-ID"]].silent_int.append(
                                csv_data[row]["Interface"])

def vrfCfg(config,csv_file):
    vrfs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:
            if csv_data[l]["name"] not in vrfs:
                vrfs[csv_data[l]["name"]] = config.Vrf(csv_data[l]["name"],
                        csv_data[l]["rd"])

            if csv_data[l]["import"] != None:
                vrfs[csv_data[l]["name"]].add(imp=csv_data[l]["import"])
            if csv_data[l]["export"] != None:
                vrfs[csv_data[l]["name"]].add(exp=csv_data[l]["export"])

    for vrf in vrfs:
        vrfs[vrf].output(config)


def objCfg(config,csv_file):
    objs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:
            if csv_data[l]["name"] not in objs:
                objs[csv_data[l]["name"]] == config.Obj(csv_data[l]["name"],
                        ipv=csv_data[l]["ipv"])
            objs[csv_data[l]["name"]].add(csv_data[l]["network"],
                    csv_data[l]["type"])

    for obj in objs:
        objs[obj].output(config)

def bgpCfg(config,csv_file):
    pass

def routesCfg(config,csv_file):
    routes = []
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for l in csv_data:
            routes.append(config.Route(csv_data[l]["dest"],
                    csv_data[l]["Next-Hop"],
                    ipv=int(csv_data[l]["ipv"]),
                    weight=csv_data[l]["Weight"],
                    vrf=csv_data[l]["VRF"]))

    for route in routes:
        route.output(config)

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
                    acl4s[csv_data[row]["name"]] = config.Acl(csv_data[row]["name"])
                    acl4s[csv_data[row]["name"]].add(csv_data[row])
            elif csv_data[row]["ipv"] == '6':
                if csv_data[row]["name"] in acl6s:
                    acl6s[csv_data[row]["name"]].add(csv_data[row])
                else:
                    acl64s[csv_data[row]["name"]] = config.Acl6(csv_data[row]["name"])
                    acl6s[csv_data[row]["name"]].add(csv_data[row])
        for acl in acl4s:
            acl4s[acl].output(config)

        for acl in acl6s:
            acl6s[acl].output(config)

