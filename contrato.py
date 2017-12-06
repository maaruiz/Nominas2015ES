'''
Created on 26/07/2015

@author: miguelangel
'''
from Funciones.Datos.contrato_dat import SqlContratos, Contratos_codigo

class Contrato():
    """
    Almacena y devuelve los datos de un contrato.
    """
    def __init__(self, idcontrato):
        """
        Necesitamos intoducir el id del contrato
        """
        self.id = idcontrato
        SqlCont = SqlContratos(self.id)
        self.identificador_sepe
        self.codigo = SqlCont.codigo()
        self.descripcion = SqlCont.descripcion()
        self.fecha_inicio = SqlCont.fecha_inicio()
        self.fecha_final = SqlCont.fecha_final()
        self.es_indefinido = SqlCont.contrato_oficial.es_indefinido()
        self.es_temporal = SqlCont.contrato_oficial.es_temporal()
        self.es_jornada_completa = SqlCont.contrato_oficial.jornada_completa()
        self.es_jornada_parcial = SqlCont.contrato_oficial.jornada_parcial()
        self.nombre_trabajador = SqlCont.trabajador.nombre()
        self.apellido1_trabajador = SqlCont.trabajador.apellido1()
        self.apellido2_trabajador = SqlCont.trabajador.apellido2()
        self.nacimiento_trabajador = SqlCont.trabajador.fecha_nacimiento()
        self.nif_trabajador = SqlCont.trabajador.nif()
        self.naf_trabajador = SqlCont.trabajador.naf()
        self.direccion_trabajador = SqlCont.trabajador.direccion()
        self.codpostal_trabajador = SqlCont.trabajador.cod_postal()
        self.grupocotizacion
        self.categoriaprofesional
        self.matricula
        self.nombre_empresa
        self.representante_empresa
        self.cif
        self.regimen_cotizacion
        self.actividad
        self.cod_cotizacion
        self.direccion_centro_trabajo
        self.horas_semanales
        self.horas_diarias
        self.trabaja_lunes
        self.trabaja_martes
        self.trabaja_miercoles
        self.trabaja_jueves
        self.trabaja_viernes
        self.trabaja_sabado
        self.trabaja_domingo
