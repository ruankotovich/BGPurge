import psycopg2
import sys
import parser
from query import Query


class SchemaFactory():

    dataparser = parser.Dataparser()

    con = psycopg2.connect(
        host=sys.argv[1], database=sys.argv[4], user=sys.argv[2], password=sys.argv[3])
    cur = con.cursor()

    def createSchema(self):
        self.cur.execute(Query.CREATE_SCHEMA_SQL)

    def insertProduct(self, product):
        sql = "insert into Product(pro_id, pro_asin, pro_title, pro_groupid, pro_salesrank) values (%d, \'%s\' , \'%s\' , %d , %d)" % (
            product.id, product.asin, product.title.replace("'","''"), product.groupId, product.salesrank)
        self.cur.execute(sql)

    def closeConnection(self):
        self.con.close()

    def commit(self):
        self.con.commit()


factory = SchemaFactory()
factory.createSchema()
factory.dataparser.parseFile(sys.argv[5], factory)
# factory.commit()
factory.closeConnection()


# cur.execute('select * from cidade')

# recset = cur.fetchall()

# for rec in recset:
# print(rec)
