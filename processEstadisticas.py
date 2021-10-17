# Para BeautifulSoup
from bs4 import BeautifulSoup as BS, element #analizar documentos html
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessEstadisticas():
    list_error = []
    total_errors = 0
    # Recibe HTML (nombre de la funcion method_name_repositories)
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
            self.log_error(where='requesting', html=html, exc=str(e))
    
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
        # print('\nData Estadistica\n\n', table_data)
        return table_data
        
    def estadisticas(self, metaDataDict={}):
        '''
        Algoritmo para la estraccion de data de estadisticas.
        Extraccion de estadisticas por filas (recordar el orden al momento # P	+/-	M	W	D	L	F	A)

            Parametros
            ----------
                html (longtext): Se refiere a la metadata no procesado
            
            Returns:
                dict: Metadata procesada de la estadista (revisar el orden)
        '''

        # en SOUP esta TODA la pagina
        dominio = 'https://footballdatabase.com/'

        # print('PtsLocal\n\n\n', PtsLocal)
        # Metada de estadisticas
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
        
        tableTotal = div_acum.find('div', {'id': 'total'}).find('div', attrs={'class': 'table-responsive'}).find('table')
        tableLocal = div_local.find('div', {'id': 'home'}).find('div', attrs={'class': 'table-responsive'}).find('table')
        tableVisitante = div_visit.find('div', {'id': 'away'}).find('div', attrs={'class': 'table-responsive'}).find('table')
        # print('\nDIV Estadisticas\n\n', tableTotal)
        table_data = {}
        table_data['Acumulado'] = self.getDataTable(tableTotal)
        table_data['Local'] = self.getDataTable(tableLocal)
        table_data['Visistante'] = self.getDataTable(tableVisitante)
        return table_data
    
    def run_process(self, parameters={}):
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