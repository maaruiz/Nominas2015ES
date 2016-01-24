from Funciones.funs import sql_basica, si_no, select_sql

class Regimen_SegSocial:
    def __init__(self, idregimen):
        self.idregimen = idregimen
        self.descripcion = self.dato_regsegsocial('descripcion')
        self.codigo = self.dato_regsegsocial('codigo')
    def dato_regsegsocial(self, campo):
        # Retorna el valor de un campo de la empresa
        try:
            dato = sql_basica(campo,'empresa', 'idempresa', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato


class Incapacidad_Temp:
    def __init__(self, idit):
        self.id = idit
        self.regimen_id = self.dato_it('idtb_regimen')
        self.desdedia = self.dato_it('desdedia')
        self.hastadia = self.dato_it('hastadia')
        self.porcentaje = self.dato_it('porcentaje')
        self.es_cont_comun = si_no(self.dato_it('convert(es_contcomun,unsigned)'))
        self.es_enfermedad_prof = si_no(self.dato_it('convert(es_enfprof,unsigned)'))
        self.es_pagoempresa = si_no(self.dato_it('convert(es_pagoempresa,unsigned)'))
        self.es_pagodelegado = si_no(self.dato_it('convert(es_pagodelegado, unsigned)'))
        self.concepto = self.dato_it('concepto')
        self.regimen = Regimen_SegSocial(self.regimen_id)
    def dato_it(self, campo):
        dato = sql_basica(campo, 'tb_it', 'idtb_it', self.id)
        return dato


class Tipo_Cotizacion:
    def __init__(self, idtipo):
        self.id = idtipo
        self.descripcion = self.dato_tipocot('descripcion')
        self.regimen_id = self.dato_tipocot('idregimen_segsocial')
        self.es_cont_comun = si_no(self.dato_tipocot('convert(es_contcomun, unsigned)'))
        self.es_desempleo = si_no(self.dato_tipocot('convert(es_desempleo, unsigned)'))
        self.es_fogasa = si_no(self.dato_tipocot('convert(es_fogasa, unsigned)'))
        self.es_formacion_prof = si_no(self.dato_tipocot('convert(es_formprof, unsigned)'))
        self.es_duracion_determinada = si_no(self.dato_tipocot('convert(es_dura_determinada, unsigned)'))
        self.es_duracion_indefinida = si_no(self.dato_tipocot('convert(es_dura_indefinida, unsigned)'))
        self.es_tpo_completo = si_no(self.dato_tipocot('convert(es_tpo_completo, unsigned)'))
        self.es_tpo_parcial = si_no(self.dato_tipocot('convert(es_tpo_parcial, unsigned)'))
        self.es_horaextra_fuerzamayor = si_no(self.dato_tipocot('convert(es_hora_extra_fmayor, unsigned)'))
        self.es_horaextra_resto = si_no(self.dato_tipocot('convert(es_hora_extra_resto, unsigned)'))
        self.regimen = Regimen_SegSocial(self.regimen_id)

    def __call__(self, idtipo):
        self.__init__(idtipo)

    def dato_tipocot(self, campo):
        dato = sql_basica(campo, 'tb_tiposcot', 'idtb_tiposcot', self.id)
        return dato


class Tipo_cotizacion_ejercicio:
    """

    """
    def __init__(self, idtipo_ejercicio):
        self.id = idtipo_ejercicio
        self.categoria_id = self.dato_tipocot('idtb_tipocot')
        self.ejercicio = self.dato_tipocot('ejercicio')
        self.tipo_empresa = self.dato_tipocot('empresa')
        self.tipo_trabajador = self.dato_tipocot('trabajador')
        self.tipo_total = self.tipo_empresa + self.tipo_trabajador
        self.es_tpo_parcial = si_no(self.dato_tipocot('convert(tpo_parcial, unsigned)'))
        self.es_tpo_completo = si_no(self.dato_tipocot('convert(tpo_completo, unsigned)'))
        self.es_duracion_indefinida = si_no(self.dato_tipocot('convert(dura_indefinida, unsigned)'))
        self.es_duracion_determinada = si_no(self.dato_tipocot('convert(dura_determinada, unsigned)'))
        self.categoria = Tipo_Cotizacion(self.categoria_id)

    def dato_tipocot(self, campo):
        dato = sql_basica(campo, 'tb_tiposcot_ejercicio', 'idtb_tiposcot_ejercicio', self.id)
        return dato


class Grupo_cotizacion:
    def __init__(self, idgrupo):
        self.id = idgrupo
        self.regimen_id = self.dato_grupocot('idregimen')
        self.concepto = self.dato_grupocot('nombre')
        self.regimen = Regimen_SegSocial(self.regimen_id)
    def dato_grupocot(self, campo):
        dato = sql_basica(campo, 'tb_grupos_cotizacion', 'idgrupos_cotizacion', self.id)
        return dato


class Grupo_cotizacion_bases:
    def __init__(self, idgrupocot_bases):
        self.id =idgrupocot_bases
        self.grupocot_id = self.dato_grupocot('idtb_grupo_cotizacion')
        self.ejercicio = self.dato_grupocot('ejercicio')
        self.base_minima_mes = self.dato_grupocot('base_min_mes')
        self.base_maxima_mes = self.dato_grupocot('base_max_mes')
        self.base_minima_dia = self.dato_grupocot('base_min_dia')
        self.base_maxima_dia = self.dato_grupocot('base_max_dia')
        self.base_minima_hora = self.dato_grupocot('base_min_hora')
        self.base_maxima_hora = self.dato_grupocot('base_max_hora')
        self.grupocot = Grupo_cotizacion(self.grupocot_id)
    def dato_grupocot(self, campo):
        dato = sql_basica(campo, 'tb_grupocot_bases', 'idtb_grupocot_base', self.id)
        return dato


class Epigrafe:
    def __init__(self, idepigrafe):
        self.id = idepigrafe
        self.codigo = self.dato_epigrafe('codigo')
        self.ejercicio = self.dato_epigrafe('ejercicio')
        self.cuadro = self.dato_epigrafe('cuadro')
        self.tipo_it = self.dato_epigrafe('it')
        self.tipo_ims = self.dato_epigrafe('ims')
    def dato_epigrafe(self, campo):
        dato = sql_basica(campo, 'tb_epigrafe', 'idtb_epigrafe', self.id)
        return dato