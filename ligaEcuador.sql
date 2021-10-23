-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 22-10-2021 a las 17:33:12
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ligaEcuador`
--
CREATE DATABASE IF NOT EXISTS `ligaEcuador` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ligaEcuador`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `idEq` int(11) NOT NULL COMMENT 'Id del Equipo y PK',
  `nombre` varchar(120) NOT NULL COMMENT 'Nombre del equipo',
  `enlace` varchar(255) NOT NULL COMMENT 'Enlace del equipo para mas innformacion'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Equipos de la liga Ecuatoriana (Serie A)';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metaDataEstadisticas`
--

CREATE TABLE `metaDataEstadisticas` (
  `id` int(11) NOT NULL COMMENT 'PK del HTML extraido',
  `sitio` varchar(255) NOT NULL COMMENT 'Fuente de donde se extrajo la metadata',
  `raw_html` longtext NOT NULL COMMENT 'HTML de los metadatos',
  `opcion` varchar(50) NOT NULL COMMENT 'Local, Visitante, Total',
  `process` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se extrajo la data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metaDataPartidos`
--

CREATE TABLE `metaDataPartidos` (
  `id` int(11) NOT NULL COMMENT 'PK del HTML extraido',
  `sitio` varchar(255) NOT NULL COMMENT 'Fuente de donde se extrajo la metadata',
  `raw_html` longtext NOT NULL COMMENT 'HTML de los metadatos',
  `process` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se extrajo la data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Partidos`
--

CREATE TABLE `Partidos` (
  `idP` int(11) NOT NULL COMMENT 'ID del partido',
  `eqA` int(11) NOT NULL COMMENT 'id del Equipo A',
  `eqB` int(11) NOT NULL COMMENT 'id del Equipo B',
  `golA` int(11) NOT NULL COMMENT 'goles del Equipo A',
  `golB` int(11) NOT NULL COMMENT 'goles del Equipo B',
  `fecha` year(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PosicionesLocal`
--

CREATE TABLE `PosicionesLocal` (
  `idP` int(11) NOT NULL COMMENT 'ID del detalle o posiciones en la tabla',
  `fkEq` int(11) NOT NULL COMMENT 'FK del Equipo',
  `year` int(11) NOT NULL COMMENT 'Año de Liga',
  `Pts` int(11) NOT NULL COMMENT 'Puntos de local',
  `PJ` int(11) NOT NULL COMMENT 'Partidos jugados (local)',
  `PG` int(11) NOT NULL COMMENT 'Partidos ganados (local)',
  `PE` int(11) NOT NULL COMMENT 'Partidos empatados (local)',
  `PP` int(11) NOT NULL COMMENT 'Partidos perdidos (local)',
  `GF` int(11) NOT NULL COMMENT 'Goles a favor (local)',
  `GC` int(11) NOT NULL COMMENT 'Goles en contra (local)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabla de Posicion de local';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PosicionesTotal`
--

CREATE TABLE `PosicionesTotal` (
  `idP` int(11) NOT NULL COMMENT 'ID del detalle o posiciones en la tabla',
  `fkEq` int(11) NOT NULL COMMENT 'FK del Equipo',
  `year` int(11) NOT NULL COMMENT 'Año de Liga',
  `Pts` int(11) NOT NULL COMMENT 'Puntos acumulados',
  `PJ` int(11) NOT NULL COMMENT 'Partidos jugados',
  `PG` int(11) NOT NULL COMMENT 'Partidos ganados',
  `PE` int(11) NOT NULL COMMENT 'Partidos empatados',
  `PP` int(11) NOT NULL COMMENT 'Partidos perdidos',
  `GF` int(11) NOT NULL COMMENT 'Goles a favor',
  `GC` int(11) NOT NULL COMMENT 'Goles en contra'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabla de Posicion acumulada';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PosicionesVisitante`
--

CREATE TABLE `PosicionesVisitante` (
  `idP` int(11) NOT NULL COMMENT 'ID del detalle o posiciones en la tabla',
  `fkEq` int(11) NOT NULL COMMENT 'FK del Equipo',
  `year` int(11) NOT NULL COMMENT 'Año de Liga',
  `Pts` int(11) NOT NULL COMMENT 'Puntos (visitante)',
  `PJ` int(11) NOT NULL COMMENT 'Partidos jugados (visitante)',
  `PG` int(11) NOT NULL COMMENT 'Partidos ganados (visitante)',
  `PE` int(11) NOT NULL COMMENT 'Partidos empatados (visitante)',
  `PP` int(11) NOT NULL COMMENT 'Partidos perdidos (visitante)',
  `GF` int(11) NOT NULL COMMENT 'Goles a favor (visitante)',
  `GC` int(11) NOT NULL COMMENT 'Goles en contra (visitante)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabla de Posicion de visitante';

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`idEq`);

--
-- Indices de la tabla `metaDataEstadisticas`
--
ALTER TABLE `metaDataEstadisticas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `raw_html` (`raw_html`) USING HASH;

--
-- Indices de la tabla `metaDataPartidos`
--
ALTER TABLE `metaDataPartidos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `raw_html` (`raw_html`) USING HASH;

--
-- Indices de la tabla `Partidos`
--
ALTER TABLE `Partidos`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `eqA` (`eqA`),
  ADD KEY `eqB` (`eqB`);

--
-- Indices de la tabla `PosicionesLocal`
--
ALTER TABLE `PosicionesLocal`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `fkEq` (`fkEq`);

--
-- Indices de la tabla `PosicionesTotal`
--
ALTER TABLE `PosicionesTotal`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `fkEq` (`fkEq`);

--
-- Indices de la tabla `PosicionesVisitante`
--
ALTER TABLE `PosicionesVisitante`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `fkEq` (`fkEq`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `idEq` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Id del Equipo y PK';

--
-- AUTO_INCREMENT de la tabla `metaDataEstadisticas`
--
ALTER TABLE `metaDataEstadisticas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK del HTML extraido';

--
-- AUTO_INCREMENT de la tabla `metaDataPartidos`
--
ALTER TABLE `metaDataPartidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK del HTML extraido';

--
-- AUTO_INCREMENT de la tabla `Partidos`
--
ALTER TABLE `Partidos`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del partido';

--
-- AUTO_INCREMENT de la tabla `PosicionesLocal`
--
ALTER TABLE `PosicionesLocal`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- AUTO_INCREMENT de la tabla `PosicionesTotal`
--
ALTER TABLE `PosicionesTotal`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- AUTO_INCREMENT de la tabla `PosicionesVisitante`
--
ALTER TABLE `PosicionesVisitante`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Partidos`
--
ALTER TABLE `Partidos`
  ADD CONSTRAINT `Partidos_ibfk_1` FOREIGN KEY (`eqA`) REFERENCES `equipos` (`idEq`),
  ADD CONSTRAINT `Partidos_ibfk_2` FOREIGN KEY (`eqB`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `PosicionesLocal`
--
ALTER TABLE `PosicionesLocal`
  ADD CONSTRAINT `PosicionesLocal_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `PosicionesTotal`
--
ALTER TABLE `PosicionesTotal`
  ADD CONSTRAINT `PosicionesTotal_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `PosicionesVisitante`
--
ALTER TABLE `PosicionesVisitante`
  ADD CONSTRAINT `PosicionesVisitante_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);

-- proceed matches data
-- check the result
-- Creando Vistas funcionales
CREATE VIEW IF NOT EXISTS Clubs AS
	SELECT e.ideq, e.nombre, e.enlace
	FROM equipos e;
CREATE VIEW IF NOT EXISTS PtsTotal AS
	SELECT e.nombre, pa.Pts, pa.PJ, pa.PG, pa.PE, pa.PP, pa.GF, pa.GC, pa.year
	FROM equipos e, PosicionesTotal pa
	WHERE e.idEq = pa.fkEq;
CREATE VIEW IF NOT EXISTS PtsLocal AS
	SELECT e.nombre, pl.Pts, pl.PJ, pl.PG, pl.PE, pl.PP, pl.GF, pl.GC, pl.year
	FROM equipos e, PosicionesLocal pl
	WHERE e.idEq = pl.fkEq;
CREATE VIEW IF NOT EXISTS PtsVisitante AS
	SELECT e.nombre, pv.Pts, pv.PJ, pv.PG, pv.PE, pv.PP, pv.GF, pv.GC, pv.year
	FROM equipos e, PosicionesVisitante pv
	WHERE e.idEq = pv.fkEq;
CREATE VIEW IF NOT EXISTS TotalPartidosJugados AS
	SELECT DISTINCT fkEq, year FROM PosicionesTotal;
CREATE VIEW IF NOT EXISTS Encuentros AS
	SELECT p.eqA, p.golA, p.eqB, p.golB, p.fecha
	FROM equipos e, Partidos p
	WHERE e.idEq = p.eqA and e.idEq= p.eqB;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
