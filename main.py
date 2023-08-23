import simulation

if __name__ == "__main__":

    sim0 = simulation.simulation(r"test_cases\Example3\trial.csv")
    cat = input("Input where the cat should move [0, 1, 2, 3, 4, 5] ")
    while cat != "":
        sim0.next_state(cat)
        print('------')
        cat = input("Input where the cat should move [0, 1, 2, 3, 4, 5] ")

