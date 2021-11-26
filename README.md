Proyecto Extracción de data
======================

### Objetivo: Generar _Dataset_.

Versión `1.1.14`

#### Table of Contents

- [Aspecto Generales](#Aspecto-Generales)  
- [Puesta en marcha](#Puesta-en-marcha)
- [Datos extraídos](#Datos-extraídos)  
- [Diagrama UML](#Diagrama-UML)  
- [Formulas aplicadas](#Formulas-aplicadas)  

## Aspecto Generales

- ### Descripción

  Aplicativo para extraer metadatos y generar un dataset sobre la [liga de fútbol de Ecuador Serie A](https://footballdatabase.com/league-scores-tables/ecuador-serie-a-2021).
  
  > Fuente [footballdatabase](https://footballdatabase.com)

- ### Dependencias
  
  A continuación las dependencias más importantes usadas para extraer la metadata del sitio.
  - **_Beautifulsoup4_**

    ```python
      Versión: 4.10.0
    ```
  
  Usando BS4 para extraer la metada del sitio  [footballdatabase](https://footballdatabase.com)
  - **_PyMySQL_**
  
    ```python
      Versión: 1.0.2
    ```

  Usando PyMySQL para conectar con la Base de datos.

## Puesta en marcha

**1. Clonando el repositorio**

```git
  git clone https://github.com/Tircnais/LigaEcuadorDataSet.git
```

**2. Implementar el DLL proporcionado**

> [ligaEcuador.sql](https://github.com/Tircnais/LigaEcuadorDataSet/blob/master/ligaecuador.sql)

**3. Instalando dependencias**

```python
  pip3 install requirements.txt
```

Instalar dependencias del proyecto

```python
  pip3 install -r requirements.txt
```

Si se tiene problemas al instalar dependencias del proyecto

**4. Ejecutando el proyecto**

```python
  python main.py
```

## Datos extraídos

Los datos que se van analizar son: las estadisticas y partidos por año fueron extraidos apartir del año 2009 - 2021.

### Equipos

| ideq | nombre | enlace | img |
|------|--------|--------|-----|
| 1 | Barcelona SC | https://footballdatabase.com/clubs-ranking/barcelona-sc-guayaquil | https://footballdatabase.com/logos/club/80px/708.png |
| 2 | Independiente | https://footballdatabase.com/clubs-ranking/independiente-del-valle-sangolqui | https://footballdatabase.com/logos/club/80px/713.png |
| 3 | Emelec | https://footballdatabase.com/clubs-ranking/emelec | https://footballdatabase.com/logos/club/80px/711.png |

El **ideq** es el número de registro correspondiente.

### Estadisticas

| idP | fkEq | year | Pts | PJ | PG | PE | PP | GF | GC |
|-----|------|------|-----|----|----|----|----|----|----|
| 1   | 1    | 2021 | 20  | 8  | 7  | 1  | 0  | 17 | 3  |
| 2   | 2    | 2021 | 13  | 7  | 5  | 1  | 1  | 4  | 3  |
| 3   | 3    | 2021 | 11  | 7  | 3  | 2  | 2  | 5  | 2  |

En dicha tabla la columna **fkEq** es la llave foranea hacia la tabla **Equipos**, year es el año. Para obtener el orden de **posicion** se debe realizar una **consulta en base a los puntos**. **Las estadisticas se ha dividido en tres tabla** con las misma cantidad de columnas y nombres esto con el fin de obtner los puntos: **acumulados**, **local** y **visitante**.

### Partidos

| idP | Team_A | Team_B | Goal_A | Goal_B | Fecha       |
|-----|--------|--------|--------|--------|------------|
| 1   | 1      | 3      | 2      | 0      | 11/10/2021 |
| 2   | 2      | 1      | 3      | 1      | 12/10/2021 |
| 3   | 3      | 2      | 1      | 2      | 13/10/2021 |

En dicha tabla la columna Team_A y Team_B representa el ID del equipo, estos son un ejemplo de como se almacenan los registros de los partidos.

<!--
## Diagrama UML

```mermaid
sequenceDiagram
main ->> extraction_algorithms: Ejecuta la funcion footballdatabase
main--:>>>John: How about you John?
main--x Alice: I am good thanks!
main-x John: I am good thanks!
Note right of John: main thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

main--;>Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
main[Square Rect] -- Link text --;> B((Circle))
main --;> C(Round Rect)
B --;> D{Rhombus}
C --;> D
```

## Formulas aplicadas

### Distribución Poisson

### Distribución skellam



### KaTeX --- Explicacion futura de las formulas para la predicción

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$
-->