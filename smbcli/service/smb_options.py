from tools.smb_client import smbClient
import model.error_dict as error
import os
import model.success_dict as success


# 对smb共享目录的操作服务
class smbOption:
    __conn = None

    def __init__(self, conn):
        super().__init__()
        self.__conn = conn

    def upload(self, server_name, local_folder, remote_folder):
        try:
            if os.path.isfile(local_folder):
                self.upload_file(self.__conn, server_name, remote_folder, local_folder)
            elif os.path.isdir(local_folder):
                dir_name = self.get_last_name(local_folder)
                # 先查看该路是否有这个同名的文件夹，选择是否覆盖它
                remote_folder = os.path.join(remote_folder, dir_name)
                # 创建这个要上传的文件夹
                self.__conn.createDirectory(server_name, remote_folder)
                self.upload_dir(server_name, remote_folder, local_folder)
                return success.success(f"{dir_name}文件夹上传成功")
        except Exception as e:
            print(e)
            return error.error_104()
        return success.success("上传成功..")

    def upload_file(self, server_name, target_path, local_path):
        file_name = self.get_last_name(local_path)
        with open(local_path, "rb") as file:
            self.__conn.storeFile(server_name, os.path.join(target_path, file_name), file)
        file.close()

    def upload_dir(self, server_name, remote_folder, local_folder):
        for item in os.listdir(local_folder):
            item_path = os.path.join(local_folder, item)
            remote_item_path = os.path.join(remote_folder, item)
            if os.path.isfile(item_path):
                with open(item_path, 'rb') as local_file:
                    self.__conn.storeFile(server_name, remote_item_path, local_file)
                local_file.close()
            elif os.path.isdir(item_path):
                self.__conn.createDirectory(server_name, remote_item_path)
                # 递归调用
                self.upload_dir(self.__conn, server_name, remote_item_path, item_path)

    # smb中的共享文件的下载到本地
    def download(self, server_name, remote_folder_path, local_folder_path):
        try:
            dir_name = self.get_last_name(remote_folder_path)
            attributes = self.__conn.getAttributes(server_name, remote_folder_path)
            if not attributes.isDirectory:
                self.download_file(self.__conn, server_name, remote_folder_path, local_folder_path)
                dir_name = dir_name + "文件"
            if attributes.isDirectory:
                local_folder_path = local_folder_path + "/" + dir_name
                # 在本地位置创建一个同名的文件夹名，但是得要事先检查一下该位置是否存在这个同名的文件夹
                if os.path.exists(local_folder_path):
                    return error.error_110(dir_name)
                    # print(f"本地文件夹{dir_name}已存在，是否覆盖.....")
                dir_name = dir_name + "文件"
                os.mkdir(local_folder_path)
                self.download_dir(server_name, remote_folder_path, local_folder_path)
        except Exception as e:
            print(f'Error: {e}')
            return error.error_106()
        return success.success(f"{dir_name}下载成功.....")

    # 下载目标是文件的情况下
    def download_file(self, server_name, remote_path, local_path):
        file_name = remote_path.split("/")[-1]
        local_path = local_path + '/' + file_name
        with open(local_path, 'wb') as f:
            self.__conn.retrieveFile(server_name, remote_path, f)
        print(f"{file_name}文件下载成功...")

    # 下载文件夹的情况，也是使用递归完成
    def download_dir(self, server_name, remote_path, local_path):
        item_list = self.__conn.listPath(server_name, remote_path)
        for item in item_list:
            if item.filename[0] == '.':
                continue
            remote_item_path = os.path.join(remote_path, item.filename)
            local_item_path = os.path.join(local_path, item.filename)
            if not item.isDirectory:
                with open(local_item_path, 'wb') as f:
                    self.__conn.retrieveFile(server_name, remote_item_path, f)
            else:
                # 在本地创建文件夹
                os.mkdir(local_item_path)
                self.download_dir(self.__conn, server_name, remote_item_path, local_item_path)

    # 在指定的的smb文件中创建文件夹，remote_path 远程路径 file_name 创建的名字，也可以是文件夹名
    def create_dir(self, server_name, remote_path, name):
        # 创建文件或文件夹
        try:
            self.__conn.createDirectory(server_name, os.path.join(remote_path, name))
            # self.__conn.openFiles()
            return success.success(f"创建{name}文件成功")
        except Exception as e:
            print(e)
            return error.error_107()

    # 在指定的远程目录中创建指定文件,只能是local_path写死的情况下进行对创建文件名的拼接，然后创建完成后删除
    def create_file(self, server_name, remote_path, name, local_path):
        try:
            path = os.path.join(local_path, name)
            with open(path, 'w') as f:
                f.close()
            with open(path, 'r') as f:
                self.__conn.storeFile(server_name, os.path.join(remote_path, name), f)
            f.close()
            os.remove(path)
        except Exception as e:
            print(e)
            return error.error_107()
        return success.success(f"创建{name}文件成功")

    # 文件的删除
    # target_path 要删除的目标路径
    def delete_dir(self, server_name, target_path):
        name = self.get_last_name(target_path)
        try:
            attributes = self.__conn.getAttributes(server_name, target_path)
            if attributes.isDirectory:
                if len(self.__conn.listPath(server_name, target_path)) == 0:
                    self.__conn.deleteDirectory(server_name, target_path)
                else:
                    self.delete_doop(server_name, target_path)
                name = name + "文件夹"
            else:
                self.__conn.deleteFiles(server_name, target_path)
                name = name + "文件"
        except Exception as e:
            print(e)
            return error.error_105()
        return success.success(f"删除{name}成功")

    # 检测指定路径中是否存在同名文件
    def smb_exist_file(self, server_name, remote_path, file_name) -> bool:
        file_list = self.__conn.listPath(server_name, remote_path)
        file_name = file_name.strip()
        for file in file_list:
            if file.filename[0] == '.':
                continue
            if file.filename == file_name:
                return True
        return False

    # 进行文件的移动操作
    def move(self, server_name, old_path, new_path):
        try:
            if not self.__conn.getAttributes(server_name, new_path).isDirectory:
                return "目标地址不是文件夹，请重新操作...."
            name = self.get_last_name(old_path)
            self.__conn.rename(server_name, old_path, os.path.join(new_path, name))
        except Exception as e:
            print(e)
        return "操作成功....."

    # 重命名操作 传入，当前的要更该的文件路径和新的文件名字进行拼接
    def rename(self, server_name, now_path, new_name):
        try:
            list = [item for item in now_path.split("/") if item.strip()][0:-1]
            list.append(new_name)
            new_path = '/'.join(list)
            self.__conn.rename(server_name, now_path, new_path)
        except Exception as e:
            print(e)
            return "重命名失败...."
        return "操作成功....."

    # 将路径进行切割，返回路路径中最后一层级的名称
    def get_last_name(self, path):
        filter = [item for item in path.split('/') if item.strip()]
        return filter[-1]

    def delete_doop(self, server_name, target_path):
        list_name = self.__conn.listPath(server_name, target_path)
        for item in list_name:
            if item.filename != "." and item.filename != "..":
                target_item_path = target_path + "/" + item.filename.strip()
                if item.isDirectory:
                    self.delete_doop(server_name, target_item_path)
                else:
                    self.__conn.deleteFiles(server_name, target_item_path)
        self.__conn.deleteDirectory(server_name, target_path)

    # 获取指定资源的属性
    def get_attribute(self, remote_path) -> {}:
        pass

