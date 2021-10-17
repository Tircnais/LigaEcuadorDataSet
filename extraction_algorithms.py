# Celery
# from celery import shared_task, current_task

# Webscraping libraries
from bs4 import BeautifulSoup  as BS
# para consultar el sitio
import requests

import json
import datetime


class Extraction():
    list_error = []
    total_errors = 0

    # ----------------------- GENERAL MÉTHODS -----------------------
    def log_error(self, where, url, exc):
        self.total_errors=+1
        self.list_error.append(
            {
                'where': where,
                'url': url,
                'exception': exc,
                'total error': self.total_errors
            }
        )

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
            print(e)
            self.log_error(where='scrapyng', url=_url, exc=str(e))

    # Ejecutar algoritmo de extracción
    def run_extraction(self, parameters={}):
        download_obj = dict()
        download_obj["method_name"] = parameters['method_name']
        download_obj["url"] = parameters['url']
        algorith_name = download_obj.get('method_name')
        print('Algoritmo extracción\t', algorith_name)
        metodo = getattr(self, algorith_name, None)
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta
    
    # Eliminar Objetos
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")