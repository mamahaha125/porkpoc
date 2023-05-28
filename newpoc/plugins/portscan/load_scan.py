import ctypes
import json

# 加载Go编译的DLL
scanner = ctypes.CDLL("./newpoc/plugins/portscan/scan.dll")

# 定义ScanPort函数的参数类型和返回类型
scanner.ScanPort.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
scanner.ScanPort.restype = ctypes.c_char_p

def scan_ports(ip, start_port, end_port, channel_size):
    # 创建内存缓冲区来保存开放的端口
    ports_array = (ctypes.c_int * (end_port - start_port + 1))()

    # 调用ScanPort函数并传递内存缓冲区
    result = scanner.ScanPort(ip.encode(), start_port, end_port, ports_array, channel_size)

    # 解析返回的JSON数据

    if result:
        open_ports = json.loads(result.decode())
        return open_ports
    else:
        return "Failed to retrieve open ports."

# 调用scan_ports函数进行端口扫描

