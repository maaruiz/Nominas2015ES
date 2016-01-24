'''
Created on 04/10/2015

@author: miguelangel
'''
from Funciones.funs import select_sql
from Funciones.Datos.contrato_dat import Contrato

class NomBorrar:
    '''
    classdocs
    '''


    def __init__(self, idempresa, mes, anio, idcontrato = 0, esnomina=True, esfiniquito=False, esnominapextra=False):
        '''
        Constructor
        '''
        self.empresa_id = idempresa
        self.esnomina = esnomina
        self.esnominapextra = esnominapextra
        self.esfiniquito = esfiniquito
        self.mes = mes
        self.anio = anio
        self.contrato_id = idcontrato
        try:
            self.contrato = Contrato(self.contrato_id)
        except:
            pass

    def borrar_mes(self):
        print "Borramos las nominas ..."
        sql = ("DELETE "
                       "nominas, nomina_devengos "
                    "FROM "
                       "nominas "
                     "left join nomina_devengos "
                       "ON nominas.idnomina = nomina_devengos.idnomina "
                   "WHERE "
                      "nominas.idempresa=%s and month(nominas.fecha)=%s "
                      "and year(nominas.fecha)=%s ")
        if self.contrato_id:
            sql1 = "and  nominas.idemp_contratos = " + unicode(self.contrato_id) + " "
        else:
            if self.esfiniquito:
                sql1 = "and nominas.es_finiquito "
            elif self.esnominapextra:
                sql1 = "and nominas.es_nominapextra "
            else:
                sql1 = ''
        sql += sql1
        print sql
        select_sql((sql, (self.empresa_id, self.mes, self.anio)))