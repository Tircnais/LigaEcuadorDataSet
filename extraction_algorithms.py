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

    def soup_url(self, url):
        try:
            print('URL entrante:\t%s'%(url))
            web = requests.get(url)
            content = web.content
            soup = BS(content, 'html.parser')
            return soup
        except Exception as e:
            self.log_error(where='extraccion raw HTML: %s' %url, funtion='Funcion: soup_url', exc=str(e))

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
            contenido = soup.find('div', {'id': 'wrap'})
            div_cnt = contenido.find('div', {'class': 'mainfdb'})
            # print('Dato a guardar\t', div_cnt)
            PtsTotal = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'total'})
            PtsLocal = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'home'})
            PtsVisitante = div_cnt.find('div', {'class': 'tab-content'}).find('div', {'id': 'away'})
            extract = 0
            if type(contenido) is None and type(PtsTotal) is None and type(PtsLocal) is None and type(PtsVisitante) is None:
                self.log_error(where='scrapyng: %s' %_url, funtion='Funcion: footballdatabase', exc='No se encontro el elemento HTML')
                errores_extraccion = self.log_error
                extract = 1 if len(self.list_error) == 0 else 0
            else:
                errores_extraccion = None
                extract = 1 if len(self.list_error) == 0 else 0
            metadata_estadistica = {
                'raw_html': contenido,
                'Acumulado': PtsTotal,
                'Local': PtsLocal,
                'Visitante': PtsVisitante,
                'errors': errores_extraccion,
                'extact': extract
            }
            return metadata_estadistica
        except Exception as e:
            # print('exc\n',str(e))
            self.log_error(where='scrapyng: %s' %_url, funtion='Funcion: footballdatabase', exc=str(e))
            metadata_estadistica = {
                'raw_html': None,
                'Acumulado': None,
                'Local': None,
                'Visitante': None,
                'errors': self.list_error,
                'extact': 1 if len(self.list_error) == 0 else 0
            }
            return metadata_estadistica

    def extracMetadataPartidos(self, dicPartidos: dict):
        """Extraccion de metada de los partidos jugados

            Args:
                dicPartidos (dict): Diccionario con todo el html correspondiente a la URL.

            Returns:
                dict: Con la metadata de partidos jugados
        """
        _url = dicPartidos['url']
        # Es obtiene la URL enviada
        dominio = _url.split('/')
        dominio = dominio[0]+'//'+dominio[2]+'/'
        # variables para almacenar la metadata de partidos
        dicMetadataPartidos = {}
        try:
            # print('URL estadisticas\t', _url)
            # se consulta el HTML
            soup = self.soup_url(_url)
            # print('HTML Partidos\n\n', soup)
            primer_url_partidos = soup.find('div', {'id': 'wrap'}).find('div', {'class': 'mainfdb'}).findAll('div', {'class': 'row'})[1].find('div', {'class': 'col-md-5'}).find('a', {'class': 'clickme'}).get('href')
            primer_url_partidos = dominio + primer_url_partidos[1:len(primer_url_partidos)]
            # URL de los partidos correspondientes a esa estadistica (o anio)
            # print('primer_url_partidos:\t', primer_url_partidos)
            try:
                div_cnt = self.soup_url(primer_url_partidos)
                # print('MetadaData partidos\t', div_cnt)
                sig_Partidos = div_cnt.find('ul', {'class' : 'pagination-sm'}).findAll('li')
                lista_urls = []
                for sig_url in sig_Partidos:
                    # lista de partidos
                    sig_url = sig_url.find('a').get('href')
                    # extrayendo URL de cada pagina
                    sig_url = dominio + sig_url[1:len(sig_url)]
                    # print('Dominio: {}\tUrl: {}'.format(dominio, sig_url))
                    lista_urls.append(sig_url)
                lista_metadata =[]
                for url_partidos in lista_urls:
                    # print('URL partido: {}\tTipo: {}'.format(url_partidos, type(url_partidos)))
                    try:
                        div_cnt = self.soup_url(url_partidos)
                        div_cnt = div_cnt.find('div', {'id': 'wrap'}).find('div', {'class': 'mainfdb'}).findAll('div', {'class': 'row'})[1].find('div', {'class': 'col-md-8'})
                        # tabla con los resultados de partidos finalizados
                        metadataPartidos = div_cnt.findAll('div', {'class': 'club-gamelist-match'})
                        # print('\nMetadataPartidos\n\n', metadataPartidos)
                        anio = url_partidos.split('/')[-2].split('-')[-1]
                        # print('Anio partidos: {}'.format(anio))
                        lista_metadata.append((url_partidos, metadataPartidos, anio))
                        # agregando la metada de fechas (partidos) a la lista
                    except Exception as e:
                        self.log_error(where='error buscando elemento de la metada en: %s (URL)' %url_partidos, funtion='Funcion: extracMetadataPartidos', exc=str(e))
                # print('Cant partidos consultados\t{}'.format(len(lista_metadata)))
                dicMetadataPartidos['metadata'] = lista_metadata
                dicMetadataPartidos['errores_extraccion'] = self.list_error
                dicMetadataPartidos['extract'] = 1 if len(self.list_error) == 0 else 0
                return dicMetadataPartidos
            except Exception as e:
                self.log_error(where='error consultando la pag partidos %s' %primer_url_partidos, funtion='Funcion: extracMetadataPartidos', exc=str(e))
                dicMetadataPartidos['metadata'] = None
                dicMetadataPartidos['errores_extraccion'] = self.list_error
                dicMetadataPartidos['extract'] = 1 if len(self.list_error) == 0 else 0
            return dicMetadataPartidos
        except Exception as e:
            self.log_error(where='scrapyng HTML %s' %_url, funtion='Funcion: extracMetadataPartidos', exc=str(e))
            dicMetadataPartidos['metadata'] = None
            dicMetadataPartidos['errores_extraccion'] = self.list_error
            dicMetadataPartidos['extract'] = 1 if len(self.list_error) == 0 else 0
        return dicMetadataPartidos

    # Ejecutar algoritmo de extracción
    def run_extraction(self, parameters={}):
        download_obj = dict()
        download_obj["method_name"] = parameters['method_name']
        download_obj["url"] = parameters['url']
        algorith_name = download_obj.get('method_name')
        # print('ExtracciónAlgoritmos funcion a ejecutar:\t', algorith_name)
        # print('URL consultar:\t%s'%(download_obj["url"]))
        metodo = getattr(self, algorith_name, None)
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta

    # Eliminar Objetos
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")
