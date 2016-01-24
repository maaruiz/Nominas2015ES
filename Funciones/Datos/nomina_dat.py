#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import calendar
import locale
from Funciones.funs import select_sql, sql_basica, si_no, ultimodiames, poblacion, provincia
from Funciones.Datos.empresa_dat import SqlEmpresa, Cod_cotizacion
from Funciones.Datos.contrato_dat import Contrato_Devengo, Contrato_tpo_parcial, Contrato
from Procesos.Nomina.Calcular.cabecera import Cabecera
from Funciones.Generales.number_to_letter import to_word

class SqlNominas:
    """

    Conjunto de procesos que iteraccionan con la base de datos MySQL
    """
    def __init__(self, nomina=0):
        self.id = nomina
        self.base_ppextra = self.dato_nomina('base_ppextra')
        self.base_irpf = self.dato_nomina('base_irpf')
        self.base_cc = self.dato_nomina('base_cc')
        self.cif = self.dato_nomina("cif")
        self.contrato_id = self.dato_nomina('idemp_contratos')
        self.contrato = Contrato(self.contrato_id)
        try:
            self.dirtrabajador = self.contrato.trabajador.direccion_completa
            self.cptrabajador = self.contrato.trabajador.cod_postal
            self.pobtrabajador = poblacion(self.cptrabajador)
            self.provtrabajador = provincia(self.cptrabajador)
            self.motivoextincion = self.contrato.motivoextincion
        except:
            pass
        self.cta_cot_id = self.dato_nomina('idcta_cot')
        try:
            self.cta_cot = Cod_cotizacion(self.cta_cot_id)
            self.dirempresa = self.cta_cot.centro_trabajo.dircompleta
            self.cpempresa = self.cta_cot.centro_trabajo.dir_codpostal
            self.pobempresa = poblacion(self.cpempresa)
            self.provempresa = provincia(self.cpempresa)

        except:
            print 'No se activa la cta_cot'
            self.cta_cot = 0
        self.descripcion = self.dato_nomina('descripcion')
        self.empresa_id = self.dato_nomina('idempresa')
        self.es_finiquito = si_no(self.dato_nomina('es_finiquito'))
        self.es_nominapextra = si_no(self.dato_nomina('es_nominapextra'))
        self.epigrafe_id = self.dato_nomina('idtb_epigrafe')
        self.fecha = self.dato_nomina('fecha')
        self.fecha_dia = self.dato_nomina('dayofmonth(fecha)')
        self.grupo_cotizacion_id = self.dato_nomina('idgrupos_cotizacion')
        self.imp_pextra = self.dato_nomina('imp_pextra')
        self.imp_remumes = self.dato_nomina('imp_remumes')
        self.nif = self.dato_nomina('dni')
        self.naf = self.dato_nomina('naf')
        self.nombre_trabajador = self.dato_nomina('nombre')
        self.nombreempresa = SqlEmpresa(self.empresa_id).razon_social
        self.periodo = self.dato_nomina('periodo')
        self.puesto = self.dato_nomina('categoria')
        self.fecha_anio = self.dato_nomina('year(fecha)')
        self.fecha_mes = self.dato_nomina('month(fecha)')
        self.dia_nomina = self.dato_nomina('dayofmonth(fecha)')
        try:
            self.fecha_datetime = datetime.date(self.fecha_anio, self.fecha_mes, self.dia_nomina)
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
            self.fecha_formlargo = self.fecha_datetime.strftime('%d de %B de %Y')
            self.periodos = self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)
        except ValueError:
            print ('No hay nomina activa, no se crea fecha_datetime y tampoco hay periodo de tiempo')
            self.fecha_datetime = 0

        self.numero_nominas_mes = self.contrato.contratos_activos_mes(self.empresa_id, self.fecha_anio, self.fecha_mes)
        try:
            self.cabecera = Cabecera(self.empresa_id, self.fecha_mes, self.fecha_anio,
                                     self.contrato.trabajador.id)
        except AttributeError:
            print('Si no hay nómina, no hay contrato y tampoco trabajador. Se pierde la cabecera')
        self.total_devengos = self.dato_nomina('imp_totdev')
        self.total_deducciones = self.dato_nomina('tot_deducir')
        self.liquido = self.dato_nomina('liquido')
        self.liquido_letras = to_word(self.liquido)

    def __call__(self, nomina):
        self.__init__(nomina)

    def actualiza_liquido(self, nomina):
        sql = ("select emp_contratos.neto from emp_contratos "
               "inner join nominas "
               "on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "where nominas.idnomina = %s;")
        liquido = select_sql((sql, (nomina)))[0]
        sql = ("update nominas "
               "set liquido = %s "
               "where nominas.idnomina = %s")
        select_sql((sql, (liquido, nomina)))
        return liquido

    def actualiza_fecha(self):
        self.fecha = self.periodos[1].strftime('%Y-%m-%d')
        print self.fecha
        sql = ('Update nominas '
               'set fecha = ' + "'" + unicode(self.fecha) +
               "' " +
               'where idnomina = ' + unicode(self.id) +
               ' ')
        select_sql(sql)

    def actualiza_ppextra(self):
        valor = self.devengo_ppextra()
        sql = ('Update '
               '    nominas '
               'Set '
               '    base_ppextra = ' + unicode(valor) +
               ' '
               'Where '
               '    idnomina = ' + unicode(self.id) +
               ' ')
        select_sql(sql)
        self.base_ppextra = self.dato_nomina('base_ppextra')

    def anios_cotizados_acumulados(self):
        f1 = self.contrato.inicio_fecha
        f2 = self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1]
        x = f2.year - f1.year
        f1 = datetime.date(f2.year, f1.month, f1.day)
        y = (f2 - f1).days
        x = float(x) + 1 / float(self.cta_cot.calendario.diastotales) * float(y)
        return round(x, 2)

    def borrar_nomina(self):
        sql = ("Delete "
               "    nominas, nomina_devengos "
               "From "
               "    nominas "
               "        inner join "
               "            nomina_devengos "
               "            on nominas.idnomina = nomina_devengos.idnomina "
               "Where "
               "    nominas.idnomina = " + unicode(self.id) + " ")
        select_sql(sql)

    def dato_nomina(self, campo):
        try:
            dato = sql_basica(campo, 'nominas', 'idnomina', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = ""
        if isinstance(dato, datetime.date):
            dato = dato.strftime('%d/%m/%Y')
        return dato

    def devengo_indemnizacion(self):
        """

        :return:
        """
        listadevengos = self.lista_devengos_nomina()
        print listadevengos
        valor = 0
        for x in listadevengos:
            devengo = Nomina_Devengo(x[0])
            if devengo.cotiza_segsocial:
                valor = devengo.devengado + valor
        valor += float(self.base_ppextra)
        return valor

    def devengo_ppextra(self):
        # Para calcular el prorrateo de pagas extras en la cotización se tiene en cuenta si están prorrateadas o no.
        # Si no lo están, no aparecen en nómina y hay que tomarlas de los devengos de la empresa
        # para hacer el cálculo.
        # En el caso de que sea finiquito o nómina de pagas extras, no se hace el prorrateo, ya que
        # está incluido en las nóminas anteriores.
        valor = 0
        if self.lista_pagas_extras():
            listapextra = self.lista_pagas_extras()
            for x in listapextra:
                pextra = Nomina_Devengo(x[0])
                print '    ....**** Devengo pextra', pextra.concepto
                if pextra.es_para_pextra and (not self.es_finiquito and not self.es_nominapextra):
                    valor += pextra.devengado
        if self.lista_devengos_nomina():
            listapextra = self.lista_devengos_nomina()
            for x in listapextra:
                pextra = Nomina_Devengo(x[0])
                print '    ....**** Devengo pextra 2', pextra.concepto, pextra.paga_extra()
                if pextra.es_para_pextra:
                    valor += pextra.paga_extra() * pextra.coef_pextra * self.cta_cot.convenio_datos.num_pextra()
        print '    .... Valor ppextra', valor
        # Sólo en el caso de que valor sea 0 y se trate de una nómina normal hay que incluir el prorrateo
        # de pagas extras proveniente de los devengos de la empresa.
        if not valor:
            if (not self.es_finiquito and not self.es_nominapextra):
                listapextra = self.contrato.listapagasextras()
                for x in listapextra:
                    devengo = Contrato_Devengo(x[0])
                    valor += (devengo.importe / float(self.cta_cot.calendario.diastotales))
                    valor = valor * (devengo.coef_pextra )
                valor = valor * self.dias_cotizados()
        print '    .... Valor 2 pextra', valor
        return valor

    def devengo_vacaciones(self):
        """
        Nos devuelve el valor del devengo por vacaciones si se entrara en este mes en fin de contrato
        :return:
        """
        listadevengos = self.lista_devengos_nomina()
        valor = 0
        for x in listadevengos:
            devengo = Nomina_Devengo(x[0])
            if devengo.es_pagavacaciones:
                valor = valor + devengo.devengado
        return valor

    def devengos_nomina(self, contrato):
        """
        Nos devuelve todos los devengos que se encuentran en una nomina
        """
        sql = ("SELECT "
               "    idemp_devengo, orden, concepto, importe, irpf, cont_com, "
               "    desempleo, fp, fgs, it, ims, ppextra, mensual, diario, "
               "    horas, idemp_pextra, dias_efectivos, dias_naturales, "
               "    esdevengo, esirpf, esdieta, esespecie, esporcentaje "
               "FROM "
               "    emp_devengos "
               "WHERE "
               "    idemp_contrato = %s "
               "ORDER by "
               "    idemp_contrato, orden")
        return select_sql((sql, (contrato)), 1)

    def dias_no_it(self):
        self.dia_nomina

    def dias_cotizados(self):
        self.contrato(self.contrato_id)
        f1 = self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[0]
        f2 = self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1]
        x = 0
        calmes = calendar.Calendar().monthdays2calendar(self.fecha_anio, self.fecha_mes)
        for c in calmes:
            for g in c:
                if f1.day <= g[0] <= f2.day:
                    x += 1
        return x

    def dias_cotizados_acumulados(self):
        self.contrato(self.contrato_id)
        f1 = datetime.date(self.fecha_anio, 1, 1)
        if self.contrato.inicio_fecha > f1:
            f1 = self.contrato.inicio_fecha
        f2 = self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1]
        x = (f2 - f1).days + 1
        return x

    def dias_efectivos_tpo_completo(self):
        desdedia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[0].day)
        hastadia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1].day)
        cal = self.cta_cot.calendario
        cal.desde(self.fecha_anio, self.fecha_mes, desdedia)
        cal.hasta(self.fecha_anio, self.fecha_mes, hastadia)
        cal.nolaboral()
        if self.cta_cot.convenio_datos.es_sab_laboral:
            dato = cal.diastotales - cal.totaldomingos - cal.totalfestivos
        else:
            dato = cal.totalefectivos
        return dato

    def dias_efectivos_tpo_parcial(self):
        sql = ("select "
               "    count(*) "
               "from "
               "    emp_tpo_parcial "
               "        left join "
               "            nominas "
               "            on emp_tpo_parcial.idemp_contrato = nominas.idemp_contratos "
               "where "
               "    month(emp_tpo_parcial.fecha) = %s "
               "    and year(emp_tpo_parcial.fecha) = %s "
               "    and nominas.idnomina = %s "
               "    and horas > 0")
        dias = select_sql((sql, (self.fecha_mes, self.fecha_anio, self.id)))[0]

        if dias == 0:
            desdedia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[0].day)
            hastadia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1].day)
            cal = self.cta_cot.calendario
            try:
                sql = ("select (lunes>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 0)) +
                       " + (martes >0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 1)) +
                       " + (miercoles>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 2)) +
                       " + (jueves>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 3)) +
                       " + (viernes>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 4)) +
                       " + (sabado>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 5)) +
                       " + (domingo>0) * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 6)) +
                       " "
                       "from emp_tpo_parcial "
                       "left join nominas "
                       "on emp_tpo_parcial.idemp_contrato = nominas.idemp_contratos "
                       "where nominas.idnomina = %s ")
                dias = select_sql((sql, (self.id)))[0]
            except:
                dias = 0
        print "    Dias_Efectivos tiempo parcial", dias
        return dias

    def horas_cotizadas(self):
        """
        Devuelve las horas cotizadas en una nomina
        """
        horas = 0
        if self.contrato.contrato.es_tiempo_parcial is True:
            sql = ("Select sum(horas) from emp_tpo_parcial a "
                   "left join nominas b "
                   "on b.idemp_contratos = a.idemp_contrato "
                   "Where month(a.fecha) = %s and year(a.fecha) = %s "
                   "and b.idnomina = %s;")
            horas = select_sql((sql, (self.fecha_mes, self.fecha_anio, self.id)))[0]
            if horas is None:
                desdedia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[0].day)
                hastadia = int(self.contrato.periodo_nomina(self.fecha_anio, self.fecha_mes)[1].day)
                cal = self.cta_cot.calendario
                sql = ("select "
                       "lunes * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 0)) +
                       " + martes * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 1)) +
                       " + miercoles * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 2)) +
                       " + jueves * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 3)) +
                       " + viernes * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 4)) +
                       " + sabado * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 5)) +
                       " + domingo * " +
                       str(cal.diasemana_delmes(self.fecha_anio, self.fecha_mes, desdedia, hastadia, 6)) +
                       " "
                       "from emp_tpo_parcial "
                       "left join nominas "
                       "on emp_tpo_parcial.idemp_contrato = nominas.idemp_contratos "
                       "where nominas.idnomina = %s ")
                horas = select_sql((sql, (self.id)))[0]
        return horas

    def iddevengo_nomina(self, iddevengo):
        """

        Devuelve un devengo concreto de una nomina concreta

            SqlNominas().iddevengo_nomina(iddevengo)
        """
        sql = ("select "
               "    concepto, imp_cuantia, imp_precio, "
               "    nominas.nombre, nominas.empresa, month(nominas.fecha), "
               "    year(nominas.fecha) "
               "from "
               "    nomina_devengos "
               "        left join "
               "            nominas "
               "            on nominas.idnomina = nomina_devengos.idnomina "
               "        left join "
               "            emp_contratos "
               "            on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "        left join "
               "            Trabajadores "
               "            on emp_contratos.idTrabajadores = Trabajadores.idTrabajadores "
               "where "
               "    idnomina_devengo = %s")
        dato = select_sql((sql, (iddevengo)))
        return dato

    def idnom_mes(self, empresa, mes, anio, esuna):
        """

        Nos da la id de las nominas de un mes de un anio de una empresa

            SqlNominas().idnom_mes(numero_empresa, mes, anio, es_una_sola_nomina)

        Los valores para esuna son:

            esuna = 0 cuando son mas de una nomina a listar
            esuna = numero_nomina cuando solo es una nomina a listar

        En este ultimo caso hay que apoyarse en

            SqlNominas().nomina_trabajador_mes

        Devuelve el valor de idnomina
        """
        if esuna == 0:
            sql = ("SELECT idnomina "
                   "from nominas "
                   "where idempresa = %s and month(fecha) = %s "
                   "and year(fecha) = %s "
                   "and (es_finiquito is null or es_finiquito = 0);")
            dato = select_sql((sql, (empresa, mes, anio)), 1)
        else:
            dato = ((esuna,),)
        return dato

    def lista_deducciones_nomina(self):
        """
        Devuelve una tupla con los idenomina_devengo no devengos de una nomina
        """
        sql = ("Select "
               "    idnomina_devengo "
               "From "
               "    nomina_devengos "
               "Where "
               "    not esdevengo "
               "    and idnomina = " + unicode(self.id) + " ")
        return select_sql(sql, 1)

    def dic_devengos_formulario(self):
        sql = ('Select '
               '    idnomina_devengo, idform_concepto '
               'From '
               '    nomina_devengos '
               'Where '
               '    idnomina = ' + unicode(self.id))
        lista = select_sql(sql, 1)
        indice = {}
        for x in lista:
            indice[x[0]] = x[1]
        return indice

    def lista_devengos_nomina(self):
        """
        Devuelve una tupla con los idnomina_devengo de una nomina excluidas las pagas extras
        """
        sql = ("Select "
               "    idnomina_devengo "
               "From "
               "    nomina_devengos "
               "Where "
               "    esdevengo "
               "    and (idemp_pextra is null or idemp_pextra = 0) "
               "    and idnomina = " + unicode(self.id) +
               " "
               "order by "
               "    orden ")
        return select_sql(sql, 1)

    def lista_pagas_extras(self):
        """
        Devuelve una tupla con los idnomina_devengo de una nomina que sean pagas extras
        """
        sql = ("Select "
               "    idnomina_devengo "
               "From "
               "    nomina_devengos "
               "Where "
               "    idemp_pextra > 0 "
               "    and idnomina = " + unicode(self.id) + "")
        return select_sql(sql, 1)

    def listaempresas(self):
        sql = ("Select "
               "    idempresa, "
               "    concat_ws(' ',nombre, apellido1, apellido2) as nombre "
               "From "
               "    empresa "
               "Order by "
               "    nombre")
        dato = select_sql(sql, 1)
        return dato

    def nomina_a_tiempo_parcial(self):
        sql = ("SELECT "
               "    tb_contratos_tipo.jornadaparcial "
               "From "
               "    nominas "
               "        left join "
               "            emp_contratos "
               "            on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "        left join "
               "            tb_contratos_tipo "
               "            on emp_contratos.idcontratos_tipo = tb_contratos_tipo.idcontratos_tipo "
               "Where "
               "    tb_contratos_tipo.jornadaparcial "
               "    and nominas.idnomina =  %s")
        dato = select_sql((sql, (self.id)))
        if dato is None:
            dato = False
        dato = si_no(dato)
        return dato

    def nomina_trabajador_mes(self, trabajador, mes, anio, esnomina=True, esfiniquito=False, esnominapextra=False):
        """

        Devuelve el numero de nomina del trabajador de un mes y anio dados

            SqlNominas().nomina_trabajador_mes(numero_trabajador, mes, anio)
        """
        sql = ("SELECT "
               "    idnomina "
               "FROM "
               "    nominas "
               "        Left Join emp_contratos "
               "        on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "WHERE "
               "    idtrabajadores = %s "
               "    and month(fecha) = %s "
               "    and year(fecha) = %s ")
        if esnomina:
            sql = (sql + "    and (es_finiquito is null or es_finiquito = 0) ")
        elif esfiniquito:
            sql = (sql + "    and es_finiquito ")
        dato = select_sql((sql, (trabajador, mes, anio)))
        return dato[0]

    def nominas_empresa_mes(self, empresa, mes, anio, esnomina=True, esfiniquito=False, esnominapextra=False):
        """
        Listado de las nóminas de una empresa en un mes y anio dados
        """
        sql = ("SELECT idnomina "
               "FROM nominas "
               "WHERE idempresa = %s "
               "and month(fecha) = %s "
               "and year(fecha) = %s ")
        if esfiniquito:
            sql += "and es_finiquito "
        elif esnominapextra:
            sql += "and es_nominapextra "
        elif esnomina:
            sql += "and not es_finiquito and not es_nominapextra "
        sql += "ORDER BY idnomina"
        dato = select_sql((sql, (empresa, mes, anio)), 1)
        return dato

    def tipo_irpf(self, nomina):
        sql = """SELECT sum(imp_precio) as importe
                 FROM nomina_devengos
                 WHERE esirpf and idnomina = %s;"""
        dato = select_sql((sql, (nomina)))[0]
        return dato

    def tipo_segsoc(self, nomina):
        sql = """SELECT sum(imp_precio) as importe
                 FROM nomina_devengos
                 WHERE not esdevengo and not esirpf and idnomina = %s;"""
        dato = select_sql((sql, (nomina)))[0]
        return dato

    def trabajador_empresa(self, trabajador, mes, anio):
        sql = ("SELECT "
               "    nominas.idempresa "
               "FROM "
               "    nominas "
               "        left join "
               "            emp_contratos "
               "            on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "WHERE "
               "    emp_contratos.idtrabajadores = %s "
               "    and month(fecha) = %s "
               "    and year(fecha) = %s "
               "group by "
               "    nominas.idempresa;")
        dato = select_sql((sql, (trabajador, mes, anio)))[0]
        return dato

    def trabajadores(self, empresa, mes, anio, esnomina=True, esfiniquito=False, esnominapextra=False):
        sql = (""
               "SELECT "
               "    CONCAT_WS(' ',Trabajadores.nombre,Trabajadores.apellido1, "
               "    Trabajadores.apellido2) as nombre, "
               "    Trabajadores.idTrabajadores "
               "FROM "
               "    Nominas.emp_contratos "
               "        left join "
               "            Trabajadores "
               "            On Trabajadores.idTrabajadores = emp_contratos.idtrabajadores "
               "        left join "
               "            empresa "
               "            On empresa.idempresa = emp_contratos.idempresa "
               "        left join "
               "            emp_ctacot "
               "            On emp_ctacot.idctacot = emp_contratos.idemp_ctacot "
               "WHERE "
               "    emp_contratos.idempresa = %s "
               "    and emp_contratos.conversion is Null "
               "    and emp_contratos.prorroga is Null "
               "    and ("
               "        (month(fecha_ini) <= %s and year(fecha_ini)<= %s) "
               "        or (month(fecha_ini)>%s and year(fecha_ini)<%s) "
               "        ) ")
        dato = 0
        if esnomina:
            sql = (sql +
                   "    and (fecha_fin is null "
                   "        or (month(fecha_fin) >= %s and year(fecha_fin)>= %s) "
                   "        or (month(fecha_fin) <= %s and year(fecha_fin)> %s) "
                   "        ) ")
            dato = select_sql((sql, (empresa, mes, anio, mes, anio, mes,
                                 anio, mes, anio)), 1)
        if esfiniquito:
            sql = (sql +
                   "    and (month(fecha_fin) = %s and year(fecha_fin)= %s) ")
            dato = select_sql((sql, (empresa, mes, anio, mes, anio, mes,
                                 anio)), 1)
        return dato

    def trimestre_irpf(self, empresa, trim, anio):
        sql = ("SELECT idempresa, empresa, count(*), ((month(fecha)-1) div 3)+1 as trim, "
               "year(fecha), sum(imp_cuantia), sum(imp_deduccion), "
               "esirpf, esespecie "
               "FROM nomina_devengos "
               "LEFT JOIN nominas "
               "ON nominas.idnomina=nomina_devengos.idnomina"
               "WHERE ((month(fecha)-1) div 3) + 1 = %s and year(fecha) = %s "
               "and idempresa = %s "
               "group by idempresa, ((month(fecha)-1) div 3)+1, esespecie ")
        dato = select_sql((sql, (trim, anio, empresa)), 1)
        return dato

    def ver_devengos(self, trabajador, mes, anio):
        sql = ("select "
               "    nomina_devengos.idnomina_devengo, "
               "    nomina_devengos.concepto, "
               "    nomina_devengos.imp_cuantia, "
               "    nomina_devengos.imp_precio, "
               "    nomina_devengos.imp_devengo, "
               "    nomina_devengos.imp_deduccion "
               "from "
               "    nomina_devengos "
               "        left join "
               "            nominas "
               "            on nominas.idnomina = nomina_devengos.idnomina "
               "        left join "
               "            emp_contratos "
               "            on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "where "
               "    emp_contratos.idtrabajadores = %s "
               "    and month(nominas.fecha) = %s "
               "    and year(nominas.fecha) = %s "
               "    and esdevengo "
               "order by "
               "    orden")
        dato = select_sql((sql, (trabajador, mes, anio)), 1)
        return dato

    def ver_nomina(self, trabajador, mes, anio):
        sql = ("Select "
               "    empresa, cta_cot, antig, nombre, base_cc, base_irpf, "
               "    tot_dias, imp_totdev, tot_deducir  "
               "from "
               "    nominas "
               "        left join "
               "            nomina_devengos "
               "            on nominas.idnomina = nomina_devengos.idnomina "
               "        left join "
               "            emp_contratos "
               "            on nominas.idemp_contratos = emp_contratos.idemp_contratos "
               "where "
               "    emp_contratos.idtrabajadores = %s "
               "    and month(nominas.fecha) = %s "
               "    and year(nominas.fecha) = %s "
               "group by "
               "    empresa")
        dato = select_sql((sql, (trabajador, mes, anio)))
        return dato


class Nomina_Devengo:
    def __init__(self, iddevengo=0):
        self.id = iddevengo
        self.coef_pextra = self.dato_devengo('coef_pextra')
        self.concepto = self.dato_devengo('concepto')
        self.cotiza_segsocial = si_no(self.dato_devengo('cont_com'))
        self.cotiza_irpf = si_no(self.dato_devengo('irpf'))
        self.emp_devengo_id = self.dato_devengo('idemp_devengo')
        self.emp_pextra_id = self.dato_devengo('idemp_pextra')
        self.es_devengo = si_no(self.dato_devengo('esdevengo'))
        self.es_devengo_especie = si_no(self.dato_devengo('esespecie'))
        self.es_dieta = si_no(self.dato_devengo('esdieta'))
        self.es_importe_diario = si_no(self.dato_devengo('diario'))
        self.es_importe_mensual = si_no(self.dato_devengo('mensual'))
        self.es_importe_porhora = si_no(self.dato_devengo('horas'))
        self.es_indemnizacion = si_no(self.dato_devengo('es_indemnizacion'))
        self.es_irpf = si_no(self.dato_devengo('esirpf'))
        self.es_manual = si_no(self.dato_devengo('esmanual'))
        self.es_pagar_diasnaturales = si_no(self.dato_devengo('dias_naturales'))
        self.es_pagar_lunavie = si_no(self.dato_devengo('dias_efectivos'))
        self.es_pagar_sabados = si_no(self.dato_devengo('dias_efectivos'))
        self.es_pagavacaciones = si_no(self.dato_devengo('pagavacaciones'))
        self.es_para_pextra = si_no(self.dato_devengo('ppextra'))
        self.es_vacaciones = si_no(self.dato_devengo('esvacaciones'))
        self.formulario_id = self.dato_devengo('idform_concepto')
        self.importe = self.dato_devengo('importe')
        self.nomina_id = self.dato_devengo('idnomina')
        self.orden = self.dato_devengo('orden')
        try:
            self.emp_devengo = Contrato_Devengo(self.emp_devengo_id)
            self.contrato_id = self.emp_devengo.contrato_id
            self.contrato_tpo_parcial = Contrato_tpo_parcial(self.contrato_id)
            self.nomina = SqlNominas(self.nomina_id)
        except:
            pass
        # Datos a actualizar
        self.cuantia = self.dato_devengo('imp_cuantia')
        self.precio = self.dato_devengo('imp_precio')
        self.ac_devengo_horas()
        self.ac_devengo_dias()
        self.ac_devengo_mes()
        self.ac_devengo_vacaciones()
        self.ac_devengo_indemnizacion()
        self.cuantia = self.dato_devengo('imp_cuantia')
        self.precio = self.dato_devengo('imp_precio')
        self.ac_deduccion_irpf()
        self.ac_deduccion_segsocial()
        self.devengado = self.dato_devengo('imp_devengo')
        self.deducido = self.dato_devengo('imp_deduccion')
        self.ac_cotiza()

    def __call__(self, iddevengo):
        self.__init__(iddevengo)

    def ac_campo(self, campo, valor):
        sql = ("Update "
               "    nomina_devengos "
               "Set " +
               campo + "= " + unicode(valor) +
               " "
               "Where "
               "    idnomina_devengo = " + unicode(self.id) + " ")
        select_sql(sql)

    def ac_cantidad_deduccion(self):
        valor = 0
        if not self.es_devengo:
            if not self.es_irpf:
                valor = self.nomina.base_cc
                self.ac_campo('imp_cuantia', valor)
            elif self.es_irpf:
                valor = self.nomina.base_irpf
                self.ac_campo('imp_cuantia', valor)
        return valor

    def ac_cantidad_dias(self):
        valor = self.cuantia
        if self.nomina.contrato.contrato.es_tiempo_completo and self.es_importe_diario and not self.es_dieta:
            if self.es_pagar_diasnaturales:
                valor = self.nomina.dias_cotizados()
                self.ac_campo('imp_cuantia', valor)
            if self.es_pagar_lunavie:
                valor = self.nomina.dias_efectivos_tpo_completo()
                self.ac_campo('imp_cuantia', valor)
        return valor

    def ac_cantidad_horas(self):
        valor = self.cuantia
        if self.nomina.contrato.contrato.es_tiempo_parcial and not self.es_manual:
            valor = self.nomina.horas_cotizadas()
            self.ac_campo('imp_cuantia', valor)
        return valor

    def ac_cantidad_indemnizacion(self):
        valor = 0
        if self.es_indemnizacion:
            valor = self.nomina.anios_cotizados_acumulados()
            self.ac_campo('imp_cuantia', valor)
        return valor

    def ac_cantidad_mes(self):
        anio = self.nomina.fecha_anio
        mes = self.nomina.fecha_mes
        valor = 0
        if self.nomina.contrato.contrato.es_tiempo_completo and self.es_importe_mensual:
            valor = float(self.nomina.dias_cotizados()) / float(ultimodiames(mes, anio))
            valor = round(valor, 2)
            self.ac_campo('imp_cuantia', valor)
        return valor

    def ac_cantidad_vacaciones(self):
        valor = 0
        diasanio = float(self.nomina.cta_cot.calendario.diastotales)
        if self.es_vacaciones:
            diastotales = float(self.nomina.cta_cot.convenio_datos.vacaciones.dias_vacaciones)
            disfrutadas = float(self.nomina.contrato.vacaciones_disfrutadas(self.nomina.fecha_anio))
            nodisfrutadas = diastotales - disfrutadas
            valor = round(diastotales / diasanio * nodisfrutadas,1)
            self.ac_campo('imp_cuantia', round(valor, 0))
        return valor

    def ac_cotiza(self):
        # -------------- Marcamos con un '*' lo que cotiza a la Seg Social
        if self.cotiza_segsocial:
            self.ac_campo('cotiza_si_no', "'*'")

    def ac_devengo_dias(self):
        if self.nomina.contrato.contrato.es_tiempo_completo:
            if self.es_pagar_diasnaturales and self.es_importe_diario and not self.emp_pextra_id > 0:
                cantidad = self.ac_cantidad_dias()
                devengo = self.ac_precio_dias() * cantidad
                self.ac_campo('imp_devengo', devengo)

    def ac_devengo_horas(self):
        if self.nomina.contrato.contrato.es_tiempo_parcial and not self.emp_pextra_id > 0:
            cantidad = self.ac_cantidad_horas()
            valor = self.ac_precio_hora() * cantidad
            print self.ac_precio_hora(), '*', cantidad, '=', valor
            self.ac_campo('imp_devengo', valor)

    def ac_devengo_mes(self):
        if self.nomina.contrato.contrato.es_tiempo_completo and self.es_importe_mensual:
            if not self.emp_pextra_id > 0:
                valor = float(self.ac_precio_mes()) * float(self.ac_cantidad_mes())
                valor = round(valor, 2)
                self.ac_campo('imp_devengo', valor)
        if self.nomina.contrato.contrato.es_tiempo_completo and self.es_importe_diario:
            if not self.emp_pextra_id > 0:
                valor = self.ac_precio_dias() * self.ac_cantidad_dias()
                self.ac_campo('imp_devengo', valor)

    def ac_devengo_vacaciones(self):
        if self.es_vacaciones:
            valor = float(self.ac_precio_vacaciones() * self.ac_cantidad_vacaciones())
            valor = round(valor, 2)
            self.ac_campo('imp_devengo', valor)

    def ac_devengo_indemnizacion(self):
        if self.es_indemnizacion:
            valor = float(self.ac_precio_indemnizacion() * self.ac_cantidad_indemnizacion())
            valor = round(valor, 2)
            self.ac_campo('imp_devengo', valor)

    def ac_deduccion_irpf(self):
        valor = 0
        if self.es_irpf:
            precio = self.ac_precio_deduccion()
            cantidad = self.ac_cantidad_deduccion()
            valor = cantidad * precio / 100
            self.ac_campo('imp_deduccion', valor)
        return round(valor, 2)

    def ac_deduccion_segsocial(self):
        valor = 0
        if not self.es_irpf and not self.es_devengo:
            precio = self.ac_precio_deduccion()
            cantidad = self.ac_cantidad_deduccion()
            valor = cantidad * precio / 100
            self.ac_campo('imp_deduccion', valor)
        return round(valor, 2)

    def ac_importe_emp_devengo(self):
        sql = ("Update "
               "    nomina_devengos A "
               "        inner join "
               "            emp_devengos B "
               "            on A.idemp_devengo = B.idemp_devengo "
               "Set "
               "    A.importe = B.importe "
               "Where "
               "    A.idnomina_devengo = " + unicode(self.id) + " ")
        select_sql(sql)

    def ac_precio_deduccion(self):
        if not self.es_devengo:
            self.ac_campo('imp_precio', self.importe)
        return self.importe

    def ac_precio_dias(self):
        valor = 0
        if self.nomina.contrato.contrato.es_tiempo_completo:
            if self.es_pagar_diasnaturales and self.es_importe_diario:
                if not self.emp_pextra_id:
                    valor = self.importe
                    self.ac_campo('imp_precio', valor)
            if self.es_pagar_lunavie and self.es_importe_diario:
                if not self.emp_pextra_id > 0:
                    valor = self.importe
                    self.ac_campo('imp_precio', valor)
        return valor

    def ac_precio_hora(self):
        valor = 0
        if self.nomina.contrato.contrato.es_tiempo_parcial and not self.emp_pextra_id > 0:
            valor = self.precio_hora()
            if not self.es_manual:
                self.ac_campo('imp_precio', valor)
            else:
                valor = self.precio
        return valor

    def ac_precio_indemnizacion(self):
        valor = 0
        if self.es_indemnizacion:
            nomina = self.nomina.nomina_trabajador_mes(self.nomina.contrato.idtrabajador, self.nomina.fecha_mes,
                                                       self.nomina.fecha_anio)
            nomina = SqlNominas(nomina)
            valor = nomina.devengo_indemnizacion()
            valor = valor / nomina.dias_cotizados()
            self.ac_campo('imp_precio', valor)
        return valor

    def ac_precio_mes(self):
        valor = 0
        if self.nomina.contrato.contrato.es_tiempo_completo and not self.emp_pextra_id > 0:
            if self.es_importe_mensual:
                self.importe = self.dato_devengo('importe')
                valor = self.importe
                self.ac_campo('imp_precio', valor)
        return valor

    def ac_precio_vacaciones(self):
        valor = 0
        if self.es_vacaciones and not self.es_pagavacaciones:
            nomina = self.nomina.nomina_trabajador_mes(self.nomina.contrato.idtrabajador, self.nomina.fecha_mes,
                                                       self.nomina.fecha_anio)
            nomina = SqlNominas(nomina)
            valor = float(nomina.devengo_vacaciones())
            valor /= float(nomina.dias_cotizados())
        elif self.es_vacaciones and self.es_pagavacaciones:
            self.ac_importe_emp_devengo()
            self.importe = self.dato_devengo('importe')
            if self.es_importe_mensual:
                valor = (float(self.importe)/12) / self.nomina.cta_cot.convenio_datos.vacaciones.dias_vacaciones
            elif self.es_importe_diario:
                valor = self.nomina.cta_cot.convenio_datos.vacaciones.dias_vacaciones
        self.ac_campo('imp_precio', round(valor, 2))
        return valor

    def dato_devengo(self, campo):
        try:
            dato = sql_basica(campo, 'nomina_devengos', 'idnomina_devengo', self.id)
        except:
            dato = ""
        if dato is None or dato == '\x00':
            dato = False
        if isinstance(dato, datetime.date):
            dato = dato.strftime('%d/%m/%Y')
        return dato

    def form_concepto(self):
        sql = ('Select '
               '    idform_concepto '
               'From '
               '    form_nomina_celda '
               'Where '
               '    convert(A.dato, unsigned integer) = ' + unicode(self.formulario_id))
        return select_sql(sql)[0]

    def paga_extra(self):
        """
        En el prorrateo de pagas extras se tienen en cuenta dos contratos:
            1. A tiempo completo
                Los cálculos se realizan tomando como base los días y meses
                de aplicación del convenio
            2. A tiempo parcial
                Los cálculos tienen en cuenta las horas anuales totales
                marcadas por el convenio
        """
        pextra = 0
        if self.es_para_pextra:
            """
            1. Comprobamos el número de pagas extras del contrato
            2. Comprobamos el número de días que por convenio corresponden
            3. Comprobamos el calendario
            4. No lleva el coeficiente de pagas extras
            """
            num_pextra = self.nomina.cta_cot.convenio_datos.num_pextra()
            dias_una_paga = self.nomina.cta_cot.convenio_datos.num_dias_pextra() / num_pextra
            dias_anio = self.nomina.cta_cot.calendario.diastotales
            horas_anio = self.nomina.cta_cot.convenio_datos.horas_anio
            dias_efectivos_anio = self.nomina.cta_cot.calendario.totalefectivos
            if self.nomina.contrato.contrato.es_tiempo_completo:
                if self.es_importe_mensual:
                    pextra = self.devengado / 12
                elif self.es_importe_diario:
                    if self.es_pagar_diasnaturales:
                        pextra = self.precio * dias_una_paga / dias_anio
                        pextra = pextra * self.cuantia
                    elif self.es_pagar_lunavie:
                        dias = self.nomina.dias_efectivos_tpo_completo()
                        if self.es_pagar_sabados:
                            dias = self.nomina.dias_efectivos_tpo_completo()
                        pextra = self.precio * dias_una_paga / dias_efectivos_anio
                        pextra = pextra * dias
            elif self.nomina.contrato.contrato.es_tiempo_parcial:
                if self.es_importe_mensual:
                    pextra = (self.importe / horas_anio) * self.cuantia
                elif self.es_importe_diario:
                    if self.es_pagar_diasnaturales:
                        pextra = (dias_una_paga * self.importe) / horas_anio
                        pextra = pextra * self.cuantia
                    elif self.es_pagar_lunavie:
                        pass
                elif self.es_importe_porhora:
                    pass
                pass
        return pextra

    def precio_hora(self):
        es_tpo_completo = self.emp_devengo.contrato.contrato.es_tiempo_completo
        es_tpo_parcial = self.emp_devengo.contrato.contrato.es_tiempo_parcial
        diastot = self.nomina.cta_cot.calendario.diastotales
        horas_dia = self.nomina.cta_cot.convenio_datos.horas_dia
        horas_anio = self.nomina.cta_cot.convenio_datos.horas_anio
        dato = 0
        if self.es_importe_mensual:
            if es_tpo_parcial:
                dato = (self.importe * 12) / horas_anio
            elif es_tpo_completo:
                dato = (self.importe / 30) / horas_dia
        elif self.es_importe_diario:
            if es_tpo_parcial:
                if self.emp_devengo.paga_diasnaturales:
                    dato = self.importe * diastot
                    dato = dato / self.nomina.cta_cot.calendario.totalefectivos
                    dato = dato / horas_dia
                elif self.emp_devengo.paga_diasefectivos:
                    dato = self.importe / horas_dia
            elif es_tpo_completo:
                dato = self.importe / horas_dia
        elif self.es_importe_porhora:
            dato = self.importe
        return dato
