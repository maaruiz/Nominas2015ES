#!/usr/bin/python
# modulos python


# modulos Gtk
from gi.repository import Gtk
from Funciones.Generales.conexion import Basedatos

# Devuelve el valor de un combobox
def valor_combobox(combobox):
    model = combobox.get_model()
    activo = combobox.get_active()
    if activo < 0:
        return None
    return model[activo][0]

# Devuelve Si o No si es verdadero o falso
def si_no(valor):
    if valor:
        dato = True
    else:
        dato = False
    return dato

def buscar(tabla, campo, valor, campo_indice):
    num_campos = 0
    nombre_campos = []
    datos_tabla = []
    num_lineas = 0
    linea_actual = 0
    bd = Basedatos()
    sql = "select * from " + tabla
    print sql
    bd.conectar()
    bd.cursor.execute(sql)
    datos_tabla = bd.cursor.fetchall()
    print "tabla", datos_tabla
    num_lineas = len(datos_tabla)
    print "lineas", num_lineas
    num_campos = len(bd.cursor.description)
    print "campos", num_campos
    for i in range(num_campos):
        nombre_campos.append(bd.cursor.description[i][0])
        if campo == nombre_campos[i]:
            campo_index = i
            print "campo_index",campo_index
    encontrado=False
    for n in range(len(datos_tabla)):
        if datos_tabla[n][campo_index]==si_no_mysql(valor):
            linea_actual=datos_tabla[n]
            encontrado=True
            #self.actualizar()
            break
    return encontrado

def si_no_mysql(valor):
    if valor:
        valor = '\x01'
    elif not valor:
        valor = '\x00'
    else:
        pass
    return valor

# Funcion para crear sentencias en MySQL
def select_sql(sql, alldatos = 0):
    bd = Basedatos()
    cursor = bd.conectar()
    if isinstance(sql, tuple):
        cursor.execute(sql[0], sql[1])
    else:
        cursor.execute(sql)
    if alldatos:
        dato = cursor.fetchall()
    else:
        dato = cursor.fetchone()
    bd.desconectar()
    return(dato)



def sql_basica(campo, tabla, campoindice, valorindice):
    dato = ("Select "
                + campo +
            " From "
                + tabla +
            " Where "
                + campoindice +
                " = %s ")
    try:
        dato = select_sql((dato,(valorindice)))
        if dato is None:
            dato = (0,)
    except:
        dato=(0,)
    return dato[0]

def ultimodiames(mes, anio):
    elmes = str(mes)
    dicmes = {'1' : 31,
          '2' : 28,
          '3' : 31,
          '4' : 30,
          '5' : 31,
          '6' : 30,
          '7' : 31,
          '8' : 31,
          '9' : 30,
          '10' : 31,
          '11' : 30,
          '12' : 31}
    if int(anio) % 4 == 0:
        dicmes['2'] = 29
    return(dicmes[str(elmes)])


def dias_naturales(empresa, mes, anio, db):
    sql = """
           SELECT dias_mes
           FROM emp_calendario
              LEFT JOIN empresa
                ON empresa.idempresa = emp_calendario.idempresa
              LEFT JOIN calendario_mes
                ON emp_calendario.idcalendario = calendario_mes.idcalendario
           WHERE empresa.idempresa=%s
                 and calendario_mes.mes = %s
                 and calendario_mes.idcalendario = %s
        """

    dias_naturales = select_sql((sql, (empresa, mes, anio)))
    return dias_naturales

def dias_festivos(anio, mes):
    sql = ("SELECT count(*) "
           "FROM cal_festivos "
           "WHERE idcalendario = %s and mes = %s;")
    festivos = select_sql((sql, (anio, mes)))
    print "Festivos ... ", festivos[0]
    return festivos[0]

def poblacion(cp):
    sql = ("Select Municipio from t_municipios where CodPostal = %s")
    try:
        dato = select_sql((sql,(cp)))[0]
    except:
        dato = ""
    return dato

def provincia(cp):
    sql = ("Select Provincia from t_provincias where CodProv = left(%s,2)")
    try:
        dato = select_sql((sql,(cp)))[0]
    except:
        dato = ""
    return dato

def lugar(tabla, campo, idcampo, valorid):
    sql = ("Select tb_vias.idtb_vias "
           "from tb_vias "
           "inner join " + tabla + " on tb_vias.idtb_vias = "
           + tabla + "." + idcampo +
           " where " + campo + " = %s")
    try:
        dato = select_sql((sql, (valorid)))[0]
    except:
        dato = ""
    return dato

class CodPostal:
    def __init__(self,codpostal):
        self.cp = unicode(codpostal)
        self.poblacion = sql_basica('Municipio', 't_municipios', 'CodPostal', self.cp)
        self.provincia = sql_basica('Provincia', 't_provincias', 'CodProv', str(self.cp)[0:2])

class Vias:
    def __init__(self, idvia):
        self.id = idvia
        self.via = self.dato_via('via')
    def dato_via(self, campo):
        try:
            dato = sql_basica(campo,'tb_vias', 'idtb_vias', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato
    def listado(self):
        sql = ( "Select "
                    "idtb_vias, via "
                "From "
                    "tb_vias "
                "Order by "
                    "via ")
        dato = select_sql(sql, 1)
        return dato

class TablaDatos():

    def __init__(self, tabla):
        self.campos=[]
        self.campos_tipo=[]
        self.campos_valor=[]
        self.bd = Basedatos()
        self.cursor = self.bd.conectar()
        self.cursor.execute("select * from " + tabla)
    def campo(self):
        print self.cursor.description


class Lista:
    def __init__(self, *variables):
        self.lista = Gtk.ListStore(variables)