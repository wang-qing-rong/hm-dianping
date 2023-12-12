import os

from smb.smb_constants import SMB_FILE_ATTRIBUTE_HIDDEN, SMB_FILE_ATTRIBUTE_READONLY, SMB_FILE_ATTRIBUTE_SYSTEM, \
    SMB_FILE_ATTRIBUTE_DIRECTORY, SMB_FILE_ATTRIBUTE_ARCHIVE, SMB_FILE_ATTRIBUTE_INCL_NORMAL

from tools.smb_client import smbClient
from smb.SMBConnection import SMBConnection
import smb
from service.smb_options import smbOption





if __name__ == '__main__':
    loginMessage = smbClient.login(ip="192.168.10.119", username="wrq", password="1", port="6727")
    print(loginMessage)
    connection = smbClient.getSmbConnection()

    smbOption = smbOption(conn=connection)

    # 测试文件的上传和文件夹的上传
    # print(smbOption.upload(connection,server_name="vol1",local_folder="C:/新建文件夹/Test",remote_folder="/"))

    shares = connection.listShares()
    for share in shares:
        print(share.name)
    print("---------------")

    # print(smbOption.create_file(server_name="vol1", remote_path="/", local_path="C:/webDav/", name="王.vue"))

    # print(smbOption.delete_dir("vol1", target_path="/cloud-drive-vue2"))

    # file_path = '/command1.vue'
    # with connection.openFile('vol1', file_path, mode='w') as file:
    #     file.write('Your input message')
    # connection.openFile()
    attributes = connection.getAttributes("vol1", '/CentOS-7-x86_64-DVD-2009 - 副本.iso')
    print(f"文件大小{attributes.file_size}")
    print(f"文件名{attributes.filename}")
    print(f"上次修改的时间{attributes.last_write_time}")

    path = connection.listPath("vol1", "/")
    for item in path:
        if item.filename[0] == '.':
            continue
        if item.isDirectory:
            print(item.filename + " 文件夹")
        else:
            print(item.filename + " 文件")



# connection.storeFileFromOffset("vlo1","text.txt","wqrqrqrqrqrqr")
# Z:\.recycle\1111
# Z:\.recycle\123
# Z:\.recycle\cloud-drive-vue2
# Z:\.recycle\file
# Z:\.recycle\monitor
# Z:\.recycle\new
# Z:\.recycle\spring_jetty_test-master - 副本
# Z:\.recycle\SS100G
# Z:\.recycle\test1
# Z:\.recycle\TestDir
# Z:\.recycle\TestDir_1
# Z:\.recycle\zyl
# Z:\.recycle\未命名文件夹
# cycle\123
# Z:\.recycle\123\123
# Z:\.recycle\123\234
# Z:\.recycle\123\345
# Z:\.recycle\123\cloud-drive-vue2
# Z:\.recycle\123\123\234
# Z:\.recycle\123\123\345
# net use | findstr "\\\192.168.10.119\"
# Already up to date.

# getAttributes可以获取到的属性
# create_time：从 1970-01-01 00：00：00 到在远程服务器上创建此文件资源时的浮点值（以秒为单位）
# last_access_time：从 1970-01-01 00：00：00 到上次在远程服务器上访问此文件资源的时间的浮点值（以秒数为单位）
# last_write_time：从 1970-01-01 00：00：00 到远程服务器上上次修改此文件资源的时间的浮点值（以秒数为单位）
# last_attr_change_time：从 1970-01-01 00：00：00 到远程服务器上此文件资源的最后一次属性更改时间的秒数浮点值
# file_size ： 文件大小（以字节数为单位）
# alloc_size ：分配用于存储此文件的总字节数
# file_attributes ：SMB_EXT_FILE_ATTR整数值。请参阅 [MS-CIFS]：2.2.1.2.3。可以使用 smb_constants.py 中的 ATTR_xxx 常量执行按位测试以确定文件的状态。
# short_name ：包含此文件短名称的 Unicode 字符串（通常采用 8.3 表示法）
# filename ：包含此文件的长文件名的 Unicode 字符串。每个操作系统对此文件名的长度都有限制。在 Windows 上，它是 256 个字符。
# file_id ：表示文件的文件引用编号的长整型值。如果远程系统不支持此字段，则此字段将为 None 或 0。参见 [MS-FSCC]：2.4.17

