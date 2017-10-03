import psycopg2
import sys
import parser
from query import Query


class SchemaFactory():

    dataparser = parser.Dataparser()

    con = psycopg2.connect(
        host=sys.argv[1], database=sys.argv[4], user=sys.argv[2], password=sys.argv[3])
    cur = con.cursor()

    def chunkify(self, lst, n):
        return [lst[i::n] for i in xrange(n)]

    def purgeDatabase(self):
        print "Adding category foreign keys..."
        self.cur.execute(Query.ADD_CATEGORY_FOREIGN_KEY)
        print "Adding review foreign keys..."
        self.cur.execute(Query.ADD_REVIEW_FOREIGN_KEY_PRODUCT)
        self.cur.execute(Query.ADD_REVIEW_FOREIGN_KEY_CUSTOMER)
        print "Adding procat foreign keys..."
        self.cur.execute(Query.ADD_PROCAT_FOREIGN_KEY)
        print "Removing unused products..."
        self.cur.execute(Query.REMOVE_UNUSED_SIMILARS)
        print "Adding prosim foreign keys..."
        self.cur.execute(Query.ADD_PROSIM_FOREIGN_KEY)

    def createSchema(self):
        self.cur.execute(Query.CREATE_SCHEMA_SQL)

    def insertProducts(self, products):
        dataText = ','.join(self.cur.mogrify('(%s,%s,%s,%s,%s)', (int(product.id), product.asin, product.title, int(
            product.groupId), int(product.salesrank))) for product in products)
        self.cur.execute(
            "insert into Product(pro_id, pro_asin, pro_title, pro_groupid, pro_salesrank) values " + dataText)

    def insertReviews(self, reviews):
        dataText = ','.join(self.cur.mogrify('(%s,%s,%s,%s,%s,%s)', (int(review.productId), int(
            review.customerId), review.date, int(review.rating), int(review.votes), int(review.helpful))) for review in reviews)
        self.cur.execute(
            "insert into review(rev_pro_id,rev_customer_id,rev_date,rev_rating,rev_votes,rev_helpful) values " + dataText)

    def insertSimilars(self, similars):
        dataText = ','.join(self.cur.mogrify(
            '(%s,%s)', (similar.mainProductAsin, similar.similarProductAsin)) for similar in similars)
        self.cur.execute(
            "insert into SimilarProducts(sim_pro_asin,sim_pro_sim_asin) values" + dataText)

    def insertProCategories(self, pCategories):
        dataText = ','.join(self.cur.mogrify('(%s,%s)', (int(pCategory.productId), int(
            pCategory.categoryId))) for pCategory in pCategories)
        self.cur.execute(
            "insert into ProductCategory(pro_cat_pro_id,pro_cat_cat_id) values" + dataText)


    def insertGroup(self, group):
        sql = "insert into PGroup(gro_id,gro_description) values(%d, \'%s\')" % (
            group.id, group.description.replace("'", "''"))
        self.cur.execute(sql)

    def insertCustomer(self, customer):
        sql = "insert into customer(customer_id, customer_sha) values (%d, \'%s\')" % (
            customer.id, customer.sha)
        self.cur.execute(sql)
        

    def insertCategory(self, category):

        if(category.superCategory != None):
            sql = "insert into Category(cat_id, cat_description,cat_super_cat_id) values (%d, \'%s\', %d)" % (
                int(category.id), category.description.replace("'", "''"), int(category.superCategory))
        else:
            sql = "insert into Category(cat_id, cat_description,cat_super_cat_id) values (%d, \'%s\', null)" % (
                int(category.id), category.description.replace("'", "''"))

        self.cur.execute(sql)

    # def insertCustomers(self, customersCollection):

    #     ln = len(customersCollection)
    #     pieces = ln > 1000 if ln / 1000 else 1
    #     aphex = [customersCollection[i::pieces] for i in xrange(pieces)]
    #     customersCollection = None

    #     for customers in aphex:
    #         dataText = ','.join(self.cur.mogrify(
    #             '(%s,%s)', (int(customer.id), customer.sha)) for customer in customers)
    #         self.cur.execute(
    #             "insert into customer(customer_id, customer_sha) values " + dataText)

    # def insertGroups(self, groupsCollection):
    #     ln = len(groupsCollection)
    #     pieces = ln > 1000 if ln / 1000 else 1

    #     aphex = [groupsCollection[i::pieces] for i in xrange(pieces)]
    #     groupsCollection = None

    #     for groups in aphex:
    #         dataText = ','.join(self.cur.mogrify(
    #             '(%s,%s)', (int(group.id), group.description)) for group in groups)
    #         self.cur.execute(
    #             "insert into PGroup(gro_id,gro_description) values " + dataText)

    # def insertCategories(self, categoriesCollection):

    #     ln = len(categoriesCollection)
    #     pieces = ln > 1000 if ln / 1000 else 1

    #     aphex = [categoriesCollection[i::pieces] for i in xrange(pieces)]
    #     categoriesCollection = None

    #     for categorys in aphex:
    #         dataText = ','.join(self.cur.mogrify('(%s,%s,%s)', (int(
    #             category.id), category.description, category.superCategory)) for category in categorys)
    #         self.cur.execute(
    #             "insert into Category(cat_id, cat_description,cat_super_cat_id) values " + dataText)



    def closeConnection(self):
        self.con.close()

    def commit(self):
        self.con.commit()


factory = SchemaFactory()
factory.createSchema()
factory.dataparser.parseFile(sys.argv[5], factory)
factory.purgeDatabase()
factory.commit()
factory.closeConnection()


# cur.execute('select * from cidade')

# recset = cur.fetchall()

# for rec in recset:
# print(rec)
