#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 04/10/2015

@author: miguelangel
"""
from Funciones.funs import select_sql


class Cabecera:
    """
    classdocs
    """

    def __init__(self, idempresa, mes, anio, idtrabajador=0):
        """
        Constructor
        """
        self.empresa_id = idempresa
        self.mes = mes
        self.anio = anio
        self.trabajador_id = idtrabajador

    def nomina(self, esnomina=True, esfiniquito=False, esnompextra=False):
        """

        Nos devuelve todos los datos de la cabecera de una nomina en una lista

            SqlNominas().cabecera_nomina(numero_empresa, mes, anio)

        Orden de los datos:
            [0] numero de empresa
            [1] numero de contrato
            [2] numero de grupo de cotizacion
            [3] numero de epigrafe
            [4] fecha antiguedad
            [5] neto a percibir
            [6] numero de afiliacion del trabajador
            [7] numero de grupo de cotizacion
            [8] numero de epigrafe
            [9] matricula
           [10] nombre completo del trabajador
           [11] categoria profesional
           [12] nif del trabajador
           [13] nombre completo de la empresa o empresario
           [14] direccion de la empresa
           [15] codigo de cotizacion
           [16] cif de la empresa
           [17] fecha fin de contrato
           [18] es finiquito
        """
        sql = ( "SELECT "
                "   emp_contratos.idempresa, emp_contratos.idemp_contratos, "
                "   emp_contratos.idgrupos_cotizacion, emp_contratos.idtb_epigrafe, "
                "   emp_contratos.fecha_ini, neto, Trabajadores.naf, "
                "   idgrupos_cotizacion, idtb_epigrafe, matricula, "
                "   CONCAT_WS(' ',Trabajadores.nombre,Trabajadores.apellido1, "
                "             Trabajadores.apellido2) as nombre, "
                "   categoria_profesional, Trabajadores.nif, "
                "   CONCAT_WS(' ',empresa.nombre, empresa.apellido1, empresa.apellido2) as nombre, "
                "   empresa.dir, emp_ctacot.ncc, empresa.cif, "
                "   date(emp_contratos.fecha_fin) as diafin, "
                "   emp_ctacot.idctacot "
                "FROM "
                "   Nominas.emp_contratos "
                "       left join "
                "           Trabajadores "
                "           On Trabajadores.idTrabajadores = emp_contratos.idtrabajadores "
                "       left join "
                "           empresa "
                "           On empresa.idempresa = emp_contratos.idempresa "
                "       left join "
                "           emp_ctacot "
                "           On emp_ctacot.idctacot = emp_contratos.idemp_ctacot "
                "WHERE "
                "   emp_contratos.idempresa = %s "
                "   and (fecha_fin is null "
                "        or (month(fecha_fin) >= %s and year(fecha_fin)>= %s) "
                "        or (month(fecha_fin) < %s and year(fecha_fin)> %s) "
                "       ) "
                "   and ( "
                "        (month(fecha_ini) <= %s and year(fecha_ini)<= %s) "
                "         or (month(fecha_ini)>%s and year(fecha_ini)<%s) "
                "       ) "
                "   and emp_contratos.conversion is Null "
                "   and emp_contratos.prorroga is Null ")
        if self.trabajador_id > 0:
            sql = sql + "and emp_contratos.idTrabajadores = "+ unicode(self.trabajador_id) +" "
        if esnomina:
            pass
        elif esfiniquito:
            sql = sql + ' and (emp_contratos.idtb_contrato_baja >0)'
        elif esnompextra:
            pass
        dato = select_sql((sql, (self.empresa_id, self.mes, self.anio, self.mes, self.anio,
                                 self.mes, self.anio, self.mes, self.anio)), True)
        return dato