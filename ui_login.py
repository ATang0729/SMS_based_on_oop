'''登录模块

登陆成功后跳转到主模块ui_main.py；若需注册，跳转ui_register.py'''

from matplotlib.pyplot import title
import wx
import ui_register
import ui_main
import MVC
import sms_main

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class LoginWindow(wx.Dialog):
        """创建登录窗口应用程序类"""
        def __init__(self, parent, title):
            """初始化登录窗体
        
            parent为父窗口"""
            wx.Dialog.__init__(self, parent, title=title, size=(800, 600))
            panel = wx.Panel(self, wx.ID_ANY)
            # 创建控件
            labelUserID = wx.StaticText(panel, wx.ID_ANY, '用户ID:')
            self.inputTextUserID = wx.TextCtrl(panel, wx.ID_ANY, '1')
            labelPassword = wx.StaticText(panel, wx.ID_ANY, '密   码:')
            self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, '123456')

            loginBtn = wx.Button(panel, wx.ID_ANY, '登录')
            registerBtn = wx.Button(panel, wx.ID_ANY, '注册')

            topSizer = wx.BoxSizer(wx.VERTICAL)
            userSizer = wx.BoxSizer(wx.HORIZONTAL)
            passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)

            #进行几何布局
            #参数proportion管理窗口总尺寸，它是相对于别的窗口的改变而言的，它只对wx.BoxSizer有意义。
            #参数flag是一个位图，针对对齐、边框位置，增长有许多不同的标志。
            #参数border是窗口或sizer周围以像素为单位的空间总量。
            userSizer.Add(labelUserID, proportion=0, flag=wx.ALL, border=5)
            userSizer.Add(self.inputTextUserID, proportion=0, flag=wx.ALL, border=5)
            passwordSizer.Add(labelPassword, proportion=0, flag=wx.ALL, border=5)
            passwordSizer.Add(self.inputTextPassword, proportion=1, flag=wx.ALL, border=5)
            btnSizer.Add(loginBtn, proportion=0, flag=wx.ALL, border=5)
            btnSizer.Add(registerBtn, proportion=0, flag=wx.ALL, border=5)

            topSizer.Add(userSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
            topSizer.Add(passwordSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
            topSizer.Add(btnSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)

            panel.SetSizer(topSizer)
            topSizer.Fit(self)

            # 绑定事件
            loginBtn.Bind(wx.EVT_BUTTON, self.onLogin)
            registerBtn.Bind(wx.EVT_BUTTON, self.onRegister)

        def onLogin(self, event):
            userID = self.inputTextUserID.GetValue()
            password = self.inputTextPassword.GetValue()
            if len(userID.strip())==0:
                wx.MessageBox('用户ID不能为空！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            if len(password.strip())==0:
                wx.MessageBox('密码不能为空！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            # 检查用户ID和密码是否正确
            adminName = model.Admin_login(userID, password)
            if not adminName:
                wx.MessageBox('用户名或密码或角色错误，请重新输入！')
                self.inputTextUserID.SetFocus()
            else:
                self.Close(True) #关闭窗口
                title = '库存管理系统(登录：{0} {1})'.format(userID,adminName)
                mainFrame = ui_main.view_controller.MainWindow(None, title, userID, adminName)
                mainFrame.Show()
                mainFrame.Center()

        def onRegister(self, event):
            frame = ui_register.view_controller.RegisterWindow(parent=None, title='注册')
            frame.Show()
            frame.Center()
        