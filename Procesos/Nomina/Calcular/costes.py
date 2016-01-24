#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 04/10/2015

@author: miguelangel
"""
from Procesos.Nomina.Calcular.cotizacion import Bases
from Funciones.Datos.contrato_dat import Contrato
from Funciones.funs import select_sql


class CostesSegSocial:
    """
    Para hacer el cálculo de las deducciones de una nómina es necesario
    que previamente se hayan introducido los devengos de esa nómina
        Se necesitan:
            1. la nómina en cuestión
            2. los datos del contrato para conocer el tipo de contrato que es
            3. los tipos de cotización a aplicar al contrato
    """
    def __init__(self,nomina):
        self.id = nomina
        self.bases = Bases(self.id)
        self.contrato = Contrato(self.bases.nomina.contrato_id)
        self.sql = ("Select "
                        "empresa, trabajador "
                    "From "
                        "tb_tiposcot A "
                            "inner join "
                                "tb_tiposcot_ejercicio B "
                            "on A.idtb_tiposcot = B.idtb_tipocot "
                    "Where "
                        "B.ejercicio = %s ")
        if self.contrato.contrato.es_indefinido:
            self.sql += "and A.es_dura_indefinida "
        elif self.contrato.contrato.es_temporal:
            self.sql += "and A.es_dura_determinada "
        elif self.contrato.contrato.es_tiempo_completo:
            self.sql += "and A.es_tpo_completo "
        elif self.contrato.contrato.es_tiempo_parcial:
            self.sql += "and A.es_tpo_parcial "
        self.tipo_ccomun_emp = self.tipos_cont_comun()[0]
        self.tipo_ccomun_trab = self.tipos_cont_comun()[1]
        self.tipo_desempleo_emp = self.tipos_desempleo()[0]
        self.tipo_desempleo_trab = self.tipos_desempleo()[1]
        self.tipo_fp_emp = self.tipos_formacion_prof()[0]
        self.tipo_fp_trab = self.tipos_formacion_prof()[1]
        self.tipo_fogasa_emp = self.tipos_fogasa()[0]
        self.tipo_fogasa_trab = self.tipos_fogasa()[1]

        self.base_cotizacion = self.bases.base_segsocial
        self.cont_comun_empresa = round(self.tipo_ccomun_emp * self.base_cotizacion / 100, 2)
        self.cont_comun_trabajador = round(self.tipo_ccomun_trab * self.base_cotizacion / 100, 2)
        self.desempleo_empresa = round(self.tipo_desempleo_emp * self.base_cotizacion / 100, 2)
        self.desempleo_trabajador = round(self.tipo_desempleo_trab * self.base_cotizacion / 100, 2)
        self.formacion_prof_emp = round(self.tipo_fp_emp * self.base_cotizacion / 100, 2)
        self.formacion_prof_trab = round(self.tipo_fp_trab * self.base_cotizacion / 100, 2)
        self.fogasa_emp = round(self.tipo_fogasa_emp * self.base_cotizacion / 100, 2)
        self.fogasa_trabajador = round(self.tipo_fogasa_trab * self.base_cotizacion / 100, 2)
        self.segsocial_empresa = (self.cont_comun_empresa + self.desempleo_empresa +
                                  self.formacion_prof_emp + self.fogasa_emp)
        self.total_aportacion = (self.cont_comun_trabajador +
                                 self.desempleo_trabajador +
                                 self.formacion_prof_trab ) #+ self.horasextras())
        #self.total_deduccion = (self.total_aportacion + self.irpf_dineraria() +
        #                        self.irpf_especie() + self.anticipos() +
        #                        self.valor_especie() + self.otras_deducciones())
        self.sql = ( "Select "
                        "empresa, trabajador "
                    "From "
                        "tb_tiposcot A "
                            "inner join "
                                "tb_tiposcot_ejercicio B "
                            "on A.idtb_tiposcot = B.idtb_tipocot "
                    "Where "
                        "B.ejercicio = %s ")
        if self.contrato.contrato.es_indefinido:
            self.sql += "and A.es_dura_indefinida "
        elif self.contrato.contrato.es_temporal:
            self.sql += "and A.es_dura_determinada "
        elif self.contrato.contrato.es_tiempo_completo:
            self.sql += "and A.es_tpo_completo "
        elif self.contrato.contrato.es_tiempo_parcial:
            self.sql += "and A.es_tpo_parcial "

    def __call__(self, nomina):
        self.__init__(nomina)

    def tipos_cont_comun(self):
        sql = self.sql + "and A.es_contcomun "
        try:
            dato = select_sql((sql, (self.bases.nomina.fecha_anio)))
        except:
            dato = (0,0)
        return dato

    def tipos_desempleo(self):
        sql = self.sql +  "and A.es_desempleo "
        try:
            dato = select_sql((sql, (self.bases.nomina.fecha_anio)))
        except:
            dato = (0,0)
        return dato

    def tipos_formacion_prof(self):
        sql = self.sql +  "and A.es_formprof "
        try:
            dato = select_sql((sql, (self.bases.nomina.fecha_anio)))
        except:
            dato = (0,0)
        return dato

    def tipos_fogasa(self):
        sql = self.sql +  "and A.es_fogasa "
        try:
            dato = select_sql((sql, (self.bases.nomina.fecha_anio)))
        except:
            dato = (0,0)
        return dato

    def tipos_horasextras_fmayor(self):
        sql = self.sql +  "and A.es_hora_extra_fmayor "
        try:
            dato = select_sql((sql, (self.bases.nomina.fecha_anio)))
        except:
            dato = (0,0)
        return dato