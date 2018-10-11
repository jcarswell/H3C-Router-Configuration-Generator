#!/usr/bin/python3
import sys
import csv
from io import IOBase
import h3c.config

def main():
    
    int_csv = None
    bgp_csv = None
    vrf_csv = None
    routes_csv = None
    acl_csv = None
    obj_csv = None
    config = 'config.txt'

    if len(sys.argv) == 1:
        c7_build_help()
    for x in range(1,len(sys.argv)):
        opt = sys.argv[x].lower()
        try:
            arg = sys.argv[x+1]
        except IndexError:
            arg = None

        if opt == "--int":
            int_csv = arg
        elif opt == "--bgp":
            bgp_csv = arg
        elif opt == "--vrf":
            vrf_csv = arg
        elif opt == "--route":
            routes_csv = arg
        elif opt == "--acl":
            acl_csv = arg
        elif opt == "--obj":
            obj_csv = arg
        elif opt == "--out":
            config = arg
        elif opt == "--help" or opt == "-h":
            c7_build_help()
        elif opt[:2] == "--":
            print("Unkown option: {} - Ignoring".format(opt))

    with open(config, 'a+') as c:
        if vrf_csv != None:
            print("Reading VRFs: {}".format(vrf_csv))
            vrfCfg(c,vrf_csv)
        if obj_csv != None:
            print("Reading Objects: {}".format(obj_csv))
            objCfg(c,obj_csv)
        if acl_csv != None:
            print("Reading ACLs: {}".format(acl_csv))
            aclCfg(c,acl_csv)
        if int_csv != None:
            print("Reading Interfaces: {}".format(int_csv))
            intCfg(c,int_csv)
        if bgp_csv != None:
            print("Reading BGP: {}".format(bgp_csv))
            bgpCfg(c,bgp_csv)
        if routes_csv != None:
            print("Reading Routes: {}".format(routes_csv))
            routesCfg(c,routes_csv)

def intCfg(config,csv_file):
    ospfs = {}
    ospfv3s = {}
    interfaces = [{},{},{}]

    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            int_group = 0
            if "lo" in row["Interface"]:
                int_group = 0
            elif ("/" in row["Interface"] and "." not in row["Interface"]):
                int_group = 1
            else:
                int_group = 2

            if row["Interface"] not in interfaces[int_group]:
                interfaces[int_group][row["Interface"]] = h3c.config.Interface(row["Interface"],row)
            else:
                if row["dhcp-opts"] != "":
                    interfaces[int_group][row["Interface"]].add(
                            dhcp=row["dhcp-opts"])
                if row["dhcpv6-opts"] != "":
                    interfaces[int_group][row["Interface"]].add(
                            dhcpv6=row["dhcpv6-opts"])
            if row["OSPF-ID"] != "":
                if (row["OSPF-Area"] != "" and 
                        row["OSPF-Area"] not in ospfs):
                    ospfs[row["OSPF-ID"]] = h3c.config.Ospf(
                        row["OSPF-ID"],
                        row["OSPF-router-id"],
                        row["vrf"])
                    if row["OSPF-Silent"] != "":
                        ospfs[row["OSPF-ID"]].silent_int.append(
                                row["Interface"])
                if (row["OSPFv3-Area"] != "" and 
                        row["OSPFv3-Area"] not in ospfv3s):
                    ospfv3s[row["OSPF-ID"]] = h3c.config.Ospfv3(
                        row["OSPF-ID"],
                        row["OSPF-router-id"],
                        row["vrf"])
                    if row["OSPFv3-Silent"] != "":
                        ospfv3s[row["OSPF-ID"]].silent_int.append(
                                row["Interface"])

    for int_group in range(len(interfaces)):
        for interface in interfaces[int_group]:
            interfaces[int_group][interface].output(config)
            
    for ospf in ospfs:
        ospfs[ospf].output(config)
    for ospg in ospfv3s:
        ospfv3s[ospf].output(config)

def vrfCfg(config,csv_file):
    vrfs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["name"] not in vrfs:
                vrfs[row["name"]] = h3c.config.Vrf(row["name"],
                        row["rd"],auto=False)

            if row["import"] != "":
                vrfs[row["name"]].add(imp=row["import"])
            if row["export"] != "":
                vrfs[row["name"]].add(exp=row["export"])

    for vrf in vrfs:
        vrfs[vrf].output(config)


def objCfg(config,csv_file):
    objs = {}
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["name"] not in objs:
                objs[row["name"]] = h3c.config.Obj(row["name"],ipv=row["ipv"])
            objs[row["name"]].add(row["network"],
                    row["type"].lower())

    for obj in objs:
        objs[obj].output(config)

def bgpCfg(config,csv_file):
    pass

def routesCfg(config,csv_file):
    routes = []
    with open(csv_file) as data:
        csv_data = csv.DictReader(data)
        for row in csv_data:
            if row["VRF"] == "":
                vrf=None
            else:
                vrf = row["VRF"]
            if row["Weight"] == "":
                weight=None
            else:
                weight = row["Weight"]

            routes.append(config.Route(row["dest"],
                    row["Next-Hop"],
                    ipv=int(row["ipv"]),
                    weight=weight,
                    vrf=vrf))

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
                    acl4s[row["name"]] = h3c.config.Acl(row["name"])
                    acl4s[row["name"]].add(row)
            elif row["ipv"] == '6':
                if row["name"] in acl6s:
                    acl6s[row["name"]].add(row)
                else:
                    acl6s[row["name"]] = h3c.config.Acl6(row["name"])
                    acl6s[row["name"]].add(row)
    for acl in acl4s:
        acl4s[acl].output(config)

    for acl in acl6s:
        acl6s[acl].output(config)

def c7_build_help():
    print("H3C Config Builder")
    print("\nValid Options:")
    print("\n  --int [csv file]: interfaces")
    print("  --vrf [csv file]: vrfs")
    print("  --route [csv file]: routes")
    print("  --acl [csv file]: ACLs")
    print("  --obj [csv file]: Objects")
    print("  --out [config]: config file destination")
    print("        defaults to \"config.txt\"")
    print("")

if __name__ == "__main__":
    main()
