# Celery
# from celery import shared_task, current_task

# Webscraping libraries
from bs4 import BeautifulSoup as BS
# para peticiones HTTP (para consumir un API, extraer información de una página o enviar el contenido de un formulario)
import requests

class Extraction():
    list_error = []
    total_errors = 0

    # ----------------------- GENERAL MÉTHODS -----------------------
    def log_error(self, where, url, exc, total_error):
        self.total_errors=+1
        self.list_error.append(
            {
                'where': where,
                'url': url,
                'exception': exc,
                'total error': total_error
            }
        )
        return self.list_error

    def soup_url(self, url):
        try:
            web = requests.get(url)
            content = web.content
            soup = BS(content, 'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='extraccion', url=url, exc=str(e))

    # ----------------------- EXTRACTION ALGORITMHS -----------------------
    def footballdatabase(self, download):
        """Extraccion de metada para estadisticas

        Args:
            download (dict): Diccionario con todo el html correspondiente a la URL.

        Returns:
            dict: Con la metadata de Pts: Acumulado, Local, Visitante
        """
        _url = ''

        try:
            # Es obtiene la URL enviada
            _url = download['url']
            # se consulta el HTML
            soup = self.soup_url(_url)
            # se busca el contenido
            div_cnt = soup.find('div', {'id': 'wrap'}).find('div', {'class': 'mainfdb'})
            # print('Dato a guardar\t', div_cnt)
            PtsTotal = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'total'})
            PtsLocal = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'home'})
            PtsVisitante = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'away'})
            estadistica = {
                'Acumulado': PtsTotal,
                'Local': PtsLocal,
                'Visitante': PtsVisitante
            }
            return estadistica
        except Exception as e:
            print('exc\n',str(e))
            self.total_errors += 1
            self.log_error(where='scrapyng', url=_url, exc=str(e), total_error=self.total_errors)

    def extracMetadataPartidos(self, dicPartidos: dict):
        """Extraccion de metada de los partidos jugados

        Args:
            dicPartidos (dict): Diccionario con todo el html correspondiente a la URL.

        Returns:
            dict: Con la metadata de partidos jugados
        """
        # _url = ''
        dominio = 'https://footballdatabase.com/'
        try:
            _url = dicPartidos['url']
            # Es obtiene la URL enviada
            # print('URL estadisticas\t', _url)
            # se consulta el HTML
            soup = self.soup_url(_url)
            # print('HTML Partidos\n\n', soup)
            primer_url_partidos = soup.find('div', {'id': 'wrap'}).find('div', {'class': 'mainfdb'}).findAll('div', {'class': 'row'})[1].find('div', {'class': 'col-md-5'}).find('a', {'class': 'clickme'}).get('href')
            ('href')
            primer_url_partidos = dominio + primer_url_partidos[1:len(primer_url_partidos)]
            # URL de los partidos correspondientes a esa estadistica (o anio)
            # print('primer_url_partidos:\t', primer_url_partidos)
            try:
                div_cnt = self.soup_url(primer_url_partidos)
                # print('MetadaData partidos\t', div_cnt)
                sig_Partidos = div_cnt.find('ul', {'class' : 'pagination-sm'}).findAll('li')
                # variables para almacenar la metadata de partidos
                dicMetadataPartidos = {}
                lista_metadata =[]
                # print('Lista partidos\t{}'.format(sig_Partidos))
                for url_partidos in sig_Partidos:
                    # lista de partidos
                    url_partidos = url_partidos.find('a').get('href')
                    # extrayendo URL de cada pagina
                    url_partidos = dominio + url_partidos[1:len(url_partidos)]
                    # print('URL siguiente:\t', url_partidos)
                    try:
                        div_cnt = self.soup_url(url_partidos)
                        div_cnt = div_cnt.find('div', {'id': 'wrap'}).find('div', {'class': 'mainfdb'}).findAll('div', {'class': 'row'})[1].find('div', {'class': 'col-md-8'})
                        # tabla con los resultados de partidos finalizados
                        metadataPartidos = div_cnt.findAll('div', {'class': 'club-gamelist-match'})
                        # print('\nMetadataPartidos\n\n', metadataPartidos)
                        lista_metadata.append((url_partidos, metadataPartidos))
                        # agregando la metada de fechas (partidos) a la lista
                    except Exception as e:
                        self.total_errors += 1
                        self.log_error(where='error extrayendo la lista de URL de partidos', url=_url, exc=str(e), total_error = self.total_errors)
                # print('Cant partidos consultados\t{}'.format(len(lista_metadata)))
                dicMetadataPartidos['metadata'] = lista_metadata
                return dicMetadataPartidos
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='error consulta pag del Partido', url=_url, exc=str(e), total_error = self.total_errors)
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='scrapyng HTML', url=_url, exc=str(e), total_error = self.total_errors)

    # Ejecutar algoritmo de extracción
    def run_extraction(self, parameters={}):
        download_obj = dict()
        download_obj["method_name"] = parameters['method_name']
        download_obj["url"] = parameters['url']
        algorith_name = download_obj.get('method_name')
        print('ExtracciónAlgoritmos funcion a ejecutar:\t', algorith_name)
        metodo = getattr(self, algorith_name, None)
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta

    # Eliminar Objetos
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")
