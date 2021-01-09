import psutil
import socket
import uuid
from app import cache
# 公网IP,内网IP设置永久缓存，因为服务器一般不会变动，如果变动，重新部署应用会自动更新
# 其他信息经常变动，设置20秒缓存

# 获取公网IP地址
@cache.cached(timeout=0,key_prefix='get_public_ip')
def get_public_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# 获取内网IP地址
@cache.cached(timeout=0,key_prefix='get_private_ip')
def get_private_ip():
    r""" 多网卡情况下，根据前缀获取IP（Windows 下适用） """
    prefix = '192.168'
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
    return localIP

# 获取系统mac地址
@cache.cached(timeout=0,key_prefix='get_mac')
def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
    return mac

# 获取内存使用信息
@cache.cached(timeout=10,key_prefix='get_memory')
def get_memory():
    return psutil.virtual_memory().percent

# 获取硬盘使用信息
@cache.cached(timeout=10,key_prefix='get_disk')
def get_disk():
    return psutil.disk_usage("/").percent

# 获取CPU使用信息
@cache.cached(timeout=10,key_prefix='get_cpu')
def get_cpu():
    return psutil.cpu_percent(0)

