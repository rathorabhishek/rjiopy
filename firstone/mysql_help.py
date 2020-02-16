import mysql.connector
class mysqlhelp:
    def myssqlexecutequery(self,server,usr,pwd,db,query):
        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host=server, database= db)
            cnx.autocommit = True
            if cnx.is_connected():
                print('connected to '+server+ '')
                cursor = cnx.cursor()
                print(query)
                cursor.execute(query)
                cursor.close()
                cnx.close()
                print(query+ "successfully executed")
        except NameError as ex:
            print(ex)
            cnx.close()
