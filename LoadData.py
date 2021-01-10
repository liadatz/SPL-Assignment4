import sys

from DTO import Vaccine, Clinic, Supplier, Logistic
from _Repository import repo


def main(args):
    repo.create_tables()
    input = args[1]
    with open(input) as inputFile:

        # decode amounts of each type
        amounts = (inputFile.readline().replace("\n", "").split(","))

        # decode, create and insert all vaccines
        for i in range(1, int(amounts[0]) + 1):
            curr = inputFile.readline().replace("\n", "").split(",")
            vaccine = Vaccine(*curr)
            repo.vaccines.insert(vaccine)

        # creat and insert all suppliers
        for i in range(1, int(amounts[1]) + 1):
            curr = inputFile.readline().replace("\n", "").split(",")
            supplier = Supplier(*curr)
            repo.suppliers.insert(supplier)

        # creat and insert all clinics
        for i in range(1, int(amounts[2]) + 1):
            curr = inputFile.readline().replace("\n", "").split(",")
            clinic = Clinic(*curr)
            repo.clinics.insert(clinic)

        # creat and insert all logistics
        for i in range(1, int(amounts[3]) + 1):
            curr = inputFile.readline().replace("\n", "").split(",")
            logistic = Logistic(*curr)
            repo.logistics.insert(logistic)

if __name__ == '__main__':
    main(sys.argv)
