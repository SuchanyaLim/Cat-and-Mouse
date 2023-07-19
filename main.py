import simulation

if __name__ == "__main__":

    sim0 = simulation.simulation(r"test_cases\Example0\trial.csv")
    cat = input("Input where the cat should move [1, 2, 3, 4, 5, 6] ")
    while cat != "":
        sim0.next_state(cat)
        print('------')
        cat = input("Input where the cat should move [1, 2, 3, 4, 5, 6] ")

