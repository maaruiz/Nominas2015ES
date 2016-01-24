# -*- coding: utf-8 -*-
from Funciones.Datos.vacaciones import SqlVacaciones

class finiquito_calc():
    def __init__(self):
        self.contrato = 17
        pass
    def vacaciones(self):
        SqlVac = SqlVacaciones(self.contrato)
        print "Finiquito - vacaciones", SqlVac.dias_trabajados_ultimo_anio
        pass
    def indemnizacion(self):
        pass
    def otros(self):
        pass

class finiquito_imp():
    def __init__(self):
        pass
    def formato(self):
        pass
    def datos(self):
        pass
    def coordenadas(self):
        pass
    def valorcelda(self):
        pass
    def concepto(self):
        pass