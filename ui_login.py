'''登录模块

登陆成功后跳转到主模块ui_main.py；若需注册，跳转ui_register.py'''

import wx
import ui_register
import ui_main
import MVC
import os

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class Window(wx.Dialog):
        """创建登录窗口应用程序类"""
        def __init__(self, parent, title):
            """初始化登录窗体
        
            parent为父窗口"""
            self.private_key = ''
            wx.Dialog.__init__(self, parent, title=title, size=(800, 600))
            panel = wx.Panel(self, wx.ID_ANY)
            # 创建控件
            labeladminName = wx.StaticText(panel, wx.ID_ANY, '管理员名称:',size=(90,-1),style=wx.ALIGN_CENTER)
            self.inputTextadminName = wx.TextCtrl(panel, wx.ID_ANY, 'admin', size=(200,-1))
            labelPassword = wx.StaticText(panel, wx.ID_ANY, '请输入密码:',size=(90,-1),style=wx.ALIGN_CENTER)
            self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, '123456', size=(200,-1),style=wx.TE_PASSWORD)
            self.selBtn = wx.Button(panel, wx.ID_ANY, label='请上传私钥', size=(95,-1))
            self.Filename = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_READONLY, size=(200,-1))
            self.okBtn = wx.Button(panel, wx.ID_ANY, label='确认上传', size=(95,-1))
            self.FileContent = wx.TextCtrl(panel, wx.ID_ANY, '', style=(wx.TE_MULTILINE),size=(520,200))
            labelHint = wx.StaticText(panel, wx.ID_ANY, '  (完成注册后即可生成私钥文件)',size=(300,-1))

            loginBtn = wx.Button(panel, wx.ID_ANY, '登录')
            registerBtn = wx.Button(panel, wx.ID_ANY, '注册')

            mainSizer = wx.BoxSizer(wx.VERTICAL)
            topSizer = wx.BoxSizer(wx.HORIZONTAL)
            # RightSizer = wx.BoxSizer(wx.VERTICAL)
            userSizer = wx.BoxSizer(wx.HORIZONTAL)
            passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
            filenameSizer = wx.BoxSizer(wx.HORIZONTAL)
            checkSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)

            #进行几何布局
            #参数proportion管理窗口总尺寸，它是相对于别的窗口的改变而言的，它只对wx.BoxSizer有意义。
            #参数flag是一个位图，针对对齐、边框位置，增长有许多不同的标志。
            #参数border是窗口或sizer周围以像素为单位的空间总量。
            userSizer.Add(labeladminName, proportion=0, flag=wx.ALL, border=5)
            userSizer.Add(self.inputTextadminName, proportion=0, flag=wx.ALL, border=5)
            passwordSizer.Add(labelPassword, proportion=0, flag=wx.ALL, border=5)
            passwordSizer.Add(self.inputTextPassword, proportion=1, flag=wx.ALL, border=5)
            filenameSizer.Add(self.selBtn, proportion=0, flag=wx.ALL, border=5)
            filenameSizer.Add(self.Filename, proportion=0, flag=wx.ALL, border=5)
            filenameSizer.Add(labelHint, proportion=0, flag=wx.ALL, border=5)
            checkSizer.Add(self.okBtn, proportion=0, flag=wx.ALL, border=5)
            checkSizer.Add(self.FileContent, proportion=0, flag=wx.ALL, border=5)
            btnSizer.Add(loginBtn, proportion=0, flag=wx.ALL, border=5)
            btnSizer.Add(registerBtn, proportion=0, flag=wx.ALL, border=5)

            topSizer.Add(userSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
            topSizer.Add(passwordSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
            # topSizer.Add(filenameSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)

            # RightSizer.Add(filenameSizer, proportion=0, flag=wx.ALL | wx.LEFT, border=5)
            # RightSizer.Add(checkSizer, proportion=0, flag=wx.ALL | wx.LEFT, border=5)

            mainSizer.Add(topSizer, proportion=0, flag=wx.ALL | wx.LEFT, border=5)
            mainSizer.Add(filenameSizer, proportion=0, flag=wx.ALL | wx.LEFT, border=5)
            mainSizer.Add(checkSizer, proportion=0, flag=wx.ALL | wx.LEFT, border=5)
            mainSizer.Add(btnSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)

            panel.SetSizer(mainSizer)
            mainSizer.Fit(self)

            # 绑定事件
            loginBtn.Bind(wx.EVT_BUTTON, self.onLogin)
            registerBtn.Bind(wx.EVT_BUTTON, self.onRegister)
            self.selBtn.Bind(wx.EVT_BUTTON, self.onSel)
            self.okBtn.Bind(wx.EVT_BUTTON, self.onOk)

        def onLogin(self, event):
            adminName = self.inputTextadminName.GetValue()
            password = self.inputTextPassword.GetValue()
            if len(adminName.strip())==0:
                wx.MessageBox('管理员名称不能为空！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            if len(password.strip())==0:
                wx.MessageBox('密码不能为空！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            # 检查private_key是否为空
            if self.private_key == '':
                wx.MessageBox('请"上传私钥”或“确认上传”以读取私钥！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            # 检查用户ID和密码是否正确
            adminID = model.Admin_login(adminName, password, self.private_key)
            if not adminID:
                wx.MessageBox('用户名或密码或角色错误，请重新输入！')
                self.inputTextadminName.SetFocus()
            else:
                self.Close(True) #关闭窗口
                title = '库存管理系统(登录：{0} {1})'.format(adminID,adminName)
                mainFrame = ui_main.view_controller.Window(None, title, adminID, adminName)
                mainFrame.Show()
                mainFrame.Center()

        def onRegister(self, event):
            frame = ui_register.view_controller.Window(parent=None, title='注册')
            frame.Show()
            frame.Center()

        def onSel(self, event):
            '''事件处理函数：选择私钥文件'''
            wildcard = 'All files(*.*)|*.*'
            dlg = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.Filename.SetValue(dlg.GetPath())
                dlg.Destroy()
        
        def onOk(self, event):
            '''事件处理函数：确认选择私钥文件'''
            if len(self.Filename.GetValue())==0:
                wx.MessageBox('请选择私钥文件！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            # 读取私钥文件
            file = open(self.Filename.GetValue())
            self.private_key = file.read()
            self.FileContent.SetValue(self.private_key)
        