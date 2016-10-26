#!/usr/bin/env python

import socket
import base64
from .cisco_switch_tool import *
from .credentials import username, password

device = {
    'username': base64.b64decode(username),
    'password': base64.b64decode(password),
    'ip': '',
    'device_type': 'cisco_ios',
}

# variable to hold mac once found
mac = ''

def validate_ip(s):
            a = s.split('.')
            if len(a) != 4:
                return False
            for x in a:
                if not x.isdigit():
                    return False
                i = int(x)
                if i < 0 or i > 255:
                    return False
            return True

# MOVE THIS FUNCTIONALITY TO WEB
def find_core(ip_addr):
    a = ip_addr.split('.')
    return '172.{}.0.2'.format(a[1]) 

def find_port(ip_addr):
    device['ip'] = find_core(ip_addr)
    switch_ip = device['ip']
    switch = CiscoSwitchTool(**device)
    mac = switch.mac_from_ip(ip_addr)
    if mac == None:
        return (None, None, None)
    port = switch.port_from_ip(ip_addr)
    name = switch.get_switch_name()
    while port.startswith('Po'):
        ports = switch.ports_from_etherchannel(port[2:])
        name, switch_ip = switch.find_cdp_neighbor(ports[0])
        device['ip'] = switch_ip
        switch = CiscoSwitchTool(**device)
        port = switch.port_from_mac(mac)
    if name is not 'CORE' and name is not None:
        device['ip'] = switch_ip
        switch = CiscoSwitchTool(**device)
        port = switch.port_from_mac(mac)
    return (name, switch_ip, port)

### REMOVE ME
#
#ip_add = input('Enter an IP address: ')
#
###
'''
ip_add=''
choice = ''
while choice.lower() not in ['i','n']:
    choice = input("Search by (N)ame or (I)P [n/i]: ")

    if choice.lower() == 'i':
        ip_add = input('Enter an IP address: ')
        # Looping until valid IP entered
        while (validate_ip(ip_add) ==  False):
            print(ip_add + ' is not a valid IPv4 address\n')
            ip_add = input('Enter an IP address: ')
    else:
        name = input('Enter hostname: ')
        try:
            ip_add = socket.gethostbyname(name)
        except:
            ip_add = None

if ip_add != None:
    print(find_port(ip_add))
else:
    print("Device not found")

'''
