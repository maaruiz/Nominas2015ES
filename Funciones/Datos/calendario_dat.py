#!/usr/bin/python
# -*- coding: utf-8 -*-

import calendar
import datetime

from Funciones.funs import ultimodiames, select_sql
from Funciones.Datos.contrato_dat import Contrato
from wstools.Utility import DOM


class Calendario:
    """
        Realiza los calculos necesarios de los dias de trabajo entre dos fechas.
        Se necesitan pasar dos parámetros:

            desde -> tipo lista que contiene anio, mes y dia iniciales
                desde = (anio, mes, dia)
            hasta -> tipo lista que contiene anio, mes y dia finales
                hasta = (anio, mes, dia)
    """
    def __init__(self, idcalendario, anio):
        """

        Inicializa las variables que se necesitan:
           primero = dia inicial (variable datetime.date)
           ultimo = dia ultimo (variable datetime.date)

           Lista desde:
              desdeanio = anio inicial (var. INT)
              desdemes = mes anio inicial (var INT)
              desdedia = dia anio inicial (var INT)

           Lista hasta:
              hastaanio = anio final (var INT)
              hastames = mes anio final (var INT)
              hastadia = dia anio final (var INT)
        """
        self.calendario_id = idcalendario
        self.anio = anio
        self.desde(self.anio,1,1)
        self.hasta(self.anio,12,31)
        sql = ( "Select "
                    "A.idcalendario, A.descripcion, A.idmunicipio, "
                    "B.anio, B.mes, B.dia, B.idcal_festivo, "
                    "B.esfestivo_nnal, B.esfestivo_reg, B.esfestivo_loc, "
                    "B.esfestivo_convenio "
                "From "
                    "calendario A "
                        "inner join "
                            "cal_festivos B "
                        "on A.idcalendario = B.idcalendario "
                "Where "
                    "A.idcalendario = %s "
                    "and B.anio = %s;")
        self.diasfestivos = select_sql((sql,(self.calendario_id, self.anio)),1)
        self.totalanios = self.hastaanio - self.desdeanio
        self.nolaboral()

    def __call__(self, idcalendario, anio):
        self.__init__(idcalendario, anio)

    def desde(self, anio, mes, dia):
        self.desdeanio = anio
        self.desdemes = mes
        self.desdedia = dia
        self.primero = datetime.date(self.desdeanio, self.desdemes, self.desdedia)
        return anio, mes, dia

    def hasta(self, anio, mes, dia):
        self.hastaanio = anio
        self.hastames = mes
        self.hastadia = dia
        self.ultimo = datetime.date(self.hastaanio, self.hastames, self.hastadia)
        return self.hastaanio, self.hastames, self.hastadia

    def nolaboral(self):
        """
        Calcula el número de fines de semana y festivos entre las fechas introducias y
        devuelve los valores de (sab, dom, fes)
        """
        sab = 0
        dom = 0
        fes = 0
        for xanio in range(self.desdeanio, self.hastaanio + 1):
            if xanio < self.hastaanio and xanio == self.desdeanio:
                for xmes in range(self.desdemes, 12 + 1):
                    if xmes == self.desdemes:
                        sab = sab + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                 ultimodiames(xmes, xanio), 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                 ultimodiames(xmes, xanio), 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio,
                                                xmes, self.desdedia, self.hastadia)
                    else :
                        sab = sab + self.diasemana_delmes(xanio, xmes, 1,
                                                 ultimodiames(xmes, xanio), 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, 1,
                                                 ultimodiames(xmes, xanio), 6)
                        fes = fes + self.festivosdelmes(self.calendario_id,xanio, xmes, 1,
                                                 ultimodiames(xmes, xanio))
            elif self.hastaanio > xanio > self.desdeanio:
                for xmes in range(1,12+1):
                    sab = sab + self.diasemana_delmes(xanio, xmes,
                                                   1, ultimodiames(xmes, xanio), 5)
                    dom = dom + self.diasemana_delmes(xanio, xmes,
                                                   1, ultimodiames(xmes, xanio), 6)
                    fes = fes + self.festivosdelmes(self.calendario_id, xanio, xmes,
                                                    1, ultimodiames(xmes, xanio))
            elif xanio == self.hastaanio and xanio > self.desdeanio:
                for xmes in range(1, self.hastames + 1):
                    if xmes == self.hastames:
                        sab = sab + self.diasemana_delmes(xanio, xmes, 1, self.hastadia, 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, 1, self.hastadia, 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio,
                                                        xmes, 1, self.hastadia)
                    else:
                        sab = sab + self.diasemana_delmes(xanio, xmes, 1,
                                                 ultimodiames(xmes, xanio), 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, 1,
                                                 ultimodiames(xmes, xanio), 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio,
                                                        xmes, 1, ultimodiames(xmes, xanio))
            elif xanio == self.hastaanio and xanio == self.desdeanio:
                for xmes in range(self.desdemes, self.hastames + 1):
                    if xmes == self.desdemes and xmes < self.hastames:
                        sab = sab + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                       ultimodiames(xmes, xanio), 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                        ultimodiames(xmes, xanio), 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio,
                                                        xmes, self.desdedia,
                                                        ultimodiames(xmes, xanio))
                    elif self.desdemes < xmes < self.hastames:
                        sab = sab + self.diasemana_delmes(xanio, xmes, 1,
                                                       ultimodiames(xmes, xanio), 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, 1,
                                                        ultimodiames(xmes, xanio), 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio, xmes,
                                                        1, ultimodiames(xmes, xanio))
                    elif xmes > self.desdemes and xmes == self.hastames:
                        sab = sab + self.diasemana_delmes(xanio, xmes, 1, self.hastadia, 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, 1, self.hastadia, 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio, xmes,
                                                        1, self.hastadia)
                    elif xmes == self.desdemes and xmes == self.hastames:
                        sab = sab + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                       self.hastadia, 5)
                        dom = dom + self.diasemana_delmes(xanio, xmes, self.desdedia,
                                                        self.hastadia, 6)
                        fes = fes + self.festivosdelmes(self.calendario_id, xanio, xmes, self.desdedia,
                                                        self.hastadia)
        self.totaldomingos = dom
        self.totalsabados = sab
        self.totalfestivos = fes
        self.diastotales = (self.ultimo - self.primero).days + 1
        self.totalefectivos = self.diastotales - self.totalsabados - self.totaldomingos - self.totalfestivos
        return sab,dom, fes

    def festivosdelmes(self, calendario, anio, mes, desdedia, hastadia):
        """

        Calcula el numero de dias festivos de un mes teniendo en cuenta las
        fechas introducidas.
        Los parámetros que hay que introducir son de tipo INT

            Dias.festivosdelmes(calendario, anio, mes, desdedia, hastadia)

        Los diasfestivos deben aportarse de un calendario externo.
        """
        sql = ( "Select "
                    "count(*) "
                "From "
                    "cal_festivos "
                "Where "
                    "idcalendario = %s "
                    "and anio = %s "
                    "and mes = %s "
                    "and dia >= %s "
                    "and dia <= %s "
                "Group by "
                    "idcalendario;")
        dato = 0
        try:
            dato = select_sql((sql, (calendario, anio, mes, desdedia, hastadia)))[0]
        except:
            pass
        return dato

    def diasemana_delmes(self, anio, mes, desdedia, hastadia, diasemana):
        """
        Calcula el número de un dia de la semana entre fechas
        0 = lunes
        1 = martes
        2 = miercoles
        3= jueves
        4 = viernes
        5 = sabado
        6 = domingo
        """
        calmes = calendar.Calendar().monthdays2calendar(anio, mes)
        x = 0
        for c in calmes:
            if desdedia <= c[diasemana][0] <= hastadia:
                x += 1
        return x
    def dias_entre_fechas(self):
        contrato = Contrato()
        dia_final = self.hasta(anio, mes, dia)