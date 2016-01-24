"""
Created on 04/10/2015

@author: miguelangel
"""
import locale
import time

from Funciones.funs import select_sql
from Funciones.Datos.nomina_dat import Nomina_Devengo
from Procesos.Nomina.Calcular.costes import CostesSegSocial

class Actualizar:
    '''
    classdocs
    '''


    def __init__(self, nomina = 0):
        '''
        Constructor
        '''
        self.nomina_id = nomina
        self.costes = CostesSegSocial(self.nomina_id)
        self.anio = self.costes.bases.nomina.fecha_anio
        self.mes = self.costes.bases.nomina.fecha_mes
        self.dia = self.costes.bases.nomina.dia_nomina
        self.listadevengos = self.costes.bases.nomina.lista_devengos_nomina()
        self.listadeducciones = self.costes.bases.nomina.lista_deducciones_nomina()
        self.listapextras = self.costes.bases.nomina.lista_pagas_extras()
        self.fecha = self.costes.bases.nomina.actualiza_fecha()
        self.ac_devengos()
        self.ac_periodo()
        self.ac_campo('tot_dias', self.costes.bases.nomina.dias_cotizados())
        self.ac_campo('base_cc', self.costes.bases.base_segsocial)
        self.ac_campo('base_irpf', self.costes.bases.base_irpf)
        self.ac_campo('base_ppextra', self.costes.bases.base_ppextra)
        self.ac_campo('base_dfgsfp', self.costes.bases.base_segsocial)
        self.ac_campo('imp_remumes', self.costes.bases.base_remuneracion)
        if self.costes.bases.nomina.contrato.con_prorrata_pextra:
            self.ac_campo('imp_pextra', self.costes.bases.base_ppextra)
        self.ac_deducciones()
        self.ac_aporta_trabajador()
        self.ac_aportacion_empresa()
        self.ac_totales()

    def ac_aporta_trabajador(self):
        sql = ('UPDATE '
               '    nominas '
               'SET '
               '    imp_aportatrab =  ' + str(self.costes.total_aportacion) +
               ' '
               'WHERE '
               '    idnomina = %s')
        select_sql((sql, (self.nomina_id)))

    def ac_aportacion_empresa(self):
        sql = ( "update "
                    "nominas "
                "set "
                    "tipo_cc_empresa = " + str(self.costes.tipo_ccomun_emp) + ", "
                    "tipo_dp_empresa = " + str(self.costes.tipo_desempleo_emp) + ", "
                    "tipo_fp_empresa = " + str(self.costes.tipo_fp_emp) + ", "
                    "tipo_fgs_empresa = " + str(self.costes.tipo_fogasa_emp) + ", "
                    "imp_cc_empresa = " + str(self.costes.cont_comun_empresa) + ", "
                    "imp_dp_empresa = " + str(self.costes.desempleo_empresa) + ", "
                    "imp_fp_empresa = " + str(self.costes.formacion_prof_emp) + ", "
                    "imp_fgs_empresa = " + str(self.costes.fogasa_emp) + " "
                "where "
                    "nominas.idnomina = %s;")
        select_sql((sql, (self.nomina_id)),1)

    def ac_campo(self, campo, valor):
        sql = ("UPDATE "
                    "nominas "
               "SET " +
                    campo + " = " + unicode(valor) + " "
               "WHERE "
                    "idnomina = " + unicode(self.nomina_id) + " ")
        select_sql(sql)

    def ac_deducciones(self):
        self.total_deducciones = 0
        for ded in self.listadeducciones:
            deducciones = Nomina_Devengo(ded[0])
            self.total_deducciones = self.total_deducciones + deducciones.deducido

    def ac_devengos(self):
        self.total_devengo = 0
        self.pextra = 0
        for dev in self.listadevengos:
            devengo = Nomina_Devengo(dev[0])
            self.total_devengo = self.total_devengo + devengo.devengado
            self.pextra = self.pextra + devengo.paga_extra()
        for pex in self.listapextras:
            pextras = self.pextra
            devpextra = Nomina_Devengo(pex[0])
            pextras = pextras * devpextra.coef_pextra
            cuantia = self.costes.bases.nomina.dias_cotizados()
            devpextra.ac_campo('imp_cuantia', cuantia)
            if not devpextra.es_para_pextra:
                precio = pextras / cuantia
                devpextra.ac_campo('imp_devengo', pextras)
            elif devpextra.es_para_pextra:
                precio = float(devpextra.importe) / float(self.costes.bases.calendario.diastotales)
                devpextra.ac_campo('imp_devengo', round(cuantia * precio, 2))
                self.total_devengo += round(cuantia * precio, 2)
            devpextra.ac_campo('imp_precio', precio)
            devpextra(pex[0])
        if self.costes.bases.nomina.contrato.con_prorrata_pextra:
            self.total_devengo = self.total_devengo + self.costes.bases.base_ppextra
        self.ac_campo('imp_totdev', self.total_devengo)

    def ac_periodo(self):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        estemes = time.strftime("%B", time.strptime(str(self.mes) +
                                         ',' + str(self.anio), '%m,%Y'))
        p = self.costes.bases.nomina.periodos
        p = ("'" +unicode(p[0].day) + " al " + unicode(p[1].day) + " de " +
             unicode(estemes) + " " + unicode(self.anio)+ "'")
        self.ac_campo('periodo', p)
        return p

    def ac_totales(self):
        #----------------- Calculo Total Devengado y Total Deducible
        sql = ("SELECT "
                    "sum(imp_devengo), "
                    "sum(imp_deduccion) "
               "FROM "
                    "nomina_devengos "
               "WHERE "
                    "idnomina = %s;")
        select_sql((sql, (self.nomina_id)))
        sql = ("UPDATE "
                    "nominas "
               "SET "
                    "imp_totdev = %s, "
                    "tot_deducir = %s "
               "WHERE "
                    "idnomina = %s ")
        select_sql((sql, (self.total_devengo, self.total_deducciones, self.nomina_id)))
