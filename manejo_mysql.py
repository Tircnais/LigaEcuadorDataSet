import pymysql
# lib para establecer la conexion a la BD
from datetime import datetime
# lib para obtener la fecha actual (anio)
import json
# para convertir la lista de errores a JSON para poder guardar

class Database:
    # Variable para encontrar errores
    list_error = []
    total_errors = 0
    ############### CONFIGURAR ESTO ###################
    def __init__(self):
        """Abre conexion con la base de datos
        """
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='ligaecuador'
        )
        # prepare a cursor object using cursor() method
        self.cursor = self.connection.cursor()
        print('Conexion exitosa')

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

    def search_equipo(self, nombre: str):
        """Busca el ID del equipo para saber si existe

            Args:
                nombre (varchar): Nombre del equipo deportivo

            Returns:
                int: ID del equipo
        """
        sql = 'Select idEq from equipos Where nombre = %s'
        # print('Consulta\t',sql)
        try:
            self.cursor.execute(sql, (nombre, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result equipo\t', existe[0])
            return existe
        except Exception as e:
            self.log_error(where='buscando el equipo: %s (idEq)' %nombre, funtion='Funcion: search_equipo', exc=str(e))
    
    def search_Estadistica(self, equipo: str, opcion: str):
        """Busca las estadisticas del equipo para conocer las mismas. Considerar el anio para el analisis

            Args:
                equipo (varchar): Nombre del equipo deportivo
                opcion (varchar): Hace referencia a: Acumulado, Local y Visitante

            Returns:
                int: ID del equipo
        """
        id_Eq = self.search_equipo(equipo)
        sql = ''
        if id_Eq is None:
            # print('No hay estadisticas registradas de este equipo')
            return None
        else:
            # Busca sus estadisticas
            if opcion == 'Acumulado':
                sql = "Select * from posicionestotal Where fkEq = %s"
            elif opcion == 'Local':
                sql = "Select * from posicioneslocal Where fkEq = %s"
            else:
                sql = "Select * from posicionesvisitante Where fkEq = %s"
                
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (id_Eq[0], ))
                # por retornar mas de un registro fetchall
                existe = self.cursor.fetchall()
                # print('Result\t', existe)
                return existe
            except Exception as e:
                self.log_error(where='buscando las estadisticas equipo (nombre)', funtion='Funcion: search_Estadistica', exc=str(e))
                
    
    def search_EstadisticaAnio(self, equipo: str, opcion: str, anio: str):
        """Busca las estadisticas del equipo usando el anio para conocer las mismas

            Args:
                equipo (varchar): Nombre del equipo deportivo
                opcion (varchar): Hace referencia a: Acumulado, Local y Visitante
                anio (varchar): Anio de la estadistica, con el fin de filtrar (o actualizar)

            Returns:
                int: ID del equipo
        """
        id_Eq = self.search_equipo(equipo)
        if id_Eq is None:
            # print('Aun no se ha registrado este equipo')
            id_Eq = self.insert_Equipo(equipo, '')
            # print('No hay estadisticas registradas de este equipo')
            return self.search_EstadisticaAnio(equipo, opcion, anio)
        else:
            # Busca sus estadisticas
            sql = ''
            if opcion == 'Acumulado':
                sql = "Select * from posicionestotal Where fkEq = %s and year = %s"
            elif opcion == 'Local':
                sql = "Select * from posicioneslocal Where fkEq = %s and year = %s"
            else:
                sql = "Select * from posicionesvisitante Where fkEq = %s and year = %s"
                
            # print('search EstadisticaAnio ID equipo:\t',id_Eq[0])
            try:
                self.cursor.execute(sql, (id_Eq[0], anio, ))
                # por retornar mas de un registro fetchall
                existe = self.cursor.fetchone()
                # print('Result\t', existe)
                return existe
            except Exception as e:
                self.log_error(where='buscando las estadisticas equipo (%s y %s)' %(equipo, anio), funtion='Funcion: search_EstadisticaAnio', exc=str(e))
    
    def select_all_equipo(self):
        sql = 'Select * from clubs'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.log_error(where='buscando todos los equipos', funtion='Funcion: select_all_equipo', exc=str(e))
    
    def detalle_equipo(self, nombre:str):
        """Trae todas las columnas de la tabla Equipos

        Args:
            nombre (str): Nombre del equipo que busca

        Returns:
            array: Retorna un array con los campos solicitados
        """
        sql = 'Select * from equipos where nombre = %s'
        try:
            self.cursor.execute(sql, (nombre, ))
            # por retornar un registro fetchone
            equipos = self.cursor.fetchone()
            return equipos
        except Exception as e:
            self.log_error(where='buscando el detalle del equipo' %nombre, funtion='Funcion: detalle_equipo', exc=str(e))
    
    def search_IdRawEstadisticas(self, rawEst: str):
        """Busca el HTML usando el enlace del mismo

            Args:
                rawEst (str): Enlace del sito de donde se extrae la metadata

            Returns:
                int: ID del enlace o RAW a extraer
        """
        sql = 'Select id from metadataestadisticas Where raw_html = %s'
        # print('Consulta\t',sql)
        try:
            self.cursor.execute(sql, (rawEst, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.log_error(where='buscando el  ID de rawEst', funtion='Funcion: search_IdRawEstadisticas', exc=str(e))            

    def search_RawEstadisticas(self, sitio: str):
        """Busca el HTML usando el enlace del mismo

            Args:
                sitio (str): URL del HTML que esta buscando

            Returns:
                resultList: registro con el detalle del mismo
        """
        sql = 'Select id from metadataestadisticas Where sitio = %s'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql, (sitio, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.log_error(where='buscando el  ID de: %s' %sitio, funtion='Funcion: search_RawEstadisticas', exc=str(e))
    
    def search_IdRawPartidos(self, rawPartidos: str):
        """Busca el HTML usando el raw extraido

            Args:
                rawPartidos (str): Enlace del sito de donde se extrae la metadata

            Returns:
                int: ID del enlace o RAW a extraer
        """
        sql = 'SELECT id FROM metadatapartidos WHERE raw_html = %s'
        # print('Consulta\t',sql)
        try:
            self.cursor.execute(sql, (rawPartidos, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            # print('Error al buscar RAW Partidos')
            self.log_error(where='buscando el raw de Partidos (rawPartidos)', funtion='Funcion: search_IdRawPartidos', exc=str(e))
    
    def search_Partidos(self, eqA: str, golA: str, golB: str, eqB: str, year: str):
        # busca el ID cada equipo para registrar la FK del registro
        fkA = self.search_equipo(eqA)
        fkB = self.search_equipo(eqB)
        if fkA is None or fkB is None:
            # sino hay el elemento lo registra
            if fkA is None:
                fkA = self.insert_Equipo(eqA, '')
            else:
                fkB = self.insert_Equipo(eqB, '')
            # se llama a si misma ahora si registrar el resultado
            return self.search_Partidos(eqA=eqA, golA=golA, golB=golB, eqB=eqB, year=year)
        else:
            sql = 'SELECT * FROM partidos WHERE eqA = %s AND golA = %s AND golB = %s AND eqB = %s AND fecha= %s'
            # print('Buscando partido\t{}\t{}-{}\t{}\t{}'.format(fkA[0], golA, golB, fkB[0], year))
            try:
                self.cursor.execute(sql, (fkA[0], golA, golB, fkB[0], year, ))
                existe = self.cursor.fetchone()
                # por retornar un registro fetchone
                # print('Result Busq Partido\t', existe)
                return existe
            except Exception as e:
                self.log_error(where='buscando detalle del partido (%s, %s-%s, %s: %s)' %(fkA[0], golA, golB, fkB[0], year), funtion='Funcion: search_Partidos', exc=str(e))
    
    def rawNoProcessEstadisticas(self):
        """Trae la lista de HTML no procesados

            Returns:
                list: RAW no procesados
        """
        sql = 'Select raw_html, estad_total, estad_local, estad_visitante from metadataestadisticas Where process = 0'
        # print('Consulta\t',sql)
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            existe = self.cursor.fetchall()
            # print('Result\t%s\nType\t%s' %(existe, type(existe)))
            return existe
        except Exception as e:
            self.log_error(where='Listando RawEstadisticas NO procesada', funtion='Funcion: rawNoProcessEstadisticas', exc=str(e))
    
    def rawNoProcessPartidos(self):
        """Trae la lista de HTML no procesados

            Returns:
                list: RAW no procesados
        """
        try:
            sql = 'Select sitio, raw_html from metadatapartidos Where process = 0'
            # print('Consulta\t',sql)
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            existe = self.cursor.fetchall()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.log_error(where='Listando RawPartidos NO procesada', funtion='Funcion: rawNoProcessPartidos', exc=str(e))

    def insert_RawEstadisticas(self, sitio: str, raw: str, estad_total: str, estad_local: str, estad_visitante: str, anio: str, errores_extraccion: str, extract: str, fecha_process:str, errores_process:str, process:str):
        """
            Registrando el HTML de las estadisticas

            Args:
                sitio (str): URL del sitio de donde se extrae el HTML
                raw (str): HTML a guardar
                estad_total (str): html correspondiente a Estad Total
                estad_local (str): html correspondiente a Estad Local
                estad_visitante (str): html correspondiente a Estad Visitante
                anio (str): Anio de la estadistica
                fecha_process (str) : Fecha en la que se proceso (INSERT NULL)
                errores_extraccion (str): Lista de errores recolectados
                extract (str): 1/0 para deerminar si el HTML fue extraido 

            Returns:
                result: Lista con el registro realizado
        """
        idRaw = self.search_IdRawEstadisticas(raw)
        now = datetime.now()
        if now.year == anio and idRaw is not None:
            # anio actual
            # en caso de ser el anio actual actualiza el registro
            return self.actualizar_RawEstadisticas(sitio, anio, fecha_process, errores_process, process)
        else:
            # sino es al anio actual registra la estadistica
            if idRaw is None:
                # sino hay el elemento lo registra
                sql = "INSERT INTO metadataestadisticas(sitio, raw_html, estad_total, estad_local, estad_visitante, anio, errores_extraccion, extract) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                # print('Consulta insert MTD Estadisticas\t',sql)
                # print('Consulta insert MTD Estadisticas.\tSitio:\t{}\tExtract:\t{}\tfecha_extract:\t{}'.format(sitio, extract, anio))
                try:
                    errores_extraccion = json.dumps(errores_extraccion)
                    self.cursor.execute(sql, (sitio, raw, estad_total, estad_local, estad_visitante, anio, errores_extraccion, extract, ))
                    # para que persistan los datos
                    self.connection.commit()
                    idRaw = self.search_IdRawEstadisticas(raw)
                    # regresa el ID del registro
                    return idRaw
                except Exception as e:
                    self.log_error(where='Error al insertar RAW Estadisticas (%s: %s)' %(sitio, errores_extraccion), funtion='Funcion: insert_RawEstadisticas', exc=str(e))
            else:
                # si hay el registro, regresa el ID
                return idRaw

    def insert_RawPartidos(self, sitio: str, raw: str, anio: str, errores_extraccion: str, extract: str):
        """Registrando la metadata de los partidos, incluyendo los errores encontrados, al extraer

            Args:
                sitio (str): URL del sito donde se buscan los partidos
                raw (str): html a extraer
                anio (str): anio de los partidos
                errores_extraccion (str): errores encontrados al extraer la metadata
                extract (str): 1/0 para determinar si se extrajo la metadata, en caso de extraer la metadata correctamente (1)
            Returns:
                [type]: [description]
        """
        idRaw = self.search_IdRawPartidos(raw)
        # print('URL rawPartido\t',sitio)
        now = datetime.now()
        if now.year == anio and idRaw is not None:
            # anio actual
            # en caso de ser el anio actual actualiza el registro
            return self.actualizar_RawPartidos(sitio, raw, anio, errores_extraccion, extract)
        else:
            if idRaw is None:
                # sino hay el elemento lo registra
                sql = "INSERT INTO metadatapartidos(sitio, raw_html, anio, errores_extraccion, extract) VALUES (%s, %s, %s, %s, %s)"
                # print('Consulta RawPart\t',sql)
                try:
                    errores_extraccion = json.dumps(errores_extraccion)
                    self.cursor.execute(sql, (sitio, raw, anio, errores_extraccion, extract, ))
                    # para que persistan los datos
                    self.connection.commit()
                    idRaw = self.search_IdRawPartidos(raw)
                    # regresa el ID del registro
                    return idRaw
                except Exception as e:
                    # print('Error al inser RAW Partidos')
                    self.log_error(where='Error al insertar RAW Partidos (%s)' %sitio, funtion='Funcion: insert_RawPartidos', exc=str(e))
            else:
                # si hay el registro, regresa el ID
                return idRaw
    
    def actualizar_RawPartidos(self, sitio: str, raw: str, anio: str, errores_extraccion: str, extract: str):
        """
            Registrando la metadata de los partidos, incluyendo los errores encontrados, al extraer

            Args:
                sitio (str): URL del sito donde se buscan los partidos
                raw (str): html a extraer
                anio (str): anio de los partidos
                errores_extraccion (str): errores encontrados al extraer la metadata
                extract (str): 1/0 para determinar si se extrajo la metadata, en caso de extraer la metadata correctamente (1)
            Returns:
                [type]: [description]
        """
        idRaw = self.search_IdRawPartidos(raw)
        # print('URL rawPartido\t',sitio)
        if idRaw is not None:
            # sino hay el elemento lo registra
            # UPDATE metadatapartidos SET sitio='[value-2]',raw_html='[value-3]',anio='[value-4]',fecha_extract='[value-5]',errores_extraccion='[value-6]',extract='[value-7]',fecha_process='[value-8]',errores_procesamiento='[value-9]',process='[value-10]' WHERE 1
            sql = "UPDATE SET metadatapartidos SET sitio = %s, raw_html = %s, anio = %s, errores_extraccion = %s, extract = %s WHERE raw_html = %s"
            # print('Consulta RawPart\t',sql)
            try:
                errores_extraccion = json.dumps(errores_extraccion)
                self.cursor.execute(sql, (sitio, raw, anio, errores_extraccion, extract, raw, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawPartidos(raw)
                # regresa el ID del registro
                return idRaw
            except Exception as e:
                # print('Error al inser RAW Partidos')
                self.log_error(where='Error al insertar RAW Partidos (%s)' %sitio, funtion='Funcion: actualizar_RawPartidos', exc=str(e))
        else:
            # si hay el registro, regresa el ID
            return idRaw
        
    def insert_Equipo(self, nombre: str, enlace: str, img: str):
        """Insertando los equipo encontrado

            Args:
                nombre (str): nombre del equipo a buscar
                enlace (str): enlace del equipo
                img (str): foto/logo del equipo

            Returns:
                int: si es mayor a 0 existe un error para registrar algun equipo
        """
        idEq = self.search_equipo(nombre)
        if idEq is None:
            # sino hay el elemento lo registra
            sql = "INSERT INTO equipos(nombre, enlace, img) VALUES (%s, %s, %s)"
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (nombre, enlace, img, ))
                # para que persistan los datos
                self.connection.commit()
                idEq = self.search_equipo(nombre)
                # regresa el ID del registro
                # print('ID:', idEq[0])
                return idEq
            except Exception as e:
                self.log_error(where='Error al insertar Equipo (%s, %s, %s)' %(nombre, enlace, img), funtion='Funcion: insert_Equipo', exc=str(e))
        else:
            # si hay el registro, regresa el ID
            return idEq
    
    def actulizar_Equipo(self, nombre: str, enlace: str, img: str):
        """Actualizando el registro del equipo

            Args:
                nombre (str): nombre del equipo a buscar
                enlace (str): enlace del equipo
                img (str): foto/logo del equipo

            Returns:
                list: con el detalle del registro
        """
        idEq = self.search_equipo(nombre)
        if idEq is None:
            return self.insert_Equipo(nombre, enlace, img)
        else:
            # Si hay el elemento lo actualiza
            sql = 'UPDATE equipos SET enlace=%s, img=%s WHERE idEq=%s'
            # print('Actualizando equipo\t',sql)
            try:
                self.cursor.execute(sql, (enlace, img, idEq[0], ))
                # para que persistan los datos
                self.connection.commit()
                idEq = self.search_equipo(nombre)
                # regresa el ID del registro
                # print('ID:', idEq[0])
                return idEq
            except Exception as e:
                self.log_error(where='Error al actualizar Equipo (%s, %s)' %(nombre, enlace), funtion='Funcion: actulizar_Equipo', exc=str(e))
    
    def insert_Equipos(self, lista):
        """Insertando los equipo encontrado

            Args:
                lista (list): lista de equipos

            Returns:
                int: si es mayor a 0 existe un error para registrar algun equipo
        """
        errores = 0
        # print("lista de equipos:\n{}\n\n".format(lista))
        for keyElemento in lista:
            elemento = lista[keyElemento]
            # print(keyElemento, "?:_", elemento)
            for k in elemento:
                # acedemos a cada llave(k), valor(v) de cada diccionario
                nombre = k['nombre']
                link = k['link']
                img = k['img']
                # print('Equipo a insertar:\t{}, {}, {}'.format(nombre, link, img))
                idEq = self.insert_Equipo(nombre, link, img)
                equipo = ''
                if idEq is None:
                    errores +=1
                    print('Error al registrar', nombre)
                else:
                    # print('Registro exitoso')
                    equipo = self.detalle_equipo(nombre)
                    if equipo[2] == '' or equipo[3] == '':
                        # sino hay enlace del equipo, actualiza el registro
                        idEq = self.actulizar_Equipo(nombre, link, img)
                    else:
                        pass
        return errores

    def insert_Estadisticas(self, opcion: str, equipo: str, anio: str, pts: str, pj: str, pg: str, pe: str, pp: str, gf: str, gc: str):
        """
            Inserta las estadisticas de los equipos en las respectivas tablas usando las palabras clave (Acumulado, Local y Visitante)
            Ojo si ingresa cualquier otro valor estos se ingresan en la ultima tabla (visitante)

            Args:
                opcion (str): hace referencia a los puntos de: Acumulado, Local y Visitante
                equipo (str): FK del equipo
                anio (str): Anio de la estadistica
                pts (str): Puntos acumulados de esta manera
                pj (str): PARTIDOS JUGADOS a la fecha
                pg (str): PARTIDOS GANADOS a la fecha
                pe (str): PARTIDOS EMPATADOS a la fecha
                pp (str): PARTIDOS PERDIDOS a la fecha
                gf (str): PARTIDOS GOLES a FAVOR a la fecha
                gc (str): PARTIDOS GOLES en CONTRA a la fecha

            Returns:
                list: Result list del registro
        """
        # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc))
        # se analiza si existe un registro con el ID del equipo y el anio (para no duplicar registros)
        regEstad = self.search_EstadisticaAnio(equipo, opcion, anio)
        # Se toma el 2 valor del Result pueste este corresponde al FK del Equipo
        # print('\nBuscando estadisticas\n{}\n\n'.format(regEstad))
        now = datetime.now()
        if now.year == anio and regEstad is not None:
            # anio actual
            # en caso de ser el anio actual actualiza el registro
            return self.actualizar_Estadisticas(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc)
        else:
            if regEstad is None:
                #  or regEstad == 0 or len(regEstad) == 0
                # sino hay registro alguno
                idEq = self.search_equipo(equipo)
                if idEq is None:
                    # inserta el registro del equipo
                    idEq = self.insert_Equipo(equipo, '')
                    # se llama a la funcion para proceder a registrar la estadistica
                    return self.insert_Estadisticas(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc)
                else:
                    sql = ''
                    # si esta registro el equipo, regresa el ID del registro
                    if opcion == 'Acumulado':
                        sql = "INSERT INTO posicionestotal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    elif opcion == 'Local':
                        sql = "INSERT INTO posicioneslocal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    else:
                        sql = "INSERT INTO posicionesvisitante(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    try:
                        self.cursor.execute(sql, (idEq[0], anio, pts, pj, pg, pe, pp, gf, gc, ))
                        # para que persistan los datos
                        self.connection.commit()
                        idEq = self.search_EstadisticaAnio(equipo, opcion, anio)
                        # regresa el ID del registro
                        # print('ID:', idEq[0])
                        return idEq
                    except Exception as e:
                        # raise
                        self.log_error(where='Error al insertar Estadisticas', funtion='Funcion: insert_Estadisticas', exc=str(e))
            else:
                return regEstad

    def actualizar_Estadisticas(self, opcion: str, equipo: str, anio: str, pts: str, pj: str, pg: str, pe: str, pp: str, gf: str, gc: str):
        """
            ACTUALIZA las estadisticas de los equipos en las respectivas tablas usando las palabras clave (Acumulado, Local y Visitante)
            Ojo si ingresa cualquier otro valor estos se ingresan en la ultima tabla (visitante)

            Args:
                opcion (str): hace referencia a los puntos de: Acumulado, Local y Visitante
                equipo (str): FK del equipo
                anio (str): Anio de la estadistica
                pts (str): Puntos acumulados de esta manera
                pj (str): PARTIDOS JUGADOS a la fecha
                pg (str): PARTIDOS GANADOS a la fecha
                pe (str): PARTIDOS EMPATADOS a la fecha
                pp (str): PARTIDOS PERDIDOS a la fecha
                gf (str): PARTIDOS GOLES a FAVOR a la fecha
                gc (str): PARTIDOS GOLES en CONTRA a la fecha

            Returns:
                list: Result list del registro
        """
        # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc))
        # se analiza si existe un registro con el ID del equipo y el anio (para no duplicar registros)
        regEstad = self.search_EstadisticaAnio(equipo, opcion, anio)
        # Se toma el 2 valor del Result pueste este corresponde al FK del Equipo
        # print('\nBuscando estadisticas\n{}\n\n'.format(regEstad))
        if regEstad is not None:
            #  or regEstad == 0 or len(regEstad) == 0
            # sino hay registro alguno
            idEq = self.search_equipo(equipo)
            if idEq is None:
                # inserta el registro del equipo
                idEq = self.insert_Equipo(equipo, '')
                # se llama a la funcion para proceder a registrar la estadistica
                return self.actualizar_Estadisticas(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc)
            else:
                sql = ''
                # si esta registro el equipo, regresa el ID del registro
                # UPDATE posicionestotal SET idP='[value-1]',fkEq='[value-2]',year='[value-3]',Pts='[value-4]',PJ='[value-5]',PG='[value-6]',PE='[value-7]',PP='[value-8]',GF='[value-9]',GC='[value-10]' WHERE 1
                if opcion == 'Acumulado':
                    sql = "UPDATE posicionestotal SET year = %s, Pts = %s, PJ = %s, PG = %s, PE = %s, PP = %s, GF = %s, GC = %s WHERE fkEq= %s"
                elif opcion == 'Local':
                    sql = "UPDATE posicioneslocal SET year = %s, Pts = %s, PJ = %s, PG = %s, PE = %s, PP = %s, GF = %s, GC = %s WHERE fkEq= %s"
                else:
                    sql = "UPDATE posicionesvisitante SET year = %s, Pts = %s, PJ = %s, PG = %s, PE = %s, PP = %s, GF = %s, GC = %s WHERE fkEq= %s"
                try:
                    self.cursor.execute(sql, (anio, pts, pj, pg, pe, pp, gf, gc, idEq[0], ))
                    # para que persistan los datos
                    self.connection.commit()
                    idEq = self.search_EstadisticaAnio(equipo, opcion, anio)
                    # regresa el ID del registro
                    # print('ID:', idEq[0])
                    return idEq
                except Exception as e:
                    # raise
                    self.log_error(where='Error al insertar Estadisticas', funtion='Funcion: actualizar_Estadisticas', exc=str(e))
        else:
            return regEstad

    def insert_Partido(self, eqA: str, golA: str, golB: str, eqB: str, year: str):
        existe = self.search_Partidos(eqA=eqA, golA=golA, golB=golB, eqB=eqB, year=year)
        if existe is None:
            # sino hay el elemento lo registra            
            sql = 'INSERT INTO partidos(eqA, golA, golB, eqB, fecha) VALUES (%s,%s,%s,%s,%s)'
            # print('Consulta\t',sql)
            fkA = self.search_equipo(eqA)
            fkB = self.search_equipo(eqB)
            # print('insert Partid\t{}::{}::\t{}-{}\t{}::{}::\t{}'.format(eqA, type(fkA), golA, golB, eqB, type(fkB), year))
            try:
                # consultamos las FK de los equipos que jugaron
                self.cursor.execute(sql, (fkA[0], golA, golB, fkB[0], year, ))
                # para que persistan los datos
                self.connection.commit()
                existe = self.search_Partidos(eqA=eqA, golA=golA, golB=golB, eqB=eqB, year=year)
                # regresa el ID del registro
                # print('ID reg partido:', existe)
                return existe
            except Exception as e:
                self.log_error(where='Insertando el partido', funtion='Funcion: insert_Partido', exc=str(e))
        else:
            # si hay el registro, regresa el ID
            return existe
    
    def actualizar_RawEstadisticas(self, sitio: str, anio: str, fecha_process:str, errores_process:str, process:str):
        """Usa el sitio y opcion para buscar el HTML corespondiente a esos parametros.

            Args:
                sitio (str): URL de la cual se extrae la metadata
                opcion (str): Hace referencia los pts: Acumulado, Local y Visitante
                fecha_process (str): Fecha en la que se procesa la data
                error_process (str): Lista de errores al momento de procesar
                process (str): 1/0 Para conocer si fue (1) o no procesado (0)

            Returns:
                list: Returna None o array en caso de encontrar el registro
        """
        idRaw = self.search_RawEstadisticas(sitio)
        # print('Estadisticas url-Act::\t{}\t\tOpcion:\t{}'.format(sitio, opcion))
        if idRaw is None:
            # sino hay el registro regresa NONE
            return idRaw
        else:
            # si hay el registro, regresa el registro
            sql = "UPDATE metadataestadisticas SET fecha_process=%s, errores_procesamiento=%s, process=%s WHERE sitio=%s and anio=%s"
            # print('Consulta actualizar MTD Estadisticas\t',sql)
            try:
                self.cursor.execute(sql, (fecha_process, errores_process, process, sitio, anio, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_RawEstadisticas(sitio)
                # regresa el ID del registro
                return idRaw
            except Exception as e:
                self.log_error(where='Error al actualizar RAW Estadisticas (%s: %s)' %(sitio, anio), funtion='Funcion: actualizar_RawEstadisticas', exc=str(e))
                
    
    def actualizar_RawPartido(self, sitio: str, raw: str, fecha_process:str, errores_procesamiento:str, process:str):
        """Usa el sitio y opcion para buscar el HTML corespondiente a esos parametros.

            Args:
                sitio (str): URL de la cual se extrae la metadata
                raw (str): metadata del sitio
                fecha_process (str): Fecha en la que se procesa la data
                errores_procesamiento (str): Lista de errores al momento de procesar
                process (str): 1/0 Para conocer si fue (1) o no procesado (0)

            Returns:
                list: Returna None o array en caso de encontrar el registro
        """
        # print('Fecha de procesamiento:\t{}\tTipo:\t{}'.format(fecha_process, type(fecha_process)))
        idRaw = self.search_IdRawPartidos(raw)
        if idRaw is None:
            # sino hay el registro regresa NONE
            return idRaw
        else:
            # el caso idoneo es 1 (vprocess)
            sql = 'UPDATE metadatapartidos SET fecha_process=%s, errores_procesamiento=%s, process=%s WHERE sitio=%s and raw_html=%s'
            # print('Consulta update MTD Partidos\t',sql)
            try:
                self.cursor.execute(sql, (fecha_process, errores_procesamiento, process, sitio, raw, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawPartidos(raw)
                # regresa el ID del registro
                return idRaw
            except Exception as e:
                self.log_error(where='Error al actualizar RAW Partidos (%s)' %sitio, funtion='Funcion: actualizar_RawPartido', exc=str(e))
    
    def estadisticasTotales(self):
        """Funcion util que hace uso de la vista (EstadisticasTotales) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM estadisticastotales'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.log_error(where='Error al mostrar la estadistica totales/acumuladas', funtion='Funcion: estadisticasTotales', exc=str(e))

    def estadisticasLocales(self):
        """Funcion util que hace uso de la vista (EstadisticasLocal) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM estadisticaslocal'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.log_error(where='Error al mostrar la estadistica locales', funtion='Funcion: estadisticasLocales', exc=str(e))
    
    def estadisticasVisitantes(self):
        """Funcion util que hace uso de la vista (EstadisticasVisitantes) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM estadisticasvisitantes'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.log_error(where='Error al mostrar la estadistica visitantes', funtion='Funcion: estadisticasVisitantes', exc=str(e))
    
    def encuentros(self):
        """Funcion util que hace uso de la vista (Encuentros) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM encuentros'
        # p.idP, eqA, eqB, p.golA, p.golB, p.fecha
        # datos de la vista
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.log_error(where='Error los encuentros o partidos hasta la fecha de procesamiento', funtion='Funcion: encuentros', exc=str(e))
            
    
    def version(self):
        # ejecuta el SQL query usando el metodo execute().
        self.cursor.execute("SELECT VERSION()")

    def close(self):
        # cerramos la conexion
        print('Conexion cerrada')
        self.connection.close()
