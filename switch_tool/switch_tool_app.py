#!/usr/bin/env python

import socket
import base64
from . import cisco_switch_tool, juniper_switch_tool
from .credentials import username, password
import pdb

device = {
    'username': base64.b64decode(username),
    'password': base64.b64decode(password),
    'ip': '',
    'device_type': 'cisco_ios',
}

# variable to hold mac once found
mac = ''

_CORES = {
    '172.17': '172.17.0.2',
    '172.18': '172.18.0.2',
    '172.19': '172.19.0.2',
    '172.20': '172.20.0.2',
    '172.21': '172.21.0.2',
    '172.22': '172.22.0.2',
}

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
    ip = a[0] + '.' + a[1]
    return _CORES[ip]

def find_port(ip_addr):
    device['ip'] = find_core(ip_addr)
    if device['ip'] == '172.20.0.2':
        device['device_type'] = 'juniper'
        return _juniper_find_port(ip_addr)
    else:
        return _cisco_find_port(ip_addr)   

def _cisco_find_port(ip_addr):
    switch_ip = device['ip']
    switch = cisco_switch_tool.CiscoSwitchTool(**device)
    mac = switch.mac_from_ip(ip_addr)
    if mac == None:
        return (None, None, None)
    port = switch.port_from_ip(ip_addr)
    name = switch.get_switch_name()
    while port.startswith('Po'):
        ports = switch.ports_from_etherchannel(port[2:])
        name, switch_ip = switch.find_cdp_neighbor(ports[0])
        device['ip'] = switch_ip
        switch = cisco_switch_tool.CiscoSwitchTool(**device)
        port = switch.port_from_mac(mac)
    if name is not 'CORE' and name is not None:
        device['ip'] = switch_ip
        switch = cisco_switch_tool.CiscoSwitchTool(**device)
        port = switch.port_from_mac(mac)
    return (name, switch_ip, port)

def _juniper_find_port(ip_addr):
    switch_ip = device['ip']
    switch = juniper_switch_tool.JuniperSwitchTool(**device)
    mac = switch.mac_from_ip(ip_addr)
    if mac == None:
        return (None, None, None)
    port = switch.port_from_ip(ip_addr)
    name = switch.get_switch_name()
    while port.startswith('Po'):
        ports = switch.ports_from_etherchannel(port[2:])
        name, switch_ip = switch.find_neighbor(ports[0])
        device['ip'] = switch_ip
        switch = juniper_switch_tool.JuniperSwitchTool(**device)
        port = switch.port_from_mac(mac)
    if name is not 'CORE' and name is not None:
        device['ip'] = switch_ip
        switch = juniper_switch_tool.JuniperSwitchTool(**device)
        port = switch.port_from_mac(mac)
    return (name, switch_ip, port)

