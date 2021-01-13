import sys
from DTO import Vaccine, Supplier, Clinic, Logistic
from _Repository import repo


def main(argv):
    loadData(argv[1])
    executeOrder(argv[2])


def loadData(path):
    repo.create_tables()
    with open(path) as inputFile:

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


def executeOrder(path):
    # repo.create_tables()
    with open(path) as inputFile:
        f = open("output.txt", "w")
        # decode amounts of each
        for line in inputFile:
            command = line.replace("\n", "").split(",")
            # receive shipment
            if len(command) == 3:
                vaccine = Vaccine(repo.vaccines.getNumberOfVaccines() + 1, command[2], repo.suppliers.getID(command[0]),
                                  command[1])
                repo.vaccines.insert(vaccine)
                logistic_id = repo.suppliers.get_logistic_by_name(command[0])
                repo.logistics.update_count_received(logistic_id, command[1])
            else:
                repo.pull_vaccines(command[0], int(command[1]))
                repo.clinics.update_amount(command[0], command[1])
            line = repo.get_output_addition()
            f.write(line)
        f.close()


if __name__ == '__main__':
    main(sys.argv)
