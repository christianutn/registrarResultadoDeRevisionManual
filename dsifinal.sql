CREATE DATABASE  IF NOT EXISTS `bd_dsi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bd_dsi`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_dsi
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alcance_sismo`
--

DROP TABLE IF EXISTS `alcance_sismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alcance_sismo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) DEFAULT NULL,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alcance_sismo`
--

LOCK TABLES `alcance_sismo` WRITE;
/*!40000 ALTER TABLE `alcance_sismo` DISABLE KEYS */;
/*!40000 ALTER TABLE `alcance_sismo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cambio_estado`
--

DROP TABLE IF EXISTS `cambio_estado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cambio_estado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_hora_fin` datetime DEFAULT NULL,
  `fecha_hora_inicio` datetime DEFAULT NULL,
  `estado_id` int NOT NULL,
  `evento_sismico_id` int NOT NULL,
  `empleado_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_CambioEstado_Estado_idx` (`estado_id`),
  KEY `FK_CambioEstado_EventoSismico_idx` (`evento_sismico_id`),
  KEY `FK_CambioEstado_Empleado_idx` (`empleado_id`),
  CONSTRAINT `FK_CambioEstado_Empleado` FOREIGN KEY (`empleado_id`) REFERENCES `empleado` (`id`),
  CONSTRAINT `FK_CambioEstado_Estado` FOREIGN KEY (`estado_id`) REFERENCES `estado` (`id`),
  CONSTRAINT `FK_CambioEstado_EventoSismico` FOREIGN KEY (`evento_sismico_id`) REFERENCES `evento_sismico` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cambio_estado`
--

LOCK TABLES `cambio_estado` WRITE;
/*!40000 ALTER TABLE `cambio_estado` DISABLE KEYS */;
/*!40000 ALTER TABLE `cambio_estado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clasificacion_sismo`
--

DROP TABLE IF EXISTS `clasificacion_sismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clasificacion_sismo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `km_profundidad_desde` float DEFAULT NULL,
  `km_profundidad_hasta` float DEFAULT NULL,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clasificacion_sismo`
--

LOCK TABLES `clasificacion_sismo` WRITE;
/*!40000 ALTER TABLE `clasificacion_sismo` DISABLE KEYS */;
/*!40000 ALTER TABLE `clasificacion_sismo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_muestra_sismica`
--

DROP TABLE IF EXISTS `detalle_muestra_sismica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_muestra_sismica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valor` float NOT NULL,
  `tipo_de_dato_id` int NOT NULL,
  `muestra_sismica_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_DetalleMuestraSismica_TipoDeDato_idx` (`tipo_de_dato_id`),
  KEY `FK_DetalleMuestraSismica_MuestraSismica_idx` (`muestra_sismica_id`),
  CONSTRAINT `FK_DetalleMuestraSismica_MuestraSismica` FOREIGN KEY (`muestra_sismica_id`) REFERENCES `muestra_sismica` (`id`),
  CONSTRAINT `FK_DetalleMuestraSismica_TipoDeDato` FOREIGN KEY (`tipo_de_dato_id`) REFERENCES `tipo_de_dato` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_muestra_sismica`
--

LOCK TABLES `detalle_muestra_sismica` WRITE;
/*!40000 ALTER TABLE `detalle_muestra_sismica` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_muestra_sismica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `apellido` varchar(45) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `telefono` varchar(10) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estacion_sismologica`
--

DROP TABLE IF EXISTS `estacion_sismologica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estacion_sismologica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_estacion` varchar(45) NOT NULL,
  `documento_certificacion_adq` varchar(45) NOT NULL,
  `fecha_solicitud_certificacion` date NOT NULL,
  `latitud` float NOT NULL,
  `longitud` float NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `nro_certificacion_adquisicion` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacion_sismologica`
--

LOCK TABLES `estacion_sismologica` WRITE;
/*!40000 ALTER TABLE `estacion_sismologica` DISABLE KEYS */;
/*!40000 ALTER TABLE `estacion_sismologica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado`
--

DROP TABLE IF EXISTS `estado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ambito` varchar(45) NOT NULL,
  `nombre_estado` varchar(45) NOT NULL,
  `es_bloqueado` tinyint DEFAULT NULL,
  `es_rechazado` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado`
--

LOCK TABLES `estado` WRITE;
/*!40000 ALTER TABLE `estado` DISABLE KEYS */;
/*!40000 ALTER TABLE `estado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_sismico`
--

DROP TABLE IF EXISTS `evento_sismico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_sismico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_hora_ocurrencia` datetime DEFAULT NULL,
  `latitud_epicentro` float DEFAULT NULL,
  `latitud_hipocentro` float DEFAULT NULL,
  `longitud_epicentro` float DEFAULT NULL,
  `longitud_hipocentro` float DEFAULT NULL,
  `valor_magnitud` float DEFAULT NULL,
  `alcance_sismo_id` int NOT NULL,
  `origen_generacion_id` int NOT NULL,
  `clasificacion_sismo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_EventoSismico_AlcanceSismo_idx` (`alcance_sismo_id`),
  KEY `FK_EventoSismico_OrigenDeGeneracion_idx` (`origen_generacion_id`),
  KEY `FK_EventoSismico_ClasificacionSismo_idx` (`clasificacion_sismo_id`),
  CONSTRAINT `FK_EventoSismico_AlcanceSismo` FOREIGN KEY (`alcance_sismo_id`) REFERENCES `alcance_sismo` (`id`),
  CONSTRAINT `FK_EventoSismico_ClasificacionSismo` FOREIGN KEY (`clasificacion_sismo_id`) REFERENCES `clasificacion_sismo` (`id`),
  CONSTRAINT `FK_EventoSismico_OrigenDeGeneracion` FOREIGN KEY (`origen_generacion_id`) REFERENCES `origen_de_generacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_sismico`
--

LOCK TABLES `evento_sismico` WRITE;
/*!40000 ALTER TABLE `evento_sismico` DISABLE KEYS */;
/*!40000 ALTER TABLE `evento_sismico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muestra_sismica`
--

DROP TABLE IF EXISTS `muestra_sismica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muestra_sismica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_hora_muestra` datetime NOT NULL,
  `serie_temporal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_MuestraSismica_SerieTemporal_idx` (`serie_temporal_id`),
  CONSTRAINT `FK_MuestraSismica_SerieTemporal` FOREIGN KEY (`serie_temporal_id`) REFERENCES `serie_temporal` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestra_sismica`
--

LOCK TABLES `muestra_sismica` WRITE;
/*!40000 ALTER TABLE `muestra_sismica` DISABLE KEYS */;
/*!40000 ALTER TABLE `muestra_sismica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `origen_de_generacion`
--

DROP TABLE IF EXISTS `origen_de_generacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `origen_de_generacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) DEFAULT NULL,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `origen_de_generacion`
--

LOCK TABLES `origen_de_generacion` WRITE;
/*!40000 ALTER TABLE `origen_de_generacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `origen_de_generacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serie_temporal`
--

DROP TABLE IF EXISTS `serie_temporal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serie_temporal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `condicion_alarma` varchar(45) DEFAULT NULL,
  `fecha_hora_registro_muestras` datetime DEFAULT NULL,
  `fecha_hora_registro` datetime DEFAULT NULL,
  `frecuencia_muestreo` float DEFAULT NULL,
  `sismografo_id` int DEFAULT NULL,
  `evento_sismico_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_SerieTemporal_Sismografo_idx` (`sismografo_id`),
  KEY `FK_SerieTemporal_EventoSismico_idx` (`evento_sismico_id`),
  CONSTRAINT `FK_SerieTemporal_EventoSismico` FOREIGN KEY (`evento_sismico_id`) REFERENCES `evento_sismico` (`id`),
  CONSTRAINT `FK_SerieTemporal_Sismografo` FOREIGN KEY (`sismografo_id`) REFERENCES `sismografo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serie_temporal`
--

LOCK TABLES `serie_temporal` WRITE;
/*!40000 ALTER TABLE `serie_temporal` DISABLE KEYS */;
/*!40000 ALTER TABLE `serie_temporal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sesion`
--

DROP TABLE IF EXISTS `sesion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sesion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_hora_inicio` datetime NOT NULL,
  `fecha_hora_fin` datetime DEFAULT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Sesion_Usuario_idx` (`usuario_id`),
  CONSTRAINT `FK_Sesion_Usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sesion`
--

LOCK TABLES `sesion` WRITE;
/*!40000 ALTER TABLE `sesion` DISABLE KEYS */;
/*!40000 ALTER TABLE `sesion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sismografo`
--

DROP TABLE IF EXISTS `sismografo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sismografo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_adquisicion` date DEFAULT NULL,
  `identificador_sismografo` varchar(45) DEFAULT NULL,
  `nro_serie` varchar(45) DEFAULT NULL,
  `estacion_sismologica_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Sismografo_EstacionSismologica_idx` (`estacion_sismologica_id`),
  CONSTRAINT `FK_Sismografo_EstacionSismologica` FOREIGN KEY (`estacion_sismologica_id`) REFERENCES `estacion_sismologica` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sismografo`
--

LOCK TABLES `sismografo` WRITE;
/*!40000 ALTER TABLE `sismografo` DISABLE KEYS */;
/*!40000 ALTER TABLE `sismografo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_de_dato`
--

DROP TABLE IF EXISTS `tipo_de_dato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_de_dato` (
  `id` int NOT NULL AUTO_INCREMENT,
  `denominacion` varchar(45) DEFAULT NULL,
  `nombre_unidad_medida` varchar(45) DEFAULT NULL,
  `valor_umbral` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_de_dato`
--

LOCK TABLES `tipo_de_dato` WRITE;
/*!40000 ALTER TABLE `tipo_de_dato` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo_de_dato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `contraseña` varchar(45) NOT NULL,
  `empleado_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Usuario_Empleado_idx` (`empleado_id`),
  CONSTRAINT `FK_Usuario_Empleado` FOREIGN KEY (`empleado_id`) REFERENCES `empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'bd_dsi'
--

--
-- Dumping routines for database 'bd_dsi'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 11:07:53
