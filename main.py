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

# Abriendo la conexion a la BD
objExtraction = Extraction()
objDB = Database()
diccionario = {'method_name': 'footballdatabase'}
anio = 2021

while anio > 2008:
    diccionario['url'] = f"https://footballdatabase.com/league-scores-tables/ecuador-serie-a-{anio}"
    url = diccionario['url']
    # print('URL a consultar:\t{}'.format(url))
    print('Anio extraer data:\t{}'.format(anio))
    anio = int(anio) - 1
    anio = int(anio)
    
    metadataEstadisticas = objExtraction.run_extraction(parameters=diccionario)
    # Dicionario con la metadata extraida (Acumulado, Local, Visitante)
    # print('Estadisticas metadata\n\n\n\n', metadataEstadisticas, '\n\n\n\n')
    for item in metadataEstadisticas:
        sitio = url
        opcion = item
        raw = metadataEstadisticas[item]
        valido = objDB.insert_RawEstadisticas(sitio, raw, opcion, anio)
        if valido is None:
            print('Error al insertar RawEstadistica\t\tOpcion:\t{}\t\tRawEst:\t{}'.format(opcion, raw))
        else:
            # print('Registro de RAW Estadistica exitoso')
            pass
            # print(raw)
    # Traemos la lista de Raw No procesados
    rawNoPross_Estadisticas = objDB.rawNoProcessEstadisticas()
    # Cast de Tupla a Dict
    metadata_Estadisticas = dict((x, y) for x, y in rawNoPross_Estadisticas)
    # print('Metadatos no procesados\n', metadata_Estadisticas)
    metadata_Estadisticas['method_name'] = 'procesEquipos'
    objProcessEquipos = ProcessMetaData()
    # print('keys\t', metadata_Estadisticas.keys())
    processEstadisticas = objProcessEquipos.run_ProcessEquipos(parameters=metadata_Estadisticas)
    # print('Data Procesada\n', processEstadisticas)
    del objProcessEquipos

    # Insertando los equipos
    errores = objDB.insert_Equipos(processEstadisticas)

    objProEstadisticas = ProcessEstadisticas()
    metadata_Estadisticas['method_name'] = 'estadisticas'
    estadisticas = objProEstadisticas.run_process(metadata_Estadisticas)
    # retorna un dict con Acumulado, Local, Visitante
    # eliminando el objetdo creado
    del objProEstadisticas
    # print('\nData Procesada Estadisticas\n\n',estadisticas)
    # Insertando Data procesada
    for key in estadisticas:
        # print('estadisticas-key::\t', key)
        # print('Como\tClub\tYear\tPts\tGD\tPJ\tPG\tPE\tPP\tGA\tGC')
        resgHtmlEstadista =''
        for element in estadisticas[key]:
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
            actHtmlEstadista = objDB.actualizar_RawEstadisticas(sitio = url, opcion = key)
            if actHtmlEstadista is None:
                pass
            else:
                print('Registro Estadistica actualizado:\t{}#\t\tSitio:\t{}\t\tOpcion\t{}'.format(actHtmlEstadista[0], url, opcion))
    
    # URL para metadata de partidos
    dicDataPartidos = {'url': url}
    # asignamos el nombre la funcion que extra el HTML de partidos
    dicDataPartidos['method_name'] = 'extracMetadataPartidos'
    # agrengado el nombre de la funcion que extrae la metadadata de partidos
    # print('\n\nTipo dato enviado a procesar partidos\t', type(dicDataPartidos))
    dicMetadataPartidos = objExtraction.run_extraction(parameters=dicDataPartidos)
    # print('Tipo Metadata Partidos\t{}'.format(type(dicMetadataPartidos)))
    # agrengado el nombre de la funcion que procesa la data de partidos
    for metaPartidos in dicMetadataPartidos['metadata']:
        # recorriendo la lista de HTML extraido
        # print('URL\t{}\nRawPartido\n{}'.format(metaPartidos[0], metaPartidos[1]))
        insertMdPartido = objDB.insert_RawPartidos(metaPartidos[0], metaPartidos[1])
        # print('Raw partidos (tipo):\t{}'.format(type(insertMdPartido)))
        if insertMdPartido is None:
            print('No se inserto la metadadata (URL) de partidos\t{}'.format(metaPartidos[1]))
        else:
            # print('Se inserto la metadadata de partidos')
            pass
        
        # ProcessPartidos
        dictMtPartido = {}
        rawNoPross_Partido = objDB.rawNoProcessPartidos()
        # dictMtPartido = dict((x, y) for x, y in rawNoPross_Partido)
        # print('Metadatos no procesados\n', metadata_Estadisticas)
        dictMtPartido['metadata'] = rawNoPross_Partido
        dictMtPartido['method_name'] = 'processDataPartidos'
        partido = ProcessPartidos()
        dataPartido = partido.run_process(dictMtPartido)
        # Orden de lista que regresa ((equipoA, golA, equipoB, golB, url_partidos, anio))
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
                resgHtmlPartidos = objDB.actualizar_RawPartido(sitio = metaPartidos[0], raw=metaPartidos[1])
                if resgHtmlPartidos is None:
                    pass
                else:
                    print('Registro partido actualizado:\t{}#\t::\tSitio:\t{}'.format(resgHtmlPartidos[0], url))
            # eliminando objeto creado
        del partido

objArchivos = generar_CSV()
estadisticaGeneral = objDB.estadisticasTotales()
estadisticaLocal = objDB.estadisticasLocales()
estadisticaVisitante = objDB.estadisticasVisitantes()
encuentros = objDB.encuentros()
print('CSV Tipo\t:{}'.format(type(estadisticaGeneral)))
print('CSV Tipo\t:{}'.format(type(estadisticaLocal)))
print('CSV Tipo\t:{}'.format(type(estadisticaVisitante)))
print('CSV Tipo\t:{}'.format(type(encuentros)))
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
