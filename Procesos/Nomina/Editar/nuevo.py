#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 04/10/2015

@author: miguelangel
"""
import locale
import time

from Funciones.Datos.nomina_dat import SqlNominas
from Funciones.funs import select_sql, ultimodiames
from Funciones.Datos.contrato_dat import Contrato
from Procesos.Nomina.Calcular.cotizacion import Bases
from Procesos.Nomina.Calcular.cabecera import Cabecera


class Alta:
    """
    classdocs
    """
    def __init__(self, mes, anio, empresa, trabajador=0, esnomina=True, esfiniquito=False, esnominapextra=False):
        """
        Constructor
        """
        self.mes = mes
        self.anio = anio
        self.dia = ultimodiames(mes, anio)
        self.fecha = str(self.anio) + "-" + str(self.mes) + "-" + str(self.dia)
        self.empresa = empresa
        self.es_finiquito = esfiniquito
        self.es_nomina = esnomina
        self.es_nominapextra = esnominapextra
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        self.estemes = time.strftime("%B", time.strptime(str(self.mes) + ',' + str(self.anio), '%m,%Y'))
        self.trabajador_id = trabajador
        self.SqlNom = SqlNominas()
        self.cabecera = Cabecera(self.empresa, self.mes, self.anio, self.trabajador_id)
        print "*********** ALTA NOMINA **************"
        print 'Nomina:', self.es_nomina, '         Finiquito:', self.es_finiquito
        self.nominas_empresa()

    def nominas_empresa(self):
        """
        1. Insertamos las cabeceras de las nominas sin calculos
           basados en los contratos de la empresa ACTUALIZADOS
        """
        print "insertamos los nuevos registros ...."
        f = self.cabecera.nomina(self.es_nomina, self.es_finiquito, self.es_nominapextra)
        sql = "Select max(idnomina) as maxid from nominas"
        j = select_sql(sql)[0]

        if not j:
            j = 0
        for filas in f:
            j += 1  # numero de nomina o idnomina
            print "Insertamos las cabeceras de la nomina ************************", j
            sql = ('INSERT INTO nominas '
                   '(`idnomina`, `idempresa`, `idemp_contratos`, '
                   '`idgrupos_cotizacion`, `idtb_epigrafe`, `antig`, '
                   '`descripcion`, `liquido`, `naf`, `tarifa`, `epigrafe`, '
                   '`matricula`, `nombre`, `categoria`, `dni`, `empresa`, '
                   '`dir`, `cta_cot`, `cif`, fecha, idcta_cot, es_finiquito) '
                   'VALUES '
                   '(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, '
                   '%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            select_sql((sql,
                        (j, filas[0], filas[1], filas[2], filas[3],
                         str(filas[4]), ("Nominas de " + self.estemes +
                                         " de " + str(self.anio)), filas[5], filas[6], filas[7],
                         filas[8], filas[9], filas[10], filas[11], filas[12],
                         filas[13], filas[14], filas[15], filas[16],
                         self.fecha, filas[18], self.es_finiquito)))
            # Comprobamos si el contrato es de jornada parcial
            self.SqlNom(j)
            z = self.SqlNom.nomina_a_tiempo_parcial()

            # ## Insertamos los devengos de nominas
            print "Insertamos los devengos de nominas ***************************", j, self.SqlNom.contrato.trabajador.nombre
            """
        2. Insertamos los devengos de las nominas a las nóminas a calcular
            """
            sql = ('SELECT '
                   'idemp_devengo, orden, concepto, importe, irpf, cont_com, '
                   'desempleo, fp, fgs, it, ims, ppextra, mensual, diario, '
                   'horas, idemp_pextra, dias_efectivos, dias_naturales, '
                   'esdevengo, esirpf, esdieta, esespecie, esporcentaje, '
                   'esmanual, coef_pextra, fraccionhoras, idform_concepto, '
                   'esvacaciones, pagavacaciones, es_complemento_it_cc, '
                   'es_complemento_it_ef, es_indemnizacion '
                   'FROM '
                   'emp_devengos '
                   'WHERE '
                   'idemp_contrato = %s ')
            sql1 = sql + ('and '
                          '(esdevengo '
                          'and not es_indemnizacion '
                          'and not esvacaciones '
                          'and not es_complemento_it_cc '
                          'and not es_complemento_it_ef '
                          'and (not idemp_pextra or idemp_pextra is null)) ')

            sql1 += 'ORDER by idemp_contrato, orden '
            h = select_sql((sql1, (filas[1])), 1)
            k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
            orden = 0
            sql2 = ("INSERT INTO nomina_devengos "
                    "(`idnomina_devengo`, `idnomina`, `idemp_devengo`, "
                    "`orden`, `concepto`, `importe`, `irpf`, `cont_com`, "
                    "`desempleo`,`fp`, `fgs`, `it`, `ims`, `ppextra`, "
                    "`mensual`, `diario`, `horas`, `idemp_pextra`, "
                    "`dias_efectivos`, `dias_naturales`, `esdevengo`, "
                    "esirpf, esdieta, esespecie, esporcentaje, esmanual, "
                    "coef_pextra, fraccionhoras, idform_concepto, "
                    "esvacaciones, pagavacaciones, es_complemento_it_cc, "
                    "es_complemento_it_ef, es_indemnizacion) "
                    "VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                    "%s, %s, %s, %s)")
            print "*********************** Devengos "
            if self.es_nomina:
                for col in h:
                    print '    ',col[2], col[3]
                    orden += 1
                    if not k:
                        k = 1
                    else:
                        k += 1

                    campos = (k, j, col[0], orden, col[2], col[3],
                              col[4], col[5], col[6], col[7], col[8],
                              col[9], col[10], col[11], col[12],
                              col[13], z, col[15], col[16],
                              col[17], col[18], col[19], col[20],
                              col[21], col[22], col[23], col[24],
                              col[25], col[26], col[27], col[28],
                              col[29], col[30], col[31])
                    select_sql((sql2, campos))
            """
        3. Insertamos las pagas extras si están prorrateadas de las nóminas a calcular o es finiquito o es nomina
            """
            contrato = Contrato(filas[1])
            if (contrato.con_prorrata_pextra or (
                        not contrato.con_prorrata_pextra and self.es_finiquito) or self.es_nominapextra):
                print "*********************** Prorrateo pagas extras / Finiquito "
                sql1 = sql + ("and "
                              "(esdevengo "
                              "and not es_indemnizacion "
                              "and not esvacaciones "
                              "and not es_complemento_it_cc "
                              "and not es_complemento_it_ef "
                              "and  idemp_pextra) "
                              "ORDER by "
                              "orden")
                h = select_sql((sql1, (filas[1])), 1)
                k = select_sql("Select max(idnomina_devengo) "
                               "from nomina_devengos")[0]
                for col in h:
                    print '    ',col[2], col[3]
                    orden += 1
                    if not k:
                        k = 1
                    else:
                        k += 1
                    campos = (k, j, col[0], orden, col[2], col[3],
                              col[4], col[5], col[6], col[7], col[8],
                              col[9], col[10], col[11], col[12],
                              col[13], z, col[15], col[16],
                              col[17], col[18], col[19], col[20],
                              col[21], col[22], col[23], col[24],
                              col[25], col[26], col[27], col[28],
                              col[29], col[30], col[31])
                    select_sql((sql2, campos))
            """
        4. Insertamos los devengos si hay baja por enfermedad
            """
            # Comprobamos si hay baja por IT
            base = Bases(j)
            print "*********************** Bases"
            try:
                base.it_nomina.it_dias_mes
                print "*********************** IT "
                sql1 = sql + ("and es_complemento_it_cc "
                              "ORDER by "
                              "idemp_contrato, orden")
                h = select_sql((sql1, (filas[1])), 1)
                k = select_sql("Select max(idnomina_devengo) "
                               "from nomina_devengos")[0]
                for col in h:
                    print '    ',col[2], col[3]
                    orden += 1
                    if not k:
                        k = 1
                    else:
                        k += 1
                    campos = (k, j, col[0], orden, col[2], col[3],
                              col[4], col[5], col[6], col[7], col[8],
                              col[9], col[10], col[11], col[12],
                              col[13], z, col[15], col[16],
                              col[17], col[18], col[19], col[20],
                              col[21], col[22], col[23], col[24],
                              col[25], col[26], col[27], col[28],
                              col[29], col[30], col[31])
                    select_sql((sql2, campos))
            except:
                pass
            '''
            5. Insertamos la indemnización si es un finiquito
            '''
            print "*********************** Indemnizacion Finiquito"
            if self.es_finiquito:
                sql1 = sql + (" and (es_indemnizacion "
                              " or esvacaciones) "
                              " ORDER by "
                              " idemp_contrato, orden ")
                h = select_sql((sql1, (filas[1])), 1)
                k = select_sql("Select max(idnomina_devengo) "
                               "from nomina_devengos")[0]
                for col in h:
                    print '    ', col[2], col[3]
                    orden += 1
                    if not k:
                        k = 1
                    else:
                        k += 1
                    campos = (k, j, col[0], orden, col[2], col[3],
                              col[4], col[5], col[6], col[7], col[8],
                              col[9], col[10], col[11], col[12],
                              col[13], z, col[15], col[16],
                              col[17], col[18], col[19], col[20],
                              col[21], col[22], col[23], col[24],
                              col[25], col[26], col[27], col[28],
                              col[29], col[30], col[31])
                    select_sql((sql2, campos))
            """
            6. Insertamos las deducciones
            """

            sql1 = sql + ("and not esdevengo "
                          "ORDER by "
                          "idemp_contrato, orden")
            h = select_sql((sql1, (filas[1])), 1)
            k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
            print "*********************** Deducciones "

            for col in h:
                print '    ', col[2], col[3]
                orden += 1
                if not k:
                    k = 1
                else:
                    k += 1
                campos = (k, j, col[0], orden, col[2], col[3],
                          col[4], col[5], col[6], col[7], col[8],
                          col[9], col[10], col[11], col[12],
                          col[13], z, col[15], col[16],
                          col[17], col[18], col[19], col[20],
                          col[21], col[22], col[23], col[24],
                          col[25], col[26], col[27], col[28],
                          col[29], col[30], col[31])
                select_sql((sql2, campos))
        # self.actualizar = Actualizar(j)
        return
