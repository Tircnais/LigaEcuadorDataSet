# Para BeautifulSoup
from bs4 import BeautifulSoup as BS, element #analizar documentos html
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessEstadisticas():
    list_error = []
    total_errors = 0
    # Recibe HTML (nombre de la funcion method_name_repositories)
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
        try:
            soup = BS(html,'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='requesting', funtion='soup_html process Estad', exc=str(e))
    
    def getDataTable(self, tableTotal: str):
        """Tabla con las estadisticas de los partidos jugados, revisar el orden de las estadisticas.

        Args:
            tableTotal (str): Tabla con la metadata para procesar obtenida de la BD

        Returns:
            list: Con las estadisticas procesadas
        """
        # Get the table having the class wikitable
        gdp_table = tableTotal.thead.tr.find_all('th')
        # print('\nEncabezado\n{}\nTipo:\t{}\n\n'.format(gdp_table, type(gdp_table)))
        headings = []
        # Get all the headings of Lists
        for element in gdp_table:
            # remove any newlines and extra spaces from left and right
            td = element.text.replace('\n', ' ').strip()
            # print('\nOrden de datos Table Head TD:{}'.format(td))
            # P	+/-	M	W	D	L	F	A
            headings.append(td)
        # table tbody
        gdp_table_data = tableTotal.tbody.find_all("tr")
        # print ('TBody',gdp_table_data)
        # Get all the tables contained in "gdp_table"
        table_data = []
        for fila in gdp_table_data:
            # Get all the rows of table
            # print('\nFila\t', fila)
            t_row = []
            for td in fila.find_all("td"):
                # print('\nValores de la fila\t', td.text.replace('\n', '').strip())
                dato = td.text.replace('\n', '').strip()
                t_row.append(dato)
            table_data.append(t_row)
        print('Data Estadistica\n\n', table_data)
        return table_data
        
    def processDataEstadisticas(self, metaDataDict={}):
        '''
            Algoritmo para la estraccion de data de estadisticas.
            Extraccion de estadisticas por filas (recordar el orden al momento # P	+/-	M	W	D	L	F	A)

                Parametros
                ----------
                    html (longtext): Se refiere a la metadata no procesado
                
                Returns:
                    dict: Metadata procesada de la estadista (revisar el orden)
        '''
        # Metada de estadisticas
        # print('Llaves de la MTD extraidos\t{}'.format(metaDataDict.keys()))
        table_data = {}
        if 'Acumulado' in metaDataDict:
            # print('Key:\tAcumulado')
            # Acumulado
            div_acum = metaDataDict['Acumulado']
            # usando BS4
            div_acum = self.soup_html(div_acum)
            tableTotal = div_acum.find('div', {'id': 'total'}).find('div', attrs={'class': 'table-responsive'}).find('table')
            # print('\nDIV Estadisticas\n\n', tableTotal)
            table_data['Acumulado'] = self.getDataTable(tableTotal)
            if table_data['Acumulado'] is None:
                self.log_error(where='Procesando la MTD de estadisticas', funtion='estadisticas Opcion: Acumulado', exc='Elementos del HTML, no encontrados')
        if 'Local' in metaDataDict:
            # print('Key:\tLocal')
            # Local
            div_local = metaDataDict['Local']
            div_local = self.soup_html(div_local)
            tableLocal = div_local.find('div', {'id': 'home'}).find('div', attrs={'class': 'table-responsive'}).find('table')
            table_data['Local'] = self.getDataTable(tableLocal)
            if table_data['Local'] is None:
                self.log_error(where='Procesando la MTD de estadisticas', funtion='estadisticas Opcion: Local', exc='Elementos del HTML, no encontrados')
        if 'Visitante' in metaDataDict:
            # print('Key:\tVisitante')
            # Visitante
            div_visit = metaDataDict['Visitante']
            div_visit = self.soup_html(div_visit)
            tableVisitante = div_visit.find('div', {'id': 'away'}).find('div', attrs={'class': 'table-responsive'}).find('table')
            table_data['Visistante'] = self.getDataTable(tableVisitante)
            if table_data['Visistante'] is None:
                self.log_error(where='Procesando la MTD de estadisticas', funtion='estadisticas Opcion: Visistante', exc='Elementos del HTML, no encontrados')
        resultados = {}
        resultados['data'] = table_data
        resultados['errores_procesamiento'] = self.list_error
        resultados['process'] = 1 if len(self.list_error) == 0 else 0
        return resultados
    
    def run_process(self, parameters={}):
        download_obj = dict()
        # se asigna o recupera los datos enviados
        download_obj = parameters
        # se agrega el nombre de la funcion
        algorith_name = download_obj.get('method_name')
        print('Process Estadis funcion a ejecutar:\t', algorith_name)
        metodo = getattr(self, algorith_name, None)
        # print('Datos enviados a procesar\t', download_obj.keys())
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")