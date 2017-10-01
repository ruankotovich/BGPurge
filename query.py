class Query():

    ADD_CATEGORY_FOREIGN_KEY = """alter table category add constraint fk_cat_super_cat foreign key(cat_super_cat_id) references category(cat_id);"""
    ADD_REVIEW_FOREIGN_KEY = """alter table review add constraint fk_rev_pro foreign key(rev_pro_id) references Product(pro_id);"""
    ADD_PROCAT_FOREIGN_KEY = """alter table productcategory add constraint fk_procat_cat_id foreign key(pro_cat_cat_id) references category(cat_id),add constraint fk_procat_pro_id foreign key(pro_cat_pro_id) references product(pro_id);"""

    SELECT_A = """(select * from review where rev_pro_id = %d order by rev_rating desc, rev_helpful desc limit 5) union all (select * from review where rev_pro_id = %d order by rev_rating, rev_helpful desc limit 5);"""
    SELECT_B = """select * from product p, similarproducts, product p2 where p.pro_asin = sim_pro_asin and p2.pro_asin = sim_pro_sim_asin and p.pro_salesrank <= p2.pro_salesrank and p.pro_id = %d;"""

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
