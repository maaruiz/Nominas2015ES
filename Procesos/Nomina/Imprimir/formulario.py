#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import locale
import datetime

from Funciones.funs import select_sql, sql_basica
from Funciones.Datos.nomina_dat import SqlNominas
from reportlab.lib.units import mm

class impr_nomina():


##################################
##### CLASE IMPRIMIR NOMINAS #####
##################################


    def __init__(self, c, num_empresa, mes, anio, formnom, es_una_nomina=0):
        #### Empezamos a imprimir una nomina en un fichero PDF
        self.c = c
        self.num_empresa = num_empresa
        self.mes = mes
        self.anio = anio
        self.datos(self.c, self.num_empresa, self.mes, self.anio, formnom, es_una_nomina)

    def datos(self, c, num_empresa, mes, anio, formnom, es_una_nomina):
        # introducimos los datos en el formato que imprime solo nominas y no finiquitos
        # para imprimir finiquito ha de seleccionar una a una la nomina
        nominas = SqlNominas(0).idnom_mes(self.num_empresa, self.mes, self.anio, es_una_nomina)
        y = 0
        for p in nominas:
            FormNomina(formnom).formnomina_listaid(c) # pintamos todas las cajas
            celdas = FormNomina(formnom).formnomina_listatablas()    # preparamos la impresion de los campos de las tablas
            z = 0
            for j in celdas:
                dataform = FormCelda(j[0])
                if dataform.formconcepto_id:  # si hay un concepto de formulario enlazado
                    sql = ("Select " + dataform.campo + ", ancho_dato, "
                           "    datoalineacion, idform_celda, orden, concepto, print_etiqueta "
                           "from "
                           "    form_nomina_celda A "
                           "        inner join "
                           "            nomina_devengos B "
                           "            on convert(A.dato, unsigned integer) = B.idform_concepto "
                           "where "
                           "    idform_concepto = %s "
                           "    and idnomina = %s "
                           "group by "
                           "    concepto ")
                    valores = select_sql((sql, (dataform.formconcepto_id, p[0])), 1)
                    if valores:
                        for h in valores:
                            if dataform.label_print:
                                self.concepto(dataform.formconcepto_id, p[0], h[4],
                                              dataform.dato_ancho, c, dataform.id, dataform.label_print)
                            self.valorcelda(dataform.formconcepto_id, p[0], c, dataform.id, dataform.campo)

                else:
                    sql = (
                           "Select " + dataform.campo + ", idnomina "
                           " from " + dataform.tabla +
                           " where idnomina = " + unicode(p[0])
                           )
                    valores = select_sql(sql, 1)
                    if valores:
                        for h in valores:
                            self.valorcelda(dataform.formconcepto_id, p[0], c, dataform.id, dataform.campo)
                try:
                    pass
                    #self.valorcelda(dataform.formconcepto_id, nominas[y][0], c, dataform.id, dataform.campo)
                except MySQLdb.Error, e:
                    print "Error",e
                    sql = ("Select " + dataform.campo + ", orden "
                            "from nomina_devengos "
                            "where idnomina = %s;")

                    try:
                        concept = select_sql((sql, (nominas[y][0])), 1)
                        w = 0
                        for k in concept:
                            print 'Paso por aqui'
                            self.concepto(dataform.formconcepto_id,
                                              nominas[y][0],
                                              w[1],
                                              dataform.dato_ancho,
                                              c, dataform.id,
                                              dataform.label_print)
                            w += 1
                    except MySQLdb.Error, e:
                        print "Error",e
                z += 1
            variables = FormNomina(formnom).formnomina_listavariables()
            print variables
            for q in variables:
                varform = FormCelda(q[0])
                if varform.formconcepto_id:
                    self.valorcelda(unicode(varform.formconcepto_id), p[0], c, varform.id, varform.campo)

                pass
            c.showPage()  # ## Salto de pagina
            y += 1

    def valorcelda(self, celda, nomina, c, idform_celda, *campo):
        # # Funcion que nos devuelve el contenido de la celda
        #  de la cabecera y del pie
        # celda es idform_concepto
        try:
            sql = ("select " + unicode(campo[0]) +
                   " from nomina_devengos "
                   " where idnomina = %s and idform_concepto = %s")
            reg = select_sql((sql, (nomina, celda)))[0]
        except:
            try:
                reg = SqlNominas(nomina).dato_nomina(campo[0])
                if not reg:
                    reg = SqlNominas(nomina).__dict__[campo[0]]
            except:
                pass
        dataform = FormCelda(idform_celda)
        c.setFillGray(0)
        c.setFont("Courier", 9)
        # Comprobamos que los datos de fecha y valor queden como string correcto
        if campo[0] == 'fecha':
            reg = SqlNominas(nomina).fecha_formlargo
        if isinstance(reg, float):
            reg = "{:,.2f}".format(reg)
        if reg is not None:
            dataform.dato_draw(c,reg)


    def concepto(self, celda, nomina, orden, ancho_dato, c, idform_celda, impr):
        # # Funcion que nos imprime el cuerpo de la nomina: conceptos salariales
        try:
            celda = int(celda)
            sql = ("select "
                   "    concepto "
                   "from "
                   "    nomina_devengos B "
                   "        inner join "
                   "            form_nomina_celda A "
                   "            on convert(A.dato, unsigned integer) = B.idform_concepto "
                   "where "
                   "    idnomina = %s and B.idform_concepto = %s "
                   "    and orden = %s and (etiqueta = '' or etiqueta is null) "
                   "group by "
                   "    concepto ")
            rec = select_sql((sql, (nomina, celda, orden))) # seleccionamos los conceptos de los devengos a imprimir
            esconcepto = 1                                  # cuando hay un enlace a un form_concepto
        except ValueError:
            sql = ("select " + celda +
                   " from nomina_devengos where idnomina=%s and orden=%s")
            rec = select_sql((sql, (nomina, orden)))       # seleccionamos los conceptos de los devengos a imprimir
            esconcepto = 0                                 # cuando hay un
        if rec:
            reg = rec[0]
            dataform = FormCelda(idform_celda)
            c.setFillGray(0)
            c.setFont("Courier", 9)
            if isinstance(rec[0], float):
                reg = "{:>7,.2f}".format(rec[0])
            if reg is not None:
                if reg.strip() != '0.00':
                    if esconcepto == 0:
                        c.drawString(dataform.label_x * mm, (dataform.label_y - orden * 5) * mm +
                                     1 * mm, unicode(reg))
                    elif impr == 1:
                        c.drawString(dataform.label_x * mm, (dataform.label_y + dataform.label_alto) * mm +
                                      1 * mm, unicode(reg))


    #####  Fin de la impresion de la nomina en un fichero PDF

class FormCelda:
    def __init__(self, idform):
        self.id = idform
        self.campo = self.campoformcelda('campo')
        self.centro = self.campoformcelda('centro')
        self.dato = self.campoformcelda('dato')
        self.dato_x = self.campoformcelda('x1dato')
        self.dato_y = self.campoformcelda('y1dato')
        self.dato_alineacion = self.campoformcelda('datoalineacion')
        self.dato_ancho = self.campoformcelda('ancho_dato')
        self.dato_alto = self.campoformcelda('alto_dato')
        self.dato_bordes = self.campoformcelda('fill')
        self.font_size = self.campoformcelda('font_size')
        if self.dato is not None:
            if self.dato == 33:print '    .... Daot', self.dato, self.campo
            if self.dato > 0:
                if self.dato.isdigit():
                    self.formconcepto_id = self.campoformcelda('convert(dato, unsigned integer)')
                else:
                    self.formconcepto_id = 0
            else:
                self.formconcepto_id = 0
        else:
            self.formconcepto_id = 0
        self.formnomina_id = self.campoformcelda('idform_nomina')
        self.label = self.campoformcelda('etiqueta')
        self.label_x = self.campoformcelda('x1etiqueta')
        self.label_y = self.campoformcelda('y1etiqueta')
        self.label_ancho = self.campoformcelda('ancho_etiqueta')
        self.label_alto = self.campoformcelda('alto_etiqueta')
        self.label_print = self.campoformcelda('print_etiqueta')
        self.label_relleno = self.campoformcelda('fill_etiqueta')
        self.linea_ancho = self.campoformcelda('ancho_linea')
        self.linea_puntos_impr = self.campoformcelda('puntoslineaimprime')
        self.linea_puntos_noimpr = self.campoformcelda('puntoslineanoimprime')
        self.tabla = self.campoformcelda('tabla')


    def campoformcelda(self, campo):
        return sql_basica(campo, 'form_nomina_celda', 'idform_celda', self.id)

    def labelform(self):
        return (self.label_x, self.label_ancho, self.label_y, self.label_alto, self.label_print)

    def datoform(self):
        return (self.dato_x, self.dato_ancho, self.dato_y, self.dato_alto)

    def dato_draw(self, canvas, dato):
        if self.dato_alineacion == 'i':  # alineacion a la izquierda
            canvas.drawString((self.dato_x + 1) * mm,
                         (self.dato_y + 1) * mm, unicode(dato))
        elif self.dato_alineacion == 'c':  # alineacion al centro
            canvas.drawCentredString((self.dato_x + self.dato_ancho / 2) * mm,
                                        self.dato_y * mm + 1 * mm, unicode(dato))
        elif self.dato_alineacion == 'd':  # alineacion a la derecha
            canvas.drawRightString((self.dato_x + self.dato_ancho) * mm + 1,
                                      (self.dato_y + 1) * mm, unicode(dato))

    def label_draw(self, canvas):
        # # Definimos el formato de los titulos que acompanian
        # c.rect() -> rectangulo
        # c.setLineWidth -> ancho de linea
        # c.stFillGray -> relleno de gris del rectangulo
        # c.setDash() -> trazo de linea
        canvas.setFillGray(0.90)
        canvas.setDash(int(self.linea_puntos_impr), int(self.linea_puntos_noimpr))
        canvas.setLineWidth(self.linea_ancho)

        if self.dato_bordes:  # trazo rectangulo datos
            canvas.rect(self.dato_x * mm, self.dato_y * mm,
                       self.dato_ancho * mm, self.dato_alto * mm, fill=0)
        if self.label_relleno:  # trazo rectangulo etiquetas
            canvas.rect(self.label_x * mm, self.label_y * mm,
                       self.label_ancho * mm, self.label_alto * mm, fill=self.dato_bordes)
        canvas.setFillGray(0)
        canvas.setFont("Helvetica", self.font_size)
        try:
            if self.centro:  # si se alinea al centro
                canvas.drawCentredString((self.label_x +
                                         self.label_ancho / 2) * mm,
                                         self.label_y * mm + 1 * mm,
                                         self.label)
            else:  # en otro caso
                canvas.drawString((self.label_x + 1) * mm,
                                 (self.label_y + 1) * mm,
                                  self.label)

        except AttributeError:
            pass


class FormConcepto:
    def __init__(self, idformconcepto):
        self.id = idformconcepto
        self.descripcion = self.campoformconcepto('descripcion')

    def campoformconcepto(self, campo):
        return sql_basica(campo, 'form_conceptos', 'idform_conceptos', self.id)


class FormNomina:
    def __init__(self, idform):
        self.id = idform
        self.descripcion = self.campoformnomina('descripcion')

    def campoformnomina(self, campo):
        return sql_basica(campo, 'form_nomina', 'idform_nomina', self.id)

    def dic_formnomina_tablas(self):
        lista = self.formnomina_listatablas()
        indice = {}
        for x in lista:
            dataform = FormCelda(x[0])
            indice[x[0]] = [dataform.formconcepto_id, dataform.tabla, dataform.campo]
        return indice

    def formnomina_listaid(self, canvas):
        sql = 'select idform_celda from form_nomina_celda where idform_nomina = ' + unicode(self.id)
        lista = select_sql(sql,1)
        for x in lista:
            dataform = FormCelda(x[0])
            dataform.label_draw(canvas)

    def formnomina_listatablas(self):
        sql = ('Select '
               '    idform_celda  '
               'From '
               '    form_nomina_celda '
               'Where '
               '    tabla is not null '
               '    and tabla <>""'
               '    and idform_nomina = ' + unicode(self.id))
        return select_sql(sql, 1)

    def formnomina_listavariables(self):
        sql = ('Select '
               '    idform_celda  '
               'From '
               '    form_nomina_celda '
               'Where '
               '    (tabla is null '
               '    or tabla ="") '
               '    and (campo is not null and campo <>"") '
               '    and idform_nomina = ' + unicode(self.id))
        return select_sql(sql, 1)