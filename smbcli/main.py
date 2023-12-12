import string

import wx


class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)  # 绑定鼠标右键事件
        self.SetSize((400, 300))
        self.SetTitle('右键菜单示例')
        self.Centre()

    def OnContextMenu(self, event):
        menu = wx.Menu()  # 创建菜单

        # 添加菜单项
        item1 = menu.Append(10001, '菜单项1')
        item2 = menu.Append(10002, '菜单项2')

        # 绑定菜单项的事件处理函数
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, item1)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, item2)

        self.PopupMenu(menu)  # 在鼠标右键点击的位置显示菜单
        menu.Destroy()  # 销毁菜单

    def OnMenuSelection(self, event):
        menu_id = event.GetId()
        print(menu_id)
        if menu_id == 10001:
            print('选择了菜单项1')
        elif menu_id == 10002:
            print('选择了菜单项2')


def my_function(required_arg, *args, **kwargs):
    print("Required arg:", required_arg)

    if args:
        print("Other args:", args)

    if 'optional_arg' in kwargs:
        print("Optional arg:", kwargs['optional_arg'])

    # 这里是其他代码...


if __name__ == '__main__':
    my_function("aaaa",optional_arg="aaaa")



    # app = wx.App()
    # frame = MyFrame(None)
    # frame.Show()
    # app.MainLoop()
    # illegal_chars = set(string.punctuation) - set("-_.")
    # print(illegal_chars)
