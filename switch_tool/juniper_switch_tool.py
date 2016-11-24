#!/usr/bin/env python
import pdb
import re
from netmiko import ConnectHandler

class JuniperSwitchTool():


    def __init__(self,**kwargs):
        try:
            self.net_connect = ConnectHandler(**kwargs)
            self.ip = kwargs['ip']
        except:
            raise NetMikoTimeoutException

    ##############################################
    # search ARP table for mac based in IP address
    # return mac or None if not found
    ##############################################
    def mac_from_ip(self,ip_addr):
        cli_output = self.net_connect.send_command("sh arp no-resolve | match " + ip_addr)
        pdb.set_trace()
        if (cli_output == ''):
            print("IP Address not found " + ip_addr)
            return None
        else:
            # interate through output
            # find the line that matches IP
            for x in cli_output.splitlines():
                entry = (x.split())
                # check for 'incomplete' mac address
                if len(entry) > 2:
                    # check if IP matches, if true return MAC
                    # pdb.set_trace()
                    if entry[1] == ip_addr:
                        return entry[0]

    #############################################
    # Search mac-address table for mac address
    # return port or None if not found
    #############################################
    def port_from_mac(self,mac_addr):
        cli_output = self.net_connect.send_command("show ethernet-switching table | match " + mac_addr)
        #pdb.set_trace()
        if (cli_output == ""):
            print("MAC Address not found")
            return None
        else:
            for x in cli_output.splitlines():
                entry = x.split()
                print(entry)
                if len(entry) > 1 and entry[1] == mac_addr:
                    return entry[4]
        return None
    #############################################
    # gather information about a channel-group
    # return list of ports in group
    #############################################
    def ports_from_aggregate(self,channel_group_num):
        port_list = []
        command = 'sh lldp neighbors | match {}'.format(channel_group_num)
        output = self.net_connect.send_command(command)
         
        pdb.set_trace()
        for line in output.strip('0 \n').splitlines():
            if line.split()[0] is not None:
                port_list.append(line.split()[0])
        
        return port_list
    #######################################################
    # find CDP neighbor on port
    # function returns tuple with name,ip of CDP neighbor
    #######################################################
    def find_neighbor(self,port):
        command = 'sh lldp neighbors interface {} | match "Address |System name"'.format(port)
        output = self.net_connect.send_command(command)
        if output == "":
            return None
        else:
            name = ''
            ip_addr = ''
            for line in output.splitlines():
                pdb.set_trace()
                m1 = re.search('\s+Address\s+: (.*)', line)
                m2 = re.search('^System name\s+: (.*)', line)
                if m1 is not None:
                    ip_addr = m1.group(1)
                if m2 is not None:
                    name = m2.group(1)            
            return ((name, ip_addr))
 
    ####################################
    # run functions to find port for IP
    # returns port or None if not found
    # IP must be in switch ARP table
    ####################################
    def port_from_ip(self,ip_addr):
        mac_addr = self.mac_from_ip(ip_addr)
        pdb.set_trace()
        if mac_addr is None:
            return None
        port = self.port_from_mac(mac_addr)
        return (port)
    
    def get_switch_name(self):
        #command = 'show run | inc hostname'
        #output = self.net_connect.send_command(command)
        #pdb.set_trace()
        output = self.net_connect.find_prompt()
        pdb.set_trace()
        # prompt is 'username@devicename>', strip carot, split and return device name
        return output.strip('>').split('@')[1]
