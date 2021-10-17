# Para BeautifulSoup
from bs4 import BeautifulSoup as BS #analizar documentos html
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessPartidos():
    list_error = []
    total_errors = 0
    # Recibe HTML (nombre de la funcion method_name_repositories)
    # ----------------------- GENERAL MÉTHODS -----------------------
    def log_error(self, where, html, exc):
        self.list_error.append(
            {
                'where': where,
                'html': html,
                'exception': exc
            }
        )
    
    def soup_html(self, html):
        try:
            soup = BS(html,'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='requesting', html=html, exc=str(e))
    
    def partidos(self, html):
        '''
        Algoritmo para extraer los resultados de los partidos finalizados.

            Parametros
            ----------
                html (longtext): Se refiere al recurso no procesado
            
            Returns:
                dict: Metadata procesada del recurso
        '''

        # en SOUP esta TODA la pagina
        dominio = 'https://footballdatabase.com/'
        div_cnt = html
        soup = self.soup_html(html)

        metaData = dict()
        # print('PtsLocal\n\n\n', PtsLocal)
        # Metada de estadisticas
        equiposT = div_cnt.findAll('a', 'sm_logo-name')
        equiposL = div_cnt.findAll('a', 'sm_logo-name')
        equiposV = div_cnt.findAll('a', 'sm_logo-name')

        # Recorriendo los cursos de la pagina
        data = {}
        for table, heading in zip(gdp_table_data[1].find_all("table"), headings):
            # Get headers of table i.e., Rank, Country, GDP.
            t_headers = []
            for th in table.find_all("th"):
                # remove any newlines and extra spaces from left and right
                t_headers.append(th.text.replace('\n', ' ').strip())
            # Get all the rows of table
            table_data = []
            for tr in table.tbody.find_all("tr"): # find all tr's from table's tbody
                t_row = {}
                # Each table row is stored in the form of
                # t_row = {'Rank': '', 'Country/Territory': '', 'GDP(US$million)': ''}
                # find all td's(3) in tr and zip it with t_header
                for td, th in zip(tr.find_all("td"), t_headers):
                    t_row[th] = td.text.replace('\n', '').strip()
                table_data.append(t_row)
            # Put the data for the table with his heading.
            data[heading] = table_data
        print(data)
        return data
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")