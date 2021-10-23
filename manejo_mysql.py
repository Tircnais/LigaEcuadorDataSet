import pymysql
# lib para establecer la conexion a la BD
from datetime import datetime
# lib para obtener la fecha actual (anio)

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
            # print('Result equipo\t', existe[0])
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
            # print('No hay estadisticas registradas de este equipo')
            return None
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
                self.cursor.execute(sql, (id_Eq[0], ))
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
        if id_Eq is None:
            # print('Aun no se ha registrado este equipo')
            id_Eq = self.insert_Equipo(equipo, '')
            # print('No hay estadisticas registradas de este equipo')
            return self.search_EstadisticaAnio(equipo, opcion, anio)
        else:
            # Busca sus estadisticas
            sql = ''
            if opcion == 'Acumulado':
                sql = "Select * from PosicionesTotal Where fkEq = %s and year = %s"
            elif opcion == 'Local':
                sql = "Select * from PosicionesLocal Where fkEq = %s and year = %s"
            else:
                sql = "Select * from PosicionesVisitante Where fkEq = %s and year = %s"
                
            # print('search EstadisticaAnio ID equipo:\t',id_Eq[0])
            try:
                self.cursor.execute(sql, (id_Eq[0], anio, ))
                # por retornar mas de un registro fetchall
                existe = self.cursor.fetchone()
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
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando todos los equipos', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
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

    def search_RawEstadisticas(self, sitio: str, opcion):
        """Busca el HTML usando el enlace del mismo

        Args:
            rawEst (str): Enlace del sito de donde se extrae la metadata

        Returns:
            int: ID del enlace o RAW a extraer
        """
        sql = 'Select id from metaDataEstadisticas Where sitio = %s and opcion = %s'
        # print('Consulta\t',sql)

        try:
            self.cursor.execute(sql, (sitio, opcion, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='buscando la metadataEstadistica (rawEst)', html=sitio+'||'+opcion, exc=str(e), total_error = self.total_errors)
    
    def search_IdRawPartidos(self, rawPartidos: str):
        """Busca el HTML usando el raw extraido

        Args:
            rawPartidos (str): Enlace del sito de donde se extrae la metadata

        Returns:
            int: ID del enlace o RAW a extraer
        """
        sql = 'SELECT id FROM metaDataPartidos WHERE raw_html = %s'
        # print('Consulta\t',sql)
        try:
            self.cursor.execute(sql, (rawPartidos, ))
            # por retornar un registro fetchone
            existe = self.cursor.fetchone()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            # print('Error al buscar RAW Partidos')
            self.total_errors += 1
            self.log_error(where='buscando el raw de Partidos (rawPartidos)', html=rawPartidos, exc=str(e), total_error = self.total_errors)
    
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
            sql = 'SELECT * FROM Partidos WHERE eqA = %s AND golA = %s AND golB = %s AND eqB = %s AND fecha= %s'
            # print('Buscando partido\t{}\t{}-{}\t{}\t{}'.format(fkA[0], golA, golB, fkB[0], year))
            try:
                self.cursor.execute(sql, (fkA[0], golA, golB, fkB[0], year, ))
                existe = self.cursor.fetchone()
                # por retornar un registro fetchone
                # print('Result Busq Partido\t', existe)
                return existe
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='buscando el equipo (nombre)', html=sql, exc=str(e), total_error = self.total_errors)
    
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
        try:
            sql = 'Select sitio, raw_html from metaDataPartidos Where process = 0'
            # print('Consulta\t',sql)
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            existe = self.cursor.fetchall()
            # print('Result\t', existe)
            return existe
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='RAw NO procesado de Partidos', html='sin parametros', exc=str(e), total_error = self.total_errors)

    def insert_RawEstadisticas(self, sitio: str, raw: str, opcion: str, anio: str):
        idRaw = self.search_IdRawEstadisticas(raw)
        now = datetime.now()
        if now.year == anio:
            if idRaw is None:
                # en caso de ser el anio actual y no se ha registrado
                return self.insert_RawEstadisticas(sitio, raw, opcion, anio)
            else:
                # en caso de ser el anio actual actualiza el registro
                return self.actualizar_RawEstadisticas(sitio, opcion)
        else:
            # sino es al anio actual registra la estadistica
            if idRaw is None:
                # sino hay el elemento lo registra
                sql = "INSERT INTO metaDataEstadisticas(sitio, raw_html, opcion) VALUES (%s, %s, %s)"
                # print('Consulta insert MTD Estadisticas\t',sql)
                print('Consulta insert MTD Estadisticas.\tSitio:\t{}\t\tOpcion:\t{}'.format(sitio, opcion))
                try:
                    self.cursor.execute(sql, (sitio, raw, opcion, ))
                    # para que persistan los datos
                    self.connection.commit()
                    idRaw = self.search_IdRawEstadisticas(raw)
                    # regresa el ID del registro
                    return idRaw
                except Exception as e:
                    self.total_errors += 1
                    data = sitio+'\t'+opcion
                    self.log_error(where='Error al insertar RAW Estadisticas', html=data, exc=str(e), total_error = self.total_errors)
            else:
                # si hay el registro, regresa el ID
                return idRaw

    def insert_RawPartidos(self, sitio: str, raw: str):
        idRaw = self.search_IdRawPartidos(raw)
        # print('URL rawPartido\t',sitio)
        if idRaw is None:
            # sino hay el elemento lo registra
            sql = "INSERT INTO metaDataPartidos(sitio, raw_html) VALUES (%s, %s)"
            # print('Consulta RawPart\t',sql)
            try:
                self.cursor.execute(sql, (sitio, raw, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawPartidos(raw)
                # regresa el ID del registro
                
                return idRaw
            except Exception as e:
                # print('Error al inser RAW Partidos')
                self.total_errors += 1
                self.log_error(where='Error al insertar RAW Partidos', html=sitio, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return idRaw
        
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
                return idEq
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al insertar Equipo', html=nombre+'\t'+enlace, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return idEq
    
    def actulizar_Equipo(self, nombre: str, enlace: str):
        idEq = self.search_equipo(nombre)
        if idEq is None:
            return self.insert_Equipos(nombre, enlace)
        else:
            # Si hay el elemento lo actualiza
            sql = 'UPDATE equipos SET enlace=%s WHERE idEq=%s'
            # print('Actualizando equipo\t',sql)
            try:
                self.cursor.execute(sql, (enlace, idEq[0], ))
                # para que persistan los datos
                self.connection.commit()
                idEq = self.search_equipo(nombre)
                # regresa el ID del registro
                # print('ID:', idEq[0])
                return idEq
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al insertar Equipo', html=nombre+'\t'+enlace, exc=str(e), total_error = self.total_errors)
    
    def insert_Equipos(self, lista):
        errores = 0
        for keyElemento in lista:
            elemento = lista[keyElemento]
            # print(keyElemento, "?:_", elemento)
            for k in elemento:
                # acedemos a cada llave(k), valor(v) de cada diccionario
                nombre = k['nombre']
                link = k['link']
                # print('Equipo a insertar:\t{}\t::\t{}'.format(nombre, link))
                idEq = self.insert_Equipo(nombre, link)
                equipo = ''
                if idEq is None:
                    errores +=1
                    print('Error al registrar', nombre)
                else:
                    # print('Registro exitoso')
                    equipo = self.detalle_equipo(nombre)
                    if equipo[2] == '':
                        # sino hay enlace del equipo, actualiza el registro
                        idEq = self.actulizar_Equipo(nombre, link)
                    else:
                        pass
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
                    sql = "INSERT INTO PosicionesTotal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                elif opcion == 'Local':
                    sql = "INSERT INTO PosicionesLocal(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                else:
                    sql = "INSERT INTO PosicionesVisitante(fkEq, year, Pts, PJ, PG, PE, PP, GF, GC) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
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
                    self.total_errors += 1
                    self.log_error(where='Error al insertar Estadisticas', html='Revisar el orden de los datos a insertar', exc=str(e), total_error = self.total_errors)
        else:
            return regEstad

    def insert_Partido(self, eqA: str, golA: str, golB: str, eqB: str, year: str):
        existe = self.search_Partidos(eqA=eqA, golA=golA, golB=golB, eqB=eqB, year=year)
        if existe is None:
            # sino hay el elemento lo registra            
            sql = 'INSERT INTO Partidos(eqA, golA, golB, eqB, fecha) VALUES (%s,%s,%s,%s,%s)'
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
                self.total_errors += 1
                self.log_error(where='buscando el equipo (nombre)', html=sql, exc=str(e), total_error = self.total_errors)
        else:
            # si hay el registro, regresa el ID
            return existe
    
    def actualizar_RawEstadisticas(self, sitio: str, opcion: str):
        """Usa el sitio y opcion para buscar el HTML corespondiente a esos parametros.

        Args:
            sitio (str): URL de la cual se extrae la metadata
            opcion (str): Hace referencia los pts: Acumulado, Local y Visitante

        Returns:
            array: Returna None o array en caso de encontrar el registro
        """
        idRaw = self.search_RawEstadisticas(sitio, opcion)
        print('Act. estadisticas-url::\t{}\t\tOpcion:\t{}'.format(sitio, opcion))
        if idRaw is None:
            # sino hay el registro regresa NONE
            return idRaw
        else:
            # si hay el registro, regresa el registro
            sql = "UPDATE metaDataEstadisticas SET process=1 WHERE sitio=%s and opcion=%s"
            # print('Consulta actualizar MTD Estadisticas\t',sql)
            try:
                self.cursor.execute(sql, (sitio, opcion, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_RawEstadisticas(sitio, opcion)
                # regresa el ID del registro
                return idRaw
            except Exception as e:
                self.total_errors += 1
                data = sitio+'\t'+opcion
                self.log_error(where='Error al actualizar RAW Estadisticas', html=data, exc=str(e), total_error = self.total_errors)
    
    def actualizar_RawPartido(self, sitio: str, raw: str):
        idRaw = self.search_IdRawPartidos(raw)
        if idRaw is None:
            # sino hay el registro regresa NONE
            return idRaw
        else:
            # si hay el registro, regresa el registro
            sql = 'UPDATE metaDataPartidos SET process=1 WHERE sitio=%s and raw_html=%s'
            # print('Consulta update MTD Partidos\t',sql)
            try:
                self.cursor.execute(sql, (sitio, raw, ))
                # para que persistan los datos
                self.connection.commit()
                idRaw = self.search_IdRawPartidos(raw)
                # regresa el ID del registro
                return idRaw
            except Exception as e:
                self.total_errors += 1
                self.log_error(where='Error al actualizar RAW Partidos', html=sitio, exc=str(e), total_error = self.total_errors)
    
    def estadisticasTotales(self):
        """Funcion util que hace uso de la vista (EstadisticasTotales) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM EstadisticasTotales'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='Error al mostrar la estadistica totales/acumuladas', html='sin parametros', exc=str(e), total_error = self.total_errors)

    def estadisticasLocales(self):
        """Funcion util que hace uso de la vista (EstadisticasLocal) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM EstadisticasLocal'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='Error al mostrar la estadistica locales', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
    def estadisticasVisitantes(self):
        """Funcion util que hace uso de la vista (EstadisticasVisitantes) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM EstadisticasVisitantes'
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='Error al mostrar la estadistica visitantes', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
    def encuentros(self):
        """Funcion util que hace uso de la vista (Encuentros) mencionada para generar el archivo CSV.

        Returns:
            array: Retorna la estadistica del equipo
        """
        sql = 'SELECT * FROM Encuentros'
        # p.idP, eqA, eqB, p.golA, p.golB, p.fecha
        # datos de la vista
        try:
            self.cursor.execute(sql)
            # por retornar un registro fetchone
            equipos = self.cursor.fetchall()
            return equipos
        except Exception as e:
            self.total_errors += 1
            self.log_error(where='Error los encuentros o partidos hasta la fecha', html='sin parametros', exc=str(e), total_error = self.total_errors)
    
    def version(self):
        # ejecuta el SQL query usando el metodo execute().
        self.cursor.execute("SELECT VERSION()")

    def close(self):
        # cerramos la conexion
        print('Conexion cerrada')
        self.connection.close()
