#!/usr/bin/python
# -*- coding: utf-8 -*-
from Funciones.funs import select_sql
from Funciones.Datos.contrato_dat import Contrato
import Procesos.Nomina.Calcular.cotizacion


class Registros:
    def __init__(self):
        pass
    def ins_registros(self):
        """

        1. Insertamos las cabeceras de las nominas sin calculos
           basados en los contratos de la empresa ACTUALIZADOS
        """
        print "insertamos los nuevos registros ...."
        f = self.SqlNom.cabecera_nomina(self.empresa, self.mes, self.anio)
        sql = "Select max(idnomina) as maxid from nominas"
        j = select_sql((sql))[0]

        if not j:
            j = 0
        for filas in f:
            j += 1
            print "Insertamos las cabeceras de la nomina ....", j
            sql = ("INSERT INTO nominas "
                      "(`idnomina`, `idempresa`, `idemp_contratos`, "
                      "`idgrupos_cotizacion`, `idtb_epigrafe`, `antig`, "
                      "`descripcion`, `liquido`, `naf`, `tarifa`, `epigrafe`, "
                      "`matricula`, `nombre`, `categoria`, `dni`, `empresa`, "
                      "`dir`, `cta_cot`, `cif`, fecha, idcta_cot) "
                  "VALUES "
                      "(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                       "%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            select_sql((sql,
                      (j, filas[0], filas[1], filas[2], filas[3],
                       str(filas[4]), ("Nominas de " + self.estemes +
                       " de " + self.anio), filas[5], filas[6], filas[7],
                       filas[8], filas[9], filas[10], filas[11], filas[12],
                       filas[13], filas[14], filas[15], filas[16],
                       self.fecha, filas[18])))
            # Comprobamos si el contrato es de jornada parcial
            z = self.SqlNom.nomina_a_tiempo_parcial(j)

            # ## Insertamos los devengos de nominas
            print "Insertamos los devengos de nominas...", j
            """
        2. Insertamos los devengos de las nóminas a las nóminas a calcular
            """
            sql = ("SELECT "
                      "idemp_devengo, orden, concepto, importe, irpf, cont_com, "
                      "desempleo, fp, fgs, it, ims, ppextra, mensual, diario, "
                      "horas, idemp_pextra, dias_efectivos, dias_naturales, "
                      "esdevengo, esirpf, esdieta, esespecie, esporcentaje, "
                      "esmanual, coef_pextra, fraccionhoras, idform_concepto, "
                      "esvacaciones, pagavacaciones, es_complemento_it_cc, "
                      "es_complemento_it_ef "
                    "FROM "
                      "emp_devengos ")
            sql1 = sql + ("WHERE "
                      "idemp_contrato = %s "
                      "and "
                            "(esdevengo "
                            "and not es_complemento_it_cc "
                            "and not es_complemento_it_ef "
                            "and not idemp_pextra or idemp_pextra is null) "
                    "ORDER by "
                      "idemp_contrato, orden")
            h = select_sql((sql1, (filas[1])), 1)
            k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
            orden = 0
            for col in h:
                orden += 1
                if not k:
                    k = 1
                else:
                    k += 1
                sql2 = ("INSERT INTO nomina_devengos "
                      "(`idnomina_devengo`, `idnomina`, `idemp_devengo`, "
                      "`orden`, `concepto`, `importe`, `irpf`, `cont_com`, "
                      "`desempleo`,`fp`, `fgs`, `it`, `ims`, `ppextra`, "
                      "`mensual`, `diario`, `horas`, `idemp_pextra`, "
                      "`dias_efectivos`, `dias_naturales`, `esdevengo`, "
                      "esirpf, esdieta, esespecie, esporcentaje, esmanual, "
                      "coef_pextra, fraccionhoras, idform_concepto, "
                      "esvacaciones, pagavacaciones, es_complemento_it_cc, "
                      "es_complemento_it_ef) "
                      "VALUES "
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                         "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                         "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                         "%s, %s, %s)")
                campos = (k, j, col[0], orden, col[2], col[3],
                                col[4], col[5], col[6], col[7], col[8],
                                col[9], col[10], col[11], col[12],
                                col[13], z, col[15], col[16],
                                col[17], col[18], col[19], col[20],
                                col[21], col[22], col[23], col[24],
                                col[25], col[26], col[27], col[28],
                                col[29], col[30])
                select_sql((sql2, campos))
            """
        3. Insertamos las pagas extras si están prorrateadas de las nóminas a calcular
            """
            contrato = Contrato(filas[1])
            if contrato.con_prorrata_pextra:
                print "*********************** Prorrateo pagas extras "
                print col
                print "     Tiene prorrateada las pagas extras"
                sql1 = sql + ("WHERE "
                                "idemp_contrato = %s "
                                "and "
                                    "(esdevengo "
                                    "and not es_complemento_it_cc "
                                    "and not es_complemento_it_ef "
                                    "and  idemp_pextra) "
                            "ORDER by "
                                "idemp_contrato, orden")
                h = select_sql((sql1, (filas[1])), 1)
                k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
                for col in h:
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
                                col[29], col[30])
                    select_sql((sql2, campos))
            """
        3. Insertamos los devengos si hay baja por enfermedad
            """
            # Comprobamos si hay baja por IT
            base = Procesos.Nomina.Calcular.cotizacion.Bases(j)

            if base.it_dias_mes() > 0:
                print "*********************** IT "
                print col
                sql1 = sql + ("WHERE "
                      "idemp_contrato = %s "
                      "and es_complemento_it_cc "
                    "ORDER by "
                      "idemp_contrato, orden")
                h = select_sql((sql1, (filas[1])),1)
                k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
                for col in h:
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
                                col[29], col[30])
                    select_sql((sql2, campos ))
            """
        4. Insertamos las deducciones
            """

            sql1 = sql + ("WHERE "
                            "idemp_contrato = %s "
                            "and not esdevengo "
                        "ORDER by "
                            "idemp_contrato, orden")
            h = select_sql((sql1, (filas[1])),1)
            k = select_sql("Select max(idnomina_devengo) + 1 "
                           "from nomina_devengos")[0]
            for col in h:
                print "*********************** Deducciones "
                print col
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
                            col[29], col[30])
                select_sql((sql2, campos))
        return

    def update_importes(self, nomina):
        """

        4. Proceso de actualizacion de los importes de las nominas
        """
        sql = ("UPDATE "
                    "nomina_devengos A "
                        "inner join "
                            "emp_devengos B "
                            "on A.idemp_devengo = B.idemp_devengo "
                "set "
                    "A.importe = B.importe "
                "where "
                    "A.idnomina =  %s ")
        select_sql((sql, nomina))