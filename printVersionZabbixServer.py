#!/usr/bin/python
import configparser
import sys

from pyzabbix import ZabbixAPI

config = configparser.ConfigParser()
config.read("config.ini")

serverURL = config.get('zabbix','server')
user = config.get('zabbix','user')
password = config.get('zabbix','password')

if len(serverURL) == 0 or len(user) == 0 or len(password) == 0:
    print("failed to read file config.ini")
    sys.exit()

conn = ZabbixAPI(url = serverURL, user = user, password = password)

version = conn.api_version()

print("Zabbix Server: ", version)