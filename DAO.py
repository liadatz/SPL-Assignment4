from DTO import Vaccine, Supplier, Clinic, Logistic


class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO Vaccines (id, date ,supplier, quantity) VALUES (?, ?, ? ,?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def getNumberOfVaccines(self):
        c = self._conn.cursor()
        c.execute("""SELECT COUNT(*) FROM Vaccines""")
        return c.fetchone()[0]  # or all?

    def update(self, suppliers_id, amount_orig):
        c = self._conn.cursor()
        c.execute("""SELECT id, quantity FROM Vaccines WHERE supplier IN (1, 2)""")
        vaccines = c.fetchall()
        i = 0
        amount = int(amount_orig)
        print(vaccines)
        while i < len(vaccines) and amount > 0:
            vaccine = vaccines[i]
            new_amount = int(vaccine[1]) - amount
            print(new_amount)
            if new_amount > 0:
                self._conn.execute("""UPDATE Vaccines SET quantity=? WHERE id=?""", [new_amount, vaccine[0]])
            elif new_amount == 0:
                self._conn.execute("""DELETE FROM Vaccines WHERE id=?""", [vaccine[0]])
                amount = amount - vaccine[1]
                print("equal zero")
            else:
                self._conn.execute("""DELETE FROM Vaccines WHERE id=?""", [vaccine[0]])
                amount = amount - vaccine[1]
                print("below zero")
            i = i + 1

class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""INSERT INTO Suppliers (id, name, logistic) VALUES (?, ?, ?)""",
                           [Supplier.id, Supplier.name, Supplier.logistic])

    def getID(self, name):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM Suppliers WHERE name=?""", [name])
        return c.fetchone()[0]

    def get_suppliers(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM Suppliers WHERE logistic=?""", [logistic_id])
        return c.fetchall()

    def get_logistic(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""SELECT logistic FROM Suppliers WHERE name=?""", [supplier_name])
        return c.fetchone()[0]


class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Clinic):
        self._conn.execute("""
               INSERT INTO Clinics (id, location, demand, logistic) VALUES (?, ?, ? ,?)
           """, [Clinic.id, Clinic.location, Clinic.demand, Clinic.logistic])

    def update_amount(self, location, received):
        self._conn.execute("""UPDATE Clinics SET demand=demand-? WHERE location=?""", [received, location])

    def get_logistic_id(self, location):
        c = self._conn.cursor()
        c.execute("""SELECT logistic FROM Clinics WHERE location=?""", [location])
        return c.fetchone()[0]


class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Logistic):
        self._conn.execute("""
               INSERT INTO Logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [Logistic.id, Logistic.name, Logistic.count_sent, Logistic.count_received])

    def update_count_received(self, logistic_id, received):
        self._conn.execute("""UPDATE Logistics SET count_received=count_received+? WHERE id=?""", [received, logistic_id])

    def update_count_sent(self, logistic_id, sent):
        self._conn.execute("""UPDATE Logistics SET count_sent=count_sent+? WHERE id=?""", [sent, logistic_id])
