#!/usr/bin/python
import configparser
import re
import sys

from pyzabbix import ZabbixAPI
from zabbixAPIClient import ZabbixAPIClient

# Check parameters
if len(sys.argv) != 4 :
    print("Usage: python3 createHost.py hostname group ip")
    sys.exit(1)

hostname=sys.argv[1]
group=sys.argv[2]
ip=sys.argv[3]

# Get zabbix client
cli = ZabbixAPIClient()

groups = cli.search_groups(group)

if len(groups) == 0:
    # Create group
    groupID = cli.create_host_group(group)
else:
    groupFound = groups[0]
    groupID = groupFound["groupid"]

cli.create_host(hostname,groupID,ip)




