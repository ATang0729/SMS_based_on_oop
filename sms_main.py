'''主模块

创建wxPython应用程序类，创建和显示登录界面(ui_login.py)'''

import wx
import ui_login


class App(wx.App):
    '''创建主程序类'''
    def OnInit(self):
        '''初始化系统'''
        frame = ui_login.view_controller.Window(parent=None, title='系统登录')
        frame.Show()
        frame.Center()
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()