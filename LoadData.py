import sys
from DTO import Vaccine, Clinic, Supplier, Logistic
# from _Repository import repo


def main(args):
    # repo.create_tables()
    input = args[1]
    with open(input) as inputFile:
        #decode amounts of each
        amounts = (inputFile.readline().replace("\n","").split(","))
        for i in range(1, int(amounts[0])+1):
            next = inputFile.readline().replace("\n","").split(",")
            vaccine = Vaccine(*next)
            print(vars(vaccine))
            #repo.Vaccines.insert(Vaccine)
        # for i in range(1, int(amounts[1])+1):
        #     print(i)
        # for i in range(1, int(amounts[2])+1):
        #     next = inputFile.readline()
        #     print(next.split(","))
if __name__ == '__main__':
    main(sys.argv)