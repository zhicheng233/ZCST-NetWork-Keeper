from loguru import logger
import requests
import config
from config import interfaceList ,auth_pw, vlanID
from routerOS_api import get_interface_ip
from telegram_bot import send_TG

#正在使用的Userid，与接口数组索引对应
used_userid = [None] * len(interfaceList)
bad_userid = []

def Logout(userid ,wlanuserip ,wlanacIp ,mac):
    url = "http://172.32.253.17/quickauthdisconn.do"
    req = requests.post(url, data={"userid": userid + "@zk", "mac": mac, "groupId": "2", "clearOperator":"0", "version": "0", "wlanacname": "VBRAS-ZHKJ1", "wlanacip": wlanacIp, "wlanuserip": wlanuserip})
    logger.info(f"{userid}:宽带账号登出,Code:" + req.json().get("code"))

def fuckServer(userid ,pw ,wlanuserip ,wlanacIp ,mac ,vlanId):
    url = "http://172.32.253.17/quickauth.do?userid="+ userid +"&passwd="+ pw +"&wlanuserip=" + wlanuserip + "&wlanacname=VBRAS-ZHKJ1&wlanacIp=" + wlanacIp + "&ssid=&vlan=" + vlanId + "&mac=" + mac + "&version=0&portalpageid=1&timestamp=1758962288328&uuid=fcc448c9-f7a4-431c-a5c7-b4db8bca8027&portaltype=0&hostname=OpenWrt&bindCtrlId=&validateType=0&bindOperatorType=2&sendFttrNotice=0"
    response = requests.get(url)
    jsonResponse = response.json()
    if jsonResponse.get("message") == "认证成功":
        logger.success(f"{userid}:宽带账号登录成功!")
        
        return True
    elif jsonResponse.get("message") == "PPPOE 认证失败,内网认证成功":
        logger.error(f"{userid}:宽带账号登录成功,但PPPOE认证失败!")
        Logout(userid ,wlanuserip ,wlanacIp ,mac)
    else:
        logger.error(f"{userid}:宽带账号登录失败!\n{jsonResponse.get('message')}")
    return False

def pass_Auth(api, intreface_name, interface_Mac):
    from utils import get_new_userid
    Index = interfaceList.index(intreface_name)
    new_userid = get_new_userid()
    wlanuserip = get_interface_ip(api, intreface_name)
    
    if fuckServer(new_userid, auth_pw, wlanuserip, config.route_ip, interface_Mac, vlanID):
        #更新已经使用的账号
        send_TG(f"✅接口{intreface_name} 宽带账号登录成功~\n账号:{new_userid}\nIP:{wlanuserip}")
        used_userid[Index] = new_userid
        bad_userid.clear()
        return True
    #记录无法登录的账号，避免重复尝试
    bad_userid.append(new_userid)
    return False
    
def network_Auth(api, intreface_name, interface_Mac):
    if not pass_Auth(api, intreface_name, interface_Mac):
        network_Auth(api, intreface_name, interface_Mac)