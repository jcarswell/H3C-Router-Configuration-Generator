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

class Acl():
    rules = {}
    name = None
    num = None

    def __init__(self,name=None,num=None):
        if n == None and r == None:
            raise ValueError("Either name or num nust be set") 
        self.name = name
        self.num = num
    
    def add(self,data):
        if type(acl) != 'dict':
            raise TypeError('data must be a dict')

        try:
            rule_num = int(data['num'])
        except ValueError:
            rule_num = 0

        while true:
            if rule_num in self.rules:
                rule_num = rule_num + 5
            else:
                break
        self.rules[rule_num] = {}
        for x in data:
            if (x == 'num' or 
                x == 'name' or 
                x == 'ipv'):
                pass
            else:
                self.rules[rule_num][x] = data[x]


    def output(self,f):
        try:
            if type(f) != 'file':
                raise TypeError("argument is not a open file")
        except NameError:
            raise ValueError("Missing argument")

        if self.num != None and self.name != None:
            f.write("acl advanced {} name {}\n".format(self.num,self.name))
        elif self.num != None:
            f.write("acl advanced {}\n".format(self.num))
        elif self.name != None:
            f.write("acl advanced name {}\n".format(self.name))
        for ruleRow in self.rules:
            # rule {num} {type} {proto} ?(vpn-instance {vpn}) ?(source ?object-group {src} ?{src-wild}) ?(destination ?object-group {dest} ?{dest-wild} (eq|range) {dest-port} ?{dest-port-end} ?{options}
            rule = " rule {} {} {} ".format(ruleRow,
                    self.rules[ruleRow]['type'],
                    self.rules[ruleRow]['proto'])
            if self.rules[ruleRow]['vpn'] != None:
                rule = rule + "vpn-instance {} ".format(self.rules[ruleRow]['vpn'])
            if self.rules[ruleRow]['src'] != None:
                try:
                    if int(self.rules[ruleRow]['src'][0]):
                        rule = rule + "{} ".format(self.rules[ruleRow]['src'])
                    if self.rules[ruleRow]['src-wild'] != None:
                        rule = rule + "{} ".format(self.rules[ruleRow]['src-wild'])
                except ValueError:
                    rule = rule + "object-group {} ".format(self.rules[ruleRow]['src'])
            if self.rules[ruleRow]['dest'] != None:
                try:
                    if int(self.rules[ruleRow]['dest'][0]):
                        rule = rule + "{} ".format(self.rules[ruleRow]['dest'])
                    if self.rules[ruleRow]['dest-wild'] != None:
                        rule = rule + "{} ".format(self.rules[ruleRow]['dest-wild'])
                except ValueError:
                    rule = rule + "object-group {} ".format(self.rules[ruleRow]['dest'])

                if self.rules[ruleRow]['proto'] != 'ip':
                    if self.rules[ruleRow]['dest-port-end'] != None:
                        rule = rule + "range {} {}".format(self.rules[ruleRow]['dest-port'],
                                self.rules[ruleRow]['dest-port-end'])
                    elif self.rules[ruleRow]['dest-port'] != None:
                        rule = rule + "eq {}".format(self.rules[ruleRow]['dest-port'])

            if self.rules[ruleRow]['options'] != None:
                rule = rule + " {}".format(self.rules[ruleRow]['options'])

            f.write(rule)



class Acl6(Acl):
    def output(self,f):
        try:
            if type(f) != 'file':
                raise TypeError("argument is not a open file")
        except NameError:
            raise ValueError("Missing argument")

        if self.num != None and self.name != None:
            f.write("acl ipv6 advanced {} name {}\n".format(self.num,self.name))
        elif self.num != None:
            f.write("acl ipv6 advanced {}\n".format(self.num))
        elif self.name != None:
            f.write("acl ipv6 advanced name {}\n".format(self.name))
        for ruleRow in self.rules:
            # rule {num} {type} {proto} ?(vpn-instance {vpn}) ?(source ?object-group {src}) ?(destination ?object-group {dest} (eq|range) {dest-port} ?{dest-port-end} ?{options}
            rule = " rule {} {} {} ".format(ruleRow,
                    self.rules[ruleRow]['type'],
                    self.rules[ruleRow]['proto'])
            if self.rules[ruleRow]['vpn'] != None:
                rule = rule + "vpn-instance {} ".format(self.rules[ruleRow]['vpn'])
            if self.rules[ruleRow]['src'] != None:
                try:
                    if int(self.rules[ruleRow]['src'][0]):
                        rule = rule + "{} ".format(self.rules[ruleRow]['src'])
                    #if self.rules[ruleRow]['src-wild'] != None:
                    #    rule = rule + "{} ".format(self.rules[ruleRow]['src-wild'])
                except ValueError:
                    rule = rule + "object-group {} ".format(self.rules[ruleRow]['src'])
            if self.rules[ruleRow]['dest'] != None:
                try:
                    if int(self.rules[ruleRow]['dest'][0]):
                        rule = rule + "{} ".format(self.rules[ruleRow]['dest'])
                    #if self.rules[ruleRow]['dest-wild'] != None:
                    #    rule = rule + "{} ".format(self.rules[ruleRow]['dest-wild'])
                except ValueError:
                    rule = rule + "object-group {} ".format(self.rules[ruleRow]['dest'])

                if self.rules[ruleRow]['proto'] != 'ip':
                    if self.rules[ruleRow]['dest-port-end'] != None:
                        rule = rule + "range {} {}".format(self.rules[ruleRow]['dest-port'],
                                self.rules[ruleRow]['dest-port-end'])
                    elif self.rules[ruleRow]['dest-port'] != None:
                        rule = rule + "eq {}".format(self.rules[ruleRow]['dest-port'])

            if self.rules[ruleRow]['options'] != None:
                rule = rule + " {}".format(self.rules[ruleRow]['options'])

            f.write(rule)






