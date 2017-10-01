class Query():

    CREATE_SCHEMA_SQL = """
drop table if exists review;
drop table if exists productCategory;
drop table if exists similarproducts;
drop table if exists pgroup;
drop table if exists category;
drop table if exists product;

create table Product(
    pro_id int not null unique,
    pro_asin varchar(30) not null,
    pro_title varchar(500) not null,
    pro_groupid int not null,
    pro_salesrank int default 0,
    primary key(pro_id, pro_asin)
);

create table SimilarProducts(
    sim_pro_asin varchar(30) not null,
    sim_pro_sim_asin varchar(30) not null,
    primary key(sim_pro_asin, sim_pro_sim_asin)
--    foreign key(sim_pro_asin) references product(pro_asin),
--    foreign key(sim_pro_sim_asin) references product(pro_asin)
);

create table PGroup(
	gro_id int not null unique,
	gro_description varchar(100),
	primary key(gro_id)
);

create table Category(
	cat_id int not null unique,
	cat_description varchar(150),
	cat_super_cat_id int default null,
	primary key(cat_id)
--    foreign key(cat_super_cat_id) references category(cat_id)
);

create table ProductCategory(
	pro_cat_cat_id int not null,
	pro_cat_pro_id int not null,
	primary key(pro_cat_cat_id, pro_cat_pro_id)
--	foreign key(pro_cat_cat_id) references category(cat_id),
--	foreign key(pro_cat_pro_id) references product(pro_id)
);

create table Review(
    rev_id serial not null,
    rev_pro_id int not null,
    rev_customer_id varchar(40) not null,
    rev_date date not null,
    rev_rating smallint default 0,
    rev_votes smallint default 0,
    rev_helpful smallint default 0,
    primary key(rev_id, rev_pro_id, rev_customer_id)
--    foreign key(rev_pro_id) references Product(pro_id),
);
"""
