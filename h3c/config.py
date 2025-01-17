# Router Build (comware7|h3c) all configuration object classes 
import ipaddress
from io import IOBase

class Acl():
    """ Acl
    Object storage for IPv4 base ACL data
    """

    rules = {}
    name = None
    num = None

    def __init__(self,name=None,num=None):
        """ __init__(name,num)
        initalize's a new Acl object must have either name or num
        or both in order to successfully create the object
        Args
          name: Default (None): the Acl Name
          num: Default(None): the Acl Number

        Returns: None
        """
        # Set the class defaults
        self.rules = {}
        self.name = None
        self.num = None

        if (name != None and
                not isinstance(name,str)):
            raise TypeError("name must be a string")
        else:
            self.name = name

        if num != None and not isinstance(num,int):
            raise ValueError("num must be an int")
        else:
            self.num = num

        if name == None and num == None:
            raise ValueError("Either name or num nust be set") 
    
    def is_ip(self,ip,strict=False):
        try:
            temp = ipaddress.ip_address(ip)
            return True
        except:
            pass
        if not strict:
            try:
                temp = ipaddress.ip_network(ip)
                return True
            except:
                pass

    def add(self,data):
        if not isinstance(data,dict):
            raise TypeError('data must be a dict')

        try:
            rule_num = int(data['num'])
        except ValueError:
            rule_num = 0

        while True:
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

    def __str__(self):
        """ Acl.__str__()
        Generates a comware 7 based ipv4 access-list configuration section

        Returns: string of configuration
        
        Rule string format:
            rule {num} {type} {proto} ?(vpn-instance {vpn}) 
                ?(source ?object-group {src} ?{src-wild}) 
                ?(destination ?object-group {dest} ?{dest-wild} ?(eq|range) 
                ?{dest-port} ?{dest-port-end} ?{options}
        """


        # Create ACL rule header
        if self.num != None and self.name != None:
            config = "acl advanced {} name {}\n".format(self.num,self.name)
        elif self.num != None:
            config = "acl advanced {}\n".format(self.num)
        elif self.name != None:
            config = "acl advanced name {}\n".format(self.name)
        
        # Create the rules
        for ruleRow in self.rules:
            config += " rule {} {} {} ".format(ruleRow,
                    self.rules[ruleRow]['type'],
                    self.rules[ruleRow]['proto'])
            if self.rules[ruleRow]['vpn'] != "":
                config +=  "vpn-instance {} ".format(self.rules[ruleRow]['vpn'])
            if self.rules[ruleRow]['src'] != "":
                config += "source "
                if self.is_ip(self.rules[ruleRow]['src'],strict=True):
                    config +=  "{} ".format(self.rules[ruleRow]['src'])
                    if self.is_ip(self.rules[ruleRow]['src-wild'],strict=True):
                        config +=  "{} ".format(self.rules[ruleRow]['src-wild'])
                    else:
                        config += "0.0.0.0 "
                else:
                    config +=  "object-group {} ".format(self.rules[ruleRow]['src'])
            if self.rules[ruleRow]['dest'] != "":
                config += "destination "
                if self.is_ip(self.rules[ruleRow]['dest'],strict=True):
                    config +=  "{} ".format(self.rules[ruleRow]['dest'])
                    if self.is_ip(self.rules[ruleRow]['dest-wild'],strict=True):
                        config +=  "{} ".format(self.rules[ruleRow]['dest-wild'])
                    else:
                        config += "0.0.0.0 "
                else:
                    config +=  "object-group {}".format(self.rules[ruleRow]['dest'])

                if self.rules[ruleRow]['proto'] != 'ip':
                    if self.rules[ruleRow]['dest-port-end'] != "":
                        config +=  " destination-port range {} {}".format(self.rules[ruleRow]['dest-port'],
                                self.rules[ruleRow]['dest-port-end'])
                    elif self.rules[ruleRow]['dest-port'] != "":
                        config +=  " destination-port eq {}".format(self.rules[ruleRow]['dest-port'])

            if self.rules[ruleRow]['options'] != "":
                config +=  " {}".format(self.rules[ruleRow]['options'])
            
            config += "\n"
        
        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f,IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))


class Acl6(Acl):
    """ Acl6 extends Acl
    overwites the base class with support for IPv6 based access-lists
    """

    def __str__(self):

        if self.num != None and self.name != None:
            config = "acl ipv6 advanced {} name {}\n".format(self.num,self.name)
        elif self.num != None:
            config = "acl ipv6 advanced {}\n".format(self.num)
        elif self.name != None:
            config = "acl ipv6 advanced name {}\n".format(self.name)
        for ruleRow in self.rules:
            config += " rule {} {} {} ".format(ruleRow,
                    self.rules[ruleRow]['type'],
                    self.rules[ruleRow]['proto'])
            if self.rules[ruleRow]['vpn'] != "":
                config +=  "vpn-instance {} ".format(self.rules[ruleRow]['vpn'])
            if self.rules[ruleRow]['src'] != "":
                config += "source "
                if self.is_ip(self.rules[ruleRow]['src']):
                    config +=  "{} ".format(self.rules[ruleRow]['src'])
                else:
                    config +=  "object-group {} ".format(self.rules[ruleRow]['src'])
            if self.rules[ruleRow]['dest'] != "":
                config += "destination "
                if self.is_ip(self.rules[ruleRow]['dest']):
                    config +=  "{} ".format(self.rules[ruleRow]['dest'])
                else:
                    config +=  "object-group {}".format(self.rules[ruleRow]['dest'])

                if self.rules[ruleRow]['proto'] != 'ipv6':
                    if self.rules[ruleRow]['dest-port-end'] != "":
                        config +=  " destination-port range {} {}".format(self.rules[ruleRow]['dest-port'],
                                self.rules[ruleRow]['dest-port-end'])
                    elif self.rules[ruleRow]['dest-port'] != "":
                        config +=  " destination-port eq {}".format(self.rules[ruleRow]['dest-port'])

            if self.rules[ruleRow]['options'] != "":
                config +=  " {}".format(self.rules[ruleRow]['options'])
            
            config += "\n"
        
        return config
        
class Interface():
    """ Interface Config objects
    """
    
    fields = ["description","shutdown",
            "link-mode","combo","ip","mask","ipv6",
            "vrf","acl","aclv6","OPSF-ID","OSPF-Area",
            "OSPFv3-Area","vrrp-id","vrrp-ip","dhcp-mode",
            "dhcp-opts","dhcpv6-mode","dhcpv6-opts",
            "dhcp-trust","int-opts","vlan"]
    link_mode = None
    combo = None
    shutdown = False
    description = None
    vrf = None
    ip = {4:None,6:None}
    mask = None
    ospf = {}
    ospfv3 = {}
    vrrp = {}
    vlan = None
    dhcp_mode = None
    dhcp_opts = []
    dhcpv6_mode = None
    dhcpv6_opts = []
    dhcp_trust = False
    int_opts = []
    acl = {4:None,6:None}
    name = ""
    interface = ""

    def __init__(self,name,config):
        """ __init__(name,config)
        Initalize a new Interface object and build the configuration

        Arguments:
            name(string) = the Interface name
            config(dict) = Interface configuration data
        """
        self.link_mode = None
        self.combo = None
        self.shutdown = False
        self.description = None
        self.vrf = None
        self.ip = {4:None,6:None}
        self.mask = None
        self.ospf = {}
        self.ospfv3 = {}
        self.vrrp = {}
        self.vlan = None
        self.dhcp_mode = None
        self.dhcp_opts = []
        self.dhcpv6_mode = None
        self.dhcpv6_opts = []
        self.dhcp_trust = False
        self.int_opts = []
        self.acl = {4:None,6:None}
        self.name = ""
        self.interface = ""
        self.vlan = None

        int_name = ""
        ospf_pid = None
        ospf_area = None
        ospfv3_area = None
        vrrp_id = None
        vrrp_ip = None
        self.interface = name

        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        elif (len(name) <= 11 and "g" in name.lower()):
            int_name = "GigabitEthernet"
            for l in name:
                try:
                    int(l)
                    int_name += l
                except ValueError:
                    if (l == '/' or l == '.'):
                        int_name += l
        elif (len(name) <= 11 and "f" in name.lower()):
            int_name = "FastEthernet"
            for l in name:
                try:
                    int(l)
                    int_name = int_name + l
                except ValueError:
                    if (l == '/' or l == '.'):
                        int_name = int_name + 1
        elif "lo" in name.lower():
            int_name = "LoopBack"
            for l in name:
                try:
                    int(l)
                    int_name = int_name + l
                except ValueError:
                    pass
        else:
            int_name = name
        
        self.name = int_name

        if not isinstance(config,dict):
            raise TypeError("config must be a dict")
        for item in config:
            if item not in self.fields:
                pass
            if config[item] != None:
                if item == "description":
                    if config[item] != '':
                        self.description = config[item]
                elif item == "shutdown":
                    if config[item] != '':
                        self.shutdown = True
                elif item == "link-mode":
                    if config[item] != '':
                        self.link_mode = config[item]
                elif item == "combo":
                    if config[item] != '':
                        self.combo = config[item]
                elif item == "ip":
                    if config[item] != '':
                        self.ip[4] = config[item]
                elif item == "ipv6":
                    if config[item] != '':
                        self.ip[6] = config[item]
                elif item == "mask":
                    if config[item] != '':
                        self.mask = config[item]
                elif item == "OSPF-ID":
                    if config[item] != '':
                        ospf_pid = config[item]
                elif item == "OSPF-Area":
                    if config[item] != '':
                        ospf_area = config[item]
                elif item == "OSPFv3-Area":
                    if config[item] != '':
                        ospfv3_area = config[item]
                elif item == "vrrp-id":
                    if config[item] != '':
                        vrrp_id = config[item]
                elif item == "vrrp-ip":
                    if config[item] != '':
                        vrrp_ip= config[item]
                elif item == "dhcp-mode":
                    if config[item] != '':
                        self.dhcp_mode = config[item]
                elif item == "dhcp-opts":
                    if config[item] != '':
                        self.dhcp_opts.append(config[item])
                elif item == "dhcpv6-opts":
                    if config[item] != '':
                        self.dhcpv6_opts.append(config[item])
                elif item == "dhcpv6-mode":
                    if config[item] != '':
                        self.dhcpv6_mode = config[item]
                elif item == "dhcp-trust":
                    if config[item] != '':
                        self.dhcp_trust = True
                elif item == "vrf":
                    if config[item] != '':
                        self.vrf = config[item]
                elif item == "acl":
                    if config[item] != '':
                        self.acl[4] = config[item]
                elif item == "aclv6":
                    if config[item] != '':
                        self.acl[6] = config[item]
                elif item == "vlan":
                    if config[item] != '':
                        self.vlan = config[item]
        
        if ospf_pid != None and ospf_area != None:
            self.ospf[ospf_pid] = ospf_area
        if ospf_pid != None and ospfv3_area != None:
            self.ospfv3[ospf_pid] = ospfv3_area
        if vrrp_id != None and vrrp_ip != None:
            self.vrrp[vrrp_id] = vrrp_ip

    def add(self,dhcp=None,dhcpv6=None,opts=None):
        """ add(dhcp,dhcpv6,opts)
        Add aditional options to dhcp_opts, dhcpv6_opts or int_opts

        Arguments:
            dhcp (str|None): String to add to dhcp_opts
            dhcpv6 (str|None): String to add to dhcpv6_opts
            opts (str|None): String to add to int_opts

        returns: None
        """

        if (dhcp != None or dhcp != ''):
            self.dhcp_opts.append(dhcp)
        if (dhcpv6 != None or dhcpv6 != ''):
            self.dhcpv6_opts.append(dhcpv6)
        if (opts != None or opts != ''):
            self.int_opts.append(opts)

    def __str__(self):
        dhcp = None
        dhcpv6 = None 

        config = "interface {} \n".format(self.name)
        if (self.link_mode != None and (
                self.link_mode.lower() == "bridge" or
                self.link_mode.lower() == "route")):
            config += " port link-mode {}\n".format(self.link_mode.lower())
        if (self.combo != None and (
                self.combo.lower() == "copper" or
                self.combo.lower() == "fiber")):
            config += " combo enable {}\n".format(self.combo.lower())
        if self.description != None:
            config += " description \"{}\"\n".format(self.description)
        if self.vrf != None:
            config += " ip binding vpn-instance {}\n".format(self.vrf)
        if self.ip[4] != None and self.mask != None:
            config += " ip address {} {}\n".format(self.ip[4],self.mask)
        if self.ospf != {}:
            for pid in self.ospf:
                config += " ospf {} area {}\n".format(pid,self.ospf[pid])
        if self.ospfv3 != {}:
            for pid in self.ospfv3:
                config += " ospfv3 {} area {}\n".format(pid,self.ospfv3[pid])

        if self.vrrp != {}:
            for vrid in self.vrrp:
                config += " vrrp vrid {} virtual-ip {}\n".format(vrid,self.vrrp[vrid])

        if self.vlan != None:
            config += " vlan-type dot1q vid {}\n".format(self.vlan)

        if self.acl[4] != None:
            config += " packet-filter name {} inbound\n".format(self.acl[4])
        if self.acl[6] != None:
            config += " packet-filter ipv6 name {} inbound\n".format(self.acl[6])

        if (self.dhcp_mode != None and (
                self.dhcp_mode.lower() == "dhcp" or 
                self.dhcp_mode.lower() == "relay")):
            dhcp = self.dhcp_mode.lower()
            config += " dhcp select {}\n".format(dhcp)
            if self.dhcp_opts != []:
                for opt in self.dhcp_opts:
                    config += " dhcp {} {}\n".format(dhcp,opt)

        if (self.dhcpv6_mode != None and (
                self.dhcpv6_mode.lower() == "dhcp" or 
                self.dhcpv6_mode.lower() == "relay")):
            dhcpv6 = self.dhcpv6_mode.lower()
            config += " ipv6 dhcp select {}\n".format(dhcpv6)
            if self.dhcpv6_opts != []:
                for opt in self.dhcpv6_opts:
                    config += " ipv6 dhcp {} {}\n".format(dhcpv6,opt)

        if self.ip[6] != None:
            config += " ipv6 address {}\n".format(self.ip[6])
        if self.dhcp_trust:
            config += " dhcp snooping trust\n"
        if self.shutdown:
            config += " shutdown\n"
        if self.int_opts != []:
            for opt in self.int_opts:
                if opt != None:
                    config += " {}\n".format(opt)

        config += "#\n"
        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f,IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))

class Ospf():

    pid = None
    router_id = ""
    vrf = None
    silent_int = []

    def __init__(self,pid,router_id,vrf=None):
        """ __init__(pid,router_id,vrf)
        Initalizes a new Ospf config object

        Arguments:
            pid (int): the process id for the Ospf instance
            router_id (string): the router-id for the Ospf instance
            vrf (string|None): the vrf that the Ospf instance resides in

        Returns: Class object
        """
        self.pid = None
        self.router_id = ""
        self.vrf = None
        self.silent_int = []

        try:
            self.pid = int(pid)
        except ValueError:
            raise TypeError("pid must be an int")
        
        if not isinstance(router_id,str):
            raise TypeError("id must be a string")
        else:
            self.router_id = router_id

        if vrf != None:
            self.vrf = str(vrf)

    def addInterface(self,interface):
        if not isinstance(interface,str):
            raise TypeError("interface must be a string")
        else:
            self.silent_int.append(interface)


    def __str__(self):
        """ __str__()
        Returns a string object of the configuration
        """
        
        if self.vrf != None:
            config = "ospf {} router-id {} vpn-instance {}\n".format(self.pid,
                    self.router_id,
                    self.vrf)
        else:
            config = "ospf {} router-id {}\n".format(self.pid,self.router_id)

        if self.silent_int != []:
            for interface in self.silent_int:
                config = config + " silent-interface {}\n".format(interface)

        config = config + "#\n"

        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f,IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))

class Ospfv3(Ospf):
    def __str__(self):
        """ __str__()
        Returns a string object of the configuration
        """
        
        if self.vrf != None:
            config = "ospfv3 {} vpn-instance {}\n".format(self.pid,self.vrf)
        else:
            config = "ospfv3 {}\n".format(self.pid)

        config = config + " router-id {}\n".format(self.router_id)
        
        if self.silent_int != []:
            for interface in self.silent_int:
                config = config + " silent-interface {}\n".format(interface)

        config = config + "#\n"

        return config

class Vrf():
    name = ""
    rd = None
    imports = []
    exports = []
    
    def __init__(self,name,rd,auto=True):
        self.name = ""
        self.rd = None
        self.imports = []
        self.exports = []

        if not isinstance(name,str):
            raise TypeError("name must be a string")
        else:
            self.name = name

        if (not isinstance(rd,str) and rd != None):
            raise TypeError("rd must be a string")
        else:
            self.rd = rd
            if auto and rd != None:
                self.imports.append(rd)
                self.exports.append(rd)
            
    def add(self,imp=None,exp=None):
        if (imp != None and
                imp not in self.imports):
            self.imports.append(imp)
        if (exp != None and
                exp not in self.exports):
            self.exports.append(exp)

    def __str__(self):
        """ __str__()
        Returns a string object of the configuration
        """

        config = "ip vpn-instance {}\n".format(self.name)

        if self.rd != None:
            config += " route-distinguisher {}\n".format(self.rd)

            if self.imports != []:
                config += " vpn-target "
                for rd in self.imports:
                    config += "{} ".format(rd)
                config += "import-extcommunity\n"

            if self.exports != []:
                config += " vpn-target "
                for rd in self.exports:
                    config += "{} ".format(rd)
                config += "export-extcommunity\n"

        config += " #\n"
        config += " address-family ipv4\n"
        config += " #\n"
        config += " address-family ipv6\n"
        config += "#\n"

        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f,IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))

class Route():

    ipv = None
    dest = None
    mask = None
    nh = None
    weight = None
    vrf = None

    def __init__(self,dest,nh,ipv=4,weight=None,vrf=None):
        """ __init__(dest,nh,ipv,weight,vrf)
        sets up a route object

        Arguments:
            dest (string): ip address of destination including mask
            nh (string): next-hop ip address 
            ipv (int|4): IP Version
            weight (int|10): route weight
            vrf (string|None): VRF instance

        returns: Class object
        """
        self.ipv = ipv
        self.dest = dest
        self.nh = nh
        self.weight = weight
        self.vrf = vrf
         
    def __str__(self):
        """ __str__()
        Returns a string object of the configuration
        """
        if self.ipv == 4:
            config = " ip route-static "
        elif self.ipv == 6:
            config = " ipv6 route-static "

        if self.vrf != None:
            config += "vpn-instance {} ".format(self.vrf)

        config += "{} {}".format(self.dest,self.nh)
        
        if self.weight != None:
            config += " preferance {}".format(self.weight)

        config += "\n"

        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f,IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))

class Obj():
    objects = {}
    name = ""
    ipv = 4

    def __init__(self,name,ipv=4):
        self.objects = {}
        self.name = ""
        self.ipv = 4
        if not isinstance(name,str):
            raise TypeError("name must be of type str")

        self.name = name
        try:
            self.ipv = int(ipv)
        except ValueError:
            raise TypeError("ipv must be an int")

    def add(self,obj,obj_type):
        if (obj_type == "host" or obj_type == "subnet"):
            self.objects[obj] = obj_type
        else:
            raise ValueError("obj_type must be either 'host' or 'subnet'")

    def __str__(self):
        """ __str__()
        Returns a string object of the configuration
        """
        if self.objects == {}:
            return 
        config = "object-group "
        if self.ipv == 4:
            config += "ip address {}\n".format(self.name)
        elif self.ipv == 6:
            config += "ipv6 address {}\n".format(self.name)

        for obj in self.objects:
            if self.objects[obj] == 'host':
                config += " network host address {}\n".format(obj)
            elif self.objects[obj] == 'subnet':
                config += " network subnet {}\n".format(obj)

        return config

    def output(self,f):
        # Check to see if f is a IOBase otherwise raise an ValueError
        try:
            if not isinstance(f, IOBase):
                raise TypeError("argument is not a open IOBase")
        except NameError:
            raise ValueError("Missing argument")
        f.write(str(self))
