export USER="user123"
export PASSWORD="password123"
export URL_ZABBIX="http://myzabbix.com/api_jsonrpc.php"
export HOST="myhost"

##
# Login
##
TOKEN=$(curl -s -k -X POST -H 'Content-Type:application/json' -d'{"jsonrpc": "2.0","method":"user.login","params":{"user":"'$USER'","password":"'$PASSWORD'"},"auth": null,"id":0}' $URL_ZABBIX|jq -e -r '.result')

if [ $? -eq 1 ]
then
	echo "Login failed"
        exit 1
fi

##
# Check if host exists
##
ID=$(curl -s -k -X POST -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"host.get","params":{"output":"['hostid']","filter":{"host":"'$HOST'"}},"auth":"'$TOKEN'", "id":1}' $URL_ZABBIX|jq -e -r '.result[0].hostid')

if [ $? -eq 1 ]
then
	echo "$HOST not found"
else
	echo "$HOST ID - $ID"
fi
