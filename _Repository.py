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
        all_quantities = c.execute("""SELECT SUM(quantity) FROM vaccines""").fetchall()[0]
        all_demands = c.execute("""SELECT SUM(demand) FROM clinics""").fetchall()[0]
        all_received = c.execute("""SELECT SUM(count_received) FROM logistics""").fetchall()[0]
        all_sent = c.execute("""SELECT SUM(count_sent) FROM logistics""").fetchall()[0]
        line = str(all_quantities[0]) + ',' + str(all_demands[0]) + ',' + str(all_received[0]) + ',' + str(
            all_sent[0])
        return line

    def pull_vaccines(self, clinic_name, demand):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM vaccines ORDER BY datetime(date) ASC""")
        vaccines_ids = (c.fetchall())
        i = 0
        while i < len(vaccines_ids) and demand > 0:
            c.execute("""SELECT * FROM vaccines WHERE id=?""", [*vaccines_ids[i]])
            vaccine = Vaccine(*(c.fetchone()))
            new_amount = vaccine.quantity - demand
            if new_amount > 0:
                self._conn.execute("""UPDATE vaccines SET quantity=? WHERE id=?""", [new_amount, vaccine.id])
                self.logistics.update_count_sent(self.clinics.get_logistic_id(clinic_name), demand)
                break
            elif new_amount == 0:
                self._conn.execute("""DELETE FROM vaccines WHERE id=?""", [vaccine.id])
                self.logistics.update_count_sent(self.clinics.get_logistic_id(clinic_name), demand)
                break
            else:
                self._conn.execute("""DELETE FROM vaccines WHERE id=?""", [vaccine.id])
                demand = demand - vaccine.quantity
                self.logistics.update_count_sent(self.clinics.get_logistic_id(clinic_name), vaccine.quantity)
            i = i + 1

    def create_tables(self):
        if self.isExist:
            self._conn.executescript("""DROP  TABLE vaccines""")
            self._conn.executescript("""DROP  TABLE suppliers""")
            self._conn.executescript("""DROP  TABLE clinics""")
            self._conn.executescript("""DROP  TABLE logistics""")

        self._conn.executescript("""
        CREATE TABLE vaccines (
                id       INTEGER            PRIMARY KEY,
                date     DATE               NOT NULL,
                supplier INTEGER REFERENCES suppliers(id),
                quantity INTEGER            NOT NULL 
            );

        CREATE TABLE suppliers (
                id       INTEGER            PRIMARY KEY,
                name     STRING             NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );

        CREATE TABLE clinics (
                id       INTEGER            PRIMARY KEY,
                location STRING             NOT NULL,
                demand   INTEGER            NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );

          CREATE TABLE logistics (
                id             INTEGER     PRIMARY KEY,
                name           STRING      NOT NULL,
                count_sent     INTEGER     NOT NULL,
                count_received INTEGER     NOT NULL

              );
      """)


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
