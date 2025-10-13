import collections

import routeros_api
from routeros_api.api_structure import StringField


def get_api(host, username, password, port, plaintext_login, use_ssl, ssl_verify, ssl_verify_hostname, ssl_context):
    connection = routeros_api.RouterOsApiPool(
        host,
        username=username,
        password=password,
        port=port,
        plaintext_login=plaintext_login,
        use_ssl=use_ssl,
        ssl_verify=ssl_verify,
        ssl_verify_hostname=ssl_verify_hostname,
        ssl_context=ssl_context,
    )
    api = connection.get_api()
    return api

def ping_test(api, target_ip, count="3", interface=None):
    default_structure = collections.defaultdict(lambda: StringField(encoding='windows-1250'))
    ping_resource = api.get_resource('/', structure=default_structure)
    ping_result = ping_resource.call('ping', {
        'address': target_ip, 
        'count': count,
        'interface': interface
    })
    return ping_result

def get_interface_mac(api, interface_name):
    interface_resource = api.get_resource('/interface')
    interface_info = interface_resource.get(name=interface_name)
    if interface_info:
        return interface_info[0].get('mac-address')
    return None

def get_interface_ip(api, interface_name):
    ip_resource = api.get_resource('/ip/address')
    ip_info = ip_resource.get(interface=interface_name)
    if ip_info:
        return ip_info[0].get('address').split('/')[0]
    return None