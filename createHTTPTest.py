#!/usr/bin/python
import configparser
import re
import sys

from pyzabbix import ZabbixAPI
from zabbixAPIClient import ZabbixAPIClient

def is_group_created(hosts, group):
    hostFound = hosts[0]
    groups = hostFound['groups']
    for g in groups:
        if g['name'] == group:
            return True 
    return False

# Check parameters
if ( len(sys.argv) != 4 ):
    print("Usage: python3 createHTTPTest.py hostname group url")
    sys.exit(1)

hostname=sys.argv[1]
group=sys.argv[2]
url=sys.argv[3]

# Get zabbix client
cli = ZabbixAPIClient()

# Check if host already exist in group
hosts = cli.search_hosts(hostname)

if len(hosts) == 1 and is_group_created(hosts, group):
    hostFound = hosts[0]
    hostID = hostFound["hostid"]
else:
    # Create group
    groupID = cli.create_host_group(group)
    # Create host
    hostID = cli.create_host(hostname, groupID,status=1)
    
cli.create_http_test(hostID, url)
    




