# Para BeautifulSoup
from bs4 import BeautifulSoup as BS #analizar documentos html

# Algoritmos de procesamiento de cada repositorio
class ProcessPartidos():
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
            self.log_error(where='buscando las estadisticas equipo (nombre)', funtion='soup_html process Partidos', exc=str(e))
    
    def processDataPartidos(self, html):
        """Algoritmo para extraer los resultados de los partidos finalizados.

            Parametros
            ----------
                html (longtext): Se refiere al recurso no procesado
            
            Returns:
                dict: Metadata procesada del recurso
        """
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
            listaPaginasHtml = element[1].split(', ')
            anio = url_partidos.split('/')[-2].split('-')[-1]
            # print('URL c/pagina (resultados):\t{}. Anio:\t{}\n'.format(url_partidos, anio))
            # print('List_Pag_HTML\n%s\n\n'%listaPaginasHtml)
            # print('EquipoA\tResultados\tEquipoB\tAnio')
            for pagina in listaPaginasHtml:
                # Recorriendo cada pagina
                # print('Pagina_HTML\n%s\n\n'%pagina)
                # Recorriendo los partidos de la pagina
                try:
                    dataPartido = self.soup_html(pagina)
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
                    golA = resultado[0]
                    golB = resultado[1]
                    # print('{}\t{}-{}\t{}\t{}'.format(equipoA, golA, golB, equipoB, url_partidos))
                    encuentro.append((equipoA, golA, equipoB, golB, url_partidos, anio))
                    # agrega los partidos de esa pag
                except Exception as e:
                    self.log_error(where='scrapyng HTML', funtion='processDataPartidos. URL: %s' %url_partidos, exc=str(e))
        resultadosPartidos['data'] = encuentro
        resultadosPartidos['errores_procesamiento'] = self.list_error
        resultadosPartidos['process'] = 1 if len(self.list_error) == 0 else 0
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