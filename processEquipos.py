# Para BeautifulSoup
from bs4 import BeautifulSoup as BS #analizar documentos html
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessMetaData():
    # Recibe HTML (consultdo de la BD para procesar los datos)
    list_error = []
    total_errors = 0

    # ----------------------- GENERAL MÉTHODS -----------------------
    def log_error(self, where, html, exc, total_error):
        self.total_errors=+1
        self.list_error.append(
            {
                'where': where,
                'html': html,
                'exception': exc,
                'total error': total_error
            }
        )
        return self.list_error
    
    def soup_html(self, html):
        try:
            soup = BS(html,'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='procesamiento', html=html, exc=str(e))
    
    def footballdatabase(self, metaDataDict={}):
        '''
        Algoritmo para el repositorio de OER Commons, retorna un diccionario con la metadata del recurso.

            Parametros
            ----------
                html (longtext): Se refiere al recurso no procesado
            
            Returns:
                dict: Metadata procesada del recurso
        '''

        # dominio del sitio
        dominio = 'https://footballdatabase.com/'
        # Metadata de los resultados
        # Acumulado
        div_acum = metaDataDict['Acumulado']
        # Local
        div_local = metaDataDict['Local']
        # Visitante
        div_visit = metaDataDict['Visitante']
        # usando BS4
        div_acum = self.soup_html(div_acum)
        div_local = self.soup_html(div_local)
        div_visit = self.soup_html(div_visit)
        # print('PtsLocal\n\n\n', PtsLocal)
        # Metada de equipos
        equiposT = div_acum.findAll('a', 'sm_logo-name')
        equiposL = div_local.findAll('a', 'sm_logo-name')
        equiposV = div_visit.findAll('a', 'sm_logo-name')
        # Lista de equipos
        EqTotal = list()
        EqLocal = list()
        EqVisitante = list()
        # print('Total')
        for elemento in equiposT:
            titulo = elemento.get_text()
            link = dominio + elemento.get('href')
            info = {'nombre': titulo, 'link': link}
            EqTotal.append(info)
            # print(titulo, '\t', link)
        # print('Local')
        for elemento in equiposL:
            titulo = elemento.get_text()
            link = dominio + elemento.get('href')
            info = {'nombre': titulo, 'link': link}
            EqLocal.append(info)
            # print(titulo, '\t', link)
        # print('Visitante')
        for elemento in equiposV:
            titulo = elemento.get_text()
            link = dominio + elemento.get('href')
            info = {'nombre': titulo, 'link': link}
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
        download_obj = dict()
        # se asigna o recupera los datos enviados
        download_obj = parameters
        # se agrega el nombre de la funcion
        algorith_name = download_obj.get('method_name')
        print('Algoritmo procesamiento\t', algorith_name)
        metodo = getattr(self, algorith_name, None)
        # print('Datos enviados a procesar\t', download_obj.keys())
        
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")