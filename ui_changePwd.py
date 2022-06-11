'''修改密码界面'''

import MVC
import wx

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class ChangePwdWindow(wx.Frame):
        '''创建修改密码窗体类'''
        def __init__(self, parent, title, userid):
            '''初始化窗体'''
            self.adminID = userid

            #创建控件
            wx.Frame.__init__(self, parent, title=title, size=(300, 200))
            panel = wx.Panel(self, wx.ID_ANY)
            LabelOldPwd = wx.StaticText(panel, label='输入旧密码:')
            self.InputTextOldPwd = wx.TextCtrl(panel, wx.ID_ANY, '123456')
            LabelNewPwd = wx.StaticText(panel, label='输入新密码:')
            self.InputTextNewPwd = wx.TextCtrl(panel, wx.ID_ANY, '123456')
            LabelNewPwd2 = wx.StaticText(panel, label='确认新密码:')
            self.InputTextNewPwd2 = wx.TextCtrl(panel, wx.ID_ANY, '123456')
            ButtonOK = wx.Button(panel, wx.ID_OK, '确定')
            ButtonCancel = wx.Button(panel, wx.ID_CANCEL, '取消')
            self.Bind(wx.EVT_BUTTON, self.OnOK, ButtonOK)
            self.Bind(wx.EVT_BUTTON, self.OnCancel, ButtonCancel)

            #创建布局
            MainSizer = wx.BoxSizer(wx.VERTICAL)
            OldPwdSizer = wx.BoxSizer(wx.HORIZONTAL)
            NewPwdSizer = wx.BoxSizer(wx.HORIZONTAL)
            NewPwd2Sizer = wx.BoxSizer(wx.HORIZONTAL)
            ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
            OldPwdSizer.Add(LabelOldPwd, 0, wx.ALL, 5)
            OldPwdSizer.Add(self.InputTextOldPwd, 0, wx.ALL, 5)
            NewPwdSizer.Add(LabelNewPwd, 0, wx.ALL, 5)
            NewPwdSizer.Add(self.InputTextNewPwd, 0, wx.ALL, 5)
            NewPwd2Sizer.Add(LabelNewPwd2, 0, wx.ALL, 5)
            NewPwd2Sizer.Add(self.InputTextNewPwd2, 0, wx.ALL, 5)
            ButtonSizer.Add(ButtonOK, 0, wx.ALL, 5)
            ButtonSizer.Add(ButtonCancel, 0, wx.ALL, 5)
            MainSizer.Add(OldPwdSizer, 0, wx.ALL, 5)
            MainSizer.Add(NewPwdSizer, 0, wx.ALL, 5)
            MainSizer.Add(NewPwd2Sizer, 0, wx.ALL, 5)
            MainSizer.Add(ButtonSizer, 0, wx.ALL, 5)
            
            panel.SetSizer(MainSizer)
            MainSizer.Fit(self)

        def OnOK(self, event):
            new_pwd = self.InputTextNewPwd.GetValue()
            new_pwd2 = self.InputTextNewPwd2.GetValue()
            # 判断两次密码是否一致
            if new_pwd != new_pwd2:
                wx.MessageBox('两次密码不一致，请重新输入！', '提示', wx.OK | wx.ICON_INFORMATION)
            else:
                old_pwd = self.InputTextOldPwd.GetValue()
                Flag = model.change_password(self.adminID, old_pwd, new_pwd)
                if Flag:
                    wx.MessageBox('修改成功！', '提示', wx.OK | wx.ICON_INFORMATION)
                    self.Close(True)
                else:
                    wx.MessageBox('修改失败！原密码不正确', '提示', wx.OK | wx.ICON_INFORMATION)
                    self.InputTextOldPwd.SetValue('')
                    self.InputTextNewPwd.SetValue('')
                    self.InputTextNewPwd2.SetValue('')
                    self.InputTextOldPwd.SetFocus()

        def OnCancel(self, event):
            self.Close(True)
