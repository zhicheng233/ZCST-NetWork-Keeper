import asyncio
from time import sleep

import routerOS_api
import network_Auth as network_auth_module
from config import (
    host,
    username,
    password,
    port,
    plaintext_login,
    use_ssl,
    ssl_verify,
    ssl_verify_hostname,
    ssl_context,
    interfaceList,
    testIP,
    sleep_time,
)
import utils
from telegram_bot import send_TG, start_bot
from network_Auth import network_Auth
from loguru import logger

from utils import read_userid, load_cache, save_cache


def interface_pool():
    while True:
        logger.info("开始检查...")
        for interface in interfaceList:
            logger.info("开始检查接口: " + interface)
            interface_check(interface)
        logger.success(f"检查完成, {sleep_time}秒后重新检查")
        sleep(sleep_time)

        save_cache(interfaceList, network_auth_module.used_userid)


def interface_check(interface_name):
    api = routerOS_api.get_api(
        host,
        username,
        password,
        port,
        plaintext_login,
        use_ssl,
        ssl_verify,
        ssl_verify_hostname,
        ssl_context,
    )
    interface_stauts = utils.isInterfaceUp(
        routerOS_api.ping_test(api, testIP, "3", interface_name)
    )
    if not interface_stauts:
        interface_mac = routerOS_api.get_interface_mac(api, interface_name)
        logger.warning(f"⚠️接口:{interface_name} 下线! Mac:{interface_mac}")
        send_TG(f"⚠️接口:{interface_name} 下线! Mac:{interface_mac}")
        network_Auth(api, interface_name, interface_mac)


if __name__ == "__main__":
    logger.add("./logs.log", rotation="10 MB", encoding="utf-8")
    start_bot()
    send_TG("已启动喵awa😋")
    read_userid()
    cache = load_cache()
    if cache != {}:
        cached_userids = [cache.get(interface_name) for interface_name in interfaceList]
        network_auth_module.used_userid[:] = cached_userids
    interface_pool()
