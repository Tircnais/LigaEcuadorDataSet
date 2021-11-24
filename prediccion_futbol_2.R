# Instalando librerias ----------------------------------------------------
# conexion a MySQL
install.packages('RMariaDB')
remotes::install_github('r-dbi/DBI')
remotes::install_github('r-dbi/RMariaDB')
# para la grafia de distribucion
install.packages('plotrix')
# modelo de distribuci?n poisson
install.packages('poisson')
# modelo de distribuci?n skellam
install.packages("skellam")

# llamando a las librerias ------------------------------------------------
library(RMariaDB)
library(plotrix)
library(poisson)
library(skellam)

userName <- 'root'
localuserpassword <- ''
localhost <- 'localhost'
dbName <- 'ligaecuador'
# usando la Lib para realizar la conexion
conectBD <- dbConnect(RMariaDB::MariaDB(), user=userName, password=localuserpassword, dbname=dbName, host=localhost)
# Muestra las tablas de la BD ---------------------------------------------
dbListTables(conectBD)

# Como llamar a las vistas de la BD ---------------------------------------
# Funciones ---------------------------------------------------------------
# Consultas a la BD
consultaSQL <- function(conexion, consulta) {
  # usando dbGetQuery para obtener DATAFRAME
  resultado <- dbGetQuery(conexion, consulta)
  return(resultado)
}

infoGeneral <- function(infoA, infoB, eqA, eqB) {
  tbInfo = data.frame(
    stringsAsFactors=FALSE,
    Encabezado = c("Pronóstico", "Media Goles Local", "Media Goles Visitante"),
    EquipoA = infoA,
    EquipoB = infoB
  )
  # Renombrando columnas (la primera col es de informaci?n)
  names(tbInfo)[2] <- eqA
  names(tbInfo)[3] <- eqB
  return(tbInfo)
}

partidosLocalA <- function(partidos, equipoA, anio) {
  if (anio >= 2009 && class(anio) != 'character') {
    # message(sprintf("%s anio\n", anio))
    # equipo que juega como local y en el ultimo anio
    eqLocalA <- partidos[partidos$eqA == eqA & partidos$fecha==anio,]
  }else{
    # cat(sprintf("%s anio", anio))
    eqLocalA <- partidos[partidos$eqA == eqA,]
  }
  return(eqLocalA)
}

partidosVisitanteA <- function(partidos, equipoA, anio) {
  if (anio >= 2009 && class(anio) != 'character') {
    # message(sprintf("%s anio\n", anio))
    # equipo que juega como visitante y en el ultimo anio
    eqVisitanteA <- partidos[partidos$eqB == eqA & partidos$fecha==anio,]
  }else{
    # cat(sprintf("%s anio", anio))
    eqVisitanteA <- partidos[partidos$eqB == eqA,]
  }
  return(eqVisitanteA)
}

partidosLocalB <- function(partidos, equipoB, anio) {
  if (anio >= 2009 && class(anio) != 'character') {
    # message(sprintf("%s anio\n", anio))
    # equipo que juega como local y en el ultimo anio
    eqLocalA <- partidos[partidos$eqA == eqB & partidos$fecha==anio,]
  }else{
    # cat(sprintf("%s anio", anio))
    eqLocalA <- partidos[partidos$eqA == eqB,]
  }
  return(eqLocalA)
}

partidosVisitanteB <- function(partidos, equipoB, anio) {
  if (anio >= 2009 && class(anio) != 'character') {
    # message(sprintf("%s anio\n", anio))
    # equipo que juega como visitante y en el ultimo anio
    eqVisitanteA <- partidos[partidos$eqB == eqB & partidos$fecha==anio,]
  }else{
    # cat(sprintf("%s anio", anio))
    eqVisitanteA <- partidos[partidos$eqB == eqB,]
  }
  return(eqVisitanteA)
}

tablaPoissonDetalle <- function(datosA, datosB, eqA, eqB) {
  tablaP = data.frame(
    stringsAsFactors=FALSE,
    Encabezado = c("Resultado", "% Local", "% Visitante"),
    EquipoA = datosA,
    EquipoB = datosB
  )
  # Renombrando columnas (la primera col es de informaci?n)
  names(tablaP)[2] <- eqA
  names(tablaP)[3] <- eqB
  return(tablaP)
}

tablaPoisson <- function(datosA, datosB, datosProbP, eqA, eqB) {
  tablaP = data.frame(
    stringsAsFactors=FALSE,
    Encabezado = c("Gane", "Pierda"),
    EquipoA = datosA,
    EquipoB = datosB,
    Probabilidad = datosProbP
  )
  # Renombrando columnas (la primera col es de informaci?n)
  names(tablaP)[2] <- eqA
  names(tablaP)[3] <- eqB
  return(tablaP)
}


tablaSkellam <- function(datosA, datosB, datosP, eqA, eqB) {
  tbSkellam = data.frame(
    stringsAsFactors=FALSE,
    Encabezado = c("Empate", "Gane", "Pierda"),
    EquipoA = datosA,
    EquipoB = datosB,
    Probabilidad = datosP
  )
  # Renombrando columnas (la primera col es de informaci?n)
  names(tbSkellam)[2] <- eqA
  names(tbSkellam)[3] <- eqB
  return(tbSkellam)
}

mediaGoles <- function(dataframeLocal, dataframeVisitante) {
  # cast de data.frame a numeric, y obteniendo el promedio
  media_goles_local <- mean(as.numeric(unlist(dataframeLocal)))
  media_goles_visitante <- mean(as.numeric(unlist(dataframeVisitante)))
  # Renombrando columnas (la primera col es de informaci?n)
  media_equipo <- data.frame(media_goles_local, media_goles_visitante)
  # controlando cuando no hay datos
  if (is.nan(dim(media_equipo)[1])== TRUE) {
    media_equipo[1] <- 0
  }
  if(is.nan(dim(media_equipo)[2])== TRUE) {
    media_equipo[2] <- 0
  }
  # Redondeo
  media_equipo[1] <- round(media_equipo[1], 2)
  media_equipo[2] <- round(media_equipo[2], 2)
  return(media_equipo)
}

distribucion_poisson <- function(goles, media_goles) {
  probilidad <- dpois(goles, media_goles)
  # Redondeo
  probilidad <- round(probilidad*100, 2)
  return(probilidad)
}

distribucion_poisson_probabilidad <- function(probabilidad, media_goles) {
  # dada una probabilidad #goles a anotar
  cantGolAL <- qpois(probabilidad, media_goles, lower.tail = TRUE)
  return(cantGolAL)
}

distribucion_skellam <- function(resultado, media_goles_a, media_goles_b) {
  pEmpateSkellam <- skellam::dskellam(resultado,media_goles_a, media_goles_b)
  # Redondeo
  probilidad <- round(pEmpateSkellam*100, 2)
  return(probilidad)
}

joinTablas <- function(tabla_Poisson, tabla_Skellam, elementoComunes) {
  resumen <- merge(x = tabla_Poisson, y = tabla_Skellam, by = elementoComunes) # Equivalente
  names(resumen)[4] <- 'Prob_Poisson'
  names(resumen)[5] <- 'Prob_Skellam'
  return(resumen)
}

probabilidad_ocurrencia_evento <- function(probUno, probDos) {
  prob_ocurrencia <- round((probUno*probDos)/100, 2)
  return(prob_ocurrencia)
}

# query, usando dbSendQuery obtiene mariadbresult
# equipos <- dbSendQuery(conectBD, "SELECT idEq, nombre FROM clubs")
# d1 <- dbFetch(equipos, n = 10) # extract data in chunks of 10 rows
# dbHasCompleted(equipos)
# d2 <- dbFetch(equipos, n = -1) # extract all remaining data
# dbHasCompleted(equipos)
# dbClearResult(equipos)

# Cargando datos ----------------------------------------------------------
clubs <- consultaSQL(conectBD, "SELECT * FROM clubs")
partidos <- consultaSQL(conectBD, "SELECT eqA, eqB, golA, golB, fecha FROM Encuentros")
estLocal <- consultaSQL(conectBD, "SELECT nombre, year, GF, GC FROM EstadisticasLocal")
estVisitante <- consultaSQL(conectBD, "SELECT nombre, year, GF, GC FROM EstadisticasVisitantes")
estTotal <- consultaSQL(conectBD, "SELECT nombre, year, GF, GC FROM EstadisticasTotales")
anios <- consultaSQL(conectBD, "SELECT DISTINCT year FROM EstadisticasLocal")
conteo <- consultaSQL(conectBD, "SELECT * FROM conteo_estadisticas")
# tipo
class(estLocal)
# Usando un modelo estadistico --------------------------------------------
# Uniendo tablas usando JOIN
estadisticaLV <- merge(x = estLocal, y = estVisitante, by = c("nombre", "year")) # Equivalente

# Analisis VS -------------------------------------------------------------
# Equipos a analizar
eqA <- 'Universidad Católica'
eqB <- 'Orense SC'
# Resultado
golesA <- 1
golesB <- 0

# Analisis Equipo A -------------------------------------------------------
# Probabilidad de que un equipo gane como Local (Filtramos las estadisticas del equipo a analizar)
eqLocalA <- partidosLocalA(partidos, eqA, 0)
# Probabilidad de que un equipo gane como Visitante (Filtramos las estadisticas del equipo a analizar)
eqVisitanteA <- partidosVisitanteA(partidos, eqA, 0)
# media de goles
infoA <- mediaGoles(eqLocalA[3], eqVisitanteA[3])
# cast dataframe a numeric
media_eqLA <- as.numeric(infoA[1])
media_eqVA <- as.numeric(infoA[2])

# Probabilidad de ganar por X goles
# Distribuci?n de Poisson
# probabilidad acumulada, es decir, mas 2 goles P(2)+P(3)+P(4)+...
p_eqAL <- distribucion_poisson(golesA, media_eqLA)
p_eqAV <- distribucion_poisson(golesA, media_eqVA)

# En que caso tiene mayor probabilidad de ganar
if (p_eqAL > p_eqAV) {
  cat(sprintf("%s gana como local", eqA))
} else {
  message(sprintf("%s gana como visitante\n", eqA))
}
# Analisis Equipo B -------------------------------------------------------
# Probabilidad de que un equipo gane como Local (Filtramos las estadisticas del equipo a analizar)
eqLocalB <- partidosLocalB(partidos, eqB, 0)
# Probabilidad de que un equipo gane como Visitante (Filtramos las estadisticas del equipo a analizar)
eqVisitanteB <- partidosVisitanteB(partidos, eqB, 0)

infoB <- mediaGoles(eqLocalB[3], eqVisitanteB[3])
# cast dataframe a numeric
media_eqLB <- as.numeric(infoB[1])
media_eqVB <- as.numeric(infoB[2])

# Probabilidad de ganar por X goles
# Distribuci?n de Poisson
# probabilidad acumulada, es decir, mas 2 goles P(2)+P(3)+P(4)+...
p_eqBL <- distribucion_poisson(golesB, media_eqLB)
p_eqBV <- distribucion_poisson(golesB, media_eqVB)

# En que caso tiene mayor probabilidad de ganar
if (p_eqBL > p_eqBV) {
  cat(sprintf("%s gana como local", eqB))
} else {
  message(sprintf("%s gana como visitante\n", eqB))
}

# Resultados aplicando Distribucion Poisson -------------------------------
pAcomoL <- probabilidad_ocurrencia_evento(p_eqAL, p_eqBV)
pBcomoL <- probabilidad_ocurrencia_evento(p_eqBL, p_eqAV)
# sprintf("%1.2f%%", pAcomoL)
# class(pAcomoL)
cat(sprintf("%1.2f%% de que se cumpla la predicción; Local=%s, Visitante=%s\n", pAcomoL, eqA, eqB))
cat(sprintf("%1.2f%% de que se cumpla la predicción; Local=%s, Visitante=%s\n", pBcomoL, eqB, eqA))

# Quien tiene mayor ventaja de Local/Visitante
if (p_eqAL > p_eqBL) {
  cat(sprintf("%s gana como local\n", eqA))
}else{
  cat(sprintf("%s gana como local\n", eqB))
}
if (p_eqAV > p_eqBV) {
  cat(sprintf("%s gana como visitante\n", eqA))
}else{
  cat(sprintf("%s gana como visitante\n", eqB))
}
# Quien tiene mas probabilidad de ganar
if (p_eqAL > p_eqBV) {
  message(sprintf("%s gana si %s es visitante\n", eqA, eqB))
}else if (p_eqAV < p_eqBL) {
  message(sprintf("%s gana si %s es local\n", eqB, eqA))
}
if (p_eqBL > p_eqAV) {
  message(sprintf("%s gana si %s es visitante\n", eqB, eqA))
}else if (p_eqBV < p_eqAL) {
  message(sprintf("%s gana si %s es local\n", eqB, eqA))
}

datosInfoA = c(golesA, media_eqLA, media_eqVA)
datosInfoB = c(golesB, media_eqLB, media_eqVB)
tbInfo <- infoGeneral(datosInfoA, datosInfoB, eqA, eqB)

detalleA = c(golesA, p_eqAL, p_eqAV)
detalleB = c(golesB, p_eqBL, p_eqBV)
tbProbPoissonDetalle <- tablaPoissonDetalle(detalleA, detalleB, eqA, eqB)
datosA = c(golesA, golesB)
datosB = c(golesB, golesA)
datosProbP = c(pAcomoL, pBcomoL)
tbProbPoisson <- tablaPoisson(datosA, datosB, datosProbP, eqA, eqB)

# Cant Goles de anotar, dada la probabilidad ------------------------------
probA <- 0.60
probB <- 0.60
# Cant de Goles del Eq A como local
cantGolAL <- distribucion_poisson_probabilidad(probA, media_eqLA)
# Cant de Goles del Eq A como visitante
cantGolAV <- distribucion_poisson_probabilidad(probA, media_eqVA)
# Cant de Goles del Eq B como local
cantGolBL <- distribucion_poisson_probabilidad(probB, media_eqLB)
# Cant de Goles del Eq B como visitante
cantGolBV <- distribucion_poisson_probabilidad(probB, media_eqVB)

# Aplicando Distribucion Skellam ------------------------------------------
resultadoCero <- 0
#probabilidad de un empate (diferencia igual a 0), podemos utilizar el siguiente c?digo:
pEmpateSkellam <- distribucion_skellam(resultadoCero,media_eqLA,media_eqVB)
#deseamos calcular la probabilidad de que el equipo local gane por un gol de diferencia:
pGaneAskellam <- distribucion_skellam(golesA,media_eqLA,media_eqVB)
#Y si deseamos calcular la probabilidad de que el equipo visitante gane por un gol de diferencia:
pGaneBskellam <- distribucion_skellam(golesB-golesA,media_eqLA,media_eqVB)

datosSkellamA = c(resultadoCero, golesA, golesB)
datosSkellamB = c(resultadoCero, golesB, golesA)
datosProbSkellam = c(pEmpateSkellam, pGaneAskellam, pGaneBskellam)
tbProbSkellam <- tablaSkellam(datosSkellamA, datosSkellamB, datosProbSkellam, eqA, eqB)
# Uniendo tablas usando JOIN
resumen <- joinTablas(tbProbPoisson, tbProbSkellam, c(eqA, eqB, 'Encabezado'))

tbInfo
tbProbPoissonDetalle
tbProbPoisson
tbProbSkellam
resumen
# Always cleanup by disconnecting the database ---------------------------------------------
dbDisconnect(conectBD)
## End (cierra la conexion a la BD)
