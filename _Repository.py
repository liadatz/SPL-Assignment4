import atexit
import sqlite3
import os.path
from DAO import Vaccines, Logistics, Suppliers, Clinics


class _Repository:
    def __init__(self):
        # self.isExist = os.path.isfile('database.db')  # TODO: delete before submission
        self._conn = sqlite3.connect('database.db')
        # DAO'S
        self.vaccines = Vaccines(self._conn)
        self.clinics = Clinics(self._conn)
        self.suppliers = Suppliers(self._conn)
        self.logistics = Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        # if self.isExist:
        #     self._conn.executescript("""DROP  TABLE Vaccines""")
        #     self._conn.executescript("""DROP  TABLE Suppliers""")
        #     self._conn.executescript("""DROP  TABLE Clinics""")
        #     self._conn.executescript("""DROP  TABLE Logistics""")

        self._conn.executescript("""
        CREATE TABLE Vaccines (
                id       INTEGER            PRIMARY KEY,
                date     DATE               NOT NULL,
                supplier INTEGER REFERENCES Suppliers(id),
                quantity INTEGER            NOT NULL 
            );

        CREATE TABLE Suppliers (
                id       INTEGER            PRIMARY KEY,
                name     STRING             NOT NULL,
                logistic INTEGER REFERENCES Logistics(id)
            );

        CREATE TABLE Clinics (
                id       INTEGER            PRIMARY KEY,
                location STRING             NOT NULL,
                demand   INTEGER            NOT NULL,
                logistic INTEGER REFERENCES Logistics(id)
            );

          CREATE TABLE Logistics (
                id             INTEGER     PRIMARY KEY,
                name           STRING      NOT NULL,
                count_sent     INTEGER     NOT NULL,
                count_received INTEGER     NOT NULL

              );
      """)


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
