# Conectando a BD
from manejo_mysql import Database
# extraccion del HTML para guardar
from extraction_algorithms import Extraction
# procesamiento de la MetaData (equipos)
from processEquipos import ProcessMetaData
# procesamiento de la MetaData (estadisticas)
from processEstadisticas import ProcessEstadisticas
# procesamiento de la MetaData (partidos)
from processPartidos import ProcessPartidos
# generar CSV
from archivo_csv import generar_CSV
from datetime import datetime
# lib para obtener la fecha actual (anio)
tiempoInicio = datetime.now()
# Abriendo la conexion a la BD
objExtraction = Extraction()
objDB = Database()
diccionario = {'method_name': 'footballdatabase'}
anio = datetime.now().year

while anio > 2009:
    diccionario['url'] = f"https://footballdatabase.com/league-scores-tables/ecuador-serie-a-{anio}"
    url = diccionario['url']
    print('URL a consultar:\t{}'.format(url))
    # print('Anio extraer data:\t{}'.format(anio))
    
    metadataEstadisticas = objExtraction.run_extraction(parameters=diccionario)
    # Dicionario con la metadata extraida (Acumulado, Local, Visitante)
    # print('Estadisticas metadata\n\n\n\n', metadataEstadisticas, '\n\n\n\n')
    raw_html = metadataEstadisticas['raw_html']
    estad_total = metadataEstadisticas['Acumulado']
    estad_local = metadataEstadisticas['Local']
    estad_visitante = metadataEstadisticas['Visitante']
    errores = metadataEstadisticas['errors']
    extract = metadataEstadisticas['extact']
    fecha_process = ""
    errors_process = ""
    process = ""
    valido = objDB.insert_RawEstadisticas(url, raw_html, estad_total, estad_local, estad_visitante, str(anio), errores, extract, fecha_process, errors_process, process)
    if valido is None:
        print('Error al insertar RawEstadistica\t\tSitio:\t{}\t\tErrors:\t{}'.format(url, errores))
    else:
        # print('Registro de RAW Estadistica exitoso')
        pass
        # print(raw)
    # Traemos la lista de Raw No procesados
    rawNoPross_Estadisticas = objDB.rawNoProcessEstadisticas()
    # print('Metadatos no procesados\n', metadata_Estadisticas)
    metadata_Estadisticas = {}
    for elemento in rawNoPross_Estadisticas:
        # print({'elemento':elemento})
        # print({'Local':elemento[1]})
        metadata_Estadisticas['Acumulado']= elemento[1]
        metadata_Estadisticas['Local']= elemento[2]
        metadata_Estadisticas['Visitante']= elemento[3]
    metadata_Estadisticas['method_name'] = 'processDataEquipos'
    objProcessEquipos = ProcessMetaData()
    # print('keys\t', metadata_Estadisticas.keys())
    processEstadisticas = objProcessEquipos.run_ProcessEquipos(parameters=metadata_Estadisticas)
    # print('Data Procesada\n', processEstadisticas)
    del objProcessEquipos

    # Insertando los equipos
    # print('Tipo de dato que envia para equipos:\t{}'.format(type(processEstadisticas)))
    errores = objDB.insert_Equipos(processEstadisticas)

    objProEstadisticas = ProcessEstadisticas()
    metadata_Estadisticas['method_name'] = 'processDataEstadisticas'
    estadisticas = objProEstadisticas.run_process(metadata_Estadisticas)
    # retorna un dict con Acumulado, Local, Visitante
    # eliminando el objetdo creado
    del objProEstadisticas
    # print('\nData Procesada Estadisticas\n\n',estadisticas)
    # print('Llaves de los datos extraidos\t{}'.format(estadisticas['data'].keys()))
    # Insertando Data procesada
    for key in estadisticas['data']:
        opciones = estadisticas['data']
        # print('estadisticas-key::\t{}\tTipo:/t{}'.format(key, type(opciones[key])))
        # print('Como\tClub\tYear\tPts\tGD\tPJ\tPG\tPE\tPP\tGA\tGC')
        # P	+/-	M	W	D	L	F	A
        resgHtmlEstadista = None
        for element in opciones[key]:
            # print('Estadistas y equipo\n{}'.format(element))
            equipo = element[1]
            year = url.split('/')[-1].split('-')[-1]
            # pts acumulados
            pts = element[2]
            # gol diferncia (no se esta guardando, ya se tienen datos para esta operacion)
            gd = element[3]
            # partidos jugados
            pj = element[4]
            # partidos ganados
            pg = element[5]
            # partidos empatado
            pe = element[6]
            # partidos perdido
            pp = element[7]
            # gol a favor
            gf = element[8]
            # gol en contra
            gc = element[9]
            # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(key, equipo, year, pts, gd, pj, pg, pe, pp, gf, gc))
            # lista de posiciones
            resgHtmlEstadista = objDB.insert_Estadisticas(opcion=key, equipo=equipo, anio=year, pts=pts, pj=pj, pg=pg, pe=pe, pp=pp, gf=gf, gc=gc)
        if resgHtmlEstadista is None:
            pass
        else:
            # actualiza el registro con ese
            fecha_process = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_process = datetime.strptime(fecha_process, '%Y-%m-%d %H:%M:%S')
            # fecha del sistema con el formato deseado
            errors_process = estadisticas['errores_procesamiento']
            process = estadisticas['process']
            actHtmlEstadista = objDB.actualizar_RawEstadisticas(sitio = url, anio = year, fecha_process=fecha_process, errores_process=errors_process, process=process)
            if actHtmlEstadista is None:
                pass
            else:
                print('Registro Estadistica actualizado:\t{}#\t\tSitio:\t{}\t\tAnio\t{}'.format(actHtmlEstadista[0], url, anio))
    
    # URL para metadata de partidos
    dicDataPartidos = {'url': url}
    # asignamos el nombre la funcion que extra el HTML de partidos
    dicDataPartidos['method_name'] = 'extracMetadataPartidos'
    # agrengado el nombre de la funcion que extrae la metadadata de partidos
    # print('\n\nTipo dato enviado a procesar partidos\t', type(dicDataPartidos))
    dicMetadataPartidos = objExtraction.run_extraction(parameters=dicDataPartidos)
    # print('Tipo Metadata Partidos\t{}'.format(type(dicMetadataPartidos)))
    # print('Errores Metadata Partidos\t{}'.format(dicMetadataPartidos['errores_extraccion']))
    if dicMetadataPartidos['metadata'] is not None:
        # se insert la metadata encontrada
        for elemento in dicMetadataPartidos['metadata']:
            # recorriendo la lista de HTML extraido
            url_partido = elemento[0]
            raw_partido = elemento[1]
            anio_partido = elemento[2]
            # print('URL_partido\t{}\nAnioPartido\n{}'.format(url_partido, anio_partido))
            errores_extraccion = dicMetadataPartidos['errores_extraccion']
            extract = dicMetadataPartidos['extract']
            insertMdPartido = objDB.insert_RawPartidos(url_partido, raw_partido, anio_partido, errores_extraccion, extract)
            # print('Raw partidos (tipo):\t{}'.format(type(insertMdPartido)))
            if insertMdPartido is None:
                print('No se inserto la metadadata (URL) de partidos\t{}'.format(url_partido))
            else:
                # print('Se inserto la metadadata de partidos')
                pass
        # Procesa la metada anteriormente Insertada y la que aun no se ha procesado
        rawNoPross_Partido = objDB.rawNoProcessPartidos()
        dictMtPartido = {}
        dictMtPartido['metadata'] = rawNoPross_Partido
        dictMtPartido['method_name'] = 'processDataPartidos'
        objProcessPartido = ProcessPartidos()
        dataPartido = objProcessPartido.run_process(dictMtPartido)
        # eliminando objeto creado
        del objProcessPartido
        partidos = dataPartido['data']
        # print('Data recuperada partidos:\t{}\nValor\n{}'.format(dataPartido.keys(), type(partidos)))
        # aqui se insertan los partidos
        # print('Partidos')
        for encuentro in partidos:
            # print('DATA partido:\t'.format(encuentro))
            # (equipoA, golA, equipoB, golB, url_partidos, anio)
            eqA = encuentro[0]
            golA = encuentro[1]
            eqB = encuentro[2]
            golB = encuentro[3]
            url = encuentro[4]
            year = encuentro[5]
            # print('{}\t{}-{}\t{}\t\t{}\t{}'.format(eqA, golA, golB, eqB, url, year))
            insertPart = objDB.insert_Partido(eqA=eqA, golA=golA, golB=golB, eqB=eqB, year=year)
            # print('Registro (partido):\t#{}'.format(insertPart))
            if insertPart is None:
                pass
            else:
                # actualiza el registro con ese
                error_process = dataPartido['errores_procesamiento']
                process = dataPartido['process']
                fecha_process = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fecha_process = datetime.strptime(fecha_process, '%Y-%m-%d %H:%M:%S')
                resgHtmlPartidos = objDB.actualizar_RawPartido(sitio = url_partido, raw=raw_partido, fecha_process=fecha_process, errores_procesamiento=error_process, process=process)
                if resgHtmlPartidos is None:
                    pass
                else:
                    print('Registro partido actualizado:\t{}#\t::\tSitio:\t{}'.format(resgHtmlPartidos[0], url))
    # cambiando de anio
    anio = int(anio) - 1
    anio = int(anio)

objArchivos = generar_CSV()
estadisticaGeneral = objDB.estadisticasTotales()
estadisticaLocal = objDB.estadisticasLocales()
estadisticaVisitante = objDB.estadisticasVisitantes()
encuentros = objDB.encuentros()
"""
print('CSV Tipo\t:{}'.format(type(estadisticaGeneral)))
print('CSV Tipo\t:{}'.format(type(estadisticaLocal)))
print('CSV Tipo\t:{}'.format(type(estadisticaVisitante)))
print('CSV Tipo\t:{}'.format(type(encuentros)))
"""
objArchivos.csv_estadisticas(estadisticaGeneral, 'Acumulado')
objArchivos.csv_estadisticas(estadisticaLocal, 'Local')
objArchivos.csv_estadisticas(estadisticaVisitante, 'Visitante')
objArchivos.csv_encuentros(encuentros)

objDB.close()
# cerrando la conexion
del objExtraction
# eliminando objeto creado
# Romper ejecucion
# import sys
# sys.exit()
tiempoFin = datetime.now()
timepoEjecucion = tiempoFin - tiempoInicio
print('Inicio:\t\t{}\nFin:\t\t{}\n______________________________________\nTiempo de ejecucion\t{}'.format(tiempoInicio, tiempoFin, timepoEjecucion))
