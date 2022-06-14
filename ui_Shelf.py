'''货架管理页面'''

import MVC
import wx
import json

model = MVC.Model()

class view_controller(MVC.View_Controller):
    '''创建“视图-控制器”类'''

    #用于在内存中存储信息，并在页面退出时候将信息写入JSON文件，用作数据备份
    #每一次调用实例方法populate_products_info时，都会重写一次下列数据
    __shelves = {}  #保存产品信息的字典：shelf_id:location

    class ShelfWindow(wx.Dialog):
        """创建货架管理窗口应用程序类"""
        def __init__(self, parent, title):
            """初始化货架管理窗体
            
            parent为父窗口"""
            wx.Dialog.__init__(self, parent, title=title, size=(800, 600))
            panel = wx.Panel(self, wx.ID_ANY)
            
            # 创建控件
            lblListAction = ['新增','修改','删除']
            self.rboxAction = wx.RadioBox(panel, wx.ID_ANY, '操作', choices=lblListAction, majorDimension=1, style=wx.RA_SPECIFY_ROWS)

            self.listGrade = wx.ListCtrl(panel, wx.ID_ANY, size=(300, 200), style=wx.LC_REPORT)
            self.listGrade.InsertColumn(0, '货架编号', width=100)
            self.listGrade.InsertColumn(1, '货架位置', width=100)
            self.listGrade.InsertColumn(2, '是否在用', width=100)

            labelShelfID = wx.StaticText(panel, wx.ID_ANY, '货架编号:')
            self.txtShelfID = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            labelShelfLocation = wx.StaticText(panel, wx.ID_ANY, '货架位置:')
            self.txtShelfLocation = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            labelShelfStatus = wx.StaticText(panel, wx.ID_ANY, '是否在用:')
            self.txtShelfStatus = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            #默认为新增操作，此时禁止编辑货架编号和使用状态
            self.txtShelfID.Disable()
            self.txtShelfStatus.Disable()

            # 创建按钮
            self.btnAdd = wx.Button(panel, wx.ID_ANY, '新增')
            self.btnModify = wx.Button(panel, wx.ID_ANY, '修改')
            self.btnDelete = wx.Button(panel, wx.ID_ANY, '删除')
            self.btnSave = wx.Button(panel, wx.ID_ANY, '退出')
            self.btnModify.Disable()
            self.btnDelete.Disable()

            # 创建布局
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            optionSizer = wx.BoxSizer(wx.HORIZONTAL)
            contentSizer = wx.BoxSizer(wx.HORIZONTAL)
            enterSizer = wx.BoxSizer(wx.VERTICAL)
            SIDSizer = wx.BoxSizer(wx.HORIZONTAL)
            SLocationsizer = wx.BoxSizer(wx.HORIZONTAL)
            SStatusSizer = wx.BoxSizer(wx.HORIZONTAL)
            buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
            #添加控件到布局
            optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)
            contentSizer.Add(self.listGrade, 0, wx.ALL, 5)
            contentSizer.Add(enterSizer, 0, wx.CENTER, 5)

            SIDSizer.Add(labelShelfID, 0, wx.ALL, 5)
            SIDSizer.Add(self.txtShelfID, 0, wx.ALL, 5)
            SLocationsizer.Add(labelShelfLocation, 0, wx.ALL, 5)
            SLocationsizer.Add(self.txtShelfLocation, 0, wx.ALL, 5)
            SStatusSizer.Add(labelShelfStatus, 0, wx.ALL, 5)
            SStatusSizer.Add(self.txtShelfStatus, 0, wx.ALL, 5)
            enterSizer.Add(SIDSizer, 0, wx.ALL, 5)
            enterSizer.Add(SLocationsizer, 0, wx.ALL, 5)
            enterSizer.Add(SStatusSizer, 0, wx.ALL, 5)

            buttonSizer.Add(self.btnAdd, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnModify, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnDelete, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnSave, 0, wx.ALL, 5)

            mainSizer.Add(optionSizer,0,wx.CENTER,5)
            mainSizer.Add(contentSizer,0,wx.CENTER,5)
            mainSizer.Add(buttonSizer,0,wx.CENTER,5)

            panel.SetSizer(mainSizer)
            mainSizer.Fit(self)

            #显示货架信息
            self.populate_data()

            #绑定事件
            self.Bind(wx.EVT_RADIOBOX, self.on_rbox_action, self.rboxAction)
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_item_selected, self.listGrade)
            self.Bind(wx.EVT_BUTTON, self.onInsert, self.btnAdd)
            self.Bind(wx.EVT_BUTTON, self.onUpdate, self.btnModify)
            self.Bind(wx.EVT_BUTTON, self.onDelete, self.btnDelete)
            self.Bind(wx.EVT_BUTTON, self.on_btn_exit, self.btnSave)
        
        def populate_data(self):
            '''查询数据库，显示货架信息，每次显示都会重写一些内存数据'''
            #查询数据库，显示货架信息
            shelves_info = model.get_shelves_info()
            #清空ListGrade内容
            self.listGrade.DeleteAllItems()
            index = 0
            #清空内存数据
            view_controller.__shelves = {}
            for shelf_info in shelves_info:
                SID = str(shelf_info[0])
                SLocation = str(shelf_info[1])
                SStatus = str(shelf_info[2])
                #添加到内存数据
                view_controller.__shelves[SID] = [SLocation,SStatus]
                #添加到ListGrade
                self.listGrade.InsertItem(index, SID)
                self.listGrade.SetItem(index, 1, SLocation)
                self.listGrade.SetItem(index, 2, SStatus)
                index += 1
        
        def on_rbox_action(self, event):
            '''事件处理函数：选择操作设置不同控件'''
            action = self.rboxAction.GetStringSelection()
            if action == '新增':
                self.txtShelfID.Disable()
                self.txtShelfLocation.Enable()
                self.txtShelfStatus.Disable()
                self.btnAdd.Enable()
                self.btnModify.Disable()
                self.btnDelete.Disable()
            elif action == '修改':
                self.txtShelfID.Enable()
                self.txtShelfLocation.Enable()
                self.txtShelfStatus.Disable()
                self.btnAdd.Disable()
                self.btnModify.Enable()
                self.btnDelete.Disable()
            elif action == '删除':
                self.txtShelfID.Enable()
                self.txtShelfLocation.Disable()
                self.txtShelfStatus.Disable()
                self.btnAdd.Disable()
                self.btnModify.Disable()
                self.btnDelete.Enable()
        
        def on_list_item_selected(self, event):
            '''事件处理函数：选择ListGrade中的一项'''
            #获取选择的行号
            index = event.GetIndex()
            self.txtShelfID.SetValue(self.listGrade.GetItemText(index))
            self.txtShelfLocation.SetValue(self.listGrade.GetItem(index, 1).GetText())
            self.txtShelfStatus.SetValue(self.listGrade.GetItem(index, 2).GetText())

        def onInsert(self, event):
            '''事件处理函数：新增货架'''
            #获取输入的货架信息
            location = self.txtShelfLocation.GetValue()
            #检查输入的货架信息是否合法
            if not location:
                wx.MessageBox('请输入货架位置！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            #检查货架位置是否已存在
            info = model.get_shelves_info()
            locs = list(zip(*[i for i in info]))[1]
            if location in locs:
                wx.MessageBox('货架位置已存在！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            model.add_shelf_info(location)
            self.populate_data()

        def onUpdate(self, event):
            '''事件处理函数：修改货架位置信息'''
            #获取输入的货架信息
            shelf_id = self.txtShelfID.GetValue()
            location = self.txtShelfLocation.GetValue()
            #检查输入的货架信息是否合法
            if len(shelf_id) == 0 or len(location) == 0:
                wx.MessageBox('请输入货架信息！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            #检查货架编号是否存在
            info = model.get_shelves_info()
            sid = list(zip(*[i for i in info]))[0]
            if shelf_id not in str(sid):
                wx.MessageBox('货架编号不存在！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            #检查货架位置是否已存在
            locs = list(zip(*[i for i in info]))[1]
            if location in locs:
                wx.MessageBox('货架位置已存在！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            model.alter_shelf_info(shelf_id, location)
            self.populate_data()

        def onDelete(self, event):
            '''事件处理函数：删除货架位置信息'''
            #获取输入的货架信息
            shelf_id = self.txtShelfID.GetValue()
            #检查输入的货架信息是否合法
            if len(shelf_id) == 0:
                wx.MessageBox('请输入货架信息！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            Falg = model.del_shelf_info(shelf_id)
            if not Falg:
                wx.MessageBox('货架上有商品，不能删除！', '警告', wx.OK | wx.ICON_WARNING)
                return None
            else:
                self.populate_data()

        def on_btn_exit(self, event):
            '''事件处理函数：退出程序，同时将内存数据__shelves写入JSON文件'''
            #将内存数据__shelves写入文件
            with open('shelves.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(view_controller.__shelves, ensure_ascii=False))
            self.Close(True)

