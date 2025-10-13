#RouterOS登录参数
username = "admin"
password = ""
host = "192.168.1.1"
port = 8728
plaintext_login = True  #7.0+
use_ssl = False
ssl_verify = False
ssl_verify_hostname = False
ssl_context = None

#接口列表，根据实际情况修改接口名
interfaceList = ["macvlan1","macvlan2","macvlan3","macvlan4","macvlan5","macvlan6","macvlan7","macvlan8","macvlan9","macvlan10","macvlan11","macvlan12"]

#发包设置
vlanID = 1586  #VLAN ID,根据实际情况修改
auth_pw = "112233"
route_ip = "172.32.253.1"   #网关
testIP = "8.8.8.8"  #测试IP
sleep_time = 60

#Telegram Bot推送设置
TG_Enable = False
TG_TOKEN = "botXXX:XXX"
TG_Bot_name = "⚡珠科宽带"
chat_id = 1234567890
TG_api_url = "https://api.telegram.org/"