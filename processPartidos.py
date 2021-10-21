# Para BeautifulSoup
from bs4 import BeautifulSoup as BS #analizar documentos html
# para peticiones HTTP (para consumir un API, extraer información de una página o enviar el contenido de un formulario)
import requests

# Algoritmos de procesamiento de cada repositorio
class ProcessPartidos():
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
            self.total_errors += 1
            self.log_error(where='buscando las estadisticas equipo (nombre)', html=html, exc=str(e), total_error = self.total_errors)
    
    def processDataPartidos(self, html):
        '''
        Algoritmo para extraer los resultados de los partidos finalizados.

            Parametros
            ----------
                html (longtext): Se refiere al recurso no procesado
            
            Returns:
                dict: Metadata procesada del recurso
        '''
        listaHTML = html['metadata']
        # print('Llaves del dic de MTD partidos:\t', html.keys())
        # print('ProPat Tipo (recive):\t', type(listaHTML))
        resultadosPartidos = {}
        encuentro = []
        for element in listaHTML:
            # print('Elemento Tipo (recive):\t', type(element))
            # lista con el HTML de todos los partidos de ese anio
            url_partidos = element[0]
            # print('\nTipo del elemento:\t{}'.format(type(listaInterna)))
            # la posicion 0 es la MTD en si
            htmlPartidos = element[1]
            anio = url_partidos.split('/')[-2].split('-')[-1]
            # print('URL c/pagina (resultados):\t{}. Anio:\t{}\n'.format(url_partidos, anio))
            # print('EquipoA\tResultados\tEquipoB\tAnio')
            
            # Recorriendo cada pagina
            # Recorriendo los partidos de la pagina
            try:
                dataPartido = self.soup_html(htmlPartidos)
                # enviamos el HTML para extraer la data
                equipos = dataPartido.findAll('div', {'class':'club-gamelist-match-clubs'})
                # print('\nEquipos\t{}\n'.format(type(equipos)))
                resultado = dataPartido.find('div', {'class':'club-gamelist-match-score'}).text.replace('\n', '').replace(' ', '').split('-')
                # goles de ambos equipos
                # print('\nResultado\t{}\n'.format(resultado))
                equipoA = equipos[0].find('a').text
                # izq de la pantalla
                equipoB = equipos[1].find('a').text
                # der de la pantalla
                # print('Equipos\n{}:::{}'.format(equipoA, equipoB))
                golA = resultado[0]
                golB = resultado[1]
                # print('{}:::{}:::{}'.format(golA, golB, url_partidos))
                print('{}\t{}-{}\t{}\t{}'.format(equipoA, golA, golB, equipoB, url_partidos))
                encuentro.append((equipoA, golA, equipoB, golB, url_partidos, anio))
                # agrega los partidos de esa pag
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='scrapyng HTML', html=url_partidos, exc=str(e), total_error = self.total_errors)
        resultadosPartidos['data'] = encuentro
        return resultadosPartidos
    
    def run_process(self, parameters={}):
        download_obj = dict()
        # se asigna o recupera los datos enviados
        download_obj = parameters
        # se agrega el nombre de la funcion
        algorith_name = download_obj.get('method_name')
        print('ProcessPartidos funcion a ejecutar:\t', algorith_name)
        metodo = getattr(self, algorith_name, None)
        # print('Datos enviados a procesar\t', download_obj.keys())
        if metodo is not None:
            respuesta = metodo(download_obj)  # ejecutandose el método.
            return respuesta
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:del obj (desde el lugar donde se la llama)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")