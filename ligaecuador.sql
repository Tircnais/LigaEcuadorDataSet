-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-11-2021 a las 18:33:11
-- Versión del servidor: 10.4.21-MariaDB
-- Versión de PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ligaecuador`
--
CREATE DATABASE IF NOT EXISTS `ligaecuador` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ligaecuador`;

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `clubs`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `clubs`;
CREATE TABLE `clubs` (
`idEq` int(11)
,`nombre` varchar(120)
,`enlace` varchar(255)
,`img` varchar(255)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `conteo_estadisticas`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `conteo_estadisticas`;
CREATE TABLE `conteo_estadisticas` (
`conteo_totales` bigint(21)
,`conteo_locales` bigint(21)
,`conteo_visitante` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `encuentros`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `encuentros`;
CREATE TABLE `encuentros` (
`idP` int(11)
,`eqA` varchar(120)
,`eqB` varchar(120)
,`golA` int(11)
,`golB` int(11)
,`fecha` year(4)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

DROP TABLE IF EXISTS `equipos`;
CREATE TABLE `equipos` (
  `idEq` int(11) NOT NULL COMMENT 'Id del Equipo y PK',
  `nombre` varchar(120) NOT NULL COMMENT 'Nombre del equipo',
  `enlace` varchar(255) NOT NULL COMMENT 'Enlace del equipo para mas innformacion',
  `img` varchar(255) NOT NULL COMMENT 'foto/logo del equipo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Equipos de la liga Ecuatoriana (Serie A)';

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `estadisticaslocal`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `estadisticaslocal`;
CREATE TABLE `estadisticaslocal` (
`nombre` varchar(120)
,`year` int(11)
,`Pts` int(11)
,`PJ` int(11)
,`PG` int(11)
,`PE` int(11)
,`PP` int(11)
,`GF` int(11)
,`GC` int(11)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `estadisticastotales`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `estadisticastotales`;
CREATE TABLE `estadisticastotales` (
`nombre` varchar(120)
,`year` int(11)
,`Pts` int(11)
,`PJ` int(11)
,`PG` int(11)
,`PE` int(11)
,`PP` int(11)
,`GF` int(11)
,`GC` int(11)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `estadisticasvisitantes`
-- (Véase abajo para la vista actual)
--
DROP VIEW IF EXISTS `estadisticasvisitantes`;
CREATE TABLE `estadisticasvisitantes` (
`nombre` varchar(120)
,`year` int(11)
,`Pts` int(11)
,`PJ` int(11)
,`PG` int(11)
,`PE` int(11)
,`PP` int(11)
,`GF` int(11)
,`GC` int(11)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metadataestadisticas`
--

DROP TABLE IF EXISTS `metadataestadisticas`;
CREATE TABLE `metadataestadisticas` (
  `id` int(11) NOT NULL COMMENT 'PK del HTML extraido',
  `sitio` varchar(255) NOT NULL COMMENT 'Fuente de donde se extrajo la metadata',
  `raw_html` longtext NOT NULL COMMENT 'HTML de los metadatos',
  `estad_total` longtext DEFAULT NULL COMMENT 'Metadata de Estadistica total',
  `estad_local` longtext DEFAULT NULL COMMENT 'Metadata de Estadistica local',
  `estad_visitante` longtext DEFAULT NULL COMMENT 'Metadata de Estadistica visitante',
  `anio` varchar(4) DEFAULT NULL COMMENT 'Anio del que se extrae la metadata',
  `fecha_extract` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'fecha en la que se extrajo la metada',
  `errores_extraccion` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Errores recolectados al extraer, es decir, guardar datos en opcion.',
  `extract` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se extrajo la data ',
  `fecha_process` timestamp NULL DEFAULT NULL COMMENT 'fecha en la que se proceso la metada',
  `errores_procesamiento` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Errores recolectados al momento de procesar, es decir, extraer datos para las tablas de posiciones.',
  `process` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se proceso la data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metadatapartidos`
--

DROP TABLE IF EXISTS `metadatapartidos`;
CREATE TABLE `metadatapartidos` (
  `id` int(11) NOT NULL COMMENT 'PK del HTML extraido',
  `sitio` varchar(255) NOT NULL COMMENT 'Fuente de donde se extrajo la metadata',
  `raw_html` longtext NOT NULL COMMENT 'HTML de los metadatos',
  `anio` varchar(4) DEFAULT NULL COMMENT 'Anio del que se extrae la metadata',
  `fecha_extract` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'fecha en la que se extrajo la metada',
  `errores_extraccion` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Errores recolectados al momento de procesar, es decir, extraer los datos.' CHECK (json_valid(`errores_extraccion`)),
  `extract` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se extrajo la data'' AFTER `erroresExtraccion',
  `fecha_process` timestamp NULL DEFAULT NULL COMMENT 'fecha en la que se proceso la metada',
  `errores_procesamiento` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Errores recolectados al extraer, es decir, guardar datos en opcion.' CHECK (json_valid(`errores_procesamiento`)),
  `process` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'V/F para determinar si se extrajo la data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partidos`
--

DROP TABLE IF EXISTS `partidos`;
CREATE TABLE `partidos` (
  `idP` int(11) NOT NULL COMMENT 'ID del partido',
  `eqA` int(11) NOT NULL COMMENT 'id del Equipo A',
  `eqB` int(11) NOT NULL COMMENT 'id del Equipo B',
  `golA` int(11) NOT NULL COMMENT 'goles del Equipo A',
  `golB` int(11) NOT NULL COMMENT 'goles del Equipo B',
  `fecha` year(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `posicioneslocal`
--

DROP TABLE IF EXISTS `posicioneslocal`;
CREATE TABLE `posicioneslocal` (
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
-- Estructura de tabla para la tabla `posicionestotal`
--

DROP TABLE IF EXISTS `posicionestotal`;
CREATE TABLE `posicionestotal` (
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
-- Estructura de tabla para la tabla `posicionesvisitante`
--

DROP TABLE IF EXISTS `posicionesvisitante`;
CREATE TABLE `posicionesvisitante` (
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

-- --------------------------------------------------------

--
-- Estructura para la vista `clubs`
--
DROP TABLE IF EXISTS `clubs`;

DROP VIEW IF EXISTS `clubs`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `clubs`  AS SELECT `equipos`.`idEq` AS `idEq`, `equipos`.`nombre` AS `nombre`, `equipos`.`enlace` AS `enlace`, `equipos`.`img` AS `img` FROM `equipos` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `conteo_estadisticas`
--
DROP TABLE IF EXISTS `conteo_estadisticas`;

DROP VIEW IF EXISTS `conteo_estadisticas`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `conteo_estadisticas`  AS SELECT `pt`.`conteo_totales` AS `conteo_totales`, `pl`.`conteo_locales` AS `conteo_locales`, `pv`.`conteo_visitante` AS `conteo_visitante` FROM (((select count(0) AS `conteo_totales` from `posicionestotal`) `pt` join (select count(0) AS `conteo_locales` from `posicioneslocal`) `pl`) join (select count(0) AS `conteo_visitante` from `posicionesvisitante`) `pv`) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `encuentros`
--
DROP TABLE IF EXISTS `encuentros`;

DROP VIEW IF EXISTS `encuentros`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `encuentros`  AS SELECT `p`.`idP` AS `idP`, `tablaa1`.`nombre` AS `eqA`, `tablaa2`.`nombre` AS `eqB`, `p`.`golA` AS `golA`, `p`.`golB` AS `golB`, `p`.`fecha` AS `fecha` FROM ((`partidos` `p` join `equipos` `tablaa1` on(`tablaa1`.`idEq` = `p`.`eqA`)) join `equipos` `tablaa2` on(`tablaa2`.`idEq` = `p`.`eqB`)) ORDER BY `p`.`idP` ASC, `p`.`fecha` ASC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `estadisticaslocal`
--
DROP TABLE IF EXISTS `estadisticaslocal`;

DROP VIEW IF EXISTS `estadisticaslocal`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `estadisticaslocal`  AS SELECT DISTINCT `eq`.`nombre` AS `nombre`, `el`.`year` AS `year`, `el`.`Pts` AS `Pts`, `el`.`PJ` AS `PJ`, `el`.`PG` AS `PG`, `el`.`PE` AS `PE`, `el`.`PP` AS `PP`, `el`.`GF` AS `GF`, `el`.`GC` AS `GC` FROM (`posicioneslocal` `el` join `equipos` `eq`) WHERE `el`.`fkEq` = `eq`.`idEq` ORDER BY `el`.`year` DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `estadisticastotales`
--
DROP TABLE IF EXISTS `estadisticastotales`;

DROP VIEW IF EXISTS `estadisticastotales`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `estadisticastotales`  AS SELECT DISTINCT `eq`.`nombre` AS `nombre`, `et`.`year` AS `year`, `et`.`Pts` AS `Pts`, `et`.`PJ` AS `PJ`, `et`.`PG` AS `PG`, `et`.`PE` AS `PE`, `et`.`PP` AS `PP`, `et`.`GF` AS `GF`, `et`.`GC` AS `GC` FROM (`posicionestotal` `et` join `equipos` `eq`) WHERE `et`.`fkEq` = `eq`.`idEq` ORDER BY `et`.`year` DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `estadisticasvisitantes`
--
DROP TABLE IF EXISTS `estadisticasvisitantes`;

DROP VIEW IF EXISTS `estadisticasvisitantes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `estadisticasvisitantes`  AS SELECT DISTINCT `eq`.`nombre` AS `nombre`, `ev`.`year` AS `year`, `ev`.`Pts` AS `Pts`, `ev`.`PJ` AS `PJ`, `ev`.`PG` AS `PG`, `ev`.`PE` AS `PE`, `ev`.`PP` AS `PP`, `ev`.`GF` AS `GF`, `ev`.`GC` AS `GC` FROM (`posicionesvisitante` `ev` join `equipos` `eq`) WHERE `ev`.`fkEq` = `eq`.`idEq` ORDER BY `ev`.`year` DESC ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`idEq`);

--
-- Indices de la tabla `metadataestadisticas`
--
ALTER TABLE `metadataestadisticas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniqui_raw_html` (`raw_html`) USING HASH;

--
-- Indices de la tabla `metadatapartidos`
--
ALTER TABLE `metadatapartidos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unico_raw_html` (`raw_html`) USING HASH;

--
-- Indices de la tabla `partidos`
--
ALTER TABLE `partidos`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `eqA` (`eqA`),
  ADD KEY `eqB` (`eqB`);

--
-- Indices de la tabla `posicioneslocal`
--
ALTER TABLE `posicioneslocal`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `fkEq` (`fkEq`);

--
-- Indices de la tabla `posicionestotal`
--
ALTER TABLE `posicionestotal`
  ADD PRIMARY KEY (`idP`),
  ADD KEY `fkEq` (`fkEq`);

--
-- Indices de la tabla `posicionesvisitante`
--
ALTER TABLE `posicionesvisitante`
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
-- AUTO_INCREMENT de la tabla `metadataestadisticas`
--
ALTER TABLE `metadataestadisticas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK del HTML extraido';

--
-- AUTO_INCREMENT de la tabla `metadatapartidos`
--
ALTER TABLE `metadatapartidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK del HTML extraido';

--
-- AUTO_INCREMENT de la tabla `partidos`
--
ALTER TABLE `partidos`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del partido';

--
-- AUTO_INCREMENT de la tabla `posicioneslocal`
--
ALTER TABLE `posicioneslocal`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- AUTO_INCREMENT de la tabla `posicionestotal`
--
ALTER TABLE `posicionestotal`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- AUTO_INCREMENT de la tabla `posicionesvisitante`
--
ALTER TABLE `posicionesvisitante`
  MODIFY `idP` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID del detalle o posiciones en la tabla';

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `partidos`
--
ALTER TABLE `partidos`
  ADD CONSTRAINT `Partidos_ibfk_1` FOREIGN KEY (`eqA`) REFERENCES `equipos` (`idEq`),
  ADD CONSTRAINT `Partidos_ibfk_2` FOREIGN KEY (`eqB`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `posicioneslocal`
--
ALTER TABLE `posicioneslocal`
  ADD CONSTRAINT `PosicionesLocal_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `posicionestotal`
--
ALTER TABLE `posicionestotal`
  ADD CONSTRAINT `PosicionesTotal_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);

--
-- Filtros para la tabla `posicionesvisitante`
--
ALTER TABLE `posicionesvisitante`
  ADD CONSTRAINT `PosicionesVisitante_ibfk_1` FOREIGN KEY (`fkEq`) REFERENCES `equipos` (`idEq`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
