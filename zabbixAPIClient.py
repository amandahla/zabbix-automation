#!/usr/bin/python
import configparser
import sys

from pyzabbix import ZabbixAPI

class Singleton:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

class ZabbixAPIClient(Singleton):
    def __init__(self):
            try:
                f = open('config.ini')
                f.close()
            except IOError:
                print('[ERROR] file config.ini not found')
                sys.exit(1)

            config = configparser.ConfigParser()
            config.read("config.ini")

            serverURL = config.get('zabbix','server')
            user = config.get('zabbix','user')
            password = config.get('zabbix','password')

            if len(serverURL) == 0 or len(user) == 0 or len(password) == 0:
                print("[ERROR] failed to read config.ini")
                sys.exit(1)
            try:
                ZabbixAPIClient.__zapi = ZabbixAPI(url = serverURL, user = user, password = password)
            except:
                print("[ERROR] failed to access Zabbix {} with user {}".format(serverURL, user))
                sys.exit(1)
    
    def search_groups(self,name):
        query = {
	        'filter': { 'name': name },
            'output': [ 'groupid' ],
        }
        return self.__zapi.hostgroup.get(**query)

    def search_hosts(self,name):
        query = {
	        'filter': { 'name': name },
            'selectGroups': 'extend',
            'output': [ 'hostid' ],
        }
        return self.__zapi.host.get(**query)
    
    def create_http_test(self,hostID, url):
        try:
            self.__zapi.httptest.create(name=url,hostid=hostID,steps=[{"name": "ACCESS","url": url, "no": 1, "status_codes": "200"}])
            print("[INFO] http test {} successfully created".format(url))
        except Exception as e:
            print("[ERROR] failed to create http test {} : {}".format(url, e))
            sys.exit(1)

    def create_host_group(self, group):
        try:
            # Attention: parents groups are not automatically created.
            # "To create a nested host group, use the '/' forward slash separator, 
            # for example Europe/Latvia/Riga/Zabbix servers. 
            # You can create this group even if none of the three parent host groups (Europe/Latvia/Riga) exist. 
            # In this case creating these parent host groups is up to the user; they will not be created automatically."
            # https://www.zabbix.com/documentation/current/manual/config/hosts/host
            out = self.__zapi.hostgroup.create(name=group)
            print("[INFO] group {} successfully created".format(group))
            return out['groupids'][0]
        except Exception as e:
            print("[ERROR] failed to create group {} : {}".format(group, e))
            sys.exit(1)

    # Host status:
    # 0 - (default) monitored host
    # 1 - unmonitored host
    def create_host(self, hostname, grupoID, ip="127.0.0.1", status=0):
        try:
            out = self.__zapi.host.create(
                host=hostname,
                status=status,
                interfaces=[{
                    "type": 1,
                    "main": "1",
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": 10050
                }],
                groups=[{
                    "groupid": grupoID
                }]
            )
            print("[INFO] host {} successfully created".format(hostname))
            return out['hostids'][0]
        except Exception as e:
            print("[ERROR] failed to create host {} : {}".format(hostname, e))
            sys.exit(1)