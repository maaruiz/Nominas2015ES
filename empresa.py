#!/usr/bin/python
# -*- coding: utf-8 -*-
#### Modulo empresa
# modulos python
#import MySQLdb
#import time
#import datetime
#import os
#import sys
#import locale
#from reportlab.lib.pagesizes import A4
#from reportlab.lib.units import mm
#from reportlab.pdfgen import canvas

from Funciones.funs import valor_combobox, poblacion, provincia, lugar, Vias

# modulos reportlab
# modulos Gtk
from gi.repository import Gtk
from Funciones.Datos.empresa_dat import SqlEmpresa
from Funciones.Datos.cursor import SqlMover
#from classnomina import Nomina
#from numpy.f2py.auxfuncs import isinteger


class Empresa():

    def __init__(self):
        self.gladefile = "Ventanas/Datos/empresas.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.w4 = self.builder.get_object("w4")
        self.bSiguiente = self.builder.get_object("bSiguiente_w4")
        self.bAnterior = self.builder.get_object("bAnterior_w4")
        self.bPrimero = self.builder.get_object("bPrimero_w4")
        self.bUltimo = self.builder.get_object("bUltimo_w4")
        self.bCancelar = self.builder.get_object("bCancelar_w4")
        self.bAceptar = self.builder.get_object("bAceptar_w4")
        self.bBuscar = self.builder.get_object("bBuscar_w4")
        self.cbEsnif = self.builder.get_object("cbEsnif_w4")
        self.esnif = valor_combobox(self.cbEsnif)
        self.nif = self.builder.get_object("nif_w4")
        self.nombre = self.builder.get_object("nombre_w4")
        self.apellido1 = self.builder.get_object("apellido1_w4")
        self.apellido2 = self.builder.get_object("apellido2_w4")
        self.cbEslugar = self.builder.get_object("cbEslugar_w4")
        self.eslugar = valor_combobox(self.cbEslugar)
        self.lista_vias()
        self.direccion = self.builder.get_object("direccion_w4")
        self.num = self.builder.get_object("num_w4")
        self.num_emp = self.builder.get_object("num_emp_w4")
        self.num_empresa = self.num_emp.get_text()
        self.planta = self.builder.get_object("planta_w4")
        self.puerta = self.builder.get_object("puerta_w4")
        self.cp = self.builder.get_object("codpostal_w4")
        self.poblacion = self.builder.get_object("poblacion_w4")
        self.provincia = self.builder.get_object("provincia_w4")
        self.boxCentros = self.builder.get_object("boxCentros_w4")
        self.cbCentros = self.builder.get_object("cbCentros_w4")
        self.boxCentros.show()
        self.lista_centros()
        self.w4.show()
        self.empresa = SqlEmpresa(int(self.num_empresa))

    def on_bCancelar_w4_clicked(self, botton, data=None):
        self.w4.destroy()

    def on_w4_destroy(self, objecto, data=None):
        self.w4.destroy()

    def on_bSiguiente_w4_clicked(self, button, data=None):
        num_empresa = self.num_emp.get_text()
        SqlCursor = SqlMover('empresa', 'idempresa', 'idempresa', num_empresa)
        num_empresa = str(SqlCursor.siguiente())
        self.num_emp.set_text(str(num_empresa))

    def on_bAnterior_w4_clicked(self, button, data=None):
        num_empresa = self.num_emp.get_text()
        SqlCursor = SqlMover('empresa', 'idempresa', 'idempresa', num_empresa)
        num_empresa = str(SqlCursor.anterior())
        self.num_emp.set_text(str(num_empresa))

    def on_bPrimero_w4_clicked(self, button, data=None):
        SqlCursor = SqlMover('empresa', 'idempresa', 'idempresa', 0)
        num_empresa = str(SqlCursor.primero())
        self.num_emp.set_text(num_empresa)

    def on_bUltimo_w4_clicked(self, button, data=None):
        SqlCursor = SqlMover('empresa', 'idempresa', 'idempresa', 0)
        num_empresa = str(SqlCursor.ultimo())
        self.num_emp.set_text(num_empresa)

    def on_nombre_w4_changed(self, entry, data=None):
        nombre = self.nombre.get_text()
        SqlEmp = SqlEmpresa()
        #self.num_emp.set_text(str(SqlEmp.num_empresa('nombre', nombre)))

    def on_num_emp_w4_changed(self, entry, data=None):
        num_empresa = self.num_emp.get_text()
        empresa = SqlEmpresa(int(num_empresa))
        self.nif.set_text(empresa.cif)
        self.nombre.set_text(empresa.nombre)
        self.apellido1.set_text(empresa.apellido1)
        self.apellido2.set_text(empresa.apellido2)
        self.direccion.set_text(empresa.dir_calle)
        self.cp.set_text(empresa.cod_postal)
        self.poblacion.set_text(poblacion(self.cp.get_text()))
        self.provincia.set_text(provincia(self.cp.get_text()))
        self.cbEsnif.set_active(empresa.cod_identificacion)
        self.cbEslugar.set_active(empresa.via_id)
        self.lista_centros()

    def on_bBuscar_w4_clicked(self, button, data=None):
        pass

    def lista_vias(self):
        listvias = Gtk.ListStore(long, str)
        vias = Vias(44).listado()
        for k in vias:
            contenido = []
            for l in k:
                contenido.append(l)
            listvias.append(contenido)
        self.cbEslugar.set_model(listvias)
        render1 = Gtk.CellRendererText()
        self.cbEslugar.pack_start(render1, True)
        self.cbEslugar.add_attribute(render1, 'int', 0)
        render2 = Gtk.CellRendererText()
        self.cbEslugar.pack_start(render2, True)
        self.cbEslugar.add_attribute(render2, 'text', 1)

    def lista_centros(self):
        listcentros = Gtk.ListStore(int, str, str,str)
        centros = SqlEmpresa(self.num_empresa).listacentros()
        try:
            for h in centros:
                contenido = []
                for k in h:
                    contenido.append(k)
            listcentros.append(contenido)
            self.cbCentros.clear()
            self.cbCentros.set_model(listcentros)
            render1 = Gtk.CellRendererText()
            self.cbCentros.pack_start(render1, True)
            self.cbCentros.add_attribute(render1, 'text', 0)
            render2 = Gtk.CellRendererText()
            self.cbCentros.pack_start(render2, True)
            self.cbCentros.add_attribute(render2, 'text', 1)
            render3 = Gtk.CellRendererText()
            self.cbCentros.pack_start(render3, True)
            self.cbCentros.add_attribute(render3, 'text', 2)
            render4 = Gtk.CellRendererText()
            self.cbCentros.pack_start(render4, True)
            self.cbCentros.add_attribute(render4, 'text', 3)
            self.cbCentros.set_active(0)
        except:
            pass

    def lista_ctacot(self):
        listctacot = Gtk.ListStore()