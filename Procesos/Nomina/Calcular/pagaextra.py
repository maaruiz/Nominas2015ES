#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 10/10/2015

@author: miguelangel
'''
from Funciones.Datos.nomina_dat import SqlNominas, Nomina_Devengo

class CalcPextra:
    '''
    classdocs
    '''


    def __init__(self, idnomina = 0):
        '''
        Constructor
        '''
        self.id = idnomina
        self.nomina = SqlNominas(self.id)
        importe = 0
        for x in self.nomina.lista_devengos_nomina():
            self.devengo = Nomina_Devengo(x[0])
            importe = self.devengo.paga_extra()+importe
            print "paga extra",self.devengo.id,importe
