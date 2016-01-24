#!/usr/bin/python
# -*- coding: utf-8 -*-
#### Modulo empresa
# modulos python
#import MySQLdb
#import time
import datetime
#import os
#import sys
#import locale
#from reportlab.lib.pagesizes import A4
#from reportlab.lib.units import mm
#from reportlab.pdfgen import canvas

from Funciones.funs import  select_sql, sql_basica, Vias

# modulos reportlab
# modulos Gtk
from gi.repository import Gtk
#from Funciones.Datos.cursor import SqlMover
#from classnomina import Nomina
#from numpy.f2py.auxfuncs import isinteger

class SqlTrabajador:
    """
    Recoge y devuelve los datos de un trabajador dado a través de su id
    """

    def __init__(self, idtrabajador):
        self.id = idtrabajador
        self.apellido1 = self.dato_trabajador('apellido1')
        self.apellido2 = self.dato_trabajador('apellido2')
        self.cod_postal = self.dato_trabajador('cp')
        self.direccion = self.dato_trabajador('dir')
        self.direccion_num = self.dato_trabajador('dir_num')
        self.direccion_planta = self.dato_trabajador('dir_planta')
        self.direccion_puerta = self.dato_trabajador('dir_puerta')
        self.direccion_completa = (unicode(self.direccion) + ", " + unicode(self.direccion_num) + ", " +
                                   unicode(self.direccion_planta) + ", " + unicode(self.direccion_puerta))
        self.nif = self.dato_trabajador('nif')
        self.nif_codigo = self.dato_trabajador('cod_identificacion')
        self.naf = self.dato_trabajador('naf')
        self.nombre = self.dato_trabajador('nombre')
        self.via_id = self.dato_trabajador('idtb_vias')
        self.via = Vias(self.via_id)
        self.fecha_nacimiento = self.dato_trabajador("CONCAT_WS('/', dayofmonth(fechanaci), month(fechanaci),year(fechanaci))")

    def trabajadordatos(self, num_trabajador):
        sql = ("SELECT idTrabajadores, nombre, apellido1, apellido2, nif, naf, "
               "dir, numero, piso, puerta, cp, esnif, esnie "
               "FROM Trabajadores "
               "WHERE idTrabajadores =%s" )
        dato = select_sql((sql,(num_trabajador)))
        return dato

    def dato_trabajador(self,campo):
        try:
            dato = sql_basica(campo, 'Trabajadores', 'idTrabajadores', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        if isinstance(dato, datetime.date):
            dato = dato.strftime('%d/%m/%Y')
        return dato

    def listacontratos(self):
        sql = ("Select "
                    "CONCAT_WS(' ',empresa.nombre,empresa.apellido1, empresa.apellido2), "
                    "idcontratos_tipo, "
                    "CONCAT_WS(' ','desde',fecha_ini, 'hasta', "
                                "if(fecha_fin is null,'Actualidad',fecha_fin)) "
                    "idcontratos_tipo, "
                    "categoria_profesional "
               "from "
                    "emp_contratos "
                    "inner join "
                        "empresa "
                        "on empresa.idempresa = emp_contratos.idempresa "
               "where "
                        "idTrabajadores = %s "
               "order by "
                        "fecha_ini ")
        dato = select_sql((sql, (self.id)), 1)
        return dato
