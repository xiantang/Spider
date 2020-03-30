import pymysql
class MysqlClient(object):

    def __init__(self,db,host='',port=3306):
        '''

        :param name:
        :param host:
        :param port:
        '''

        self.conn=pymysql.connect(host=host,
                                    port=port, user='root',
                                    passwd='123456',
                                    db=db, charset='utf8')
        self.cursor=self.conn.cursor()

    def getALL(self,table):
        self.cursor.execute("select * from %s"%table)
        result=self.cursor.fetchall()
        return  result

    def closeConn(self):
        self.cursor.close()
        self.conn.close()

