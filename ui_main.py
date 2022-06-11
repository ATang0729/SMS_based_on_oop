'''主菜单模块'''

import wx
import MVC
import ui_login
import ui_changePwd
import ui_product
import ui_Item
import ui_Shelf

model = MVC.Model()

class view_controller(MVC.View_Controller):
    class MainWindow(wx.Frame):
        """创建主窗口程序类"""
        def __init__(self, parent, title, userid, username):
            wx.Frame.__init__(self, parent, title=title, size=(600, 400))
            self.userid = userid
            self.username = username
            self.CreateStatusBar() #创建状态栏

            #创建菜单并添加菜单项
            menuBar = wx.MenuBar()
            menuSys = wx.Menu()  #系统菜单：重新登录、修改密码、退出系统
            menuManage = wx.Menu() #管理菜单：商品管理、库存管理、货架管理
            menuHelp = wx.Menu()  #帮助菜单：关于

            menuLogin = menuSys.Append(wx.ID_ANY, '重新登录', '重新登录')
            menuChanePwd = menuSys.Append(wx.ID_ANY, '修改密码', '修改密码')
            menuExit = menuSys.Append(wx.ID_ANY, '退出系统', '退出系统')

            menuProduct = menuManage.Append(wx.ID_ANY, '商品管理', '商品管理')
            menuShelf = menuManage.Append(wx.ID_ANY, '货架管理', '货架管理')
            menuItem = menuManage.Append(wx.ID_ANY, '库存管理', '库存管理')

            menuAbout = menuHelp.Append(wx.ID_ANY, '关于', '关于')

            menuBar.Append(menuSys, '系统')
            menuBar.Append(menuManage, '管理')
            menuBar.Append(menuHelp, '帮助')

            #绑定事件
            self.Bind(wx.EVT_MENU, self.OnReLogin, menuLogin)
            self.Bind(wx.EVT_MENU, self.OnChangePwd, menuChanePwd)
            self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
            self.Bind(wx.EVT_MENU, self.OnProduct, menuProduct)
            self.Bind(wx.EVT_MENU, self.OnItem, menuItem)
            self.Bind(wx.EVT_MENU, self.OnShelf, menuShelf)
            self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

            self.SetMenuBar(menuBar)

        #创建绑定事件的方法
        def OnReLogin(self, event):
            '''重新登录'''
            self.Destroy()
            LoginFrame = ui_login.view_controller.LoginWindow(parent=None, title='系统登录')
            LoginFrame.Show()
            LoginFrame.Center()
        
        def OnChangePwd(self, event):
            '''修改密码'''
            ChangePwd = ui_changePwd.view_controller.ChangePwdWindow(parent=None, title='修改密码', userid = self.userid)
            ChangePwd.Show()
            ChangePwd.Center()
        
        def OnExit(self, event):
            '''退出系统'''
            self.Destroy()
        
        def OnProduct(self, event):
            '''商品管理'''
            ProductFrame = ui_product.view_controller.ProductWindow(parent=None, title='商品管理', userid = self.userid)
            ProductFrame.Show()
            ProductFrame.Center()

        def OnItem(self, event):
            '''库存管理'''
            ItemFrame = ui_Item.view_controller.ItemWindow(parent=None, title='库存管理', userid = self.userid)
            ItemFrame.Show()
            ItemFrame.Center()

        def OnShelf(self, event):
            '''货架管理'''
            ShelfFrame = ui_Shelf.view_controller.ShelfWindow(parent=None, title='货架管理')
            ShelfFrame.Show()
            ShelfFrame.Center()

        def OnAbout(self, event):
            '''关于'''
            wx.MessageBox('库存管理系统 Powered by 项晗骁200750432', '关于')
            