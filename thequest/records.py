import os
from dbmanager import DBManager
MAX_RECORDS = 10


class Records:

    ruta = os.path.join("data", "records.db")
    # file_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):

        self.lista_records = []
        # self.check_records_file()
        self.db = DBManager(self.ruta)
        self.lista_records = self.db.cargar()
        print(self.lista_records)

    def insertar_record(self, nombre, puntuacion):
        self.lista_records.append((nombre, puntuacion))
        self.lista_records.sort(key=lambda item: item[1], reverse=True)
        self.lista_records = self.lista_records[:MAX_RECORDS]
        print(self.lista_records)
        self.db.guardar(self.lista_records)
