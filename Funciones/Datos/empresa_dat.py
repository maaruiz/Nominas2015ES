#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from Funciones.funs import select_sql, sql_basica, Vias, si_no, ultimodiames
from Funciones.Datos.segsocial_dat import Regimen_SegSocial
from Funciones.Datos.convenio_dat import Convenio_datos, Convenio_pextra, Vacaciones
from Funciones.Datos.calendario_dat import Calendario
from Funciones.Datos.contrato_dat import Contrato


class SqlEmpresa:

    def __init__(self, num_empresa = 0):
        if num_empresa == 0:
            self.id = self.primera_empresa()
        else:
            self.id = num_empresa
        self.razon_social = self.dato_empresa("CONCAT_WS(' ', nombre, apellido1, apellido2)")
        self.nombre = self.dato_empresa('nombre')
        self.apellido1 = self.dato_empresa('apellido1')
        self.apellido2 = self.dato_empresa('apellido2')
        self.cif = self.dato_empresa('cif')
        self.dir_calle = self.dato_empresa('dir')
        self.dir_numero = self.dato_empresa('numero')
        self.dir_piso = self.dato_empresa('piso')
        self.cod_postal = self.dato_empresa('cp')
        self.telefono = self.dato_empresa('tlf')
        self.fax = self.dato_empresa('fax')
        self.formato_nomina = self.dato_empresa('idform_nomina')
        self.cod_identificacion = self.dato_empresa('cod_identificacion')
        self.via_id = self.dato_empresa('idtb_vias')
        self.via = Vias(self.via_id).via

    def empresadatos(self, num_empresa):
        # Nombre y apellidos, direccion postal, CIF...
        sql = ("SELECT idempresa, nombre, apellido1, apellido2, cif, dir, "
               "numero, piso, puerta, cp, escif, esnif, esnie "
               "FROM empresa "
               "WHERE idempresa=%s" )
        dato = select_sql((sql,(num_empresa)))
        return dato

    def dato_empresa(self, campo):
        # Retorna el valor de un campo de la empresa
        try:
            dato = sql_basica(campo,'empresa', 'idempresa', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato

    def listacentros(self):
        sql = ("Select num_centro, CONCAT_WS(' ',via, dir, numero) as dir, "
               "cp, Municipio "
               "from emp_centros "
               "inner join t_municipios "
               "on emp_centros.cp = t_municipios.CodPostal "
               "inner join tb_vias "
               "on emp_centros.idtb_vias = tb_vias.idtb_vias "
               "where idempresa = %s "
               "group by num_centro "
               "order by num_centro ")
        dato = select_sql((sql, (self.id)), 1)
        return dato

    def ultima_empresa(self):
        sql = ("Select max(idempresa) from empresa")
        dato = select_sql((sql))[0]
        return dato

    def primera_empresa(self):
        sql = ("Select min(idempresa) from empresa")
        dato = select_sql((sql))[0]
        return dato

    def listaempresas(self):
        sql = ( "Select "
                    "idempresa, "
                    "CONCAT_WS(' ', nombre, apellido1, apellido2) as elnombre "
                "From "
                    "empresa "
                "Order by "
                    "elnombre"
                )
        dato = select_sql(sql, 1)
        return dato

class Centro_Trabajo:
    def __init__(self, idcentro):
        self.id = idcentro
        self.numero_centro = self.dato_centro('num_centro')
        self.empresa_id = self.dato_centro('idempresa')
        self.dir_calle = self.dato_centro('dir')
        self.dir_numero = self.dato_centro('numero')
        self.dir_piso = self.dato_centro('piso')
        self.dir_puerta = self.dato_centro('puerta')
        self.dir_codpostal = self.dato_centro('cp')
        self.dircompleta = self.dir_calle + ', ' + self.dir_numero + ', ' + self.dir_piso + self.dir_puerta

    def dato_centro(self, campo):
        # Retorna el valor de un campo de la empresa
        try:
            dato = sql_basica(campo,'emp_centros', 'idemp_centro', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato

class Cod_cotizacion:
    def __init__(self, idcodigo):
        self.id = idcodigo
        self.num_empresa = self.dato_cotizacion('idempresa')
        self.centro_trabajo_id = self.dato_cotizacion('idemp_centro')
        self.cuenta_cotizacion = self.dato_cotizacion('ncc')
        self.regimen_id = self.dato_cotizacion('idregimen')
        self.convenio_id = self.dato_cotizacion('idtb_convenio')
        self.convenio_datos_id = self.dato_cotizacion('idtb_convenio_datos_actual')
        self.es_formacion = si_no(self.dato_cotizacion('convert(esformacion, unsigned'))
        self.calendario_id = self.dato_cotizacion('idcalendario')
        self.ejercicio_activo = self.dato_cotizacion('ejercicio_actual')
        self.coef_pextra = self.dato_cotizacion('coef_pextra')
        self.empresa = SqlEmpresa(self.num_empresa)
        self.regimen_seg_social = Regimen_SegSocial(self.regimen_id)
        self.centro_trabajo = Centro_Trabajo(self.centro_trabajo_id)
        self.convenio_datos = Convenio_datos(self.convenio_datos_id)
        self.calendario = Calendario(self.calendario_id, self.ejercicio_activo)

    def dato_cotizacion(self, campo):
        # Retorna el valor de un campo de la empresa
        try:
            dato = sql_basica(campo,'emp_ctacot', 'idctacot', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato

class Paga_Extra:
    def __init__(self, idpextra):
        self.id = idpextra
        self.empresa_id = self.dato_pextra('idempresa')
        self.mes_pago = self.dato_pextra('mes')
        self.concepto = self.dato_pextra('concepto')
        self.convenio_pextra_id = self.dato_pextra('idtb_conv_pextra')
        self.convenio_id = self.dato_pextra('idconvenio')
        self.coeficiente = self.dato_pextra('coeficiente')
        self.ctacot_id = self.dato_pextra('idctacot')
        try:
            self.convenio_pextra = Convenio_pextra(self.convenio_pextra_id)
            self.empresa = SqlEmpresa(self.empresa_id)
            self.ctacot = Cod_cotizacion(self.ctacot_id)
        except:
            pass

    def dato_pextra(self, campo):
        try:
            dato = sql_basica(campo, 'emp_pextra', 'idemp_pextra', self.id)
        except:
            dato = 0
        return dato

    def numero_pextras_anio(self):
        sentencia = ("Select "
                        "count(*) "
                    "From "
                        "emp_pextra "
                    "Where "
                        "idempresa = " + unicode(self.empresa_id))
        return select_sql(sentencia)[0]

class It_registro:
    def __init__(self, idit = 0):
        self.id = idit
        self.alta_dia = self.dato_it('dayofmonth(fecha_alta)')
        self.alta_mes = self.dato_it('month(fecha_alta)')
        self.alta_anio = self.dato_it('year(fecha_alta)')
        self.baja_dia = self.dato_it('dayofmonth(fecha_baja)')
        self.baja_mes = self.dato_it('month(fecha_baja)')
        self.baja_anio = self.dato_it('year(fecha_baja)')
        self.baja_fecha = datetime.date(self.baja_anio, self.baja_mes, self.baja_dia)
        self.basecot_mes_anterior = self.dato_it('basecot_mesant')
        self.contrato_id = self.dato_it('idemp_contrato')
        self.dias_cotizados_mes_anterior = self.dato_it('diascot_mesant')
        self.es_cont_comun = si_no(self.dato_it('convert(es_baja_contcomun, unsigned)'))
        self.es_enfermedad_prof = si_no(self.dato_it('convert(es_baja_enfprof,unsigned)'))
        self.basecot_diaria_it = round(self.basecot_mes_anterior / self.dias_cotizados_mes_anterior, 2)
        try:
            self.alta_fecha = datetime.date(self.alta_anio, self.alta_mes, self.alta_dia)
        except:
            self.alta_fecha = None
        self.contrato = Contrato(self.contrato_id)
        self.it_id = self.dato_it('idtb_it')

    def dato_it(self, campo):
        return sql_basica(campo, 'emp_it', 'idemp_it', self.id)

    def registro(self):
        pass

    def periodo_it(self, anio, mes, acumulado = False):
        """
        Calcula el perido de una baja por IT en vigor respecto de las fechas del
        contrato.

        Devuelve una tupla con la fecha de baja y la fecha de alta
        """
        anio = int(anio)
        mes = int(mes)
        if not acumulado:
            d1 = datetime.date(anio, mes, 1)
        else:
            d1 = self.baja_fecha
        d2 = datetime.date(anio, mes, ultimodiames(mes, anio))
        f1 = self.baja_fecha
        if self.alta_fecha is None:
            f2 = d2
        else:
            f2 = self.alta_fecha
            if f2 > d2:
                f2 = d2
        if d1 <= f2 <= d2:
            if f1 < d1:
                f1 = d1
        dato = (f1, f2)
        return dato

class Empresa_Vacaciones:
    def __init__(self, id=0):
        self.id = id
        self.idempresa = self.dato_empvacaciones('idempresa')
        self.idctacot = self.dato_empvacaciones('idemp_ctacot')
        self.idtbvacaciones = self.dato_empvacaciones('idtb_vacaciones')

    def dato_empvacaciones(self, campo):
        return sql_basica(campo, 'emp_vacaciones', 'idemp_vacaciones', self.id)

    def vacaciones_anio(self):
        dato = Vacaciones(self.idtbvacaciones)
        return dato.dias_vacaciones