from loguru import logger
import requests
from time import sleep
import config
from config import interfaceList, auth_pw, vlanID
from routerOS_api import get_interface_ip
from telegram_bot import send_TG

# 正在使用的Userid，与接口数组索引对应
used_userid = [None] * len(interfaceList)
bad_userid = []
REQUEST_TIMEOUT = 10


def Logout(userid, wlanuserip, wlanacIp, mac):
    url = "http://172.32.253.17/quickauthdisconn.do"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "http://172.32.253.17",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "referer": "http://172.32.253.17/portal/usertemp_computer/zhuhaikeji-pc/logout.html?wlanacip="
        + wlanacIp
        + "&wlanuserip="
        + wlanuserip
        + "&wlanacname=VBRAS-ZHKJ2&mac="
        + mac
        + "&version=0&msg=%E8%AE%A4%E8%AF%81%E6%88%90%E5%8A%9F&selfTicket=&macChange=false&dropLogCheck=-1&vlan=1687&groupId=2&userId="
        + userid
        + "@zk",
    }

    data = {
        "wlanacip": wlanacIp,
        "wlanuserip": wlanuserip,
        "wlanacname": "VBRAS-ZHKJ2",
        "version": "0",
        "portaltype": "",
        "userid": userid + "@zk",
        "mac": mac,
        "groupId": "2",
        "clearOperator": "0",
    }
    session = requests.Session()
    session.cookies.update(
        {
            "ABMS": "b3e6ec6d-ea56-4988-8af5-3233e1286c00",
            "JSESSIONID": "790928E53F428D769C00266EC3539A1A",
        }
    )
    try:
        req = session.post(url, headers=headers, data=data, timeout=REQUEST_TIMEOUT)
        logger.info(f"{userid}:宽带账号登出,Code:" + req.json().get("code"))
    except requests.RequestException as e:
        logger.error(f"{userid}:宽带账号登出请求失败: {e}")


def fuckServer(userid, pw, wlanuserip, wlanacIp, mac, vlanId):
    url = "http://172.32.253.17/quickauth.do"

    params = {
        "userid": userid,
        "passwd": pw,
        "wlanuserip": wlanuserip,
        "wlanacname": "VBRAS-ZHKJ2",
        "wlanacIp": wlanacIp,
        "ssid": "",
        "vlan": vlanId,
        "mac": mac,
        "version": "0",
        "portalpageid": "1",
        "timestamp": "1773585764075",
        "uuid": "82433e27-c97e-4239-951f-e4f167427fde",
        "portaltype": "0",
        "hostname": "ZCROM-PC",
        "bindCtrlId": "",
        "validateType": "0",
        "bindOperatorType": "2",
        "sendFttrNotice": "0",
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-requested-with": "XMLHttpRequest",
        "referer": "http://172.32.253.17/portal.do?wlanuserip="
        + wlanacIp
        + "&wlanacname=VBRAS-ZHKJ2&mac="
        + mac
        + "&vlan=1687&hostname=ZCROM-PC&rand=25f412481824ebe&url=http://6.6.6.6/",
    }
    session = requests.Session()
    session.cookies.update(
        {
            "ABMS": "b3e6ec6d-ea56-4988-8af5-3233e1286c00",
            "JSESSIONID": "790928E53F428D769C00266EC3539A1A",
        }
    )
    try:
        response = session.get(
            url, params=params, headers=headers, timeout=REQUEST_TIMEOUT
        )
        jsonResponse = response.json()
    except requests.RequestException as e:
        logger.error(f"{userid}:宽带账号登录请求失败: {e}")
        return False
    if jsonResponse.get("message") == "认证成功":
        logger.success(f"{userid}:宽带账号登录成功!")

        return True
    elif jsonResponse.get("message") == "PPPOE 认证失败,内网认证成功":
        logger.error(f"{userid}:宽带账号登录成功,但PPPOE认证失败!")
        Logout(userid, wlanuserip, wlanacIp, mac)
    else:
        logger.error(f"{userid}:宽带账号登录失败!\n{jsonResponse.get('message')}")
    return False


def pass_Auth(api, intreface_name, interface_Mac):
    from utils import get_new_userid

    Index = interfaceList.index(intreface_name)
    new_userid = get_new_userid()
    if not new_userid:
        logger.error("无可用宽带账号可用于重试认证")
        send_TG(f"❌接口{intreface_name} 认证失败: 无可用账号")
        return None
    wlanuserip = get_interface_ip(api, intreface_name)

    if fuckServer(
        new_userid, auth_pw, wlanuserip, config.route_ip, interface_Mac, vlanID
    ):
        # 更新已经使用的账号
        send_TG(
            f"✅接口{intreface_name} 宽带账号登录成功~\n账号:{new_userid}\nIP:{wlanuserip}"
        )
        used_userid[Index] = new_userid
        bad_userid.clear()
        return True
    # 记录无法登录的账号，避免重复尝试
    bad_userid.append(new_userid)
    return False


def network_Auth(api, intreface_name, interface_Mac):
    while True:
        result = pass_Auth(api, intreface_name, interface_Mac)
        if result is True:
            return True
        if result is None:
            return False
        sleep(0.2)
