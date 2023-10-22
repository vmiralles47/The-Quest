# modulo para gestionar los records con SQLite
import os
import sqlite3


"""
nuestra clase hará los siguiente:
    al ser instanciada, leerá los datos de la base de datos y los cargará en una lista 
    
    podrá insertar un nombre y un valor en el orden correspondiente segun puntuación. la puntuacion más baja se desechará
    volverá a escribir la lista entera en la base de datos, para lo cual antes tiene que borrarla. 

"""


class DBManager:

    def __init__(self, ruta):
        # self.ruta = os.path.join("data", "records.db")
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

        print("voy a insertar en db la lista ", lista)
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        for dupla in lista:
            consulta = f"INSERT INTO records(nombre,puntos) VALUES ('{dupla[0]}', {dupla[1]})"
            cursor.execute(consulta)

        conexion.commit()
        conexion.close()

    def borrar_lista(self):
        check_list = []
        consulta = "DELETE FROM records WHERE _rowid_ IN ('10', '9','8', '7','6','5', '4', '3', '2', '1')"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()
