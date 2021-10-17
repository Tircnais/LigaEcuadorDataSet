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

extraction = Extraction()
diccionario = {
    'url' : 'https://footballdatabase.com/league-scores-tables/ecuador-serie-a-2021',
    'method_name': 'footballdatabase'
}
# Dicionario con la metadata extraida (Acumulado, Local, Visitante)
"""
metadataEstadisticas = extraction.run_extraction(parameters=diccionario)
del extraction

# print('Estadisticas metadata\n\n\n\n', metadataEstadisticas, '\n\n\n\n')


# Abriendo la conexion a la BD
database = Database()

for item in metadataEstadisticas:
    sitio = diccionario['url']
    opcion = item
    raw = metadataEstadisticas[item]
    valido = database.insert_RawEstadisticas(sitio, raw, opcion)

    if valido >= 0:
        print('Registro de RAW Estadistica exitoso')
    else:
        print('Error al insertar\n\tOpcion:\t{}\n\tRawEst:\t{}'.format(opcion, raw))
    
    # print(raw)
"""
# Abriendo la conexion a la BD
database = Database()
# Traemos la lista de Raw No procesados
rawNoPross_Estadisticas = database.rawNoProcessEstadisticas()
# Cast de Tupla a Dict
a = dict()
metadata_Estadisticas = dict((x, y) for x, y in rawNoPross_Estadisticas)
# print('Metadatos no procesados\n', metadata_Estadisticas)
metadata_Estadisticas['method_name']= diccionario['method_name']
process = ProcessMetaData()
# print('keys\t', metadata_Estadisticas.keys())
processEstadisticas = process.run_ProcessEquipos(parameters=metadata_Estadisticas)
processEstadisticas
# print('Data Procesada\n', processEstadisticas)
del process

# database.select_equipo(1)
lista_equipos = database.select_all_equipo()
# print('Tipo\t', type(lista_equipos))
# for equipo in lista_equipos:
#     print(equipo)
errores = database.insert_Equipos(processEstadisticas)
if errores > 0:
    print('Error {} al insertar equipos', (errores))
else:
    print('Registro exitoso')


data_estadisticas = ProcessEstadisticas()
metadata_Estadisticas['method_name']= 'estadisticas'
# retorna un dict con Acumulado, Local, Visitante
estadisticas = data_estadisticas.run_process(metadata_Estadisticas)
# print('\nData Procesada Estadisticas\n\n',estadisticas)
# Insertando Data procesada
for key in estadisticas:
    print(key)
    # print('Como\tClub\tAnio\tPts\tGD\tPJ\tPG\tPE\tPP\tGA\tGC')
    for element in estadisticas[key]:
        # print('Estadistas y equipo\n{}'.format(element))
        equipo = element[1]
        anio = diccionario['url'].split('/')[-1].split('-')[-1]
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
        # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(key, equipo, anio, pts, gd, pj, pg, pe, pp, gf, gc))
        # lista de posiciones
        puntaje = database.insert_Estadisticas(opcion = key, equipo = equipo, anio = anio, pts = pts, pj = pj, pg = pg, pe = pe, pp = pp, gf = gf, gc = gc)

del estadisticas
database.close()
# ProcessPartidos

### Romper ejecucion
# import sys
# sys.exit()