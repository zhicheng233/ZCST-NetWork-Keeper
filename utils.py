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