-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Nominas
-- ------------------------------------------------------
-- Server version	5.5.46-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Nominas`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Nominas` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `Nominas`;

--
-- Table structure for table `Trabajadores`
--

DROP TABLE IF EXISTS `Trabajadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Trabajadores` (
  `idTrabajadores` int(11) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido1` varchar(45) DEFAULT NULL,
  `apellido2` varchar(45) DEFAULT NULL,
  `nif` varchar(9) NOT NULL,
  `naf` varchar(12) NOT NULL,
  `dir` varchar(45) DEFAULT NULL,
  `cp` varchar(5) DEFAULT NULL,
  `fechanaci` date DEFAULT NULL,
  `nacionalidad` int(3) DEFAULT '724',
  `cod_identificacion` int(11) DEFAULT '1',
  `idtb_vias` int(11) DEFAULT NULL,
  `dir_num` int(4) DEFAULT NULL,
  `dir_planta` varchar(4) DEFAULT NULL,
  `dir_puerta` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`idTrabajadores`,`nif`,`naf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cal_festivos`
--

DROP TABLE IF EXISTS `cal_festivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cal_festivos` (
  `idcal_festivo` int(11) NOT NULL,
  `idcalendario` int(11) DEFAULT NULL,
  `anio` int(4) DEFAULT NULL,
  `mes` int(2) DEFAULT NULL,
  `dia` int(2) DEFAULT NULL,
  `esfestivo_nnal` bit(1) DEFAULT NULL,
  `esfestivo_reg` bit(1) DEFAULT NULL,
  `esfestivo_loc` bit(1) DEFAULT NULL,
  `esfestivo_convenio` bit(1) DEFAULT NULL,
  PRIMARY KEY (`idcal_festivo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `calendario`
--

DROP TABLE IF EXISTS `calendario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calendario` (
  `idcalendario` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `idmunicipio` int(11) DEFAULT NULL,
  PRIMARY KEY (`idcalendario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_calendario`
--

DROP TABLE IF EXISTS `emp_calendario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_calendario` (
  `idemp_calendario` int(11) NOT NULL,
  `idcalendario` int(11) DEFAULT NULL,
  `idempresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_calendario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_centros`
--

DROP TABLE IF EXISTS `emp_centros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_centros` (
  `idemp_centro` int(11) NOT NULL,
  `num_centro` int(11) DEFAULT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idtb_vias` int(11) DEFAULT NULL,
  `dir` varchar(45) DEFAULT NULL,
  `numero` varchar(5) DEFAULT NULL,
  `piso` varchar(5) DEFAULT NULL,
  `puerta` varchar(5) DEFAULT NULL,
  `cp` varchar(5) DEFAULT NULL,
  `idtb_convenio` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_centro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_contratos`
--

DROP TABLE IF EXISTS `emp_contratos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_contratos` (
  `idemp_contratos` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idemp_ctacot` int(11) DEFAULT NULL,
  `idcontratos_tipo` int(11) DEFAULT NULL,
  `idtrabajadores` int(11) DEFAULT NULL,
  `fecha_ini` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `idgrupos_cotizacion` int(11) DEFAULT NULL,
  `idtb_epigrafe` int(11) DEFAULT NULL,
  `idcategoria_profesional` int(11) DEFAULT NULL,
  `grupo_cotizacion` varchar(45) DEFAULT NULL,
  `tb_epigrafe` varchar(45) DEFAULT NULL,
  `categoria_profesional` varchar(45) DEFAULT NULL,
  `prorrpextra` bit(1) DEFAULT b'0',
  `irpf` double(5,2) DEFAULT '0.00',
  `matricula` int(11) DEFAULT NULL,
  `neto` double DEFAULT '0',
  `idcon_com` int(11) DEFAULT NULL,
  `iddesempl` int(11) DEFAULT NULL,
  `idfogasa` int(11) DEFAULT NULL,
  `idfp` int(11) DEFAULT NULL,
  `conversion` int(11) DEFAULT NULL,
  `prorroga` int(11) DEFAULT NULL,
  `num_prorroga` int(11) DEFAULT NULL,
  `idtb_contrato_baja` int(11) DEFAULT NULL,
  `idtb_despido` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_contratos`),
  KEY `Empresa` (`idempresa`),
  KEY `Trabajadores` (`idtrabajadores`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_contratos_pextra`
--

DROP TABLE IF EXISTS `emp_contratos_pextra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_contratos_pextra` (
  `idemp_contratos_pextra` int(11) NOT NULL,
  `idemp_contrato` int(11) DEFAULT NULL,
  `idemp_pextra` int(11) DEFAULT NULL,
  `importe` double(12,2) DEFAULT NULL,
  `dias` int(11) DEFAULT '30',
  PRIMARY KEY (`idemp_contratos_pextra`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_contratos_vacaciones`
--

DROP TABLE IF EXISTS `emp_contratos_vacaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_contratos_vacaciones` (
  `idemp_contrato_vacaciones` int(11) NOT NULL,
  `idemp_contrato` varchar(45) DEFAULT NULL,
  `ejercicio` int(4) DEFAULT NULL,
  `fecha_inicial` date DEFAULT NULL,
  `fecha_final` date DEFAULT NULL,
  `dias_disfrutados` int(11) DEFAULT NULL,
  `dias_pendientes` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_contrato_vacaciones`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_ctacot`
--

DROP TABLE IF EXISTS `emp_ctacot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_ctacot` (
  `idctacot` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idemp_centro` int(11) DEFAULT NULL,
  `ncc` varchar(12) DEFAULT NULL,
  `idregimen` int(11) DEFAULT NULL,
  `idcontrato` int(11) DEFAULT NULL,
  `idtb_convenio` int(11) DEFAULT NULL,
  `idtb_convenio_datos_actual` int(11) DEFAULT NULL,
  `esformacion` bit(1) DEFAULT b'0',
  `idcalendario` int(11) DEFAULT NULL,
  `ejercicio_actual` int(4) DEFAULT NULL,
  `coef_pextra` double(5,2) DEFAULT NULL,
  PRIMARY KEY (`idctacot`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_devengos`
--

DROP TABLE IF EXISTS `emp_devengos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_devengos` (
  `idemp_devengo` int(11) NOT NULL,
  `idemp_contrato` int(11) DEFAULT NULL,
  `idcat_prof_devengo` int(11) DEFAULT NULL,
  `orden` int(11) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  `importe` double(10,2) DEFAULT NULL,
  `irpf` bit(1) DEFAULT b'1',
  `cont_com` bit(1) DEFAULT b'0',
  `desempleo` bit(1) DEFAULT b'1',
  `fp` bit(1) DEFAULT b'1',
  `fgs` bit(1) DEFAULT b'1',
  `it` bit(1) DEFAULT b'1',
  `ims` bit(1) DEFAULT b'1',
  `ppextra` bit(1) DEFAULT b'0',
  `mensual` bit(1) DEFAULT b'0',
  `diario` bit(1) DEFAULT b'0',
  `horas` bit(1) DEFAULT b'0',
  `idemp_pextra` int(11) DEFAULT NULL,
  `dias_efectivos` bit(1) DEFAULT b'0',
  `dias_naturales` bit(1) DEFAULT b'0',
  `esdevengo` bit(1) DEFAULT b'1',
  `esirpf` bit(1) DEFAULT b'0',
  `esdieta` bit(1) DEFAULT b'0',
  `esespecie` bit(1) DEFAULT b'0',
  `esporcentaje` bit(1) DEFAULT b'0',
  `coef_pextra` float(4,2) DEFAULT '1.00',
  `esmanual` bit(1) DEFAULT NULL,
  `fraccionhoras` bit(1) DEFAULT b'1',
  `idform_concepto` int(11) DEFAULT NULL,
  `escc` bit(1) DEFAULT b'0',
  `esdp` bit(1) DEFAULT b'0',
  `esfp` bit(1) DEFAULT b'0',
  `esfgs` bit(1) DEFAULT b'0',
  `esvacaciones` bit(1) DEFAULT b'0',
  `es_indemnizacion` bit(1) DEFAULT b'0',
  `pagavacaciones` bit(1) DEFAULT b'0',
  `es_complemento_it_cc` bit(1) DEFAULT b'0',
  `es_complemento_it_ef` bit(1) DEFAULT b'0',
  `es_complemento_it_convenio` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idemp_devengo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_it`
--

DROP TABLE IF EXISTS `emp_it`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_it` (
  `idemp_it` int(11) NOT NULL,
  `idemp_contrato` int(11) DEFAULT NULL,
  `idtb_it` int(11) DEFAULT NULL,
  `fecha_baja` date DEFAULT NULL,
  `fecha_alta` date DEFAULT NULL,
  `num_dias` int(11) DEFAULT NULL,
  `es_baja_contcomun` bit(1) DEFAULT NULL,
  `es_baja_enfprof` bit(1) DEFAULT NULL,
  `basecot_mesant` double(10,2) DEFAULT NULL,
  `diascot_mesant` int(11) DEFAULT NULL,
  `basecot_diaria_it` double(10,2) DEFAULT NULL,
  PRIMARY KEY (`idemp_it`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_pextra`
--

DROP TABLE IF EXISTS `emp_pextra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_pextra` (
  `idemp_pextra` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `mes` int(2) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  `idtb_conv_pextra` int(11) DEFAULT NULL,
  `idconvenio` int(11) DEFAULT NULL,
  `coeficiente` float(4,2) DEFAULT '1.00',
  `idctacot` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_pextra`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_tpo_parcial`
--

DROP TABLE IF EXISTS `emp_tpo_parcial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_tpo_parcial` (
  `idemp_tpo_parcial` int(11) NOT NULL,
  `idemp_contrato` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `horas` float DEFAULT NULL,
  `lunes` float(5,2) DEFAULT '0.00',
  `martes` float(5,2) DEFAULT '0.00',
  `miercoles` float(5,2) DEFAULT '0.00',
  `jueves` float(5,2) DEFAULT '0.00',
  `viernes` float(5,2) DEFAULT '0.00',
  `sabado` float(5,2) DEFAULT '0.00',
  `domingo` float(5,2) DEFAULT '0.00',
  PRIMARY KEY (`idemp_tpo_parcial`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emp_vacaciones`
--

DROP TABLE IF EXISTS `emp_vacaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp_vacaciones` (
  `idemp_vacaciones` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idemp_ctacot` int(11) DEFAULT NULL,
  `idtb_vacaciones` int(11) DEFAULT NULL,
  PRIMARY KEY (`idemp_vacaciones`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresa` (
  `idempresa` int(11) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido1` varchar(45) DEFAULT NULL,
  `apellido2` varchar(45) DEFAULT NULL,
  `cod_identificacion` int(11) DEFAULT NULL,
  `cif` varchar(45) DEFAULT NULL,
  `idtb_vias` int(11) DEFAULT NULL,
  `dir` varchar(45) DEFAULT NULL,
  `numero` varchar(5) DEFAULT NULL,
  `piso` varchar(5) DEFAULT NULL,
  `puerta` varchar(5) DEFAULT NULL,
  `cp` varchar(45) DEFAULT NULL,
  `tlf` varchar(45) DEFAULT NULL,
  `fax` varchar(45) DEFAULT NULL,
  `idconvenio` int(11) DEFAULT NULL,
  `idform_nomina` int(11) DEFAULT NULL,
  PRIMARY KEY (`idempresa`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `form_conceptos`
--

DROP TABLE IF EXISTS `form_conceptos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form_conceptos` (
  `idform_conceptos` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `essalario` bit(1) DEFAULT b'0',
  `esnosalario` bit(1) DEFAULT b'0',
  `esdeduccion` bit(1) DEFAULT b'0',
  `cotizasegsocial` bit(1) DEFAULT b'0',
  `esirpf` bit(1) DEFAULT b'0',
  `esanticipo` bit(1) DEFAULT b'0',
  `esespecie` bit(1) DEFAULT b'0',
  `espagoitemp` bit(1) DEFAULT b'0',
  `espagoitdelegado` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idform_conceptos`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `form_nomina`
--

DROP TABLE IF EXISTS `form_nomina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form_nomina` (
  `idform_nomina` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idform_nomina`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `form_nomina_celda`
--

DROP TABLE IF EXISTS `form_nomina_celda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form_nomina_celda` (
  `idform_celda` int(11) NOT NULL,
  `idform_nomina` int(11) DEFAULT NULL,
  `etiqueta` varchar(200) DEFAULT NULL,
  `dato` varchar(45) DEFAULT NULL,
  `x1dato` int(3) DEFAULT '0',
  `ancho_dato` int(3) DEFAULT '0',
  `y1dato` int(3) DEFAULT '0',
  `alto_dato` int(3) DEFAULT '0',
  `fill` int(1) DEFAULT '0',
  `font_size` int(2) DEFAULT '10',
  `x1etiqueta` int(3) DEFAULT '0',
  `ancho_etiqueta` int(3) DEFAULT '0',
  `y1etiqueta` int(3) DEFAULT '0',
  `alto_etiqueta` int(3) DEFAULT '0',
  `centro` int(1) DEFAULT '1',
  `texto_dato` varchar(45) DEFAULT NULL,
  `valor_dato` double(8,2) DEFAULT NULL,
  `ancholinea` double(5,2) DEFAULT '0.50',
  `puntoslineaimprime` int(2) DEFAULT '1',
  `puntoslineanoimprime` int(2) DEFAULT '0',
  `datoalineacion` varchar(1) DEFAULT 'c',
  `fill_etiqueta` int(1) DEFAULT '0',
  `tabla` varchar(45) DEFAULT NULL,
  `campo` varchar(45) DEFAULT NULL,
  `print_etiqueta` int(1) DEFAULT '0',
  PRIMARY KEY (`idform_celda`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nomina_devengos`
--

DROP TABLE IF EXISTS `nomina_devengos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nomina_devengos` (
  `idnomina_devengo` int(11) NOT NULL,
  `idnomina` int(11) DEFAULT NULL,
  `idemp_devengo` int(11) DEFAULT '0',
  `orden` int(11) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  `importe` double(10,2) DEFAULT NULL,
  `irpf` bit(1) DEFAULT b'1',
  `cont_com` bit(1) DEFAULT b'1',
  `desempleo` bit(1) DEFAULT b'1',
  `fp` bit(1) DEFAULT b'1',
  `fgs` bit(1) DEFAULT b'1',
  `it` bit(1) DEFAULT b'1',
  `ims` bit(1) DEFAULT b'1',
  `ppextra` bit(1) DEFAULT NULL,
  `mensual` bit(1) DEFAULT b'0',
  `diario` bit(1) DEFAULT b'0',
  `horas` bit(1) DEFAULT b'0',
  `idemp_pextra` int(11) DEFAULT NULL,
  `dias_efectivos` bit(1) DEFAULT b'0',
  `dias_naturales` bit(1) DEFAULT b'0',
  `esdevengo` bit(1) DEFAULT b'1',
  `esirpf` bit(1) DEFAULT b'0',
  `esdieta` bit(1) DEFAULT b'0',
  `cotiza_si_no` varchar(1) DEFAULT NULL,
  `imp_cuantia` double(10,2) DEFAULT NULL,
  `imp_precio` double(10,2) DEFAULT NULL,
  `imp_devengo` double(10,2) DEFAULT '0.00',
  `imp_deduccion` double(10,2) DEFAULT '0.00',
  `esespecie` bit(1) DEFAULT b'0',
  `esporcentaje` bit(1) DEFAULT b'0',
  `coef_pextra` float(4,2) DEFAULT '0.00',
  `esmanual` bit(1) DEFAULT NULL,
  `fraccionhoras` bit(1) DEFAULT b'1',
  `idform_concepto` int(11) DEFAULT NULL,
  `esvacaciones` bit(1) DEFAULT NULL,
  `es_indemnizacion` bit(1) DEFAULT b'0',
  `pagavacaciones` bit(1) DEFAULT NULL,
  `es_complemento_it_cc` bit(1) DEFAULT b'0',
  `es_complemento_it_ef` bit(1) DEFAULT b'0',
  `es_complemento_it_convenio` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idnomina_devengo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nominas`
--

DROP TABLE IF EXISTS `nominas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nominas` (
  `idnomina` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idemp_contratos` int(11) DEFAULT NULL,
  `idgrupos_cotizacion` int(11) DEFAULT NULL,
  `idtb_epigrafe` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `imp_bruto` double(10,2) DEFAULT NULL,
  `imp_neto` double(10,2) DEFAULT NULL,
  `base_irpf` double(10,2) DEFAULT NULL,
  `base_cc` double(10,2) DEFAULT NULL,
  `base_dfgsfp` double(10,2) DEFAULT NULL,
  `base_ppextra` double(10,2) DEFAULT NULL,
  `imp_pextra` double(10,2) DEFAULT NULL,
  `tot_deducir` double(10,2) DEFAULT NULL,
  `naf` varchar(12) DEFAULT NULL,
  `tarifa` int(11) DEFAULT NULL,
  `epigrafe` varchar(45) DEFAULT NULL,
  `seccion` varchar(45) DEFAULT NULL,
  `numero` varchar(45) DEFAULT NULL,
  `periodo` varchar(45) DEFAULT NULL,
  `tot_dias` int(2) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `categoria` varchar(45) DEFAULT NULL,
  `matricula` int(11) DEFAULT NULL,
  `antig` date DEFAULT NULL,
  `dni` varchar(45) DEFAULT NULL,
  `empresa` varchar(45) DEFAULT NULL,
  `dir` varchar(45) DEFAULT NULL,
  `idcta_cot` int(11) DEFAULT NULL,
  `cta_cot` varchar(45) DEFAULT NULL,
  `liquido` double(10,2) DEFAULT NULL,
  `imp_totdev` double(10,2) DEFAULT NULL,
  `cif` varchar(45) DEFAULT NULL,
  `remuneracion` double(10,2) DEFAULT NULL,
  `pextra_cobrada` double(10,2) DEFAULT NULL,
  `tipo_cc_empresa` double(10,2) DEFAULT NULL,
  `tipo_dp_empresa` double(10,2) DEFAULT NULL,
  `tipo_fp_empresa` double(10,2) DEFAULT NULL,
  `tipo_fgs_empresa` double(10,2) DEFAULT NULL,
  `imp_cc_empresa` double(10,2) DEFAULT NULL,
  `imp_dp_empresa` double(10,2) DEFAULT NULL,
  `imp_fp_empresa` double(10,2) DEFAULT NULL,
  `imp_fgs_empresa` double(10,2) DEFAULT NULL,
  `imp_remumes` double(10,2) DEFAULT NULL,
  `imp_aportatrab` double(10,2) DEFAULT NULL,
  `es_finiquito` bit(1) DEFAULT b'0',
  `es_nominapextra` bit(1) DEFAULT b'0',
  `causaextincion` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`idnomina`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_municipios`
--

DROP TABLE IF EXISTS `t_municipios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_municipios` (
  `idMunicipio` int(11) NOT NULL AUTO_INCREMENT,
  `CodProv` char(2) DEFAULT NULL,
  `CodPostal` varchar(5) DEFAULT NULL,
  `Municipio` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`idMunicipio`)
) ENGINE=InnoDB AUTO_INCREMENT=56914 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_provincias`
--

DROP TABLE IF EXISTS `t_provincias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_provincias` (
  `CodProv` char(2) NOT NULL DEFAULT '',
  `Provincia` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`CodProv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_cat_prof_devengos`
--

DROP TABLE IF EXISTS `tb_cat_prof_devengos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_cat_prof_devengos` (
  `idtb_cat_prof_devengos` int(11) NOT NULL,
  `idcategoria_profesional` int(11) DEFAULT NULL,
  `orden` int(11) DEFAULT NULL,
  `devengo` varchar(45) DEFAULT NULL,
  `importe` double(10,2) DEFAULT NULL,
  `irpf` bit(1) DEFAULT b'1',
  `cont_comun` bit(1) DEFAULT b'1',
  `desemp_fp` bit(1) DEFAULT b'1',
  `mensual` bit(1) DEFAULT b'0',
  `diario` bit(1) DEFAULT b'0',
  `hora` bit(1) DEFAULT b'0',
  `pagaextra` bit(1) DEFAULT b'0',
  `antiguedad` bit(1) DEFAULT b'0',
  `calc_antig` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idtb_cat_prof_devengos`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_categoria_profesional`
--

DROP TABLE IF EXISTS `tb_categoria_profesional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_categoria_profesional` (
  `idcategoria_profesional` int(11) NOT NULL,
  `idconvenio` int(11) DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idcategoria_profesional`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_contrato_baja`
--

DROP TABLE IF EXISTS `tb_contrato_baja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_contrato_baja` (
  `idtb_contratobaja` int(11) NOT NULL,
  `codigo` int(3) DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `esexcedencia` bit(1) DEFAULT b'0',
  `essuspension` bit(1) DEFAULT b'0',
  `escausaobjetiva` bit(1) DEFAULT b'0',
  `esdespido` bit(1) DEFAULT b'0',
  `esfintemporal` bit(1) DEFAULT b'0',
  `esextincion` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idtb_contratobaja`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_contratos_tipo`
--

DROP TABLE IF EXISTS `tb_contratos_tipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_contratos_tipo` (
  `idcontratos_tipo` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `temporal` bit(1) DEFAULT NULL,
  `indefinido` bit(1) DEFAULT NULL,
  `jornadacompleta` bit(1) DEFAULT NULL,
  `jornadaparcial` bit(1) DEFAULT NULL,
  PRIMARY KEY (`idcontratos_tipo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_convenio_datos`
--

DROP TABLE IF EXISTS `tb_convenio_datos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_convenio_datos` (
  `idtb_convenio_datos` int(11) NOT NULL,
  `idtb_convenio` int(11) DEFAULT NULL,
  `idtb_vacaciones` int(11) DEFAULT NULL,
  `ejercicio` int(4) DEFAULT NULL,
  `horas_anio` int(11) DEFAULT NULL,
  `horas_semana` int(11) DEFAULT NULL,
  `horas_dia` int(11) DEFAULT NULL,
  `fecha_ini` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `essab_laboral` bit(1) DEFAULT NULL,
  `diasefectivos_anio` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtb_convenio_datos`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_convenios`
--

DROP TABLE IF EXISTS `tb_convenios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_convenios` (
  `idtb_convenio` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `codigo` varchar(45) DEFAULT NULL,
  `fecha_alta` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `horas_anio` int(11) DEFAULT NULL,
  `horas_semana` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtb_convenio`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_convenios_pextra`
--

DROP TABLE IF EXISTS `tb_convenios_pextra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_convenios_pextra` (
  `idtb_convenio_pextra` int(11) NOT NULL,
  `idtb_convenio` int(11) DEFAULT NULL,
  `mes` int(2) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  `coeficiente` float(3,2) DEFAULT '1.00',
  `importe` double(10,2) DEFAULT NULL,
  `dias` int(11) DEFAULT NULL,
  `idtb_convenio_datos` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtb_convenio_pextra`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_despidos`
--

DROP TABLE IF EXISTS `tb_despidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_despidos` (
  `idtb_despido` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `esobjetivo` bit(1) DEFAULT b'0',
  `esdisciplinario` bit(1) DEFAULT b'0',
  `esnulo` bit(1) DEFAULT b'0',
  `esprocedente` bit(1) DEFAULT b'0',
  `esimprocedente` bit(1) DEFAULT b'0',
  `dias_anio` int(11) DEFAULT NULL,
  `max_meses` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtb_despido`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_devengos`
--

DROP TABLE IF EXISTS `tb_devengos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_devengos` (
  `idtb_devengo` int(11) NOT NULL,
  `orden` int(11) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  `irpf` bit(1) DEFAULT b'1',
  `cont_com` bit(1) DEFAULT b'0',
  `desempleo` bit(1) DEFAULT b'1',
  `fp` bit(1) DEFAULT b'1',
  `fgs` bit(1) DEFAULT b'1',
  `it` bit(1) DEFAULT b'1',
  `ims` bit(1) DEFAULT b'1',
  `ppextra` bit(1) DEFAULT NULL,
  `mensual` bit(1) DEFAULT b'0',
  `diario` bit(1) DEFAULT b'0',
  `horas` bit(1) DEFAULT b'0',
  `idemp_pextra` int(11) DEFAULT NULL,
  `dias_efectivos` bit(1) DEFAULT b'0',
  `dias_naturales` bit(1) DEFAULT b'0',
  `esdevengo` bit(1) DEFAULT b'1',
  `esirpf` bit(1) DEFAULT b'0',
  `esdieta` bit(1) DEFAULT b'0',
  `esespecie` bit(1) DEFAULT b'0',
  `esporcentaje` bit(1) DEFAULT b'0',
  `coef_pextra` float(4,2) DEFAULT '1.00',
  `esmanual` bit(1) DEFAULT NULL,
  `fraccionhoras` bit(1) DEFAULT b'1',
  `idform_concepto` int(11) DEFAULT NULL,
  `escc` bit(1) DEFAULT b'0',
  `esdp` bit(1) DEFAULT b'0',
  `esfp` bit(1) DEFAULT b'0',
  `esfgs` bit(1) DEFAULT b'0',
  `esvacaciones` bit(1) DEFAULT b'0',
  `es_indemnizacion` bit(1) DEFAULT b'0',
  `pagavacaciones` bit(1) DEFAULT b'0',
  `es_complemento_it_cc` bit(1) DEFAULT b'0',
  `es_complemento_it_ef` bit(1) DEFAULT b'0',
  `es_complemento_it_convenio` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idtb_devengo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_epigrafe`
--

DROP TABLE IF EXISTS `tb_epigrafe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_epigrafe` (
  `idtb_epigrafe` int(11) NOT NULL,
  `codigo` int(11) DEFAULT NULL,
  `ejercicio` int(4) DEFAULT NULL,
  `cuadro` int(1) DEFAULT NULL,
  `actividad` varchar(45) DEFAULT NULL,
  `it` double DEFAULT NULL,
  `ims` double DEFAULT NULL,
  PRIMARY KEY (`idtb_epigrafe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_grupos_cotizacion`
--

DROP TABLE IF EXISTS `tb_grupos_cotizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_grupos_cotizacion` (
  `idgrupos_cotizacion` int(11) NOT NULL,
  `grupo_cotizacion` int(2) DEFAULT NULL,
  `idregimen` int(11) DEFAULT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idgrupos_cotizacion`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_gruposcot_bases`
--

DROP TABLE IF EXISTS `tb_gruposcot_bases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_gruposcot_bases` (
  `idtb_grupocot_base` int(11) NOT NULL,
  `idtb_grupo_cotizacion` int(11) DEFAULT NULL,
  `ejercicio` int(4) DEFAULT NULL,
  `base_min_mes` double(10,2) DEFAULT NULL,
  `base_max_mes` double(10,2) DEFAULT NULL,
  `base_min_dia` double(10,2) DEFAULT NULL,
  `base_max_dia` double(10,2) DEFAULT NULL,
  `base_min_hora` double(10,2) DEFAULT NULL,
  `base_max_hora` double(10,2) DEFAULT NULL,
  PRIMARY KEY (`idtb_grupocot_base`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_identificacion`
--

DROP TABLE IF EXISTS `tb_identificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_identificacion` (
  `id_identificacion` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `documento` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_identificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_it`
--

DROP TABLE IF EXISTS `tb_it`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_it` (
  `idtb_it` int(11) NOT NULL,
  `idtb_regimen` int(11) DEFAULT NULL,
  `desdedia` int(2) DEFAULT NULL,
  `hastadia` int(5) DEFAULT NULL,
  `porcentaje` double(5,2) DEFAULT NULL,
  `es_contcomun` bit(1) DEFAULT NULL,
  `es_enfprof` bit(1) DEFAULT NULL,
  `es_pagoempresa` bit(1) DEFAULT NULL,
  `es_pagodelegado` bit(1) DEFAULT NULL,
  `concepto` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtb_it`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_regimen`
--

DROP TABLE IF EXISTS `tb_regimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_regimen` (
  `idregimen` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `codigo` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`idregimen`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_tiposcot`
--

DROP TABLE IF EXISTS `tb_tiposcot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_tiposcot` (
  `idtb_tiposcot` int(11) NOT NULL,
  `idregimen_segsocial` int(11) DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `es_contcomun` bit(1) DEFAULT b'0',
  `es_desempleo` bit(1) DEFAULT b'0',
  `es_fogasa` bit(1) DEFAULT b'0',
  `es_formprof` bit(1) DEFAULT b'0',
  `es_dura_determinada` bit(1) DEFAULT b'0',
  `es_dura_indefinida` bit(1) DEFAULT b'0',
  `es_tpo_completo` bit(1) DEFAULT b'0',
  `es_tpo_parcial` bit(1) DEFAULT b'0',
  `es_hora_extra_fmayor` bit(1) DEFAULT b'0',
  `es_hora_extra_resto` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idtb_tiposcot`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_tiposcot_ejercicio`
--

DROP TABLE IF EXISTS `tb_tiposcot_ejercicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_tiposcot_ejercicio` (
  `idtb_tiposcot_ejercicio` int(11) NOT NULL,
  `idtb_tipocot` int(11) DEFAULT NULL,
  `ejercicio` int(4) DEFAULT NULL,
  `empresa` double(5,2) DEFAULT '0.00',
  `trabajador` double(5,2) DEFAULT '0.00',
  `tpo_parcial` bit(1) DEFAULT b'0',
  `tpo_completo` bit(1) DEFAULT b'0',
  `dura_indefinida` bit(1) DEFAULT b'0',
  `dura_determinada` bit(1) DEFAULT b'0',
  PRIMARY KEY (`idtb_tiposcot_ejercicio`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_vacaciones`
--

DROP TABLE IF EXISTS `tb_vacaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_vacaciones` (
  `idtb_vacaciones` int(11) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `cantidad` int(3) DEFAULT NULL,
  `esdias_naturales` bit(1) DEFAULT NULL,
  `esdias_laborales` bit(1) DEFAULT NULL,
  `consab` bit(1) DEFAULT NULL,
  `condom` bit(1) DEFAULT NULL,
  `confestivos` bit(1) DEFAULT NULL,
  `cantidad_min` int(3) DEFAULT NULL,
  `esmindias_naturales` bit(1) DEFAULT NULL,
  `esmindias_laborales` bit(1) DEFAULT NULL,
  PRIMARY KEY (`idtb_vacaciones`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_vias`
--

DROP TABLE IF EXISTS `tb_vias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_vias` (
  `idtb_vias` int(11) NOT NULL,
  `via` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtb_vias`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tc2`
--

DROP TABLE IF EXISTS `tc2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc2` (
  `idtc2` int(11) NOT NULL,
  `idempresa` int(11) DEFAULT NULL,
  `idcta_cot` int(11) DEFAULT NULL,
  `mes` int(2) DEFAULT NULL,
  `anio` int(4) DEFAULT NULL,
  `num_trabajadores` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tc2_lin`
--

DROP TABLE IF EXISTS `tc2_lin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc2_lin` (
  `idtc2_lin` int(11) NOT NULL,
  `idtc2` int(11) NOT NULL,
  `idnomina` int(11) NOT NULL,
  `base_cc` double DEFAULT NULL,
  `base_at` double DEFAULT NULL,
  PRIMARY KEY (`idtc2_lin`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-24 18:03:52
