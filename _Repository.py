import atexit
import sqlite3
import os.path
from DAO import Vaccines, Logistics, Suppliers, Clinics
from DTO import Vaccine


class _Repository:
    def __init__(self):
        self.isExist = os.path.isfile('database.db')  # TODO: delete before submission
        self._conn = sqlite3.connect('database.db')
        # DAO'S
        self.vaccines = Vaccines(self._conn)
        self.clinics = Clinics(self._conn)
        self.suppliers = Suppliers(self._conn)
        self.logistics = Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def get_output_addition(self):
        c = self._conn.cursor()
        all_quantities = c.execute("""SELECT SUM(quantity) FROM Vaccines""").fetchall()[0]
        all_demands = c.execute("""SELECT SUM(demand) FROM Clinics""").fetchall()[0]
        all_received = c.execute("""SELECT SUM(count_received) FROM Logistics""").fetchall()[0]
        all_sent = c.execute("""SELECT SUM(count_sent) FROM Logistics""").fetchall()[0]
        line = str(all_quantities[0]) + ',' + str(all_demands[0]) + ',' + str(all_received[0]) + ',' + str(
            all_sent[0]) + '\n'
        return line

    def pull_vaccines(self, demand):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM Vaccines ORDER BY date""")
        vaccines_ids = (c.fetchall())
        i = 0

        while i < len(vaccines_ids) and demand > 0:
            c.execute("""SELECT * FROM Vaccines WHERE id=?""", [*vaccines_ids[i]])
            vaccine = Vaccine(*(c.fetchone()))
            new_amount = vaccine.quantity - demand
            if new_amount > 0:
                self._conn.execute("""UPDATE Vaccines SET quantity=? WHERE id=?""", [new_amount, vaccine.id])
                self.logistics.update_count_sent(self.suppliers.get_logistic_by_id(vaccine.supplier), demand)
                break
            elif new_amount == 0:
                self._conn.execute("""DELETE FROM Vaccines WHERE id=?""", [vaccine.id])
                self.logistics.update_count_sent(self.suppliers.get_logistic_by_id(vaccine.supplier), demand)
                break
            else:
                self._conn.execute("""DELETE FROM Vaccines WHERE id=?""", [vaccine.id])
                demand = demand - vaccine.quantity
                self.logistics.update_count_sent(self.suppliers.get_logistic_by_id(vaccine.supplier), vaccine.quantity)
            i = i + 1

    def create_tables(self):
        if self.isExist:
            self._conn.executescript("""DROP  TABLE Vaccines""")
            self._conn.executescript("""DROP  TABLE Suppliers""")
            self._conn.executescript("""DROP  TABLE Clinics""")
            self._conn.executescript("""DROP  TABLE Logistics""")

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
