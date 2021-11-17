# Para BeautifulSoup
from bs4 import BeautifulSoup as BS #analizar documentos html
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessMetaData():
    """Clase para procesar equipos
    """
    # Recibe HTML (consultdo de la BD para procesar los datos)
    list_error = []
    total_errors = 0

    # ----------------------- GENERAL MÉTHODS -----------------------
    def log_error(self, where, funtion, exc):
        self.total_errors=+1
        self.list_error.append(
            {
                'where': where,
                'when': funtion,
                'exception': exc,
                'total error': self.total_errors
            }
        )
        return self.list_error
    
    def soup_html(self, html):
        """Recibe el HTML del cual se va a extraer la data

            Args:
                html (str): HTML guardado para ser analizado

            Returns:
                dict: {'Where':aaa, when:bbb, error:?b}
        """
        try:
            soup = BS(html,'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='procesamiento', funtion='soup_html Equipos', exc=str(e))
    
    def processDataEquipos(self, metaDataDict={}):
        '''Algoritmo para el repositorio de OER Commons, retorna un diccionario con la metadata del recurso.

            Parametros
            ----------
                html (longtext): Se refiere al recurso no procesado
            
            Returns:
                dict: Metadata procesada del recurso
        '''

        # dominio del sitio
        dominio = 'https://footballdatabase.com'
        # Lista de equipos
        EqTotal = list()
        EqLocal = list()
        EqVisitante = list()
        # Metadata de los resultados
        # print('Keys %s' % metaDataDict.keys())
        if 'Acumulado' in metaDataDict:
            # Acumulado
            div_acum = metaDataDict['Acumulado']
            # usando BS4
            div_acum = self.soup_html(div_acum)
            # print('Pts Acumulado\n\n\n', div_acum)
            # Metada de equipos
            equiposT = div_acum.findAll('a', {'class' : 'sm_logo-name'})
            # print('Total')
            for elemento in equiposT:
                # print('elemento\t', elemento)
                titulo = elemento.get_text()
                link = dominio + elemento.get('href')
                img = elemento['style']
                img = dominio+ img.replace('background-image: url(','').replace(');','').replace('20px', '80px')
                # print('elemento:\t{}\tTipo:\t{}\ta:\t{}'.format(elemento, type(elemento), img))
                info = {'nombre': titulo, 'link': link, 'img': img}
                EqTotal.append(info)
                # print(titulo, '\t', link)
        if 'Local' in metaDataDict:
            # Local
            div_local = metaDataDict['Local']
            div_local = self.soup_html(div_local)
            equiposL = div_local.findAll('a', {'class' : 'sm_logo-name'})
            # print('Local')
            for elemento in equiposL:
                titulo = elemento.get_text()
                link = dominio + elemento.get('href')
                img = elemento['style']
                img = dominio+ img.replace('background-image: url(','').replace(');','').replace('20px', '80px')
                info = {'nombre': titulo, 'link': link, 'img': img}
                EqLocal.append(info)
                # print(titulo, '\t', link)
        if 'Visitante' in metaDataDict:
            # Visitante
            div_visit = metaDataDict['Visitante']
            div_visit = self.soup_html(div_visit)
            equiposV = div_visit.findAll('a', {'class' : 'sm_logo-name'})
            # print('Visitante')
            for elemento in equiposV:
                titulo = elemento.get_text()
                link = dominio + elemento.get('href')
                img = elemento['style']
                img = dominio+ img.replace('background-image: url(','').replace(');','').replace('20px', '80px')
                info = {'nombre': titulo, 'link': link, 'img': img}
                EqVisitante.append(info)
                # print(titulo, '\t', link) 
        # Diccionario con las estadisticas
        dataProcess = {
            'Acumulado': EqTotal,
            'Local': EqLocal,
            'Visitante': EqVisitante
        }
        return dataProcess
    
    # Ejecutar algoritmo de extracción
    def run_ProcessEquipos(self, parameters={}):
        """Extraccion de clubs/equipos deportivos

            Args:
                parameters (dict, optional, method_name): Diccionario con la opciones: Acumulado/Local/Visitante y el *metodo* a ejecutar. Defaults to {}.

            Returns:
                dict: Lista con los equipos encontrados
        """
        download_obj = dict()
        # se asigna o recupera los datos enviados
        download_obj = parameters
        # se agrega el nombre de la funcion
        algorith_name = download_obj.get('method_name')
        print('Process Equipos funcion a ejecutar:\t', algorith_name)
        # print('Process Equipos keys:\t', download_obj.keys())
        metodo = getattr(self, algorith_name, None)
        # print('Datos enviados a procesar\t', download_obj.keys())
        
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")