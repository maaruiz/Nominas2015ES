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

from Funciones.funs import valor_combobox, poblacion, provincia, lugar, \
    Vias, TablaDatos

# modulos reportlab
# modulos Gtk
from gi.repository import Gtk
from Funciones.Datos.cursor import SqlMover
from Funciones.Datos.trabajador_dat import SqlTrabajador
#from classnomina import Nomina
#from numpy.f2py.auxfuncs import isinteger


class Trabajador():

    def __init__(self):
        self.gladefile = "Ventanas/Datos/trabajadores.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.wDT = self.builder.get_object("wDT")
        self.bSiguiente = self.builder.get_object("bSiguiente_wDT")
        self.bAnterior = self.builder.get_object("bAnterior_wDT")
        self.bPrimero = self.builder.get_object("bPrimero_wDT")
        self.bUltimo = self.builder.get_object("bUltimo_wDT")
        self.bCancelar = self.builder.get_object("bCancelar_wDT")
        self.bGuardar = self.builder.get_object("bGuardar_wDT")
        self.bBuscar = self.builder.get_object("bBuscar_wDT")
        self.num_trab = self.builder.get_object("idtrab_wDT")
        self.num_trabajador = self.num_trab.get_text()
        self.cbEsnif = self.builder.get_object("cbEsnif_wDT")
        self.esnif = valor_combobox(self.cbEsnif)
        self.nif = self.builder.get_object("nif_wDT")
        self.naf = self.builder.get_object("naf_wDT")
        self.nacer = self.builder.get_object("nacer_wDT")
        self.nombre = self.builder.get_object("nombre_wDT")
        self.apellido1 = self.builder.get_object("apellido1_wDT")
        self.apellido2 = self.builder.get_object("apellido2_wDT")
        self.cbEslugar = self.builder.get_object("cbEslugar_wDT")
        self.eslugar = valor_combobox(self.cbEslugar)
        self.lista_vias()
        self.direccion = self.builder.get_object("direccion_wDT")
        self.direccion_num = self.builder.get_object("num_wDT")
        self.direccion_planta = self.builder.get_object("planta_wDT")
        self.direccion_puerta = self.builder.get_object("puerta_wDT")
        self.cp = self.builder.get_object("codpostal_wDT")
        self.poblacion = self.builder.get_object("poblacion_wDT")
        self.provincia = self.builder.get_object("provincia_wDT")
        self.boxContratos = self.builder.get_object("boxContratos_wDT")
        self.cbContratos = self.builder.get_object("cbContratos_wDT")
        self.boxContratos.show()
        self.lista_contratos()
        self.wDT.show()
        self.campos_entry = [self.num_trab, self.nombre, self.apellido1,self.apellido2,
                             self.nif, self.naf, self.direccion, self.cp,
                             self.nacer]
        self.campos_bd = ['idTrabajadores','nombre','apellido1', 'apellido2',
                          'nif', 'naf', 'dir', 'cp', 'fechanaci']

    def on_bCancelar_wDT_clicked(self, botton, data=None):
        self.wDT.destroy()

    def on_wDT_destroy(self, objecto, data=None):
        self.wDT.destroy()

    def on_bSiguiente_wDT_clicked(self, button, data=None):
        self.num_trabajador = self.num_trab.get_text()
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                              "idTrabajadores", self.num_trabajador)
        self.num_trabajador = str(SqlCursor.siguiente())
        self.num_trab.set_text(self.num_trabajador)

    def on_bAnterior_wDT_clicked(self, button, data=None):
        self.num_trabajador = self.num_trab.get_text()
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                             "idTrabajadores", self.num_trabajador)
        self.num_trabajador = str(SqlCursor.anterior())
        self.num_trab.set_text(self.num_trabajador)

    def on_bPrimero_wDT_clicked(self, button, data=None):
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                             "idTrabajadores", self.num_trabajador)
        self.num_trabajador = str(SqlCursor.primero())
        self.num_trab.set_text(self.num_trabajador)

    def on_bUltimo_wDT_clicked(self, button, data=None):
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                             "idTrabajadores", self.num_trabajador)
        self.num_trabajador = str(SqlCursor.ultimo())
        self.num_trab.set_text(self.num_trabajador)

    def on_nombre_wDT_changed(self, entry, data=None):
        nombre = self.nombre.get_text()
        #Sql = SqlEmpresa()
        #self.num_trab.set_text(str(SqlTrab.num_trabajador('nombre', nombre)))

    def on_idtrab_wDT_changed(self, entry, data=None):
        self.num_trabajador = self.num_trab.get_text()
        trabajador = SqlTrabajador(self.num_trabajador)
        self.nif.set_text(trabajador.nif)
        self.nombre.set_text(trabajador.nombre)
        self.apellido1.set_text(trabajador.apellido1)
        self.apellido2.set_text(trabajador.apellido2)
        self.direccion.set_text(trabajador.direccion)
        self.direccion_num.set_text(unicode(trabajador.direccion_num))
        self.direccion_planta.set_text(trabajador.direccion_planta)
        self.direccion_puerta.set_text(trabajador.direccion_puerta)
        self.cp.set_text(trabajador.cod_postal)
        self.poblacion.set_text(poblacion(self.cp.get_text()))
        self.provincia.set_text(provincia(self.cp.get_text()))
        self.naf.set_text(trabajador.naf)
        self.nacer.set_text(trabajador.fecha_nacimiento)
        self.cbEsnif.set_active(trabajador.nif_codigo)
        self.cbEslugar.set_active(int(lugar("Trabajadores","idTrabajadores",
                                        "idtb_vias",self.num_trabajador)))
        self.lista_contratos()

    def on_bBuscar_wDT_clicked(self, button, data=None):
        pass

    def on_bNuevo_wDT_clicked(self, button, data=None):
        for k in self.campos_entry:
            k.set_editable(1)
            k.set_text("")
        self.cbEsnif.set_sensitive(True)
        self.cbEslugar.set_sensitive(True)
        self.cbContratos.clear()
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                             "idTrabajadores", self.num_trabajador)
        num_trabajador = str(SqlCursor.nuevo())
        self.num_trab.set_text(num_trabajador)
        self.num_trab.set_editable(0)

    def on_bGuardar_wDT_clicked(self, button, data=None):
        SqlCursor = SqlMover("Trabajadores", "idTrabajadores",
                             "idTrabajadores", self.num_trabajador)
        SqlCursor.grabar(self.campos_entry, self.campos_bd)
        for i in range(len(self.campos_entry)-1):
            self.campos_entry[i].set_text("")
        self.cbEsnif.set_sensitive(False)
        self.cbEslugar.set_sensitive(False)
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


    def lista_contratos(self):
        listcontratos = Gtk.ListStore(str, int, str, str)
        contra = SqlTrabajador(self.num_trabajador).listacontratos()
        try:
            for h in contra:
                contenido = []
                for k in h:
                    contenido.append(k)
                listcontratos.append(contenido)
            self.cbContratos.clear()
            self.cbContratos.set_model(listcontratos)
            render1 = Gtk.CellRendererText()
            self.cbContratos.pack_start(render1, True)
            self.cbContratos.add_attribute(render1, 'text', 0)
            render2 = Gtk.CellRendererText()
            self.cbContratos.pack_start(render2, True)
            self.cbContratos.add_attribute(render2, 'text', 1)
            render3 = Gtk.CellRendererText()
            self.cbContratos.pack_start(render3, True)
            self.cbContratos.add_attribute(render3, 'text', 2)
            render4 = Gtk.CellRendererText()
            self.cbContratos.pack_start(render4, True)
            self.cbContratos.add_attribute(render4, 'text', 3)
            self.cbContratos.set_active(0)
        except:
            pass
