#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from Procesos.nomina_calc import calc_nomina
from Procesos.nomina_form import impr_nomina
from Funciones.Datos.empresa_dat import SqlEmpresa,Centro_Trabajo, Cod_cotizacion
from Funciones.Datos.trabajador_dat import SqlTrabajador
from Funciones.Datos.contrato_dat import Contrato, Contrato_codigo
from Funciones.Datos.nomina_dat import SqlNominas
from Procesos.nomina_frontend import vernomina


class nomina:
    def __init__(self, nomina):
        self.idnomina = nomina
        self.datos = SqlNominas(self.idnomina)
        self.anio = self.datos.fecha_anio(self.idnomina)
        self.mes = self.datos.fecha_mes(self.idnomina)
        self.dia_inicial = self.datos.periodos(self.anio, self.mes, self.idnomina)[0]
        self.dia_final = self.datos.periodos(self.anio, self.mes, self.idnomina)[1]
        self.fecha = self.datos.periodos(self.anio, self.mes, self.idnomina)[1]

    def banco_trabajador(self):
        self.iban
        self.entidad
        self.oficina
        self.dc
        self.numero
        self.tlf
    def devengos(self):
        self.concepto
        self.cantidad
        self.importe
        self.total
    def deducciones(self):
        self.cont_comunes_porcentaje
        self.cont_comunes_importe
        self.form_profesional_porcentaje
        self.form_profesional_importe
        self.desempleo_porcentaje
        self.desempleo_importe
        self.irpfdinerarias_porcetaje
        self.irpfdinerarias_importe
        self.irpfespecie_porcentaje
        self.irpfespecie_importe
        self.anticipos
    def bases(self):
        self.rem_mensual
        self.pror_pagasextras
        self.cont_comunes
        self.form_profesional
        self.desempleo
        self.irpf
    def aportacion_empresa(self):
        self.cont_comunes_porcentaje
        self.cont_comunes_importe
        self.desempleo_porcentaje
        self.desempleo_importe
        self.form_profesional_porcentaje
        self.form_profesional_importe
        self.fogasa_porcentaje
        self.fogasa_importe
    def totalnomina(self):
        self.devengado
        self.deducible
        self.liquido
    def calcular(self):
        calc_nomina(self.empresa().id, self.mes, self.anio)
    def imprimir(self):
        SqlNom = SqlNominas()
        self.formulario
        self.canvas = canvas.Canvas("nomina.pdf", pagesize=A4)
        impr_nomina(self.canvas,
                    self.empresa().id,
                    self.mes,
                    self.anio,
                    self.formulario,
                    SqlNom.nomina_trabajador_mes(self.trabajador().id, self.mes, self.anio)
                    )
        self.canvas.save()
        print os.name
        os.system("/usr/bin/evince nomina.pdf")
    def salida_pantalla(self):
        vernomina(self.trabajador.id, self.mes, self.anio, self.formulario)
