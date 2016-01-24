#!/usr/bin/python
# -*- coding: utf-8 -*-
# modulos Gtk
from gi.repository import Gtk

# modulos nomina

from Procesos.Nomina.frontend import Nomina
from Datos.empresa import Empresa
from Datos.trabajador import Trabajador
from Procesos.Nomina.finiquito import finiquito_calc


class Principal:

    def __init__(self):
        self.gladefile = "Ventanas/menuppal.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.imiEmpresas = self.builder.get_object("imiEmpresas")
        self.imiSalir = self.builder.get_object("imiSalir")
        self.imiNominas = self.builder.get_object("imiNominas")
        self.fondo = self.builder.get_object("image8")
        self.fondo.set_from_file('imagen/IMG_1699.JPG')
        self.fondo.show()
        self.window.show_all()

    def on_window1_destroy(self, window, data=None):
        Gtk.main_quit()

    def on_imiSalir_activate(self, menuitem, data=None):
        Gtk.main_quit()

    def on_imiEmpresas_activate(self, menuitem, data=None):
        Empresa()

    def on_imiNominas_activate(self, menuitem, data=None):
        Nomina()

    def on_imiFiniquitos_activate(self, menuitem, data=None):
        finiquito_calc().vacaciones()

    def on_imiTrabajadores_activate(self, menuitem, data=None):
        Trabajador()

    def on_imiCalcIrpf_activate(self, menuitem, data=None):
        self.verirpf()
##### Abrimos la ventana principal
if __name__ == "__main__":
    main = Principal()
    Gtk.main()
