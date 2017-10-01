CREATE TABLE Product(
    pro_id int not null,
    pro_asin varchar(30) not null
    pro_title varchar(50) not null,
    pro_groupId int not null,
    pro_salesRank int default 0
);
