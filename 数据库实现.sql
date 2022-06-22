-- 创建表--------------------------------------------------
create table adminsinfo
(
    AdminID   int auto_increment
        primary key,
    AdminName varchar(10) not null,
    Sex       char(2)     not null comment '“男”或“女”',
    filename  varchar(60) not null comment '用于保存加密后的密码及解密方式的文件的文件名',
    constraint UserInfo_UserID_uindex
        unique (AdminID)
)
    comment '数据库管理员基本信息表' auto_increment = 1;

create table products
(
    ProductID   int auto_increment
        primary key,
    ProductName varchar(10)          not null,
    unitPrice   decimal(5, 2)        not null comment '单位价格',
    unitInStock int                  not null comment '商品在库的数量',
    isPlaced    tinyint(1) default 0 not null comment '商品被存放则为True，否则为False',
    constraint products_ProductName_uindex
        unique (ProductName),
    constraint products_productID_uindex
        unique (ProductID)
)
    comment '商品基本信息表' auto_increment = 1;

create table shelves
(
    ShelfID  int auto_increment
        primary key,
    location varchar(10)          not null comment '货架所处的位置编号',
    isUsed   tinyint(1) default 0 not null comment '货架被使用则为True，未被使用则为False',
    constraint Shelves_location_uindex
        unique (location),
    constraint Shelves_shelfID_uindex
        unique (ShelfID)
)
    comment '货架基本信息' auto_increment = 1;

create table items
(
    ProductID  int                                not null,
    ShelfID    int                                not null,
    inTime     datetime default CURRENT_TIMESTAMP not null,
    OperatorID int                                not null comment '完成入库的管理员ID',
    primary key (ProductID, ShelfID),
    constraint items_ibfk_1
        foreign key (OperatorID) references adminsinfo (AdminID),
    constraint items_ibfk_2
        foreign key (ProductID) references products (ProductID),
    constraint items_ibfk_3
        foreign key (ShelfID) references shelves (ShelfID)
)
    comment '商品存放信息表';

-- 创建触发器--------------------------------------------------
create definer = root@localhost trigger del_product_del_item
    before delete
    on products
    for each row
begin
    declare PID int;
    set PID=OLD.ProductID;
    delete from items where items.ProductID=PID;
end ;

-- 创建索引--------------------------------------------------
/*
create index OperatorID
    on items (OperatorID);

create index ShelfID
    on items (ShelfID);
*/
-- 创建视图--------------------------------------------------
create definer = root@localhost view items_report_detailed as
select `库存管理系统`.`items`.`ProductID`  AS `产品ID`,
       `p`.`ProductName`             AS `产品名称`,
       `库存管理系统`.`items`.`ShelfID`    AS `存放的货架ID`,
       `s`.`location`                AS `存放位置`,
       `库存管理系统`.`items`.`inTime`     AS `存放时间`,
       `库存管理系统`.`items`.`OperatorID` AS `入库操作员ID`,
       `ai`.`AdminName`              AS `操作员姓名`,
       `p`.`unitInStock`             AS `商品在库数量`,
       `p`.`unitPrice`               AS `商品单价`
from (((`库存管理系统`.`items` join `库存管理系统`.`adminsinfo` `ai`
        on ((`ai`.`AdminID` = `库存管理系统`.`items`.`OperatorID`))) join `库存管理系统`.`products` `p`
       on ((`p`.`ProductID` = `库存管理系统`.`items`.`ProductID`))) join `库存管理系统`.`shelves` `s`
      on ((`s`.`ShelfID` = `库存管理系统`.`items`.`ShelfID`)));

-- comment on column items_report_detailed.存放位置 not supported: 货架所处的位置编号

-- comment on column items_report_detailed.入库操作员ID not supported: 完成入库的管理员ID

-- comment on column items_report_detailed.商品在库数量 not supported: 商品在库的数量

-- comment on column items_report_detailed.商品单价 not supported: 单位价格


-- 创建存储过程--------------------------------------------------
create
    definer = root@localhost procedure Add_Product(IN Pname varchar(10), IN UnitP decimal(5, 2), IN unitS int)
begin
    insert into products(productname, unitprice, unitinstock)
        values(Pname, UnitP, unitS);
END;

create
    definer = root@localhost procedure Add_items(IN PID int, IN SID int, IN OID int) comment '将未放置的商品放置到未使用的货架上'
begin
    insert into items(productid, shelfid, operatorid)
        values(PID,SID,OID);
    update products set isPlaced=TRUE where ProductID=PID;
    update shelves set isUsed=TRUE where ShelfID=SID;
end;

create
    definer = root@localhost procedure Add_shelves(IN Loc varchar(10))
begin
    insert into shelves(location) value (Loc);
end;

create
    definer = root@localhost procedure Alter_Product(IN PID int, IN Pname varchar(10), IN UnitP decimal(5, 2),
                                                     IN UnitS int)
begin
    update products set ProductName=Pname,unitPrice=UnitP,unitInStock=UnitS
    where ProductID=PID;
end;

create
    definer = root@localhost procedure Alter_shelves(IN SID int, IN loc varchar(10))
begin
    update shelves set location=loc
    where ShelfID=SID;
end;

create
    definer = root@localhost procedure del_items(IN PID int, IN SID int) comment '商品出库'
begin
    delete from items where ShelfID=SID and ProductID=PID;
    update products set isPlaced=False,unitInStock=0 where ProductID=PID;
    update shelves set isUsed=False where ShelfID=SID;
end;

create
    definer = root@localhost procedure del_product(IN PID int)
begin
    delete from products where ProductID=PID;
end;

create
    definer = root@localhost procedure del_shelves(IN SID int)
begin
    delete from shelves where ShelfID=SID;
end;

