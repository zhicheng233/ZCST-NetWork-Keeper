import random

from loguru import logger

from network_Auth import used_userid, bad_userid

useridList = []
def isInterfaceUp(pingResult):
    if int(pingResult[2]['packet-loss']) < 100:
        return True
    else:
        return False

def read_userid():
    global useridList
    try:
        with open("userid.txt", "r") as f:
            userid = f.read().strip().split('\n')
            useridList = userid
    except FileNotFoundError:
        useridList = []

def get_new_userid():
    while True:
        new_userid = random.choice(useridList)  #随机抽取
        if new_userid not in used_userid and new_userid not in bad_userid:  #查重
            return new_userid
        
def save_cache(interface_name_list, userid_list):
    try:
        with open("cache.txt", "w") as f:
            for i in range(len(interface_name_list)):
                f.write(f"{interface_name_list[i]}:{userid_list[i]}\n")
        logger.success("缓存已保存到cache.txt")
    except Exception as e:
        logger.error(f"保存缓存失败: {e}")
        
def load_cache():
    cache_dict = {}
    try:
        with open("cache.txt", "r") as f:
            for line in f:
                if ':' in line:
                    interface_name, userid = line.strip().split(':', 1)
                    cache_dict[interface_name] = userid
        logger.success("缓存已从cache.txt加载")
    except FileNotFoundError:
        logger.warning("cache.txt未找到，跳过加载缓存")
    except Exception as e:
        logger.error(f"加载缓存失败: {e}")
    return cache_dict