#!/usr/bin/python
# -*- coding: utf-8 -*-
#### Modulo nominas
# modulos python
import datetime
import os
import locale
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from gi.repository import Gtk

from Procesos.Nomina.Imprimir.formulario import impr_nomina
from Procesos.Nomina.calculos import CalcNomina
from Procesos.Nomina.Editar.eliminar import NomBorrar
from Funciones.Datos.nomina_dat import SqlNominas, Nomina_Devengo
from Funciones.funs import valor_combobox
from Funciones.Datos.empresa_dat import SqlEmpresa


# modulos funs


class Nomina():

    def __init__(self):
        self.gladefile = "Ventanas/nomina.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.grabarfichero1 = self.builder.get_object("grabarfichero1")
        self.window2 = self.builder.get_object("window2")
        self.lTitulo = self.builder.get_object("lTitulo")
        self.lTitulo.set_text("A darle fuerte")
        self.bBuscar = self.builder.get_object("bBuscar")
        self.bSalir = self.builder.get_object("bSalir")
        self.bImprimir = self.builder.get_object("bImprimir")
        self.cbnum = self.builder.get_object("num_emp")
        self.num = valor_combobox(self.cbnum)
        self.lista_empresas()
        self.cbmes = self.builder.get_object("mes")
        self.mes = valor_combobox(self.cbmes)
        self.anio = self.builder.get_object("anio")
        self.anio.set_text(str(datetime.datetime.today().year))
        self.formnom = self.builder.get_object("formnom")
        self.box9 = self.builder.get_object("box9")
        self.tabla = Gtk.Table(1, 1)
        self.box9.add(self.tabla)
        self.rbnomina = self.builder.get_object('rbnomina')
        self.rbfiniquito = self.builder.get_object('rbfiniquito')
        self.rbnominapextra = self.builder.get_object('rbnominapextra')
        self.on_rbnomina_toggled(self.rbnomina)
        self.tabla.show()
        self.box9.show()
        self.window2.show()

    def on_window2_destroy(self, objecto, data=None):
        self.window2.destroy()

    def on_bSalir_clicked(self, button, data=None):
        self.window2.destroy()

    def on_bImprimir_clicked(self, button, data=None):
        # self.grabarfichero1.show()
        self.canvas = canvas.Canvas("nomina.pdf", pagesize=A4)
        impr_nomina(self.canvas,
                    valor_combobox(self.cbnum),
                    valor_combobox(self.cbmes),
                    int(self.anio.get_text()),
                    valor_combobox(self.formnom), 0)
#    width, height = A4
        self.canvas.save()
        # self.anio.set_text("")
        # self.dialImprimir = dialImprimir()
        print os.name
        os.system("/usr/bin/evince nomina.pdf")

    def on_bCalcular_clicked(self, botton, data=None):
        self.calculo = CalcNomina(valor_combobox(self.cbnum),
                                   valor_combobox(self.cbmes),
                                   self.anio.get_text(), self.esnomina,
                                  self.esfiniquito, self.esnominapextra)
        self.calculo.calcular()
        # self.dialDato

    def on_bRecalculo_clicked(self, botton, data=None):
        self.calculo = CalcNomina(valor_combobox(self.cbnum),
                                   valor_combobox(self.cbmes),
                                   self.anio.get_text())
        self.calculo.recalcular()

    def on_bBorrar_clicked(self, botton, data=None):
        print botton
        supr = NomBorrar(valor_combobox(self.cbnum), valor_combobox(self.cbmes), int(self.anio.get_text()), 0,
                         self.esnomina, self.esfiniquito, self.esnominapextra)
        supr.borrar_mes()

    def lista_empresas(self):
        listaempresas = Gtk.ListStore(long, str)
        empresas = SqlEmpresa(0).listaempresas()
        for k in empresas:
            contenido = []
            for l in k:
                contenido.append(l)
            listaempresas.append(contenido)
        self.cbnum.set_model(listaempresas)
        render1 = Gtk.CellRendererText()
        self.cbnum.pack_start(render1, True)
        self.cbnum.add_attribute(render1, 'int', 0)
        render2 = Gtk.CellRendererText()
        self.cbnum.pack_start(render2, True)
        self.cbnum.add_attribute(render2, 'text', 1)

    def on_change(self, entry, data=None):
        self.tabla.destroy()
        empresa = SqlNominas(0)
        trabajadores = empresa.trabajadores(valor_combobox(self.cbnum),
                                            valor_combobox(self.cbmes),
                                            self.anio.get_text(), self.esnomina,
                                            self.esfiniquito, self.esnominapextra)
        tabla = Gtk.Table(10, 1)
        t = 0
        while t < len(trabajadores):
            boton = Gtk.Button(trabajadores[t][0])
            boton.connect("clicked", self.clicked, trabajadores[t][1])
            boton.show()
            tabla.attach(boton, 0, 1, t, t + 1)
            t += 1
        self.tabla = tabla
        self.tabla.show()
        self.box9.add(self.tabla)
        self.box9.show()

    def on_rbnomina_toggled(self, button, data=None):
        if button.get_active():
            if button.get_label() == 'Nomina':
                self.esnomina = True
                self.esfiniquito = False
                self.esnominapextra = False
            elif button.get_label() == 'Finiquito':
                self.esnomina = False
                self.esfiniquito = True
                self.esnominapextra = False
            elif button.get_label == 'Nomina pagas extras':
                self.esnomina = False
                self.esfiniquito = False
                self.esnominapextra = True
        self.on_change(self.cbnum)

    def clicked(self, widget, data=None):
        devengos = vernomina(data, valor_combobox(self.cbmes),
                             self.anio.get_text(), valor_combobox(self.formnom), self.esnomina,
                             self.esfiniquito, self.esnominapextra)



class dialImprimir:

    def __init__(self):
        self.gladefile = "Ventanas/nomina.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.bCerrar = self.builder.get_object("bCerrar")
        self.dialImprimir = self.builder.get_object("dialImprimir")
        self.dialImprimir.show()

    def on_bCerrar_clicked(self, dialog, data=None):
        self.dialImprimir.destroy()


class vernomina:

    def __init__(self, trabajador, mes, anio, fornom, esnomina=True, esfiniquito=False, esnominapextra=False):
        self.trabajador = trabajador
        self.mes = mes
        self.anio = anio
        self.fornom = fornom
        self.gladefile = "Ventanas/nomina.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.bAceptar = self.builder.get_object("bAcepta")
        self.bBorrar = self.builder.get_object('bEliminar')
        self.bCancelar = self.builder.get_object("bCancela")
        self.bRecalcular = self.builder.get_object("bRecal")
        self.esnomina = esnomina
        self.esfiniquito = esfiniquito
        self.esnominapextra = esnominapextra
        self.lantiguedad = self.builder.get_object("lantiguedad")
        self.lidempresa = self.builder.get_object("lidempresa")
        self.lcif = self.builder.get_object("lcif")
        self.lcontrato = self.builder.get_object('lcontrato')
        self.ld = self.builder.get_object("ld")
        self.ldireccion = self.builder.get_object('ldireccion')
        self.lempresa = self.builder.get_object("lemp")
        self.lhoras = self.builder.get_object('lhoras')
        self.lidcontrato = self.builder.get_object('lidcontrato')
        self.lliquido = self.builder.get_object('lliquido')
        self.lncc = self.builder.get_object("lncc")
        self.lnif = self.builder.get_object("lnif")
        self.lnaf = self.builder.get_object("lnaf")
        self.lnumcontrato = self.builder.get_object('lnumcontrato')
        self.lidnomina = self.builder.get_object('lidnomina')
        self.lperiodo = self.builder.get_object("lper")
        self.lpuesto = self.builder.get_object('lpuesto')
        dev = SqlNominas(0)
        self.lanomina = dev.nomina_trabajador_mes(self.trabajador, self.mes,
                                             self.anio, self.esnomina, self.esfiniquito,
                                                  self.esnominapextra)
        self.laempresa = dev.trabajador_empresa(self.trabajador, self.mes,
                                                self.anio)
        self.lppextra = self.builder.get_object('lppextra')
        self.lremuneracion = self.builder.get_object('lremuneracion')
        self.ltrabajador = self.builder.get_object("ltrab")
        self.lb_segsoc = self.builder.get_object("lb_segsoc")
        self.lb_irpf = self.builder.get_object("lb_irpf")
        self.rb_es_tpoparcial = self.builder.get_object("rbEs_tpoparcial")
        self.rb_es_tpocompleto = self.builder.get_object('rbEs_tpocompleto')
        self.rb_es_indefinido = self.builder.get_object('rbEs_indefinido')
        self.rb_es_temporal = self.builder.get_object('rbEs_temporal')
        self.box14 = self.builder.get_object("box14")
        self.vista = self.builder.get_object("vista")
        self.window3 = self.builder.get_object("window3")
        self.window3.show()
        if self.esnomina:
            self.nomina()
        elif self.esfiniquito:
            self.nomina()

    def nomina(self):
        self.lista = Gtk.ListStore(long, str, str, str, str, str)
        render0 = Gtk.CellRendererText()
        render0.set_property("xalign", 1.0)
        render0.set_property("visible", False)
        render1 = Gtk.CellRendererText()
        render1.set_property("xalign", 0)
        render2 = Gtk.CellRendererText()
        render2.set_property("xalign", 1.0)
        render2.set_property("editable", True)
        render2.connect('edited', self.col2_edited_cb, self.lista)
        render3 = Gtk.CellRendererText()
        render3.set_property("xalign", 1.0)
        render3.set_property("editable", True)
        render3.connect('edited', self.col3_edited_cb, self.lista)
        render4 = Gtk.CellRendererText()
        render4.set_property("xalign", 1.0)
        render5 = Gtk.CellRendererText()
        render5.set_property("xalign", 1.0)
        SqlNom = SqlNominas(self.lanomina)
        #devengos = SqlNom.ver_devengos(self.trabajador, self.mes, self.anio)
        # self.tabla = Gtk.Table(len(devengos[0]),len(devengos))
        lista_devengos = SqlNom.lista_devengos_nomina() + SqlNom.lista_pagas_extras()
        for k in lista_devengos:
            contenido = []
            devengo = Nomina_Devengo(k[0])
            #for l in k:
                # entrada = Gtk.Label(devengos[t][p])
                # self.tabla.attach(entrada,p,p+1,t,t+1)
                # entrada.show()
                # print "Dev",devengos[t][p],t, p
            #if isinstance(devengo.precio, float):
            #        l = "{0:,.2f}".format(l)
            decimales = '{0:,.2f}'
            contenido.append(devengo.id)
            contenido.append(devengo.concepto)
            contenido.append(decimales.format(devengo.cuantia))
            contenido.append(decimales.format(devengo.precio))
            contenido.append(decimales.format(devengo.devengado))
            contenido.append(decimales.format(devengo.deducido))
            self.lista.append(contenido)
        self.vista.set_model(self.lista)
        col1 = Gtk.TreeViewColumn("Num.", render0, text=0)
        col2 = Gtk.TreeViewColumn("Concepto", render1, text=1)
        col3 = Gtk.TreeViewColumn("Cant.", render2, text=2)
        col4 = Gtk.TreeViewColumn("Precio", render3, text=3)
        col5 = Gtk.TreeViewColumn("Devengo", render4, text=4)
        col6 = Gtk.TreeViewColumn("Deduccion", render5, text=5)
        self.vista.append_column(col1)
        self.vista.append_column(col2)
        self.vista.append_column(col3)
        self.vista.append_column(col4)
        self.vista.append_column(col5)
        self.vista.append_column(col6)
        self.vista.set_search_column(0)
        cabecera = SqlNom.ver_nomina(self.trabajador, self.mes, self.anio)
        self.lcif.set_text(SqlNom.cif)
        self.lcontrato.set_text(SqlNom.contrato.contrato.descripcion)
        ldir = SqlNom.cta_cot.centro_trabajo.dir_calle + ', ' + SqlNom.cta_cot.centro_trabajo.dir_numero
        self.ldireccion.set_text(ldir)
        self.lhoras.set_text(unicode(SqlNom.horas_cotizadas()))
        self.lidcontrato.set_text(unicode(SqlNom.contrato.codigo))
        self.lidnomina.set_text(unicode(SqlNom.id))
        self.lnaf.set_text(SqlNom.naf)
        self.lnif.set_text(SqlNom.nif)
        self.lncc.set_text(SqlNom.cta_cot.cuenta_cotizacion)
        self.lnumcontrato.set_text(unicode(SqlNom.contrato.idcontrato))
        self.lperiodo.set_text("Del " + SqlNom.periodo)
        try:
            self.lppextra.set_text("{:,.2f}".format(SqlNom.base_ppextra))
            self.lremuneracion.set_text("{:,.2f}".format(SqlNom.imp_remumes))
        except:
            pass
        self.lpuesto.set_text(SqlNom.puesto)
        self.lempresa.set_text(SqlNom.nombreempresa)
        self.ld.set_text(unicode(SqlNom.dias_cotizados()))
        self.lantiguedad.set_text(str(cabecera[2]))
        if SqlNom.contrato.contrato.es_tiempo_parcial:
            self.rb_es_tpoparcial.set_active(True)
        elif SqlNom.contrato.contrato.es_tiempo_completo:
            self.rb_es_tpocompleto.set_active(True)
        if SqlNom.contrato.contrato.es_indefinido:
            self.rb_es_indefinido.set_active(True)
        elif SqlNom.contrato.contrato.es_temporal:
            self.rb_es_temporal.set_active(True)
        self.ltrabajador.set_text(SqlNom.nombre_trabajador)
        self.lb_irpf.set_text("{:,.2f}".format(SqlNom.base_irpf))
        self.lliquido.set_text('{:,.2f}'.format(SqlNom.liquido))
        self.lb_segsoc.set_text("{:,.2f}".format(SqlNom.base_cc))
        self.vista.show()
        seleccion = self.vista.get_selection().get_selected()
        # self.tabla.show()
        # self.box14.add(self.tabla)
        self.box14.show()

    def on_bEliminar_clicked(self, button, data=None):
        SqlNominas(self.lanomina).borrar_nomina()
        self.nomina()

    def on_bCancela_clicked(self, button, data=None):
        self.window3.destroy()

    def on_window3_destroy(self, objecto, data=None):
        self.window3.destroy()

    def col2_edited_cb(self, celda, ruta, nuevo_texto, lista):
        lista[ruta][2] = nuevo_texto
        coef1 = float(lista[ruta][2])
        coef2 = float(lista[ruta][3])
        resultado = coef1 * coef2
        lista[ruta][4] = "{0:,.2f}".format(resultado)
        return

    def col3_edited_cb(self, celda, ruta, nuevo_texto, lista):
        lista[ruta][3] = nuevo_texto
        coef1 = float(lista[ruta][2])
        coef2 = float(lista[ruta][3])
        resultado = coef1 * coef2
        lista[ruta][4] = "{0:,.2f}".format(resultado)
        return

    def on_bAcepta_clicked(self, button, data=None):
        for x in self.lista:
            y = ['', '', '', '', '']
            devengo = Nomina_Devengo(x[0])
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            print "Precio y cuantia",devengo.cuantia, devengo.precio,
            y[2] = locale.atof(x[2])
            y[3] = locale.atof(x[3])
            y[4] = locale.atof(x[4])
            devengo.ac_campo('imp_cuantia',y[2])
            devengo.ac_campo('imp_precio', y[3])
            devengo.ac_campo('imp_devengo', y[4])
            print devengo.precio, devengo.cuantia
        calcular = CalcNomina(self.laempresa, self.mes, self.anio)
        calcular.update_devengos(self.lanomina)
        for x in self.vista.get_columns():
            self.vista.remove_column(x)
        self.lista.clear()
        self.nomina()
        return

    def on_bImpNom_clicked(self, button, data=None):
        # self.grabarfichero1.show()
        self.canvas = canvas.Canvas("nomina.pdf", pagesize=A4)
        impr_nomina(self.canvas,
                    self.laempresa,
                    self.mes,
                    self.anio,
                    self.fornom,
                    self.lanomina)
#    width, height = A4
        self.canvas.save()
        # self.anio.set_text("")
        # self.dialImprimir = dialImprimir()
        print os.name
        os.system("/usr/bin/evince nomina.pdf")

    def on_rbduracion(self, button):
        if button.get_active():
            state = "on"
        else:
            state = "off"

    def on_rbjornada(self, button):
        if button.get_active():
            state = "on"
        else:
            state = "off"
