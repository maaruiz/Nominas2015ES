'''
Created on 24/09/2015

@author: miguelangel
'''
from Funciones.funs import sql_basica, si_no, select_sql


class Convenio:
    def __init__(self, idconvenio):
        self.id = idconvenio
        self.descripcion = self.dato_convenio('descripcion')
        self.codigo = self.dato_convenio('codigo')

    def dato_convenio(self, campo):
        dato = sql_basica(campo, 'tb_convenios', 'idtb_convenio', self.id)
        return dato


class Convenio_datos:
    """

    """
    def __init__(self, indice):
        self.id = indice
        self.convenio_id = self.dato_convenio_datos('idtb_convenio')
        self.convenio = Convenio(self.convenio_id)
        self.dias_efectivos_anio = self.dato_convenio_datos('diasefectivos_anio')
        self.ejercicio = self.dato_convenio_datos('ejercicio')
        self.es_sab_laboral = si_no(self.dato_convenio_datos('convert(essab_laboral, unsigned)'))
        self.fecha_final = self.dato_convenio_datos('fecha_fin')
        self.fecha_inicial = self.dato_convenio_datos('fecha_ini')
        self.horas_anio = self.dato_convenio_datos('horas_anio')
        self.horas_semana = self.dato_convenio_datos('horas_semana')
        self.horas_dia = self.dato_convenio_datos('horas_dia')
        self.vacaciones_id = self.dato_convenio_datos('idtb_vacaciones')
        self.vacaciones = Vacaciones(self.vacaciones_id)

    def dato_convenio_datos(self, campo):
        dato = sql_basica(campo, 'tb_convenio_datos', 'idtb_convenio_datos', self.id)
        return dato

    def num_dias_pextra(self):
        sql = ("Select "
               "   sum(dias) "
               "From "
               "   tb_convenios_pextra "
               "Where "
               "   idtb_convenio = " + unicode(self.convenio_id))
        return int(select_sql(sql)[0])

    def num_pextra(self):
        sql = ("Select "
               "   count(*) "
               "From "
               "   tb_convenios_pextra "
               "Where "
               "   idtb_convenio = " + unicode(self.convenio_id))
        return int(select_sql(sql)[0])


class Convenio_pextra:
    def __init__(self, idconvenio_pextra):
        self.id = idconvenio_pextra
        self.convenio_id = self.dato_convenio_pextra('idtb_convenio')
        self.mes_pago = self.dato_convenio_pextra('mes')
        self.concepto = self.dato_convenio_pextra('concepto')
        self.coeficiente = self.dato_convenio_pextra('coeficiente')
        self.importe = self.dato_convenio_pextra('importe')
        self.dias = self.dato_convenio_pextra('dias')
        self.convenio_datos_id = self.dato_convenio_pextra('idtb_convenio_datos')
        self.convenio = Convenio(self.convenio_id)
        self.convenio_datos = Convenio_datos(self.convenio_datos_id)

    def dato_convenio_pextra(self, campo):
        dato = sql_basica(campo, 'tb_convenios_pextra', 'idtb_convenio_pextra', self.id)
        return dato


class Vacaciones:
    def __init__(self, idvacaciones):
        self.id = idvacaciones
        self.descripcion = self.dato_vacaciones('descripcion')
        self.dias_vacaciones = self.dato_vacaciones('cantidad')
        self.dias_vacaciones_min = self.dato_vacaciones('cantidad_min')
        self.es_dias_laborales = si_no(self.dato_vacaciones('esdias_laborales'))
        self.es_dias_laborales_min = si_no(self.dato_vacaciones('esmindias_laborales'))
        self.es_dias_naturales = si_no(self.dato_vacaciones('esdias_naturales'))
        self.es_dias_naturales_min = si_no(self.dato_vacaciones('esmindias_naturales'))

    def dato_vacaciones(self, campo):
        dato = sql_basica(campo, 'tb_vacaciones', 'idtb_vacaciones', self.id)
        return dato
