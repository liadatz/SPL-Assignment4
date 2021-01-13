class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date ,supplier, quantity) VALUES (?, ?, ? ,?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def getNumberOfVaccines(self):
        c = self._conn.cursor()
        c.execute("""SELECT MAX(id) FROM vaccines""")
        return c.fetchone()[0]


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)""",
                           [supplier.id, supplier.name, supplier.logistic])

    def getID(self, name):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM suppliers WHERE name=?""", [name])
        return c.fetchone()[0]

    def get_suppliers(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM suppliers WHERE logistic=?""", [logistic_id])
        return c.fetchall()

    def get_logistic_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""SELECT logistic FROM suppliers WHERE name=?""", [supplier_name])
        return c.fetchone()[0]

    def get_logistic_by_id(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""SELECT logistic FROM suppliers WHERE id=?""", [supplier_id])
        return c.fetchone()[0]


class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ? ,?)
           """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def update_amount(self, location, received):
        self._conn.execute("""UPDATE clinics SET demand=demand-? WHERE location=?""", [received, location])

    def get_logistic_id(self, location):
        c = self._conn.cursor()
        c.execute("""SELECT logistic FROM clinics WHERE location=?""", [location])
        return c.fetchone()[0]


class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def update_count_received(self, logistic_id, received):
        self._conn.execute("""UPDATE logistics SET count_received=count_received+? WHERE id=?""",
                           [received, logistic_id])

    def update_count_sent(self, logistic_id, sent):
        self._conn.execute("""UPDATE logistics SET count_sent=count_sent+? WHERE id=?""", [sent, logistic_id])
