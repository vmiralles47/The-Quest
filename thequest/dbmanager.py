# modulo para gestionar la base de datos de la lista de records con SQLite
import sqlite3


class DBManager:

    def __init__(self, ruta):
        self.records = []
        self.ruta = ruta

    def cargar(self):
        consulta = "SELECT nombre, puntos FROM records"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        self.records = cursor.fetchall()  # devuelve una lista de tuplas
        conexion.close()
        return self.records

    def guardar(self, lista):
        self.borrar_lista()
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        for dupla in lista:
            consulta = f"INSERT INTO records(nombre,puntos) VALUES ('{dupla[0]}', {dupla[1]})"
            cursor.execute(consulta)

        conexion.commit()
        conexion.close()

    def borrar_lista(self):
        consulta = "DELETE FROM records WHERE _rowid_ IN ('5', '4', '3', '2', '1')"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
