'''注册模块'''

from click import password_option
import MVC
import wx
import hashlib

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class RegisterWindow(wx.Dialog):
        '''创建注册窗口程序类'''
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title, size=(300, 200))
            panel = wx.Panel(self, wx.ID_ANY)
            # 创建控件
            labeladminName = wx.StaticText(panel, label='管理员姓名:')
            self.inputTextadminName = wx.TextCtrl(panel, wx.ID_ANY, 'admin')
            labeladminPassword = wx.StaticText(panel, label='管理员密码:')
            self.inputTextadminPw = wx.TextCtrl(panel, wx.ID_ANY, '123456')
            labeladminPassword2 = wx.StaticText(panel, label='请确认密码:')
            self.inputTextadminPw2 = wx.TextCtrl(panel, wx.ID_ANY, '123456')
            labeladminSex = wx.StaticText(panel, label='管理员性别:')
            self.inputTextadminSex = wx.TextCtrl(panel, wx.ID_ANY, '男')

            # 创建按钮
            buttonRegister = wx.Button(panel, wx.ID_OK, '注册')
            buttonCancel = wx.Button(panel, wx.ID_CANCEL, '取消')

            # 创建布局
            layout = wx.BoxSizer(wx.VERTICAL)
            nameSizer = wx.BoxSizer(wx.HORIZONTAL)
            pwSizer = wx.BoxSizer(wx.HORIZONTAL)
            pw2Sizer = wx.BoxSizer(wx.HORIZONTAL)
            sexSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)

            nameSizer.Add(labeladminName, 0, wx.ALL, 5)
            nameSizer.Add(self.inputTextadminName, 0, wx.ALL, 5)
            pwSizer.Add(labeladminPassword, 0, wx.ALL, 5)
            pwSizer.Add(self.inputTextadminPw, 0, wx.ALL, 5)
            pw2Sizer.Add(labeladminPassword2, 0, wx.ALL, 5)
            pw2Sizer.Add(self.inputTextadminPw2, 0, wx.ALL, 5)
            sexSizer.Add(labeladminSex, 0, wx.ALL, 5)
            sexSizer.Add(self.inputTextadminSex, 0, wx.ALL, 5)
            btnSizer.Add(buttonRegister, 0, wx.ALL, 5)
            btnSizer.Add(buttonCancel, 0, wx.ALL, 5)

            layout.Add(nameSizer, 0, wx.ALL, 5)
            layout.Add(pwSizer, 0, wx.ALL, 5)
            layout.Add(pw2Sizer, 0, wx.ALL, 5)
            layout.Add(sexSizer, 0, wx.ALL, 5)
            layout.Add(btnSizer, 0, wx.ALL, 5)

            panel.SetSizer(layout)
            layout.Fit(self)

            # 绑定事件
            self.Bind(wx.EVT_BUTTON, self.OnRegister, buttonRegister)
            self.Bind(wx.EVT_BUTTON, self.OnCancel, buttonCancel)

        def OnRegister(self, event):
            '''注册按钮事件'''
            adminName = self.inputTextadminName.GetValue()
            adminPw = self.inputTextadminPw.GetValue()
            adminPw2 = self.inputTextadminPw2.GetValue()
            adminSex = self.inputTextadminSex.GetValue()
            if adminPw != adminPw2:
                wx.MessageBox('两次密码不一致，请重新输入！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.inputTextadminPw.SetValue('')
                self.inputTextadminPw2.SetValue('')
                self.inputTextadminPw.SetFocus()  #设置焦点事件
            else:
                # 调用model中Admin_register方法，完成注册
                model.Admin_register(adminName, adminPw, adminSex)
                wx.MessageBox('完成注册！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.Destroy()

        def OnCancel(self, event):
            '''取消按钮事件'''
            self.Destroy()