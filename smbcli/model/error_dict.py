# 暂时没有设置语言


def error_99():
    return {"code": 99, "msg": "请输入正确的IP地址", "result": None}


def error_100():
    return {"code": 100, "msg": "请输入正确的端口格式", "result": None}


def error_101():
    return {"code": 101, "msg": "用户名或密码错误，请重新输入", "result": None}


def error_102():
    return {"code": 102, "msg": "注销失败，请重新尝试", "result": None}


def error_103():
    return {"code": 103, "msg": "获取连接失败，请重试", "result": None}


def error_104():
    return {"code": 104, "msg": "上传文件失败,请重试...", "result": None}


def error_105():
    return {"code": 105, "msg": "删除失败,请重试..", "result": None}


def error_106():
    return {"code": 106, "msg": "下载失败,请重试.....", "result": None}


def error_107():
    return {"code": 107, "msg": "创建失败，请重试....", "result": None}


def error_108():
    return {"code": 108, "msg": "上传失败，请上传到指定文件夹中...", "result": None}


def error_109():
    return {"code": 109, "msg": "下载失败，请下载到指定文件夹中...", "result": None}


def error_110(msg):
    return {"code": 110, "msg": "下载失败，本地文件" + msg + "已存在..", "result": None}
