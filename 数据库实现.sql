create table AdminsInfo
(
    AdminID   int auto_increment,
    AdminName varchar(10) not null,
    Sex      char(2)     not null comment '“男”或“女”',
    Password char(32)    not null comment '采用md5算法进行哈希加密后的密码',
    constraint UserInfo_pk
        primary key (AdminID)
)
    comment '数据库管理员基本信息表';

create unique index UserInfo_UserID_uindex
    on AdminsInfo (AdminID);

# create table CustomersInfo
# (
#     CustomerID   int auto_increment,
#     CustomerName varchar(10) not null,
#     Sex      char(2)     not null comment '“男”或“女”',
#     Password char(32)    not null comment '采用md5算法进行哈希加密后的密码',
#     constraint UserInfo_pk
#         primary key (CustomerID)
# )
#     comment '客户基本信息表';
#
# create unique index UserInfo_UserID_uindex
#     on CustomersInfo (CustomerID);

# create table categories
# (
#     categoryID int auto_increment,
#     categoryName nvarchar(10) not null ,
#     description text,
#     constraint category_pk primary key (categoryID)
# )
#     comment '商品品类表';
#
# create unique index categories_categoryID_uindex
#     on categories (categoryID);

create table Products
(
    ProductID int auto_increment,
    ProductName varchar(10) not null,
    unitPrice decimal(5,2) not null comment '单位价格',
#     categoryID int not null ,
    unitInStock int not null comment '商品在库的数量',
    isPlaced boolean not null  default FALSE comment '商品被存放则为True，否则为False',
    constraint Products_pk primary key (ProductID)
#     foreign key (categoryID) references categories(categoryID)
)
    comment '商品基本信息表';

create unique index products_productID_uindex
    on products (ProductID);

create table Shelves
(
    ShelfID int auto_increment,
    location varchar(10) not null comment '货架所处的位置编号',
    isUsed boolean not null default FALSE comment '货架被使用则为True，未被使用则为False',
    constraint Shelves_pk primary key (ShelfID)
)
    comment '货架基本信息';

create unique index Shelves_shelfID_uindex
    on shelves(ShelfID);
create unique index Shelves_location_uindex
    on shelves(location);

create table items
(
    ProductID int not null ,
    ShelfID int not null ,
    inTime datetime not null default now(),
    OperatorID int not null comment '完成入库的管理员ID',
    foreign key (OperatorID) references AdminsInfo(AdminID),
    foreign key (ProductID) references Products(ProductID),
    foreign key (ShelfID) references Shelves(ShelfID),
    primary key (ProductID,ShelfID)
)
    comment '商品存放信息表';

-- -----------------------------------------------------------------
-- 对商品信息的修改
delimiter $$
create procedure Add_Product(in Pname varchar(10),UnitP decimal(5,2),unitS int)
begin
    insert into products(productname, unitprice, unitinstock)
        values(Pname, UnitP, unitS);
END $$
delimiter ;

# call Add_Product('冰箱',300.00,20);

delimiter $$
create procedure Alter_Product(in PID int,Pname varchar(10), UnitP decimal(5,2), UnitS int)
begin
    update products set ProductName=Pname,unitPrice=UnitP,unitInStock=UnitS
    where ProductID=PID;
end $$
delimiter ;

# call Add_Product('卷笔刀',18.88,20);
# call Alter_Product(2,'冰箱',289.9);

delimiter $$
create procedure del_product(in PID int)
begin
    delete from products where ProductID=PID;
end $$
delimiter ;

# insert into shelves(location) value ('001');
# insert into AdminsInfo(adminname, sex, password) values ('张三','男','111111');
# insert into items(productid, shelfid, operatorid) values (1,1,1);
# delete from products where ProductID=1;

delimiter $$
create trigger del_product_del_item
    before delete on products for each row
begin
    declare PID int;
    set PID=OLD.ProductID;
    delete from items where items.ProductID=PID;
end $$
delimiter ;

-- -----------------------------------------------------------------
-- 对货架信息的修改
delimiter $$
create procedure Add_shelves(in Loc varchar(10))
begin
    insert into shelves(location) value (Loc);
end $$
delimiter ;

delimiter $$
create procedure Alter_shelves(in SID int,loc varchar(10))
begin
    update shelves set location=loc
    where ShelfID=SID;
end $$
delimiter ;

delimiter $$
create procedure del_shelves(in SID int)
begin
    delete from shelves where ShelfID=SID;
end $$
delimiter ;

-- -----------------------------------------------------------------
-- 对库存信息的修改
delimiter $$
create procedure Add_items(in PID int,SID int,OID int)
    comment '将未放置的商品放置到未使用的货架上'
begin
    insert into items(productid, shelfid, operatorid)
        values(PID,SID,OID);
    update products set isPlaced=TRUE where ProductID=PID;
    update shelves set isUsed=TRUE where ShelfID=SID;
end $$
delimiter ;

# delimiter $$
# create procedure Alter_items_products(in PID int, SID int, OID int)
#     comment '更换该货架上的商品，更换上的商品使用情况变为True，被换下的商品使用情况变为False'
# begin
#     update items set ProductID=PID, OperatorID=OID
#     where ProductID=PID and ShelfID=SID;
#     update products
# end $$

delimiter $$
create procedure del_items(in PID int, SID int)
    comment '商品出库'
begin
    delete from items where ShelfID=SID and ProductID=PID;
    update products set isPlaced=False,unitInStock=0 where ProductID=PID;
    update shelves set isUsed=False where ShelfID=SID;
end $$
delimiter ;

create view items_report_detailed
as
select items.ProductID 产品ID,ProductName 产品名称,items.ShelfID 存放的货架ID,
       location 存放位置,inTime 存放时间,OperatorID 入库操作员ID,
       AdminName 操作员姓名, unitInStock 商品在库数量,unitPrice 商品单价
from items
join AdminsInfo AI on AI.AdminID = items.OperatorID
join Products P on P.ProductID = items.ProductID
join Shelves S on S.ShelfID = items.ShelfID;

# call Add_items(4,1,1);

# select * from items_report_detailed;