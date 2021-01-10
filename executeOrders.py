import sys
from DTO import Vaccine
from _Repository import repo


def main(args):
    # repo.create_tables()
    commands = args[1]
    with open(commands) as inputFile:
        f = open("output.txt", "w")
        # decode amounts of each
        for line in inputFile:
            command = line.replace("\n", "").split(",")
            # receive shipment
            if len(command) == 3:
                vaccine = Vaccine(repo.vaccines.getNumberOfVaccines()+1, command[2], repo.suppliers.getID(command[0]),
                                  command[1])
                repo.vaccines.insert(vaccine)
                logistic_id = repo.suppliers.get_logistic(command[0])
                repo.logistics.update_count_received(logistic_id, command[1])
            else:
                logistic_id = repo.clinics.get_logistic_id(command[0])
                suppliers_id = repo.suppliers.get_suppliers(logistic_id)
                repo.vaccines.update(suppliers_id, command[1])
                repo.clinics.update_amount(command[0], command[1])
                repo.logistics.update_count_sent(logistic_id, command[1])
            line = repo.get_output_addition()
            f.write(line)

        f.close()

if __name__ == '__main__':
    main(sys.argv)
