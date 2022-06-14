'''修改密码界面'''

import MVC
import wx
import os

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class ChangePwdWindow(wx.Frame):
        '''创建修改密码窗体类'''
        def __init__(self, parent, title, userid):
            '''初始化窗体'''
            self.adminID = userid
            self.private_key = ''
            #创建控件
            wx.Frame.__init__(self, parent, title=title, size=(300, 200))
            panel = wx.Panel(self, wx.ID_ANY)
            LabelOldPwd = wx.StaticText(panel, label='输入旧密码:',size=(100,-1))
            self.InputTextOldPwd = wx.TextCtrl(panel, wx.ID_ANY, '123456', style=wx.TE_PASSWORD, size=(200, -1))
            LabelNewPwd = wx.StaticText(panel, label='输入新密码:',size=(100,-1))
            self.InputTextNewPwd = wx.TextCtrl(panel, wx.ID_ANY, '123456', style=wx.TE_PASSWORD, size=(200, -1))
            self.selBtn = wx.Button(panel, wx.ID_ANY, label='请上传私钥', size=(100, -1))
            self.Filename = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_READONLY, size=(150, -1))
            self.okBtn = wx.Button(panel, wx.ID_ANY, label='OK', size=(40, -1))
            # self.FileContent = wx.TextCtrl(panel, wx.ID_ANY, '', style=(wx.TE_MULTILINE),size=(530,300))
            ButtonOK = wx.Button(panel, wx.ID_OK, '确定')
            ButtonCancel = wx.Button(panel, wx.ID_CANCEL, '取消')
            self.Bind(wx.EVT_BUTTON, self.OnOK, ButtonOK)
            self.Bind(wx.EVT_BUTTON, self.OnCancel, ButtonCancel)
            self.Bind(wx.EVT_BUTTON, self.OnOpenFile, self.selBtn)
            self.Bind(wx.EVT_BUTTON, self.ReadFile, self.okBtn)

            #创建布局
            MainSizer = wx.BoxSizer(wx.VERTICAL)
            # topSizer = wx.BoxSizer(wx.HORIZONTAL)
            OldPwdSizer = wx.BoxSizer(wx.HORIZONTAL)
            NewPwdSizer = wx.BoxSizer(wx.HORIZONTAL)
            filenameSizer = wx.BoxSizer(wx.HORIZONTAL)
            # checkSizer = wx.BoxSizer(wx.HORIZONTAL)
            ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

            OldPwdSizer.Add(LabelOldPwd, 0, wx.ALL, 5)
            OldPwdSizer.Add(self.InputTextOldPwd, 0, wx.ALL, 5)
            NewPwdSizer.Add(LabelNewPwd, 0, wx.ALL, 5)
            NewPwdSizer.Add(self.InputTextNewPwd, 0, wx.ALL, 5)
            filenameSizer.Add(self.selBtn, proportion=0, flag=wx.ALL, border=5)
            filenameSizer.Add(self.Filename, proportion=1, flag=wx.ALL, border=5)
            filenameSizer.Add(self.okBtn, proportion=0, flag=wx.ALL, border=5)
            # checkSizer.Add(self.okBtn, proportion=0, flag=wx.ALL, border=5)
            # checkSizer.Add(self.FileContent, proportion=1, flag=wx.ALL, border=5)
            ButtonSizer.Add(ButtonOK, 0, wx.ALL, 5)
            ButtonSizer.Add(ButtonCancel, 0, wx.ALL, 5)
            # topSizer.Add(OldPwdSizer, 0, wx.ALL, 5)
            # topSizer.Add(NewPwdSizer, 0, wx.ALL, 5)
            # topSizer.Add(filenameSizer, 0, wx.ALL, 5)
            MainSizer.Add(OldPwdSizer, 0, wx.LEFT, 5)
            MainSizer.Add(NewPwdSizer, 0, wx.LEFT, 5)
            MainSizer.Add(filenameSizer, 0, wx.LEFT, 5)
            MainSizer.Add(ButtonSizer, 0, wx.CENTER, 5)
            
            panel.SetSizer(MainSizer)
            MainSizer.Fit(self)

        def OnOK(self, event):
            new_pwd = self.InputTextNewPwd.GetValue()
            old_pwd = self.InputTextOldPwd.GetValue()
            if self.private_key == '':
                wx.MessageBox('请点击“OK”按钮以上传私钥文件！', '提示', wx.OK | wx.ICON_INFORMATION)
                return False
            Flag = model.change_password(self.adminID, old_pwd, new_pwd,self.private_key)
            if Flag:
                wx.MessageBox('修改成功！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.Close(True)
            else:
                wx.MessageBox('修改失败！原密码不正确', '提示', wx.OK | wx.ICON_INFORMATION)
                self.InputTextOldPwd.SetValue('')
                self.InputTextNewPwd.SetValue('')
                self.Filename.SetValue('')
                # self.FileContent.SetValue('')
                self.InputTextOldPwd.SetFocus()

        def OnCancel(self, event):
            self.Close(True)

        def OnOpenFile(self, event):
            '''事件处理函数：选择私钥文件'''
            wildcard = 'All files(*.*)|*.*'
            dlg = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.Filename.SetValue(dlg.GetPath())
                dlg.Destroy()
        
        def ReadFile(self, event):
            '''事件处理函数：确认选择私钥文件'''
            if len(self.Filename.GetValue())==0:
                wx.MessageBox('请选择私钥文件！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            # 读取私钥文件
            file = open(self.Filename.GetValue())
            self.private_key = file.read()
            wx.MessageBox('私钥文件读取成功！', '提示', wx.OK | wx.ICON_INFORMATION)
            # self.FileContent.SetValue(self.private_key)

