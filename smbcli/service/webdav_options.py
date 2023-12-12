import os
import model.success_dict as success
import model.error_dict as error


class webDavOption:
    __dav = None

    def __init__(self, dav):
        super().__init__()
        self.__dav = dav

    def upload(self, remote_path, local_path):
        try:
            if not self.__dav.is_dir(remote_path):
                return error.error_108()
            file_name = local_path.split('/')[-1]
            # 文件和文件夹都能上传
            self.__dav.upload(remote_path + "/" + file_name, local_path)
            if os.path.isdir(local_path):
                file_name = file_name + "文件夹"
        except Exception as e:
            print(e)
            return error.error_104()
        return success.success(f"{file_name}上传成功...")

    def download(self, remote_path, local_path):
        try:
            if os.path.isfile(local_path):
                return error.error_109()
            name = remote_path.split("/")[-1]
            os.mkdir(local_path + "/" + name)
            self.__dav.download_sync(remote_path, local_path + "/" + name)
        except Exception as e:
            print(e)
            return "下载失败..."
        return "下载成功...."

    def create_dir(self, remote_path, name):
        try:
            self.__dav.mkDir(remote_path + "/" + name)
        except Exception as e:
            print(e)
            return "创建失败..."
        return "创建文件夹成功..."

    def create_file(self):
        pass

    def delete_file(self, remote_path):
        try:
            if not self.__dav.check(remote_path):
                return "没有找到该路径"
            self.__dav.clean(remote_path)
        except Exception as e:
            print(e)
            return "删除失败"
        return success.success("删除成功...")

    # 检查是否有相同的文件名或文件名
    def exist_file(self, remote_path, name):
        dav_list = self.__dav.list(remote_path)
        for item in dav_list:
            if item[0] == ".":
                continue
            if item in '/':
                item = item.split('/')[0]
            if item == name:
                return True
        return False

    def move_dir(self, remote_path, target_path):
        name = self.get_last_name(remote_path)
        target_path = target_path + "/" + name
        try:
            self.__dav.move(remote_path, target_path)
        except Exception as e:
            print(e)
            return f"移动{name}文件失败...."
        return "操作成功...."

    def rename(self, remote_path, new_name):
        item = [x for x in remote_path.split("/")[0:-1] if x.strip()]
        item.append(new_name)
        new_path = "/".join(item)
        try:
            self.__dav.move(remote_path, new_path)
        except Exception as e:
            print(e)
            return e
        return "重命名成功....."

    def get_last_name(self, path):
        filter = [item for item in path.split('/') if item.strip()]
        return filter[-1]

    def get_status(self):
        if self.__dav is None:
            return False


