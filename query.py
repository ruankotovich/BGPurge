class Query():

    ADD_CATEGORY_FOREIGN_KEY = """alter table category add constraint fk_cat_super_cat foreign key(cat_super_cat_id) references category(cat_id);""" 
    ADD_REVIEW_FOREIGN_KEY_PRODUCT = """alter table review add constraint fk_rev_pro foreign key(rev_pro_id) references Product(pro_id);""" 
    ADD_REVIEW_FOREIGN_KEY_CUSTOMER = """alter table review add constraint fk_rev_cus foreign key(rev_customer_id) references Customer(customer_id);""" 
    ADD_PROCAT_FOREIGN_KEY = """alter table productcategory add constraint fk_procat_cat_id foreign key(pro_cat_cat_id) references category(cat_id),add constraint fk_procat_pro_id foreign key(pro_cat_pro_id) references product(pro_id);""" 
    REMOVE_UNUSED_SIMILARS = """delete from similarproducts where sim_pro_surrogate_id in (select sim_pro_surrogate_id from product p1 join similarproducts on p1.pro_asin = sim_pro_asin left join product p2 on p2.pro_asin = sim_pro_sim_asin where p2.pro_asin is null);""" 
    ADD_PROSIM_FOREIGN_KEY = """alter table similarproducts add constraint fk_simpro_pro_asin foreign key(sim_pro_asin) references product(pro_asin), add constraint fk_simpro_pro_sim_asin foreign key(sim_pro_sim_asin) references product(pro_asin);""" 
 
    SELECT_A = """(select * from review join customer on rev_customer_id = customer_id join product on rev_pro_id = pro_id where pro_asin = \'%s\' order by rev_rating desc, rev_helpful desc limit 5) union all (select * from review join customer on rev_customer_id = customer_id join product on rev_pro_id = pro_id where pro_asin = \'%s\' order by rev_rating, rev_helpful desc limit 5);""" 
    SELECT_B = """select p2.pro_id,p2.pro_asin,p2.pro_title,p2.pro_salesrank from product p, similarproducts, product p2 where p.pro_asin = sim_pro_asin and p2.pro_asin = sim_pro_sim_asin and p.pro_salesrank <= p2.pro_salesrank and p2.pro_salesrank > 0 and p.pro_asin = \'%s\';""" 
    SELECT_C = """select r.rev_date, avg(rev_rating) as rev_rating_average from product join review r on rev_pro_id = pro_id where pro_asin = \'%s\' group by r.rev_date order by rev_date ;"""
    SELECT_D = """SELECT rank_filter.gro_description,rank_filter.pro_asin, rank_filter.pro_title,rank_filter.pro_salesrank  FROM (
        SELECT *, 
        rank() OVER (
            PARTITION BY gro_id
            ORDER BY pro_salesrank ASC
        )
        FROM (select * from pgroup join product on pro_groupid = gro_id where pro_salesrank > 0) as did
    ) rank_filter where rank <= 10;"""

    SELECT_E = """select pro_title, avg(rev_rating) as ravg, avg(rev_helpful) as havg 
from review join product p on rev_pro_id = pro_id
group by pro_id, pro_title order by ravg desc, ravg desc limit 10"""

    SELECT_F = """select cat_id,cat_description, avg(p.ravg) cat_avg from category join productcategory on cat_id = pro_cat_cat_id join  (select p.pro_id,avg(rev_rating) as ravg, avg(rev_helpful) as havg from review  join product p on rev_pro_id = pro_id  group by pro_id) as p on p.pro_id = pro_cat_pro_id group by cat_id,cat_description order by cat_avg desc limit 5;"""
    SELECT_G = """SELECT gro_id, customer_sha, c  FROM (
        SELECT *, 
        rank() OVER (
            PARTITION BY gro_id
            ORDER BY c DESC
        )
        FROM (  select rev_customer_id,gro_id, count(*) as c from product
        join review on rev_pro_id = pro_id
        join pgroup on gro_id = pro_groupid
        join customer on rev_customer_id = customer_id
        group by rev_customer_id, gro_id
        order by c desc) as did
    ) rank_filter
    join customer cp on rev_customer_id = cp.customer_id
  where rank <= 10
    order by gro_id, rank;
"""
    

    CREATE_SCHEMA_SQL = """
drop table if exists review;
drop table if exists productCategory;
drop table if exists similarproducts;
drop table if exists pgroup;
drop table if exists category;
drop table if exists product;
drop table if exists customer;


create table Product(
    pro_id int not null unique,
    pro_asin varchar(30) unique not null,
    pro_title varchar(500) not null,
    pro_groupid int not null,
    pro_salesrank int default 0,
    primary key(pro_id, pro_asin)
);

create table SimilarProducts(
    sim_pro_surrogate_id serial not null, 
    sim_pro_asin varchar(30) not null,
    sim_pro_sim_asin varchar(30) not null,
    primary key(sim_pro_surrogate_id) 
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
--  foreign key(pro_cat_cat_id) references category(cat_id),
--  foreign key(pro_cat_pro_id) references product(pro_id)
);

create table Review(
    rev_id serial unique not null,
    rev_pro_id int not null,
    rev_customer_id int not null,
    rev_date date not null,
    rev_rating smallint default 0,
    rev_votes smallint default 0,
    rev_helpful smallint default 0,
    primary key(rev_id, rev_pro_id, rev_customer_id)
--    foreign key(rev_pro_id) references Product(pro_id),
);
create table Customer(
    customer_id int unique not null,
    customer_sha varchar(40) unique not null,
    primary key(customer_id, customer_sha)
);
"""
#BACKUP
