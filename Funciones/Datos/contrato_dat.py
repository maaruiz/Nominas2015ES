import datetime

from Funciones.funs import si_no, sql_basica, ultimodiames, select_sql
from Funciones.Datos.trabajador_dat import SqlTrabajador


class ContratoExtincion(object):
    def __init__(self, idbaja=0):
        self.idextincion = idbaja

    def dato_contratoextincion(self, campo):
        return sql_basica(campo, 'tb_contrato_baja', 'idtb_contratobaja', self.idextincion)

    def ac_extincion(self):
        self.codextincion = self.dato_contratoextincion('codigo')
        self.motivoextincion = self.dato_contratoextincion('descripcion')
        self.escausaobjetiva = si_no(self.dato_contratoextincion('escausaobjetiva'))
        self.esdespido = si_no(self.dato_contratoextincion('esdespido'))
        self.esexcedencia = si_no(self.dato_contratoextincion('esexcedencia'))
        self.esextincion = si_no(self.dato_contratoextincion('esextincion'))
        self.esfintemporal = si_no(self.dato_contratoextincion('esfintemporal'))
        self.essuspension = si_no(self.dato_contratoextincion('essuspension'))


class Despido:
    def __init__(self, iddespido):
        self.id = iddespido
        self.descripcion = self.dato_despido('descripcion')
        self.dias_anio = self.dato_despido('dias_anio')
        self.max_meses = self.dato_despido('max_meses')
        self.esdisciplinario = si_no(self.dato_despido('esdisciplinario'))
        self.esimprocedente = si_no(self.dato_despido('esimprocedente'))
        self.esnulo = si_no(self.dato_despido('esnulo'))
        self.esprocedente = si_no(self.dato_despido('esprocedente'))
        self.esobjetivo = si_no(self.dato_despido('esobjetivo'))

    def dato_despido(self, campo):
        return sql_basica(campo, 'tb_despidos', 'idtb_despido', self.id)


class Contrato(ContratoExtincion):
    """
    Conjunto de sentencias SQL para recuperar los datos de un contrato de
    una empresa de la base de datos
    """
    def __init__(self, idcontrato = 0):
        """
        Se necesita aportar el id del contrato
        """
        self.idcontrato = idcontrato
        try:
            self.codigo = self.dato_contrato('idcontratos_tipo')
            self.idextincion = self.dato_contrato('idtb_contrato_baja')
            self.ac_extincion()
            self.despido_id = self.dato_contrato('idtb_despido')
            try:
                self.despido = Despido(self.despido_id)
            except:
                pass
            self.empresa_id = self.dato_contrato('idempresa')
            self.inicio_dia = self.dato_contrato('dayofmonth(fecha_ini)')
            self.inicio_mes = self.dato_contrato('month(fecha_ini)')
            self.inicio_anio = self.dato_contrato('year(fecha_ini)')
            self.inicio_fecha = datetime.date(self.inicio_anio, self.inicio_mes, self.inicio_dia)
            self.final_dia = self.dato_contrato('dayofmonth(fecha_fin)')
            self.final_mes = self.dato_contrato('month(fecha_fin)')
            self.final_anio = self.dato_contrato('year(fecha_fin)')
            self.liquido_a_cobrar = self.dato_contrato('neto')
            try:
                self.final_fecha = datetime.date(self.final_anio, self.final_mes, self.final_dia)
            except:
                self.final_fecha = None
            self.idtrabajador = self.dato_contrato('idtrabajadores')
            self.categoria_profesional = self.dato_contrato('categoria_profesional')
            self.cta_cotizacion_id = self.dato_contrato('idemp_ctacot')
            self.con_prorrata_pextra = si_no(self.dato_contrato('prorrpextra'))
            self.contrato = Contrato_codigo(self.codigo)
            self.trabajador = SqlTrabajador(self.idtrabajador)
        except:
            pass

    def __call__(self, idcontrato):
        self.__init__(idcontrato)

    def contratos_activos_mes(self, idempresa, anio, mes):
        anio = int(anio)
        mes = int(mes)
        if idempresa:
            self.empresa_id = idempresa
        sql = ( "Select "
                    "count(*) "
                "From "
                    "emp_contratos "
                "Where "
                    "idempresa = %s "
                    "and (fecha_fin is null "
                        "or (month(fecha_fin) >= %s "
                            "and year(fecha_fin)>= %s)) "
                    "and (month(fecha_ini) <= %s "
                        "and year(fecha_ini)<= %s) "
                    "and (conversion is Null "
                        "and prorroga is Null)")
        dato = select_sql((sql, (self.empresa_id, mes, anio, mes, anio)))[0]
        return dato

    def dato_contrato(self, campo):
        """
         Retorna el valor de un campo del contrato
        """
        try:
            dato = sql_basica(campo, 'emp_contratos', 'idemp_contratos', self.idcontrato)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        return dato

    def listapagasextras(self):
        sql = ('Select '
               '    idemp_devengo '
               'From '
               '    emp_devengos '
               'Where '
               '    idemp_contrato = ' + unicode(self.idcontrato) +
               '    and idemp_pextra >0')
        return select_sql(sql, 1)

    def periodo_nomina(self, anio, mes):
        """
        Calcula el perido de una nomina en vigor respecto de las fechas del
        contrato.

        Devuelve una tupla con la fecha inicial y la final
        """
        f2 = None
        anio = int(anio)
        mes = int(mes)
        d1 = datetime.date(anio, mes, 1)
        d2 = datetime.date(anio, mes, ultimodiames(mes, anio))
        f1 = self.inicio_fecha
        if self.final_fecha is None:
            f2 = d2
        else:
            f2 = self.final_fecha
            if f2 > d2:
                f2 = d2
        if d1 <= f2 <= d2:
            if f1 < d1:
                f1 = d1
        dato = (f1, f2)
        return dato

    def tpo_parcial(self):
        if self.contrato.es_tiempo_parcial:
            sql = ( "Select "
                        "idemp_tpo_parcial "
                    "From "
                        "emp_tpo_parcial "
                    "Where "
                        "idemp_contrato = " + self.idcontrato )
            dato = select_sql(sql)[0]
            self.contrato_tpo_parcial = Contrato_tpo_parcial(dato)

    def vacaciones_disfrutadas(self, anio):
        sql = ('Select '
               '    sum(fecha_final - fecha_inicial + 1) '
               'From '
               '    emp_contratos_vacaciones '
               'Where '
               '    idemp_contrato = ' + unicode(self.idcontrato) + ' '
               '    and ejercicio = ' + unicode(anio) + ' '
               'Group by '
               '    idemp_contrato and ejercicio ')
        try:
            dato = select_sql(sql)[0]
        except:
            dato = 0
        return dato

    def vacaciones_nodisfrutadas(self, anio):
        disfrutadas = self.vacaciones_disfrutadas(anio)



class Contrato_codigo:
    """
    Devuelve los tipos de contratos admitidos por la administracion
    y sus caracteristicas
    """
    def __init__(self, codigo):
        self.codigo = codigo
        self.es_temporal = si_no(self.dato_codcontrato('convert(temporal, unsigned)'))
        self.descripcion = self.dato_codcontrato('descripcion')
        self.es_indefinido = si_no(self.dato_codcontrato('convert(indefinido, unsigned)'))
        self.es_tiempo_completo = si_no(self.dato_codcontrato('convert(jornadacompleta, unsigned)'))
        self.es_tiempo_parcial = si_no(self.dato_codcontrato('convert(jornadaparcial, unsigned)'))

    def dato_codcontrato(self, campo):
        """
         Retorna el valor de un campo del contrato
        """
        dato = sql_basica(campo, 'tb_contratos_tipo', 'idcontratos_tipo', self.codigo)
        return dato


class Contrato_Devengo:
    def __init__(self, iddevengo):
        self.id = iddevengo
        self.coef_pextra = self.dato_contrato_devengo('coef_pextra')
        self.concepto = self.dato_contrato_devengo('concepto')
        self.contrato_id = self.dato_contrato_devengo('idemp_contrato')
        self.cotiza_desempleo = si_no(self.dato_contrato_devengo('convert(desempleo, unsigned)'))
        self.cotiza_fogasa = si_no(self.dato_contrato_devengo('convert(fgs, unsigned)'))
        self.cotiza_fprofesional = si_no(self.dato_contrato_devengo('convert(fp, unsigned)'))
        self.cotiza_ims = si_no(self.dato_contrato_devengo('convert(ims, unsigned)'))
        self.cotiza_irpf = si_no(self.dato_contrato_devengo('convert(irpf, unsigned)'))
        self.cotiza_it = si_no(self.dato_contrato_devengo('convert(it, unsigned)'))
        self.cotiza_segsocial = si_no(self.dato_contrato_devengo('convert(cont_com, unsigned)'))
        self.es_diario = si_no(self.dato_contrato_devengo('convert(diario, unsigned)'))
        self.es_devengo = si_no(self.dato_contrato_devengo('convert(esdevengo, unsigned)'))
        self.es_dieta = si_no(self.dato_contrato_devengo('convert(esdieta, unsigned)'))
        self.es_especie = si_no(self.dato_contrato_devengo('convert(esespecie, unsigned)'))
        self.es_irpf = si_no(self.dato_contrato_devengo('convert(esirpf, unsigned)'))
        self.es_mensual = si_no(self.dato_contrato_devengo('convert(mensual, unsigned)'))
        self.es_pextra = si_no(self.dato_contrato_devengo('convert(ppextra, unsigned)'))
        self.es_porcentaje = si_no(self.dato_contrato_devengo('convert(esporcentaje, unsigned)'))
        self.es_vacaciones = si_no(self.dato_contrato_devengo('esvacaciones'))
        self.fraccion_hora = si_no(self.dato_contrato_devengo('convert(fraccionhoras, unsigned)'))
        self.form_concepto_id = self.dato_contrato_devengo('idform_concepto')
        self.importe = self.dato_contrato_devengo('importe')
        self.orden = self.dato_contrato_devengo('orden')
        self.pextra_id = self.dato_contrato_devengo('idemp_pextra')
        self.paga_diasefectivos = si_no(self.dato_contrato_devengo('convert(dias_efectivos, unsigned)'))
        self.paga_diasnaturales = si_no(self.dato_contrato_devengo('convert(dias_naturales, unsigned)'))
        self.paga_vacaciones = si_no(self.dato_contrato_devengo('convert(pagavacaciones, unsigned)'))
        self.contrato = Contrato(self.contrato_id)

    def dato_contrato_devengo(self, campo):
        return sql_basica(campo, 'emp_devengos', 'idemp_devengo', self.id)

    def nuevo(self):
        pass


class Contrato_tpo_parcial:
    def __init__(self, idcontrato):
        self.id = idcontrato
        self.emp_contrato_id = self.dato_Contrato_tpo_parcial('idemp_contrato')
        self.dia = self.dato_Contrato_tpo_parcial("CONCAT_WS('/', dayofmonth(fecha), month(fecha), year(fecha))")
        self.horas_dia = self.dato_Contrato_tpo_parcial('horas')
        self.horas_lunes = self.dato_Contrato_tpo_parcial('lunes')
        self.horas_martes = self.dato_Contrato_tpo_parcial('martes')
        self.horas_miercoles = self.dato_Contrato_tpo_parcial('miercoles')
        self.horas_jueves = self.dato_Contrato_tpo_parcial('jueves')
        self.horas_viernes = self.dato_Contrato_tpo_parcial('viernes')
        self.horas_sabado = self.dato_Contrato_tpo_parcial('sabado')
        self.horas_domingo = self.dato_Contrato_tpo_parcial('domingo')

    def dato_Contrato_tpo_parcial(self, campo):
        dato = sql_basica(campo, 'emp_tpo_parcial', 'idemp_tpo_parcial', self.id)
        return dato


class Vacaciones:
    def __init__(self, idvacaciones=0):
        """

        :type self: object
        """
        self.id = idvacaciones
        self.anio = self.dato_vacacionesemp('ejercicio')
        self.contrato_id = self.dato_vacacionesemp('idemp_contrato')
        self.contrato = Contrato(self.contrato_id)
        self.fecha_final = datetime.datetime(self.dato_vacacionesemp('fecha_final'), '%Y-%m-%d')
        self.fecha_inicial = datetime.datetime(self.dato_vacacionesemp('fecha_inicial'), '%Y-%m-%d')
        self.dias_disfrutados = (self.fecha_final - self.fecha_inicial).days
        self.dato_contratoextincion()
        self.dias_disfrutados = self.dato_vacacionesemp('dias_disfrutados')
        self.dias_pendientes = self.dato_vacacionesemp('dias_pendientes')

    def dato_contratoextincion(self):
        sql = ('Update '
                '    emp_contratos_vacaciones '
                'Set '
                '    dias_disfrutados = %s '
                'Where '
                '    idemp_contrato_vacaciones = ' + unicode(self.id) + ' '
                '    and ejercicio = ' + unicode(self.anio) + ' ')
        if self.dias_disfrutados is not None:
            select_sql((sql, (self.dias_disfrutados + 1)))
        else:
            select_sql((sql, (0)))

    def dato_vacacionesemp(self, campo):
        return sql_basica(campo, 'emp_contratos_vacaciones', 'idemp_contrato_vacaciones', self.id)
