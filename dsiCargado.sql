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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alcance_sismo`
--

LOCK TABLES `alcance_sismo` WRITE;
/*!40000 ALTER TABLE `alcance_sismo` DISABLE KEYS */;
INSERT INTO `alcance_sismo` VALUES (1,'Distancia epicentral hasta 100 km','Sismo local'),(2,'Distancia epicentral entre 101 y 1000 km','Sismo regional'),(3,'Distancia epicentral mayor a 1000 km','Tele sismo');
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
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cambio_estado`
--

LOCK TABLES `cambio_estado` WRITE;
/*!40000 ALTER TABLE `cambio_estado` DISABLE KEYS */;
INSERT INTO `cambio_estado` VALUES (80,'2025-11-09 08:15:00','2025-11-09 07:30:00',1,1,1),(81,'2025-11-09 09:00:00','2025-11-09 08:20:00',2,1,2),(82,'2025-11-09 10:10:00','2025-11-09 09:05:00',3,1,3),(83,NULL,'2025-11-09 10:15:00',1,1,4),(84,'2025-11-08 14:45:00','2025-11-08 14:00:00',1,2,2),(85,'2025-11-08 16:00:00','2025-11-08 14:50:00',2,2,3),(86,NULL,'2025-11-08 16:10:00',3,2,1),(87,'2025-11-07 10:00:00','2025-11-07 09:00:00',1,3,3),(88,'2025-11-07 11:20:00','2025-11-07 10:05:00',2,3,4),(89,NULL,'2025-11-07 11:30:00',3,3,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clasificacion_sismo`
--

LOCK TABLES `clasificacion_sismo` WRITE;
/*!40000 ALTER TABLE `clasificacion_sismo` DISABLE KEYS */;
INSERT INTO `clasificacion_sismo` VALUES (1,0,70,'Sismo superficial'),(2,70,300,'Sismo intermedio'),(3,300,NULL,'Sismo profundo');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_muestra_sismica`
--

LOCK TABLES `detalle_muestra_sismica` WRITE;
/*!40000 ALTER TABLE `detalle_muestra_sismica` DISABLE KEYS */;
INSERT INTO `detalle_muestra_sismica` VALUES (1,0.5,1,1),(2,1.2,2,1),(3,3.4,3,1),(4,0.8,1,2),(5,1,2,2),(6,2.5,3,2),(7,0.3,1,3),(8,1.7,2,3),(9,3,3,3),(10,0.9,1,4),(11,1.1,2,4),(12,2.8,3,4);
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
INSERT INTO `empleado` VALUES (1,'Perez','Leonel','3516365487','perez@gmail.com'),(2,'Pérez','Juan','3511234567','juan.perez@ejemplo.com'),(3,'González','María','3519876543','maria.gonzalez@ejemplo.com'),(4,'López','Carlos','3514567890','carlos.lopez@ejemplo.com'),(5,'Rodríguez','Ana','3517412589','ana.rodriguez@ejemplo.com'),(6,'Martínez','Lucía','3513692581','lucia.martinez@ejemplo.com'),(7,'Fernández','Diego','3517539512','diego.fernandez@ejemplo.com'),(8,'Torres','Sofía','3518529637','sofia.torres@ejemplo.com'),(9,'Ramírez','José','3519517534','jose.ramirez@ejemplo.com'),(10,'Suárez','Carla','3512589637','carla.suarez@ejemplo.com'),(11,'Herrera','Matías','3511472583','matias.herrera@ejemplo.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacion_sismologica`
--

LOCK TABLES `estacion_sismologica` WRITE;
/*!40000 ALTER TABLE `estacion_sismologica` DISABLE KEYS */;
INSERT INTO `estacion_sismologica` VALUES (1,'CBA01','DOC-2024-001','2024-01-15',-31.4201,-64.1888,'Estación Córdoba Centro','CERT-001'),(2,'SJ02','DOC-2024-002','2024-02-10',-31.5375,-68.5364,'Estación San Juan','CERT-002'),(3,'MZA03','DOC-2024-003','2024-03-05',-32.8895,-68.8458,'Estación Mendoza','CERT-003'),(4,'SLT04','DOC-2024-004','2024-04-12',-24.7821,-65.4232,'Estación Salta','CERT-004'),(5,'TUC05','DOC-2024-005','2024-05-07',-26.8241,-65.2226,'Estación Tucumán','CERT-005'),(6,'NQN06','DOC-2024-006','2024-06-19',-38.9516,-68.0591,'Estación Neuquén','CERT-006'),(7,'BRC07','DOC-2024-007','2024-07-09',-41.1335,-71.3103,'Estación Bariloche','CERT-007'),(8,'JUJ08','DOC-2024-008','2024-08-23',-24.1858,-65.2995,'Estación Jujuy','CERT-008'),(9,'USH09','DOC-2024-009','2024-09-15',-54.8019,-68.303,'Estación Ushuaia','CERT-009'),(10,'SFE10','DOC-2024-010','2024-10-28',-31.6333,-60.7,'Estación Santa Fe','CERT-010');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado`
--

LOCK TABLES `estado` WRITE;
/*!40000 ALTER TABLE `estado` DISABLE KEYS */;
INSERT INTO `estado` VALUES (1,'evento_sismico','pendiente_revision',0,0),(2,'evento_sismico','auto_detectado',0,0),(3,'evento_sismico','bloqueado',1,0),(4,'evento_sismico','rechazado',0,1),(5,'evento_sismico','confirmado',0,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_sismico`
--

LOCK TABLES `evento_sismico` WRITE;
/*!40000 ALTER TABLE `evento_sismico` DISABLE KEYS */;
INSERT INTO `evento_sismico` VALUES (1,'2025-03-12 14:35:00',-31.4201,-31.45,-64.1888,-64.2,4.5,1,1,1),(2,'2025-04-08 03:12:00',-32.45,-32.47,-63.95,-63.98,5.8,2,1,2),(3,'2025-05-15 09:27:00',-30.2,-30.23,-66.3,-66.31,6.2,3,1,3),(4,'2025-06-20 21:45:00',-31.1,-31.13,-64.5,-64.52,3.9,1,2,1),(5,'2025-07-02 18:10:00',-33,-33.02,-65.2,-65.25,7.1,3,1,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestra_sismica`
--

LOCK TABLES `muestra_sismica` WRITE;
/*!40000 ALTER TABLE `muestra_sismica` DISABLE KEYS */;
INSERT INTO `muestra_sismica` VALUES (1,'2025-11-09 07:30:00',1),(2,'2025-11-09 08:15:00',1),(3,'2025-11-09 09:00:00',2),(4,'2025-11-09 10:00:00',2),(5,'2025-11-09 11:30:00',3),(6,'2025-11-09 12:15:00',3),(7,'2025-11-09 13:45:00',1),(8,'2025-11-09 14:30:00',2),(9,'2025-11-09 15:00:00',3),(10,'2025-11-09 16:15:00',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `origen_de_generacion`
--

LOCK TABLES `origen_de_generacion` WRITE;
/*!40000 ALTER TABLE `origen_de_generacion` DISABLE KEYS */;
INSERT INTO `origen_de_generacion` VALUES (1,'Generado por actividad tectónica entre placas','Tectónico'),(2,'Resultado de actividad volcánica cercana','Volcánico'),(3,'Producto de un colapso de cavidades subterráneas','Colapso'),(4,'Originado por explosiones o actividades humanas','Artificial'),(5,'Relacionado con el impacto de meteoritos','Meteorítico'),(6,'Asociado a deslizamientos o avalanchas de gran magnitud','Deslizamiento'),(7,'Movimiento inducido por extracción de recursos naturales','Inducido por extracción'),(8,'Generado por fracturamiento hidráulico','Fracking'),(9,'De origen no identificado tras el análisis inicial','Desconocido'),(10,'Producido por el ajuste isostático de la corteza','Isostático');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serie_temporal`
--

LOCK TABLES `serie_temporal` WRITE;
/*!40000 ALTER TABLE `serie_temporal` DISABLE KEYS */;
INSERT INTO `serie_temporal` VALUES (1,'Normal','2025-11-09 07:35:00','2025-11-09 07:30:00',50,1,1),(2,'Alerta','2025-11-09 07:36:00','2025-11-09 07:31:00',50,1,1),(3,'Normal','2025-11-09 07:40:00','2025-11-09 07:35:00',60,2,1),(4,'Normal','2025-11-08 14:05:00','2025-11-08 14:00:00',50,3,2),(5,'Alerta','2025-11-08 14:10:00','2025-11-08 14:05:00',50,3,2),(6,'Normal','2025-11-07 09:05:00','2025-11-07 09:00:00',55,4,3),(7,'Alerta','2025-11-07 09:10:00','2025-11-07 09:05:00',55,4,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sesion`
--

LOCK TABLES `sesion` WRITE;
/*!40000 ALTER TABLE `sesion` DISABLE KEYS */;
INSERT INTO `sesion` VALUES (1,'2025-11-10 08:00:00','2025-11-10 12:00:00',1),(2,'2025-11-10 09:30:00','2025-11-10 11:45:00',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sismografo`
--

LOCK TABLES `sismografo` WRITE;
/*!40000 ALTER TABLE `sismografo` DISABLE KEYS */;
INSERT INTO `sismografo` VALUES (1,'2023-01-15','SISMO-001','NS-1001',1),(2,'2023-02-20','SISMO-002','NS-1002',1),(3,'2023-03-05','SISMO-003','NS-1003',2),(4,'2023-03-18','SISMO-004','NS-1004',2),(5,'2023-04-10','SISMO-005','NS-1005',3),(6,'2023-04-25','SISMO-006','NS-1006',3);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_de_dato`
--

LOCK TABLES `tipo_de_dato` WRITE;
/*!40000 ALTER TABLE `tipo_de_dato` DISABLE KEYS */;
INSERT INTO `tipo_de_dato` VALUES (1,'Magnitud Richter','Grados Richter',4),(2,'Aceleración máxima','m/s²',2.5),(3,'Velocidad del suelo','cm/s',20),(4,'Desplazamiento del terreno','mm',50),(5,'Profundidad del hipocentro','km',70),(6,'Duración del evento','segundos',60),(7,'Energía liberada','Joules',1000000000000),(8,'Distancia al epicentro','km',300),(9,'Intensidad percibida','Escala Mercalli',6),(10,'Frecuencia dominante','Hz',10);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'juanperez','pass123',1),(2,'mariasanchez','clave456',2),(3,'carlorossi','1234abcd',3),(4,'anagomez','qwerty',4),(5,'pedrolopez','pwd789',1),(6,'lauracastro','securepass',2),(7,'miguelhernandez','miclave',3),(8,'sofiadiaz','pass987',4);
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

-- Dump completed on 2025-11-11  8:15:56
