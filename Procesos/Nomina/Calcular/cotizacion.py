#!/usr/bin/python
# -*- coding: utf-8 -*-
from Funciones.Datos.contrato_dat import Contrato, Contrato_Devengo

from Funciones.Datos.empresa_dat import It_registro
from Funciones.Datos.segsocial_dat import Grupo_cotizacion_bases
from Funciones.Datos.calendario_dat import Calendario
from Funciones.Datos.nomina_dat import SqlNominas, Nomina_Devengo
from Funciones.funs import select_sql



##################################
##### CLASE CALCULO NOMINAS  #####
##################################

class Bases:
    '''
    :return:
    '''
    def __init__(self, nomina):
        self.id = nomina
        self.nomina = SqlNominas(self.id)
        self.grupo_cot_id = self.nomina.grupo_cotizacion_id
        self.anio = self.nomina.fecha_anio
        self.mes = self.nomina.fecha_mes
        self.contrato_id = self.nomina.contrato_id
        self.cta_cot_id = self.nomina.cta_cot_id
        self.coef_pextra = self.nomina.cta_cot.coef_pextra
        self.lista_devengos = self.nomina.lista_devengos_nomina()
        self.lista_pextra = self.nomina.lista_pagas_extras()
        self.calendario = Calendario(self.cta_cot_id, self.anio)
        self.bases_cotizacion()

    def __call__(self, nomina):
        self.__init__(nomina)

    def bases_cotizacion(self):
        '''
        :return:
        '''
        self.base_irpf = 0
        self.base_remuneracion = 0
        self.base_irpf_especie = 0
        self.base_ppextra = 0
        self.base_irpf_segsoc = 0
        self.base_segsoc_sinirpf = 0
        self.base_irpf_sinsegsoc = 0
        self.no_cotizan = 0
        self.nomina.actualiza_ppextra()
        self.nomina = SqlNominas(self.id)
        self.base_ppextra = self.nomina.base_ppextra
        # Para calcular las bases de cotización distinguimos entre devengos y pagas extras
        # Comprobamos que los devengos cotizan a la seguridad social al igual que las pagas extras
        # Comprobamos que los devengos cotizan en el IRPF al igual que las pagas extras
        # Los prorrateos de pagas extras se calculan en SqlNominas.devengo_ppextra()
        for x in (self.lista_devengos + self.lista_pextra):
            devengo = Nomina_Devengo(x[0])
            print '    ....****>>>> Devengo/segsoc/irpf', devengo.concepto, devengo.cotiza_segsocial, devengo.cotiza_irpf
            if devengo.cotiza_segsocial:
                    self.base_remuneracion = self.base_remuneracion + devengo.devengado
            if devengo.cotiza_irpf:
                if devengo.es_devengo_especie:
                    self.base_irpf_especie = self.base_irpf_especie + devengo.devengado
                else:
                    self.base_irpf = self.base_irpf + devengo.devengado
            if devengo.cotiza_irpf and devengo.cotiza_segsocial:
                self.base_irpf_segsoc = self.base_irpf_segsoc + devengo.devengado
            if not devengo.cotiza_irpf and devengo.cotiza_segsocial:
                self.base_segsoc_sinirpf = self.base_segsoc_sinirpf + devengo.devengado
            if devengo.cotiza_irpf and not devengo.cotiza_segsocial:
                self.base_irpf_sinsegsoc = self.base_irpf_sinsegsoc + devengo.devengado
            if not devengo.cotiza_irpf and not devengo.cotiza_segsocial:
                self.no_cotizan = self.no_cotizan + devengo.devengado

        self.base_segsocial = self.base_ppextra + self.base_remuneracion


    def base_it(self):
        base_it_tot = 0
        try:
            self.it_nomina = It_nomina(self.id)
            self.dias_pendientes = self.it_nomina.it_dias_pendientes
            dias_acumulados = self.it_nomina.it_dias_acumulados
            dias_aplicados = dias_acumulados - self.dias_pendientes
            base_it_dia = self.it_nomina.it.basecot_diaria_it
            if self.it_nomina.it.es_cont_comun:
                sql = ( "Select "
                            "desdedia, hastadia, porcentaje "
                        "From "
                            "tb_it "
                        "Where "
                            "es_contcomun "
                            "order by desdedia ")
                dato = select_sql(sql,1)
                for j in dato:
                    if j[0] >= dias_aplicados and self.dias_pendientes >0:
                        if (j[1]-j[0]+1) >= self.dias_pendientes:
                            base_it_tot += base_it_dia * j[2] * self.dias_pendientes
                            dias_aplicados = dias_aplicados + self.dias_pendientes
                            self.dias_pendientes = self.dias_pendientes - self.dias_pendientes
                        else:
                            base_it_tot += base_it_dia * j[2] * (j[1] - j[0] + 1)
                            dias_aplicados = dias_aplicados + j[1]-j[0]+1
                            self.dias_pendientes -= dias_aplicados
            if self.it_registro.es_enfermedad_prof:
                pass
        except:
            pass
        return base_it_tot

    def no_cotizan(self):
        """
        Devengos que no cotizan ni en seguridad social ni en irpf
        """
        sql = ( "SELECT "
                    "sum(imp_devengo) as importe "
                "FROM "
                    "nomina_devengos "
                "WHERE "
                    "esdevengo "
                    "and (not cont_com "
                    "AND not irpf) "
                    "and idnomina = %s;")
        dato = select_sql((sql, (self.id)))[0]
        if dato is None:
            dato = 0
        return dato

    def control_base_min_max(self):
        sql = ( "Select "
                    "B.idtb_grupocot_base "
                "From "
                    "tb_grupos_cotizacion A "
                        "inner join "
                            "tb_gruposcot_bases B"
                            "on A.idgrupos_cotizacion = B.idtb_grupo_cotizacion "
                "Where "
                    "A.idgrupos_cotizacion = %s "
                    "and B.ejercicio = %s ")
        dato = select_sql((sql, (self.grupo_cot_id, self.anio)))[0]
        self.grupo_cot_bases = Grupo_cotizacion_bases(dato)



class It_nomina:
    def __init__(self, nomina):
        """
        Gestiona el cálculo de la IT del trabajador respecto de una nomina dada
        """
        self.id = nomina
        self.SqlNom = SqlNominas(self.id)
        self.mes = self.SqlNom.fecha_mes
        self.anio = self.SqlNom.fecha_anio
        self.it = It_registro(self.buscar_it_nomina())
        self.it_fechas_mes = self.it.periodo_it(self.anio, self.mes)
        self.it_fecha_inicial = self.it_fechas_mes[0]
        self.it_fecha_final = self.it_fechas_mes[1]
        self.it_dias_mes = (self.it_fecha_final - self.it_fecha_final).days + 1
        self.it_fechas_acumulado_total = self.it.periodo_it(self.anio, self.mes, True)
        self.it_dias_acumulados = (self.it_fechas_acumulado_total[1]-self.it_fechas_acumulado_total[0]).days + 1
        self.it_dias_pendientes = self.it_dias_acumulados
    def buscar_it_nomina(self):
        sql = ( "Select "
                    "idemp_it "
                "From "
                    "emp_it "
                "Where "
                    "idemp_contrato = " + unicode(self.SqlNom.contrato.id) + " "
                    "and fecha_baja >= '" + self.SqlNom.contrato.inicio_fecha.isoformat() + "' "
                    "and (fecha_alta is null "
                         "or ((month(fecha_alta) >= " + unicode(self.SqlNom.fecha_mes) + " "
                              "and year(fecha_alta) >= " + unicode(self.SqlNom.fecha_anio) +") "
                         "and (month(fecha_baja) <= " + unicode(self.SqlNom.fecha_mes) +" "
                              "and year(fecha_baja) <= " + unicode(self.SqlNom.fecha_anio) +")))")
        return select_sql(sql)[0]
    def devengo(self):
        self.it.basecot_diaria_it
        pass

