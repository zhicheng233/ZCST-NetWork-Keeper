# ZCST宽带保活器
适用于RouterOS软路由的多播校园宽带保活器，基于RouterOS API，支持Telegram Bot推送

![](https://count.getloli.com/@ZCST-NetWork-MWAN-Keeper?name=ZCST-NetWork-MWAN-Keeper&theme=capoo-2&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto&prefix=0)
# 快速开始
- 1.安装**Python3.10**以上版本
- 2.确保你的RouterOS版本在7.19以上，并且已经配置好vlan多播接口
- 3.在`config.py`中配置好RouterOS登录参数以及RouterOS上的vlan多播接口名称，以及**VLANID**
- 4.在RouterOS中开启API服务并在防火墙中放行相应的端口
- 5.在`userid.txt`中填入你拥有的宽带账号，一行一个
- 6.安装依赖
    ```bash
    pip install -r requirements.txt
    ```
- 7.运行main.py
    ```bash
    python main.py
    ```
- 8.保持程序运行即可

# VLANID获取方式
仅提供思路
## 方法一:
使用脚本进行VLANID爆破>[由NMNMCC学长根据咱提供的信息编写的程序:easy-net](https://github.com/NMNMCC/easy-net/tree/main/internal/vlan)
## 方法二:
使用浏览器F12开发者工具,对认证网页的请求进行抓包

# 多线程？
目前程序是单线程的,目前来看并没有多线程的需求

# 原理
程序通过RouterOS API连接到RouterOS软路由,然后在指定的vlan多播接口上发送Ping,从而实现检测账号是否在线，如果下线则更换新的账号进行登录

# 致谢
感谢[Ra1n4](https://ra1n4.ink/)([GeekerCloud](https://github.com/GeekerCloud-official))提供的RouterOS设备和网络方面的解答以及情绪支持~也非常高兴能参与到[GeekerCloud](https://github.com/GeekerCloud-official)的项目开发

感谢[NMNMCC](https://github.com/NMNMCC/)对咱的思路进行更好的实现

