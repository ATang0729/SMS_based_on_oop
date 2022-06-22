'''库存管理页面'''

import MVC
import wx
import json

model = MVC.Model()

class view_controller(MVC.View_Controller):

    #用于在内存中存储信息，并在页面退出时候将信息写入JSON文件，用作数据备份
    #每一次调用实例方法populate_data时，都会重写一次下列数据
    __items = []  #保存库存信息的列表：[[productID, shelfID]]

    class Window(wx.Dialog):
        """创建库存管理窗口应用程序类"""
        def __init__(self, parent, title, userid):
            """初始化库存管理窗体
            
            parent为父窗口"""
            self.adminID = userid
            wx.Dialog.__init__(self, parent, title=title, size=(800, 600))
            self.panel = wx.Panel(self, wx.ID_ANY)
            # 创建控件
            lblListAction = ['入库管理','出库管理']
            self.rboxAction = wx.RadioBox(self.panel, label='操作类型', choices=lblListAction, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            ## 创建列表框
            self.listGrade = wx.ListCtrl(self.panel, wx.ID_ANY, size=(720, 300), style=wx.LC_REPORT)
            self.listGrade.InsertColumn(0, '商品编号', width=80)
            self.listGrade.InsertColumn(1, '商品名称', width=80)
            self.listGrade.InsertColumn(2, '货架编号', width=80)
            self.listGrade.InsertColumn(3, '存放位置', width=80)
            self.listGrade.InsertColumn(4, '操作时间', width=80)
            self.listGrade.InsertColumn(5, '操作员ID', width=80)
            self.listGrade.InsertColumn(6, '操作人员', width=80)
            self.listGrade.InsertColumn(7, '在库数量', width=80)
            self.listGrade.InsertColumn(8, '商品单价', width=80)
            ## 获取可用的货架信息和商品信息
            available_productIDs = model.get_available_goods_info()
            available_shelfIDs = model.get_available_shelves()
            ## 创建输入框
            labelPID = wx.StaticText(self.panel, wx.ID_ANY, '商品编号:')
            self.PID_choice = wx.ComboBox(self.panel, wx.ID_ANY, size=(120,-1), choices=available_productIDs, style=wx.CB_SORT)
            labelSID = wx.StaticText(self.panel, wx.ID_ANY, '货架编号:')
            self.SID_choice = wx.ComboBox(self.panel, wx.ID_ANY, size=(120,-1), choices=available_shelfIDs, style=wx.CB_SORT)
            labelTIME = wx.StaticText(self.panel, wx.ID_ANY, '操作时间:')
            self.txtTIME = wx.TextCtrl(self.panel, wx.ID_ANY, size=(120, -1),style=wx.TE_PROCESS_ENTER)
            labelUSER = wx.StaticText(self.panel, wx.ID_ANY, '操作人员:')
            self.txtUSER = wx.TextCtrl(self.panel, wx.ID_ANY, size=(120, -1),style=wx.TE_PROCESS_ENTER)
            ## 创建“入库管理”、“出库管理”和“保存退出”按钮
            self.btnEnter = wx.Button(self.panel, wx.ID_ANY, '入库管理')
            self.btnOut = wx.Button(self.panel, wx.ID_ANY, '出库管理')
            self.btnSave = wx.Button(self.panel, wx.ID_ANY, '保存退出')
            ## 默认为入库管理，隐藏出库管理的控件，禁止编辑操作时间和操作人员
            self.txtTIME.Disable()
            self.txtUSER.Disable()
            self.btnOut.Disable()

            # 绑定事件
            self.Bind(wx.EVT_RADIOBOX, self.OnRadioBox, self.rboxAction)
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.listGrade)
            self.Bind(wx.EVT_BUTTON, self.onInsert, self.btnEnter)
            self.Bind(wx.EVT_BUTTON, self.onDelete, self.btnOut)
            self.Bind(wx.EVT_BUTTON, self.OnExit, self.btnSave)

            # 创建Sizer
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            optionSizer = wx.BoxSizer(wx.HORIZONTAL)
            contentSizer = wx.BoxSizer(wx.HORIZONTAL)
            labaelSizer = wx.BoxSizer(wx.VERTICAL)
            PIDSizer = wx.BoxSizer(wx.HORIZONTAL)
            SIDSizer = wx.BoxSizer(wx.HORIZONTAL)
            timeSizer = wx.BoxSizer(wx.HORIZONTAL)
            operatorSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)

            # 加入Sizer
            optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)

            PIDSizer.Add(labelPID, 0, wx.ALL, 5)
            PIDSizer.Add(self.PID_choice, 0, wx.ALL, 5)
            SIDSizer.Add(labelSID, 0, wx.ALL, 5)
            SIDSizer.Add(self.SID_choice, 0, wx.ALL, 5)
            timeSizer.Add(labelTIME, 0, wx.ALL, 5)
            timeSizer.Add(self.txtTIME, 0, wx.ALL, 5)
            operatorSizer.Add(labelUSER, 0, wx.ALL, 5)
            operatorSizer.Add(self.txtUSER, 0, wx.ALL, 5)

            labaelSizer.Add(PIDSizer, 0, wx.ALL, 5)
            labaelSizer.Add(SIDSizer, 0, wx.ALL, 5)
            labaelSizer.Add(timeSizer, 0, wx.ALL, 5)
            labaelSizer.Add(operatorSizer, 0, wx.ALL, 5)

            contentSizer.Add(self.listGrade, 0, wx.ALL, 5)
            contentSizer.Add(labaelSizer, 0, wx.CENTER, 5)

            btnSizer.Add(self.btnEnter, 0, wx.ALL, 5)
            btnSizer.Add(self.btnOut, 0, wx.ALL, 5)
            btnSizer.Add(self.btnSave, 0, wx.ALL, 5)

            mainSizer.Add(optionSizer, 0, wx.CENTER, 5)
            mainSizer.Add(contentSizer, 0, wx.CENTER, 5)
            mainSizer.Add(btnSizer, 0, wx.CENTER, 5)

            # 加入到self.panel中
            self.panel.SetSizer(mainSizer)
            mainSizer.Fit(self)

            #显示库存信息
            self.populate_data()
    
        #定义方法
        def populate_data(self):
            '''显示库存信息，使用库存信息视图，并刷新可用的商品编号和货架编号'''
            # 获取库存信息
            data = model.get_items_info()
            # 清空列表
            self.listGrade.DeleteAllItems()
            index = 0
            # 清空内存数据
            view_controller.__items = []
            for item in data:
                # 获取信息
                pid = item[0]
                Pname = item[1]
                sid = item[2]
                Slocation = item[3]
                time = str(item[4])
                uid = item[5]
                Uname = item[6]
                num = item[7]
                price = item[8]
                # 添加到列表中
                self.listGrade.InsertItem(index, str(pid))
                self.listGrade.SetItem(index, 1, Pname)
                self.listGrade.SetItem(index, 2, str(sid))
                self.listGrade.SetItem(index, 3, Slocation)
                self.listGrade.SetItem(index, 4, time)
                self.listGrade.SetItem(index, 5, str(uid))
                self.listGrade.SetItem(index, 6, Uname)
                self.listGrade.SetItem(index, 7, str(num))
                self.listGrade.SetItem(index, 8, str(price))
                # 将信息存入内存数据
                view_controller.__items.append([pid,sid])
                index += 1
            available_productIDs = model.get_available_goods_info()
            available_shelfIDs = model.get_available_shelves()
            self.PID_choice.SetItems(available_productIDs)
            self.SID_choice.SetItems(available_shelfIDs)

        def OnRadioBox(self, event):
            '''事件处理函数：选择操作类型'''
            # 获取选择的操作类型
            action = self.rboxAction.GetStringSelection()
            if action == '入库管理':
                # 显示入库管理控件
                # print('入库管理')
                self.btnEnter.Enable()
                self.btnOut.Disable()
            elif action == '出库管理':  
                # 显示出库管理控件
                # print('出库管理')
                self.btnEnter.Disable()
                self.btnOut.Enable()

        def OnListItemSelected(self, event):
            '''事件处理函数：选择库存信息'''
            # 夺取选中的商品信息
            ## 获取选中的行号
            index = event.GetIndex()
            ## 获取选中的商品信息
            self.PID_choice.SetValue(self.listGrade.GetItem(index).GetText())
            self.SID_choice.SetValue(self.listGrade.GetItem(index, 2).GetText())
            self.txtTIME.SetValue(self.listGrade.GetItem(index, 4).GetText())
            self.txtUSER.SetValue(self.listGrade.GetItem(index, 5).GetText())

        def onInsert(self,event):
            '''事件处理函数：入库管理'''
            # 获取输入的商品信息
            pid = self.PID_choice.GetValue()
            sid = self.SID_choice.GetValue()
            # 判断输入数据是否合法
            if pid == '' or sid == '':
                wx.MessageBox('请输入商品信息！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.PID_choice.SetFocus()
                return None
            # 判断商品是否可以入库
            pids_avail = model.get_available_goods_info()
            if pid not in pids_avail:
                wx.MessageBox('商品已入库或不存在！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.PID_choice.SetFocus()
                return None
            # 判断货架是否被使用
            sids_avail= model.get_available_shelves()
            if sid not in sids_avail:
                wx.MessageBox('该货架已被使用或不存在！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.SID_choice.SetFocus()
                return None
            # 验证无误，允许入库
            model.add_item_info(pid, sid ,adminID=self.adminID)
            self.populate_data()

        def onUpdate(self,event):
            '''继承父类的方法，但此处不需要实现'''
            pass

        def onDelete(self, event):
            '''事件处理函数：出库管理'''
            # 获取输入的商品信息
            pid = self.PID_choice.GetValue()
            sid = self.SID_choice.GetValue()
            # 判断输入数据是否合法
            if pid == '' or sid == '':
                wx.MessageBox('请输入商品信息！', '提示', wx.OK | wx.ICON_INFORMATION)
                self.PID_choice.SetFocus()
                return None
            # 验证无误
            model.del_item_info(pid, sid)
            self.populate_data()
        
        def OnExit(self, event):
            '''事件处理函数：备份数据到JSON文件并退出系统'''
            with open('items.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(view_controller.__items, ensure_ascii=False))
            self.Destroy()
