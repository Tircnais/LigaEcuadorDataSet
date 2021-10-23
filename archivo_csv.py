# Conectando a BD
from manejo_mysql import Database
# usado para crear el CSV
import csv

class generar_CSV():
    """Clase usada para generar el CSV
    """
    def csv_estadisticas(self, estadistica, opcion):
        # csv_estadisticas
        salida = []
        for element in estadistica:
            equipo = element[0]
            year = element[1]
            # pts acumulados
            pts = element[2]
            # partidos jugados
            pj = element[3]
            # partidos ganados
            pg = element[4]
            # partidos empatado
            pe = element[5]
            # partidos perdido
            pp = element[6]
            # gol a favor
            gf = element[7]
            # gol en contra
            gc = element[8]
            print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(equipo, year, pts, pj, pg, pe, pp, gf, gc))
            salida.append([equipo, year, pts, pj, pg, pe, pp, gf, gc])
        if opcion == 'Acumulado':
            with open('estadisticaGeneral.csv', 'w') as csvfile:
                csvfile.write("equipo,year,pts,pj,pg,pe,pp,gf,gc\n")
                wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                wr.writerows(salida)
        elif opcion == 'Local':
            with open('estadisticaLocal.csv', 'w') as csvfile:
                csvfile.write("equipo,year,pts,pj,pg,pe,pp,gf,gc\n")
                wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                wr.writerows(salida)
        else:
            with open('estadisticaVisitante.csv', 'w') as csvfile:
                csvfile.write("equipo,year,pts,pj,pg,pe,pp,gf,gc\n")
                wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                wr.writerows(salida)

    def csv_encuentros(self, partidos):
        """Metodo que genera el CSV de los partidos jugados hasta la fecha registrados

        Args:
            partidos ([type]): Lista de partidos
        """
        encuentros = []
        for element in partidos:
            # ID Registro
            idRes = element[0]
            # equipo A
            equipoA = element[1]
            # equipo B
            equipoB = element[2]
            golA = element[3]
            golB = element[4]
            fecha = element[5]
            print('{}\t{}\t{}\t{}\t{}'.format(equipoA, equipoB, golA, golB, fecha))
            encuentros.append([equipoA, equipoB, golA, golB, fecha])
        with open('partidos.csv', 'w') as csvfile:
            csvfile.write("equipo,year,pts,pj,pg,pe,pp,gf,gc\n")
            wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            wr.writerows(encuentros)
