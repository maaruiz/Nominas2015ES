import datetime
from Funciones.funs import select_sql
from Funciones.Datos.nomina_dat import SqlNominas

class SqlVacaciones():

    def __init__(self, contrato):
        sql = ("Select "
                    "A.idemp_contratos, A.idempresa, A.idemp_ctacot, "
                    "A.idtrabajadores, A.fecha_fin, A.fecha_ini, B.idtb_vacaciones, "
                    "C.cantidad, C.cantidad_min, C.esdias_naturales, "
                    "C.esdias_laborales, C.consab, C.condom, C.confestivos, "
                    "C.esmindias_naturales, C.esmindias_laborales, "
                    "1 + datediff(fecha_fin, "
                                "if(year(fecha_fin) = year(fecha_ini), "
                                   "fecha_ini, "
                                   "makedate(year(fecha_fin),1))"
                                ") "
               "from emp_contratos A "
                    "inner join emp_vacaciones B "
                        "on A.idempresa = B.idempresa "
                        "and A.idemp_ctacot = B.idemp_ctacot "
                    "inner join tb_vacaciones C "
                        "on B.idtb_vacaciones = C.idtb_vacaciones "
               "where A.idemp_contratos = %s ")
        datos = select_sql((sql, contrato))
        print datos
        self.idcontrato = datos[0]
        self.idempresa = datos[1]
        self.idcuentacot = datos[2]
        self.idtrabajador = datos[3]
        self.fincontrato = datos[4]
        self.inicontrato = datos[5]
        self.idvacaciones = datos[6]
        self.cant_dias = datos[7]
        self.cant_dias_min = datos[8]
        self.dias_trabajados_ultimo_anio= datos[16]
        self.dias_vacaciones = self.dias_vacaciones_anio()
        self.dias_vacaciones_apagar = round(float(self.dias_vacaciones) / 365 * float(self.dias_trabajados_ultimo_anio),2)

    def importe(self):
        sql = ("Select ")
        pass

    def dias_vacaciones_anio(self):
        if self.cant_dias_min > self.cant_dias:
            return self.cant_dias_min
        else:
            return self.cant_dias