#!/usr/bin/python
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

    for x in range(1,len(sys.argv)):
        opt = sys.argv[x].lower()
        try:
            arg = sys.argv[x+1]
        except IndexError:
            arg = None

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
            vrfCfg(c,vrf_csv)
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
            if row["Interface"] not in interfaces:
                interfaces[row["Interface"]] in config.Interface(
                        row["Interface"],row)
            else:
                if row["dhcp-opts"] != None:
                    interfaces[row["Interface"]].add(
                            dhcp=row["dhcp-opts"])
                if row["dhcpv6-opts"] != None:
                    interfaces[row["Interface"]].add(
                            dhcpv6=row["dhcpv6-opts"])
            if row["OSPF-ID"] != None:
                if (row["OSPF-Area"] != None and 
                                 row["OSPF-Area"] not in ospfs):
                    ospfs[row["OSPF-ID"]] = config.ospf(
                        row["OSPF-ID"],
                        row["OSPF-router-id"])
                    if row["OSPF-Silent"] != None:
                        ospfs[row["OSPF-ID"]].silent_int.append(
                                row["Interface"])
                if (row["OSPFv3-Area"] != None and 
                        row["OSPFv3-Area"] not in ospfv3s):
                    ospfv3s[row["OSPFv3-ID"]] = config.ospf(
                        row["OSPF-ID"],
                        row["OSPF-router-id"])
                    if row["OSPFv3-Silent"] != None:
                        ospfv3s[row["OSPF-ID"]].silent_int.append(
                                row["Interface"])

def vrfCfg(config,csv_file):
    vrfs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["name"] not in vrfs:
                vrfs[row["name"]] = config.Vrf(row["name"],
                        row["rd"])

            if row["import"] != None:
                vrfs[row["name"]].add(imp=row["import"])
            if row["export"] != None:
                vrfs[row["name"]].add(exp=row["export"])

    for vrf in vrfs:
        vrfs[vrf].output(config)


def objCfg(config,csv_file):
    objs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["name"] not in objs:
                objs[row["name"]] == config.Obj(row["name"],
                        ipv=row["ipv"])
            objs[row["name"]].add(row["network"],
                    row["type"])

    for obj in objs:
        objs[obj].output(config)

def bgpCfg(config,csv_file):
    pass

def routesCfg(config,csv_file):
    routes = []
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            routes.append(config.Route(row["dest"],
                    row["Next-Hop"],
                    ipv=int(row["ipv"]),
                    weight=row["Weight"],
                    vrf=row["VRF"]))

    for route in routes:
        route.output(config)

def aclCfg(config,csv_file):
    acl4s = {}
    acl6s = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["ipv"] == '4':
                if row["name"] in acl4s:
                    acl4s[row["name"]].add(row)
                else:
                    acl4s[row["name"]] = config.Acl(row["name"])
                    acl4s[row["name"]].add(row)
            elif row["ipv"] == '6':
                if row["name"] in acl6s:
                    acl6s[row["name"]].add(row)
                else:
                    acl64s[row["name"]] = config.Acl6(row["name"])
                    acl6s[row["name"]].add(row)
        for acl in acl4s:
            acl4s[acl].output(config)

        for acl in acl6s:
            acl6s[acl].output(config)

if __name__ == "__main__":
    main()
