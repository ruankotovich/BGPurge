import psycopg2
import sys
import parser
from query import Query


class SchemaFactory():

    dataparser = parser.Dataparser()

    con = psycopg2.connect(
        host=sys.argv[1], database=sys.argv[4], user=sys.argv[2], password=sys.argv[3])
    cur = con.cursor()

    def purgeDatabase(self):
        self.cur.execute(Query.ADD_CATEGORY_FOREIGN_KEY)
        self.cur.execute(Query.ADD_REVIEW_FOREIGN_KEY)
        self.cur.execute(Query.ADD_PROCAT_FOREIGN_KEY)
        self.cur.execute(Query.REMOVE_UNUSED_SIMILARS)
        self.cur.execute(Query.ADD_PROSIM_FOREIGN_KEY)

    def createSchema(self):
        self.cur.execute(Query.CREATE_SCHEMA_SQL)

    def insertProduct(self, product):
        sql = "insert into Product(pro_id, pro_asin, pro_title, pro_groupid, pro_salesrank) values (%d, \'%s\' , \'%s\' , %d , %d)" % (
            product.id, product.asin, product.title.replace("'", "''"), product.groupId, product.salesrank)
        self.cur.execute(sql)

    def insertReview(self, review):
        sql = "insert into review(rev_pro_id,rev_customer_id,rev_date,rev_rating,rev_votes,rev_helpful) values (%d, \'%s\', \'%s\', %d, %d, %d)" % (
            review.productId, review.customerId, review.date, review.rating, review.votes, review.helpful)
        self.cur.execute(sql)

    def insertSimilar(self, similar):
        sql = "insert into SimilarProducts(sim_pro_asin,sim_pro_sim_asin) values (\'%s\', \'%s\')" % (
            similar.mainProductAsin, similar.similarProductAsin)
        self.cur.execute(sql)

    def insertProCategory(self, pCategory):
        sql = "insert into ProductCategory(pro_cat_pro_id,pro_cat_cat_id) values (%d, %d)" % (
            int(pCategory.productId), int(pCategory.categoryId))
        self.cur.execute(sql)

    def insertGroup(self, group):
        sql = "insert into PGroup(gro_id,gro_description) values(%d, \'%s\')" % (
            group.id, group.description.replace("'", "''"))
        self.cur.execute(sql)

    def insertCategory(self, category):

        if(category.superCategory != None):
            sql = "insert into Category(cat_id, cat_description,cat_super_cat_id) values (%d, \'%s\', %d)" % (
                int(category.id), category.description.replace("'", "''"), int(category.superCategory))
        else:
            sql = "insert into Category(cat_id, cat_description,cat_super_cat_id) values (%d, \'%s\', null)" % (
                int(category.id), category.description.replace("'", "''"))

        self.cur.execute(sql)

    def closeConnection(self):
        self.con.close()

    def commit(self):
        self.con.commit()


factory = SchemaFactory()
# factory.createSchema()
factory.dataparser.parseFile(sys.argv[5], factory)
factory.purgeDatabase()
# factory.commit()
factory.closeConnection()


# cur.execute('select * from cidade')

# recset = cur.fetchall()

# for rec in recset:
# print(rec)
