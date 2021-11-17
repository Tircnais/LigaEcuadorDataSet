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

class FuncionesComunes():
    """Clase que agrupa las funciones que necesitan ser actualizadas en tiempo de ejecucion
    """
    def extractMtdEstadisticas(self):
        objExtraction = Extraction()
        objDB = Database()
        diccionario = {'method_name': 'footballdatabase'}
        anio = datetime.now().year

        while anio > 2009:
            diccionario['url'] = f"https://footballdatabase.com/league-scores-tables/ecuador-serie-a-{anio}"
            url = diccionario['url']
            # print('URL a consultar:\t{}'.format(url))
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
            valido = objDB.insert_RawEstadisticas(url, raw_html, estad_total, estad_local, estad_visitante, str(anio), fecha_process, errores, extract, fecha_process, errors_process, process)
            if valido is None:
                print('Error al insertar RawEstadistica\t\tSitio:\t{}\t\tErrors:\t{}'.format(url, errores))
            else:
                # print('Registro de RAW Estadistica exitoso')
                pass
        return ''
    
    def ListaRawNoProcessEstadisticas(self):
        objDB = Database()
        rawNoPross_Estadisticas = objDB.rawNoProcessEstadisticas()
        del objDB
        return rawNoPross_Estadisticas
    
    def ListaRawNoProcessPartidos(self):
        objDB = Database()
        rawNoPross_Partido = objDB.rawNoProcessPartidos()
        del objDB
        dictMtPartido = {}
        dictMtPartido['metadata'] = rawNoPross_Partido
        dictMtPartido['method_name'] = 'processDataPartidos'
        partido = ProcessPartidos()
        dataPartido = partido.run_process(dictMtPartido)
        del partido
        return dataPartido
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")
    