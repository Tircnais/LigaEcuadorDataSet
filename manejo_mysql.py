import pymysql#.cursors

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
            db='ligaEcuador'
            # cursorclass=pymysql.cursors.DictCursor
        )

        # prepare a cursor object using cursor() method
        self.cursor = self.connection.cursor()
        print('Conexion exitosa')

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
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando el equipo (nombre)', html=nombre, exc=str(e), total_error = self.total_errors)
    
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
            print('No hay estadisticas registradas de este equipo')
        else:
            # Busca sus estadisticas
            if opcion == 'Acumulado':
                sql = "Select * from PosicionesTotal Where fkEq = %s"
            elif opcion == 'Local':
                sql = "Select * from PosicionesLocal Where fkEq = %s"
            else:
                sql = "Select * from PosicionesVisitante Where fkEq = %s"
                
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (id_Eq, ))
                # por retornar mas de un registro fetchall
                existe = self.cursor.fetchall()
                # print('Result\t', existe)
                return existe
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='buscando las estadisticas equipo (nombre)', html=equipo, exc=str(e), total_error = self.total_errors)
    
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
        sql = ''
        if id_Eq is None:
            print('Aun no se ha registrado este equipo')
            id_Eq = self.insert_Equipo(equipo, '')
            print('No hay estadisticas registradas de este equipo')
            return 0
        else:
            # Busca sus estadisticas
            if opcion == 'Acumulado':
                sql = "Select idP, year from PosicionesTotal Where fkEq = %s and year = %s"
            elif opcion == 'Local':
                sql = "Select idP, year from PosicionesLocal Where fkEq = %s and year = %s"
            else:
                sql = "Select idP, year from PosicionesVisitante Where fkEq = %s and year = %s"
                
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (id_Eq, anio, ))
                # por retornar mas de un registro fetchall
                existe = self.cursor.fetchall()
                # print('Result\t', existe)
                return existe
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='buscando las estadisticas equipo (nombre y anio)', html=equipo+' '+anio, exc=str(e), total_error = self.total_errors)
    
    def select_all_equipo(self):
        sql = 'Select * from equipos'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            """Listando equipos registrados
            for equipo in equipos:
                print('ID:', equipo[0])
                print('equipo:', equipo[1])
                print('enlace:', equipo[2])
            """
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando todos los equipos', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
    def search_IdRawEstadisticas(self, rawEst: str):
        """Busca el HTML usando el enlace del mismo

        Args:
            rawEst (str): Enlace del sito de donde se extrae la metadata

        Returns:
            int: ID del enlace o RAW a extraer
        """
        sql = 'Select id from metaDataEstadisticas Where raw_html = %s'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql, (rawEst, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando la metadataEstadistica (rawEst)', html=rawEst, exc=str(e), total_error = self.total_errors)
    
    def search_IdRawPartidos(self, rawPartidos: str):
        """Busca el HTML usando el enlace del mismo

        Args:
            rawPartidos (str): Enlace del sito de donde se extrae la metadata

        Returns:
            int: ID del enlace o RAW a extraer
        """
        sql = 'Select id from metaDataPartidos Where raw_html = %s'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql, (rawPartidos, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando el raw de Partidos (rawPartidos)', html=rawPartidos, exc=str(e), total_error = self.total_errors)
    
    def rawNoProcessEstadisticas(self):
        """Trae la lista de HTML no procesados

        Returns:
            list: RAW no procesados
        """
        sql = 'Select opcion, raw_html from metaDataEstadisticas Where process = 0'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            existe = self.cursor.fetchall()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='RAw NO procesado de Estadisticas', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
    def rawNoProcessPartidos(self):
        """Trae la lista de HTML no procesados

        Returns:
            list: RAW no procesados
        """
        sql = 'Select id from metaDataPartidos Where process = 0'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            existe = self.cursor.fetchall()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='RAw NO procesado de Partidos', html='sin parametros', exc=str(e), total_error = self.total_errors)

    def insert_RawEstadisticas(self, sitio: str, raw: str, opcion: str):
        idRaw = self.search_IdRawEstadisticas(raw)
        if idRaw is None:
            # sino hay el elemento lo registra
            sql = "INSERT INTO metaDataEstadisticas(sitio, raw_html, opcion) VALUES (%s, %s, %s)"
            print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (sitio, raw, opcion, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawEstadisticas(raw)
                # regresa el ID del registro
                # print('ID:', idRaw[0])
                return idRaw[0]
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al insertar RAW Estadisticas', html=sitio+'\t'+raw+'\t'+opcion, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return idRaw[0]

    def insert_RawPartidos(self, sitio: str, raw: str):
        idRaw = self.search_IdRawPartidos(raw)
        if idRaw is None:
            # sino hay el elemento lo registra
            sql = "INSERT INTO metaDataPartidos(sitio, raw_html) VALUES (%s, %s)"
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (sitio, raw, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawPartidos(raw)
                # regresa el ID del registro
                print('ID:', idRaw[0])
                return idRaw[0]
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al insertar RAW Partidos', html=sitio+'\t'+raw, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return idRaw[0]
        
    def insert_Equipo(self, nombre: str, enlace: str):
        idEq = self.search_equipo(nombre)
        if idEq is None:
            # sino hay el elemento lo registra
            sql = "INSERT INTO equipos(nombre, enlace) VALUES (%s, %s)"
            # print('Consulta\t',sql)
            try:
                self.cursor.execute(sql, (nombre, enlace, ))
                # para que persistan los datos
                self.connection.commit()
                idEq = self.search_equipo(nombre)
                # regresa el ID del registro
                # print('ID:', idEq[0])
                return idEq[0]
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al insertar Equipo', html=nombre+'\t'+enlace, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return idEq[0]
    
    def insert_Equipos(self, lista):
        errores = 0
        for keyElemento in lista:
            elemento = lista[keyElemento]
            # print(keyElemento, "?:_", elemento)
            for k in elemento:
                # .items()
                # acedemos a cada llave(k), valor(v) de cada diccionario
                nombre = k['nombre']
                link = k['link']
                # print('A insertar\n\n\r\n',nombre, link)
                idEq = self.insert_Equipo(nombre, link)
                if idEq>0:
                    # print('Registro exitoso')
                    pass
                else:
                    errores =+1
                    print('Error al registrar', nombre)
        return errores

    def insert_Estadisticas(self, opcion: str, equipo: str, anio: str, pts: str, pj: str, pg: str, pe: str, pp: str, gf: str, gc: str):
        """Inserta las estadisticas de los equipos en las respectivas tablas usando las palabras clave (Acumulado, Local y Visitante)
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
            [type]: [description]
        """
        # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc))
        # se analiza si existe un registro con el ID del equipo y el anio (para no duplicar registros)
        regEstad = self.search_EstadisticaAnio(equipo, opcion, anio)
        # Se toma el 2 valor del Result pueste este corresponde al FK del Equipo
        # print('\nBuscando estadisticas\n{}\n\n'.format(regEstad))
        if type(regEstad) == list or type(regEstad) == tuple and len(regEstad) >= 0:
            # UN SOLO registro (no debe haber mas de uno EQ y ANIO)
            anio = ''
            if type(regEstad) == list:
                anio == regEstad[1]
            elif type(regEstad) == tuple and len(regEstad) >= 0:
                anio == regEstad[0][1]
            # si el equipo y anio son iguales a cualquier registro, se necesita una actualizacion (esto en especial para el anio en 
            # transcurso)
            print('\nEstos registros requieren actualizacion\n{}\t{}\t{}\n'.format(equipo, opcion, anio))
        elif regEstad is None or regEstad == 0 or len(regEstad) == 0:
            # sino hay registro alguno
            idEq = self.search_equipo(equipo)
            if idEq == None:
                # inserta el registro del equipo
                idEq = self.insert_Equipo(equipo, '')
                # se llama a la funcion para proceder a registrar la estadistica
                return self.insert_Estadisticas(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc)
            else:
                sql = ''
                # si esta registro el equipo, regresa el ID del registro
                if opcion == 'Acumulado':
                    sql = "INSERT INTO PosicionesTotal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    # print('Consulta\t',sql)    
                elif opcion == 'Local':
                    sql = "INSERT INTO PosicionesLocal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                else:
                    sql = "INSERT INTO PosicionesVisitante(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                try:
                    self.cursor.execute(sql, (idEq, anio, pts, pj, pg, pe, pp, gf, gc, ))
                    # para que persistan los datos
                    self.connection.commit()
                    idEq = self.search_EstadisticaAnio(equipo, opcion, anio)
                    # regresa el ID del registro
                    # print('ID:', idEq[0])
                    return idEq[0]
                except Exception as e:
                    # raise
                    self.total_errors += 1
                    self.log_error(where='Error al insertar Estadisticas', html='Revisar el orden de los datos a insertar', exc=str(e), total_error = self.total_errors)
        else:
            # self.insert_Estadisticas(opcion, equipo, anio, pts, pj, pg, pe, pp, gf, gc)
            self.total_errors += 1
            self.log_error(where='Caso no previsto', html='Revisar el orden de los datos a insertar', exc=str(e), total_error = self.total_errors)
        
    def version(self):
        # ejecuta el SQL query usando el metodo execute().
        self.cursor.execute("SELECT VERSION()")

    def close(self):
        # cerramos la conexion
        print('Conexion cerrada')
        self.connection.close()
