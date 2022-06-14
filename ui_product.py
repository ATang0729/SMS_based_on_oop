'''商品管理页面'''

import MVC
import wx
import json

model = MVC.Model()


class view_controller(MVC.View_Controller):
    
    #用于在内存中存储信息，并在页面退出时候将信息写入JSON文件，用作数据备份
    #每一次调用实例方法populate_data时，都会重写一次下列数据
    __products = {}  #保存产品信息的字典：product_id:name,price,number,isPlaced

    class ProductWindow(wx.Dialog):
        """创建商品管理窗口应用程序类"""
        def __init__(self, parent, title, userid):
            '''初始化程序类'''
            wx.Dialog.__init__(self, parent, title=title, size=(600, 300))
            self.userid = userid
            panel = wx.Panel(self)

            #创建组件
            lblListAction = ['新增','修改','删除']
            self.rboxAction = wx.RadioBox(panel, label='操作', choices = lblListAction)

            self.listGrade = wx.ListCtrl(panel, wx.ID_ANY, size=(450,200), style=wx.LC_REPORT)
            self.listGrade.InsertColumn(0, '商品编号', width=90)
            self.listGrade.InsertColumn(1, '商品名称', width=90)
            self.listGrade.InsertColumn(2, '商品单价', width=90)
            self.listGrade.InsertColumn(3, '在库数量', width=90)
            self.listGrade.InsertColumn(4, '是否上架', width=90)

            labelProductID = wx.StaticText(panel, label='商品编号:')
            self.inputTextPID = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            labelProductName = wx.StaticText(panel, label='商品名称:')
            self.inputTextName = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            labelProductPrice = wx.StaticText(panel, label='商品单价:')
            self.inputTextPrice = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            labelProductNumber = wx.StaticText(panel, label='在库数量:')
            self.inputTextNumber = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
            # 默认为新增商品，此时禁止修改商品编号
            self.inputTextPID.Disable()
            
            #创建按钮
            self.btnAdd = wx.Button(panel, label='新增')
            self.btnModify = wx.Button(panel, label='修改')
            self.btnDelete = wx.Button(panel, label='删除')
            self.btnExit = wx.Button(panel, label='退出')
            self.btnModify.Disable()
            self.btnDelete.Disable()
            
            #绑定事件
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.rboxAction)
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onList, self.listGrade)
            self.btnAdd.Bind(wx.EVT_BUTTON, self.onInsert)
            self.btnModify.Bind(wx.EVT_BUTTON, self.onUpdate)
            self.btnDelete.Bind(wx.EVT_BUTTON, self.onDelete)
            self.btnExit.Bind(wx.EVT_BUTTON, self.OnExit)
            
            #创建Sizer
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            optionSizer = wx.BoxSizer(wx.HORIZONTAL)
            contentSizer = wx.BoxSizer(wx.HORIZONTAL)
            enterSizer = wx.BoxSizer(wx.VERTICAL)
            PIDSizer = wx.BoxSizer(wx.HORIZONTAL)
            namesSizer = wx.BoxSizer(wx.HORIZONTAL)
            pricesSizer = wx.BoxSizer(wx.HORIZONTAL)
            numbersSizer = wx.BoxSizer(wx.HORIZONTAL)
            buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

            #添加组件到Sizer
            optionSizer.Add(self.rboxAction, 0, wx.ALL, 5)

            PIDSizer.Add(labelProductID, 0, wx.ALL, 5)
            PIDSizer.Add(self.inputTextPID, 0, wx.ALL, 5)
            namesSizer.Add(labelProductName, 0, wx.ALL, 5)
            namesSizer.Add(self.inputTextName, 0, wx.ALL, 5)
            pricesSizer.Add(labelProductPrice, 0, wx.ALL, 5)
            pricesSizer.Add(self.inputTextPrice, 0, wx.ALL, 5)
            numbersSizer.Add(labelProductNumber, 0, wx.ALL, 5)
            numbersSizer.Add(self.inputTextNumber, 0, wx.ALL, 5)
            enterSizer.Add(PIDSizer, 0, wx.ALL, 5)
            enterSizer.Add(namesSizer, 0, wx.ALL, 5)
            enterSizer.Add(pricesSizer, 0, wx.ALL, 5)
            enterSizer.Add(numbersSizer, 0, wx.ALL, 5)

            buttonSizer.Add(self.btnAdd, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnModify, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnDelete, 0, wx.ALL, 5)
            buttonSizer.Add(self.btnExit, 0, wx.ALL, 5)

            contentSizer.Add(self.listGrade, 0, wx.ALL, 5)
            contentSizer.Add(enterSizer, 0, wx.CENTER, 5)

            mainSizer.Add(optionSizer, 0, wx.CENTER, 5)
            mainSizer.Add(contentSizer, 0, wx.CENTER, 5)
            mainSizer.Add(buttonSizer, 0, wx.CENTER, 5)

            #设置Panel的Sizer
            panel.SetSizer(mainSizer)
            mainSizer.Fit(self)

            #显示商品信息
            self.populate_data()
        
        #定义方法
        def populate_data(self):
            '''显示商品信息'''
            #获取商品信息
            products_info = model.get_goods_info()
            #清空listGrade内容
            self.listGrade.DeleteAllItems()
            index = 0 
            #清空内存数据
            view_controller.__products = {}
            for info in products_info:
                PID = str(info[0])
                name = info[1]
                price = str(info[2])
                number = str(info[3])
                isPlaced = str(info[4])
                self.listGrade.InsertItem(index,PID)      #商品ID
                self.listGrade.SetItem(index,1,name)      #商品名称
                self.listGrade.SetItem(index,2,price)     #商品单价
                self.listGrade.SetItem(index,3,number)    #商品数量
                self.listGrade.SetItem(index,4,isPlaced)  #是否上架
                view_controller.__products[PID] = [name,price,number,isPlaced]
                index += 1

        def onRadioBox(self, event):
            '''事件处理函数：选择操作设置不同控件'''
            action = self.rboxAction.GetStringSelection()
            if action == '新增':
                self.inputTextPID.Disable()
                self.inputTextName.Enable()
                self.inputTextPrice.Enable()
                self.inputTextNumber.Enable()
                self.btnAdd.Enable()
                self.btnModify.Disable()
                self.btnDelete.Disable()
            elif action == '修改':
                self.inputTextPID.Enable()
                self.inputTextName.Enable()
                self.inputTextPrice.Enable()
                self.inputTextNumber.Enable()
                self.btnAdd.Disable()
                self.btnModify.Enable()
                self.btnDelete.Disable()
            elif action == '删除':
                self.inputTextPID.Enable()
                self.inputTextName.Disable()
                self.inputTextPrice.Disable()
                self.inputTextNumber.Disable()
                self.btnAdd.Disable()
                self.btnModify.Disable()
                self.btnDelete.Enable()
        
        def onList(self, event):
            '''事件处理函数：选择商品信息'''
            #获取选中的商品信息
            index = event.GetIndex()
            self.inputTextPID.SetValue(self.listGrade.GetItem(index,0).GetText())
            self.inputTextName.SetValue(self.listGrade.GetItem(index,1).GetText())
            self.inputTextPrice.SetValue(self.listGrade.GetItem(index,2).GetText())
            self.inputTextNumber.SetValue(self.listGrade.GetItem(index,3).GetText())

        def onInsert(self, event):
            '''事件处理函数：新增商品'''
            #获取输入的商品信息
            name = self.inputTextName.GetValue()
            price = self.inputTextPrice.GetValue()
            number = self.inputTextNumber.GetValue()
            #检查输入的商品信息是否合法
            if len(name) == 0 or len(price) == 0 or len(number) == 0:
                wx.MessageBox('请输入完整的商品信息！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            #检查商品名称是否重复
            info = model.get_goods_info()
            pnames = list(zip(*info))[1]
            if name in pnames:
                wx.MessageBox('商品名称重复！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            model.add_good_info(name, price, number)
            self.populate_data()

        def onUpdate(self, event):
            '''事件处理函数：修改商品'''
            #获取输入的商品信息
            pid = self.inputTextPID.GetValue()
            name = self.inputTextName.GetValue()
            price = self.inputTextPrice.GetValue()
            number = self.inputTextNumber.GetValue()
            #检查输入的商品信息是否合法
            if len(pid) == 0 or len(name) == 0 or len(price) == 0 or len(number) == 0:
                wx.MessageBox('请输入完整的商品信息！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            model.alter_good_info(pid, name, price, number)
            self.populate_data()

        def onDelete(self, event):
            '''事件处理函数：删除商品'''
            pid = self.inputTextPID.GetValue()
            if len(pid) == 0:
                wx.MessageBox('请输入商品ID！', '提示', wx.OK | wx.ICON_INFORMATION)
                return None
            model.delete_good_info(pid)
            self.populate_data()

        def OnExit(self, event):
            '''事件处理函数：退出程序，同时将内存数据__products写入JSON文件'''
            with open('products.json', 'w',encoding='utf-8') as f:
                f.write(json.dumps(view_controller.__products,ensure_ascii=False))
            self.Close(True)
