import os

from . import MAX_RECORDS
from .dbmanager import DBManager


class Records:

    ruta = os.path.join("thequest/data", "records.db")

    def __init__(self):

        self.lista_records = []
        # self.check_records_file()
        self.db = DBManager(self.ruta)
        self.lista_records = self.db.cargar()

    def es_record(self, puntuacion):
        self.lista_records.sort(key=lambda item: item[1], reverse=True)
        return puntuacion > self.lista_records[len(self.lista_records)-1][1]

    def insertar_record(self, nombre, puntuacion):
        self.lista_records.append((nombre, puntuacion))
        self.lista_records.sort(key=lambda item: item[1], reverse=True)
        self.lista_records = self.lista_records[:MAX_RECORDS]
        self.db.guardar(self.lista_records)
        self.lista_records = self.db.cargar()

    def actualizar(self):
        self. lista_records = self.db.cargar()
