# Router Build (comware7|h3c) all configuration object classes 

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
        if (name != None and
                type(name) != string):
            raise TypeError("name must be a string")
        else
            self.name = name
        if (num != None)
                try:
                    int(num)
                except ValueError:
                    raise TypeError("num must be an int")
        else:
            self.num = int(num)
        if name == None and num == None:
            raise ValueError("Either name or num nust be set") 
    
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
        """ Acl.output(filename)
        Generates a comware 7 based ipv4 access-list configuration section
        
        Arguments:
          f = file that we are writting the config to

        Returns: None
        
        Rule string format:
            rule {num} {type} {proto} ?(vpn-instance {vpn}) 
                ?(source ?object-group {src} ?{src-wild}) 
                ?(destination ?object-group {dest} ?{dest-wild} ?(eq|range) 
                ?{dest-port} ?{dest-port-end} ?{options}
        """

        # Check to see if f is a file otherwise raise an ValueError
        try:
            if type(f) != 'file':
                raise TypeError("argument is not a open file")
        except NameError:
            raise ValueError("Missing argument")

        # Create ACL rule header
        if self.num != None and self.name != None:
            f.write("acl advanced {} name {}\n".format(self.num,self.name))
        elif self.num != None:
            f.write("acl advanced {}\n".format(self.num))
        elif self.name != None:
            f.write("acl advanced name {}\n".format(self.name))
        
        # Create the rules
        for ruleRow in self.rules:
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

        def __str__(self):
            return("IPv4 Access-list {} with {} rules".format(self.name,len(self.rules)+1))


class Acl6(Acl):
    """ Acl6 extends Acl
    overwites the base class with support for IPv6 based access-lists
    """
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

class Interface():
    """ Interface Config objects
    """
    
    link_mode = None
    combo = None
    shutdown = FALSE
    description = ""
    vrf = ""
    ip = {4:None,6:None}
    ospf = {}
    ospfv3 = {}
    vrrp = {}
    vlan = None
    dhcp_mode = None
    dhcp_opts = []
    dhcpv6_mode = None
    dhcpv6_opts = []
    ip_opts = []
    acl = {4:None 6:None}

    def __init__(self,name,config):
        """ __init___(name,config)
        Initalize a new Interface object and build the configuration

        Arguments:
            name(string) = the Interface name
            config(dict) = Interface configuration data
        """
        self.name = name
        for item in config:
            pass

    def __str__(self):
        

    def output(seld,f):
        f.write(self)

class Ospf():

    pid = None
    router_id = ""
    vrf = None
    silent_int = []

    def __init__(self,pid,router_id,vrf=None)
    """ __init__(pid,router_id,vrf)
    Initalizes a new Ospf config object

    Arguments:
        pid (int): the process id for the Ospf instance
        router_id (string): the router-id for the Ospf instance
        vrf (string|None): the vrf that the Ospf instance resides in

    Returns: Class object
    """
    try:
        self.pid = int(pid)
    except ValueError:
        raise TypeError("pid must be an int")
    
    if type(router_id) != 'string'
        raise TypeError("id must be a string")
    else
        self.router_id = router_id

    if vrf != None:
        self.vrf = str(vrf)

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

    def Output(self,f):
        f.write(self)

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
