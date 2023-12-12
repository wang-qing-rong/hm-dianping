import ipaddress

from smb.SMBConnection import SMBConnection
import model.error_dict as error
import model.success_dict as success


# ip:192.168.10.119
# user:wrq
# pwd:1
# 默认端口：445

def isAddress(ip):
    ip = str(ip).strip()
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def isPort(port):
    try:
        int(port)
        return True
    except ValueError:
        return False


class SMBClient:
    # 登录smb
    # __smbConnection = None
    __conn = None

    def login(self, ip, username, password, port):
        if isAddress(ip) is False:
            return error.error_99()
        if isPort(port) is False:
            return error.error_100()
        # 执行登录操作
        try:
            self.__conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)
            if self.__conn is None:
                return error.error_101()
            # 与指定服务器的IP和端口进行连接，查看是否连接成功
            result = self.__conn.connect(ip, int(port))  # smb协议默认端口445
            if result is False:
                return error.error_101()
        # 登录过程中抛出的异常处理
        except Exception as e:
            print(e)
            return error.error_101()
        return success.success("登录成功")

    def getSmbConnection(self):
        if self.__conn is None:
            return error.error_101()
        return self.__conn

    # 用户注销操作
    def display(self):
        try:
            if self.__conn is not None:
                self.__conn.close()
                self.__conn.auth_result = False
                return success.success("注销成功")
        except Exception as e:
            return error.error_102()


smbClient = SMBClient()
