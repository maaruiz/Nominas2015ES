from Funciones.funs import select_sql


class SqlMover:

    def __init__(self, tabla, idcampo, campo, valor):
        self.tabla = tabla
        self.id = idcampo
        self.campo = campo
        self.valor = valor

    def orden(self):
        sql = ("Select " + self.id + " from " + self.tabla +
               " where " + self.campo + " LIKE %s")
        dato = select_sql((sql, ('%' + self.valor + '%')))[0]
        return dato

    def ultimo(self):
        sql = ("Select max(" + self.id + ") from " + self.tabla)
        dato = select_sql((sql))[0]
        return dato

    def primero(self):
        sql = ("Select min(" + self.id + ") from " + self.tabla)
        dato = select_sql((sql))[0]
        return dato

    def siguiente(self):
        dato = self.valor
        sql = ("Select " + self.id + " from " + self.tabla +
               " where " + self.id +
               " >= %s order by " + self.id + " ASC limit 2")
        if dato == "":
            dato = select_sql((sql, self.valor), 1)[0][0]
        else:
            try:
                dato = select_sql((sql, self.valor), 1)[1][0]
            except:
                pass
        return dato

    def anterior(self):
        dato = self.valor
        sql = ("Select " + self.id + " from " + self.tabla +
               " where " + self.id +
               " <= %s order by " + self.id + " desc limit 2")
        if dato == "":
            dato = select_sql((sql, self.valor), 1)[0][0]
        else:
            try:
                dato = select_sql((sql, self.valor), 1)[1][0]
            except:
                pass
        return dato

    def nuevo(self):
        sql = ("Select max(" + self.id + ") + 1 "
               "from " + self.tabla)
        dato = select_sql((sql))[0]
        return dato

    def grabar(self, widgets = None, campos = None):

        sql = ("insert into " + self.tabla + " set ")
        for k in (range(len(widgets))):
            d = widgets[k].get_text()
            print "d",len(d), campos[k], d
            if len(d) == 10:
                if d[2] == '/' and d[5] == '/':
                    d = d[6:10] + '-' + d[3:5] + '-' + d[0:2]
                    print d
                    widgets[k].set_text(d)
                    print d, widgets[k].get_text()
            sql = sql + campos[k] + " = '" + widgets[k].get_text() + "'"
            if k < max(range(len(widgets))):
                sql += ", "
        select_sql((sql))
        pass