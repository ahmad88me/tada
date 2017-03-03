from learning import train, measure_representativeness, test


def main():
    training_files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
    model = train(training_files)
    repr = measure_representativeness(model, training_files)
    print "\nrepresentativeness of the training files is: \n"
    for i in xrange(len(repr)):
        print "%s: %f" % (training_files[i], repr[i])
    testing_files = ["novHighC.csv", "nodeid.csv"]
    test(model, testing_files)

if __name__ == "__main__":
    main()
