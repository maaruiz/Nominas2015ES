import MySQLdb

class Basedatos():

    def __init__(self, host='localhost', user='root', password=''):
        self.host = host
        self.user = user
        self.password = password
        pass

    def db(self):
        self.cursor.execute("set lc_time_names = 'es_ES';")
        return self.database

    def conectar(self):
        self.database = MySQLdb.connect(host=self.host, user=self.user,
                                        passwd=self.password, charset='utf8',
                                        db="Nominas")
        self.cursor = self.database.cursor()
        return self.cursor

    def desconectar(self):
        self.actualizar()
        self.database.close()

    def actualizar(self):
        self.database.commit()
