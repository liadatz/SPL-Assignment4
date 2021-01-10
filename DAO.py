from DTO import Vaccine, Supplier, Clinic, Logistic

class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO Vaccines (id, date ,supplier, quantity) VALUES (?, ?, ? ,?)
           """, [vaccine.id, vaccine.date , vaccine.supplier , vaccine.quantity])


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""
               INSERT INTO Suppliers (id, name, logistic) VALUES (?, ? ,?)
           """, [Supplier.id, Supplier.name , Supplier.logistic])


class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Clinic):
        self._conn.execute("""
               INSERT INTO Clinics (id, location, demand, logistic) VALUES (?, ?, ? ,?)
           """, [Clinic.id, Clinic.location , Clinic.demand , Clinic.logistic])

    # def find(self, product_id):
    #     c = self._conn.cursor()
    #     c.execute("""
    #         SELECT  *FROM Products WHERE id = ?
    #     """, [product_id])
    #
    #     return Product(*c.fetchone())
    #
    # def update(self, product):
    #     self._conn.execute("""
    #            UPDATE Products SET quantity=(?) WHERE id=(?)
    #        """, [product.quantity, product.id])


class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Logistic):
        self._conn.execute("""
               INSERT INTO Logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [Logistic.id, Logistic.name , Logistic.count_sent, Logistic.count_received])

