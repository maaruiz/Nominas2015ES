#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import locale
from gi.repository import Gtk

from Funciones.funs import select_sql, Basedatos, ultimodiames
from Funciones.Datos.nomina_dat import SqlNominas, Nomina_Devengo
from Funciones.Datos.contrato_dat import Contrato
from Procesos.Nomina.Editar.nuevo import Alta
from Procesos.Nomina.Calcular.costes import CostesSegSocial
from Procesos.Nomina.Editar.actualizar import Actualizar
from Procesos.Nomina.Editar.eliminar import NomBorrar


# -----------------------------------
# ----- CLASE CALCULO NOMINAS  ------
# -----------------------------------


class CalcNomina:
    """
    Proceso que calcula las nóminas de una empresa en un mes y en un anio
    concretos
    """

    def __init__(self, empresa, mes, anio, esnomina=True, esfiniquito=False, esnominapextra=False):
        self.empresa = empresa
        self.dia = ultimodiames(mes, anio)
        self.mes = mes
        self.anio = anio
        self.nomina = SqlNominas(0)
        self.NomDev = Nomina_Devengo
        self.num_nominas = Contrato(0).contratos_activos_mes(self.empresa, self.anio, self.mes)
        self.fecha = str(self.anio) + "-" + str(self.mes) + "-" + str(self.dia)
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        self.estemes = time.strftime("%B", time.strptime(str(self.mes) + ',' + str(self.anio), '%m,%Y'))
        self.esnomina = esnomina
        self.esfiniquito = esfiniquito
        self.esnominapextra = esnominapextra
        self.borrarnominas = NomBorrar(self.empresa, self.mes, self.anio, 0, self.esnomina, self.esfiniquito,
                                       self.esnominapextra)
        print "Empieza el calculo ..."

    def calcular(self):
        """
        El proceso de calcular raliza 3 tareas:
           1. Elimina los registros de la nómina a calcular si los hubiera
           2. Inserta los nuevos registros de la nómina a calcular tomando
              los datos de:
              a) los devengos de la empresa
              b) los dias de it de los trabajadores en la empresa
              c) pagas extras de la empresa
           3. Realiza el cálculo de todos los devengos y deducciones
        """
        self.borrarnominas.borrar_mes()
        self.alta_nomina = Alta(self.mes, self.anio, self.empresa, 0, self.esnomina, self.esfiniquito,
                                self.esnominapextra)
        self.recalcular()
        return

    def recalcular(self):
        try:
            nominas = self.nomina.nominas_empresa_mes(self.empresa, self.mes,
                                                      self.anio, self.esnomina, self.esfiniquito, self.esnominapextra)
            print "****************************  Recalculando  ******************"
            try:
                for j in nominas:
                    self.update_devengos(j[0])
            except:
                md = Gtk.MessageDialog(None, Gtk.DIALOG_DESTROY_WITH_PARENT,
                                       Gtk.MESSAGE_ERROR, Gtk.BUTTONS_CLOSE, "Error, no se pudo conectar")
                pass
        except:
            print "No se ha recalculado...."

    def actual_dietas(self, nomina):
        # --------- Calculo de las dietas dado un importe fijo neto
        SN = SqlNominas(nomina)
        neto = SN.contrato.liquido_a_cobrar
        if neto > 0:
            self.calc_dietas(nomina)
            print "Volvemos a actualizar"
            Actualizar(nomina)
        else:
            print "    No hay dietas ...."

    def calc_minimos_cotizacion(self, nomina, base_cot):
        # --------- Calculo de las bases minimas de cotizacion
        horas_cot = self.nomina.horas_cotizadas()
        dias_cot = self.nomina.dias_cotizados()
        if horas_cot:
            sql = ("SELECT tb_grupos_cotizacion.base_min_hora, nominas.base_cc "
                   "FROM Nominas.nominas "
                   "left join tb_grupos_cotizacion "
                   "on nominas.idgrupos_cotizacion = tb_grupos_cotizacion.idgrupos_cotizacion "
                   "where nominas.idnomina = %s;")
            base_min = select_sql((sql, (nomina)))[0]
            if base_cot / horas_cot < base_min:
                base_cot = base_min * horas_cot
        elif dias_cot:
            sql = ("SELECT tb_grupos_cotizacion.base_min_dia, nominas.base_cc "
                   "FROM Nominas.nominas "
                   "left join tb_grupos_cotizacion "
                   "on nominas.idgrupos_cotizacion = tb_grupos_cotizacion.idgrupos_cotizacion "
                   "where nominas.idnomina = %s;")
            base_min = select_sql((sql, (nomina)))[0]
            if base_cot / dias_cot < base_min:
                base_cot = base_min * dias_cot
        return base_cot

    def calc_liquido(self, nomina):
        # ------------ Calculo Total Liquido
        self.nomina(nomina)
        self.liquido = self.nomina.actualiza_liquido(nomina)
        if self.liquido == 0:
            sql = ("UPDATE nominas "
                   "SET liquido = imp_totdev - tot_deducir "
                   "WHERE idnomina = %s ")
            select_sql((sql, (nomina)))

    # Calculo nuevo de los devengos de las nominas
    def update_devengos(self, nomina):
        print "Actualizamos precios, cuantias y devengos ....", nomina
        self.actualizar = Actualizar(nomina)

        print "Calcula dietas ..."
        self.actual_dietas(nomina)

        print "Calcula liquido nomina ..."
        self.calc_liquido(nomina)

    def calc_dietas(self, nomina):
        """
         Se tienen en cuenta:
       1. Bases que cotizan en seg.social e irpf (incluidas las pagas extras)
       2. Bases que solo cotizan en seg. social o irpf
       3. Bases que no cotizan ni en seg.social ni en irpf
       4. Bases para las pagas extras
       5. Tipos de cotizacion
        """
        bd = Basedatos()
        cursor = bd.conectar()
        # -----------   1. Bases que cotizan en seg.social e irpf
        costes = CostesSegSocial(nomina)
        self.b_segsoc_irpf = costes.bases.base_irpf_segsoc
        print "    Base segsoc, irpf", self.b_segsoc_irpf
        if not self.b_segsoc_irpf:
            self.b_segsoc_irpf = 0

        # ------------  2a. Bases que cotizan solo en seg.social
        self.b_segsoc = costes.bases.base_segsoc_sinirpf
        print "    Base segsoc", self.b_segsoc
        if not self.b_segsoc:
            self.b_segsoc = 0

        # ------------   2b. Bases que cotizan solo en irpf
        self.b_irpf = costes.bases.base_irpf_sinsegsoc
        print "    Base irpf", self.b_irpf
        if not self.b_irpf:
            self.b_irpf = 0

        # ------------   3. Bases que no cotizan ni en seg.social ni en irpf
        self.base = costes.bases.no_cotizan
        print "    Bases ", self.base
        if not self.base:
            self.base = 0

        # ------------  Tipos de cotizacion seg. social
        self.tipo_segsoc = costes.tipo_ccomun_trab
        self.tipo_segsoc = self.tipo_segsoc + costes.tipo_desempleo_trab
        self.tipo_segsoc = self.tipo_segsoc + costes.tipo_fp_trab
        self.tipo_segsoc /= 100
        print "    Tipo seg_social ", self.tipo_segsoc

        # -----------  Tipos de irpf
        self.tipo_irpf = self.nomina.tipo_irpf(nomina) / 100
        print "    Tipo irpf ", self.tipo_irpf

        # ----------  Calculo de dietas
        SN = SqlNominas(nomina)
        devengo = costes.bases.nomina.total_devengos
        print "    ********* Devengo", devengo
        neto = SN.contrato.liquido_a_cobrar
        print "    ********* Neto", neto
        basess = costes.base_cotizacion
        baseirpf = costes.bases.base_irpf
        """
        self.dietas = (self.neto - (self.b_segsoc_irpf *
                     (1 - self.tipo_segsoc - self.tipo_irpf)) -
                      (self.b_segsoc * (1 - self.tipo_segsoc)) +
                      (self.ppextra * self.tipo_segsoc) -
                      (self.b_irpf * (1 - self.tipo_irpf)) -
                      self.base)
        """
        self.dietas = (neto - devengo + basess * self.tipo_segsoc + baseirpf * self.tipo_irpf) / (
                        1 - self.tipo_segsoc - self.tipo_irpf)
        print "    Dietas", self.dietas
        sql = ("SELECT irpf, cont_com "
               "FROM nomina_devengos "
               "WHERE esdieta and idnomina = %s;")
        cursor.execute(sql, (nomina))
        self.coef_dieta = cursor.fetchone()
        if self.coef_dieta[0] == '\x00':
            self.tipo_irpf = 0
        if self.coef_dieta[1] == '\x00':
            self.tipo_segsoc = 0
        #self.dietas = self.dietas / (1 - self.tipo_segsoc - self.tipo_irpf)
        sql = ("UPDATE nomina_devengos "
               "SET imp_precio = %s, imp_devengo = %s, importe = %s "
               "WHERE idnomina=%s and esdieta ")
        cursor.execute(sql, (self.dietas, self.dietas, self.dietas, nomina))
        bd.desconectar()
        print "    Fin calculo dietas ... ", self.dietas

# ## Fin calculo de nominas
