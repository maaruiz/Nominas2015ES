#!/usr/bin/env python
# modulos python
import MySQLdb
import datetime
import calendar
import time
import locale
import math
import sys

#modulos reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import gray, black

# modulos Gtk
from gi.repository import Gtk


##### Menu principal

class Principal:

  def __init__(self):
    self.gladefile = "gtk/menuppal.glade"
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    self.builder.connect_signals(self)
    self.window = self.builder.get_object("window1")
    self.imiSalir = self.builder.get_object("imiSalir")
    self.imiNominasImprimir = self.builder.get_object("imiNominasImprimir")
    self.imiNominasCalcular = self.builder.get_object("imiNominasCalcular") 
    self.window.show()

  def on_window1_destroy(self, object, data=None):
    Gtk.main_quit()

  def on_imiSalir_activate(self, menuitem, data=None):
    self.db.close()
    Gtk.main_quit()

  def on_imiNominasImprimir_activate(self, menuitem, data=None):
    self.ImpNomina = Nomina()

  def on_imiNominasCalcular_activate(self, menuitem, data=None):
    self.ImpNomina = Nomina()


##### Abrimos la ventana principal
if __name__ == "__main__":
  main = Principal()
  Gtk.main()