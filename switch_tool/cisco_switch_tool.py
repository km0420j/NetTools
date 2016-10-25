#!/usr/bin/env python
import pdb
import re
from netmiko import ConnectHandler

class CiscoSwitchTool():


    def __init__(self,**kwargs):
        self.net_connect = ConnectHandler(**kwargs)
        self.ip = kwargs['ip']
    

    ##############################################
    # search ARP table for mac based in IP address
    # return mac or None if not found
    ##############################################
    def mac_from_ip(self,ip_addr):
        cli_output = self.net_connect.send_command("sh arp | inc " + ip_addr)
        if (cli_output == ''):
            print("IP Address not found " + ip_addr)
            return None
        else:
            # interate through output
            # find the line that matches IP
            for x in cli_output.splitlines():
                entry = (x.split())
                # check for 'incomplete' mac address
                
                # check if IP matches, if true return MAC
                if entry[1] == ip_addr:
                    # check for 'incomplete' mac address
                    if entry[3] == 'Incomplete':
                        return None
                    else:
                        return entry[3]

    #############################################
    # Search mac-address table for mac address
    # return port or None if not found
    #############################################
    def port_from_mac(self,mac_addr):
        cli_output = self.net_connect.send_command("sh mac add | inc " + mac_addr)
        if (cli_output == ""):
            print("MAC Address not found")
            return None
        else:
            for x in cli_output.splitlines():
                entry = x.split()
                print(entry)
                return entry[3]
    #############################################
    # gather information about a channel-group
    # return list of ports in group
    #############################################
    def ports_from_etherchannel(self,channel_group_num):
        port_list = []
        command = 'sh etherchannel {} detail'.format(channel_group_num)
        output = self.net_connect.send_command(command)
        for line in output.splitlines():
            m = re.search('^Port: (.*)', line)
            if m is not None:
                port_list.append(m.group(1))
        
        return port_list
    #######################################################
    # find CDP neighbor on port
    # function returns tuple with name,ip of CDP neighbor
    #######################################################
    def find_cdp_neighbor(self,port):
        command = 'sh cdp neighbors {} detail'.format(port)
        output = self.net_connect.send_command(command)
        if output == "":
            return None
        else:
            name = ''
            ip_addr = ''
            for line in output.splitlines():
                m1 = re.search('^Device ID: (.*)', line)
                m2 = re.search('^  IP address: (.*)', line)
                if m1 is not None:
                    name = m1.group(1)
                elif m2 is not None:
                    ip_addr = m2.group(1)
            
            return ((name, ip_addr))
 
    ####################################
    # run functions to find port for IP
    # returns port or None if not found
    # IP must be in switch ARP table
    ####################################
    def port_from_ip(self,ip_addr):
        mac_addr = self.mac_from_ip(ip_addr)
        if mac_addr is None:
            return None
        port = self.port_from_mac(mac_addr)
        return (port)

    ####################################
    # return the hostname of device
    ####################################
    def get_switch_name(self):
        command = 'sh run | inc hostname'
        output = self.net_connect.send_command(command)
        return output.strip('hostname ')

