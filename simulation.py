# Contains class implementation of the game state

import td_qlearning

class simulation:

    tiles = ['c', 'm', 'n', 'n', 'n', 'n']  #{'A':'c', 'B':'m', 'C':'n', 'D':'n', 'E':'n', 'F':'n'}
    mouse_loc = 1 #index of mouse             VVV
                                            # cat can be at any location except B
                                            # B is home base for mouse

    def __init__(self, file_path):
        '''
        Creates a simulation of the cat and mouse chase
        '''
        self.trial = td_qlearning.td_qlearning(file_path)
        self.start_sim(self.trial)

        return

    def __str__(self):
        
        rep = "------\n"

        for i in range(len(self.tiles)):
            if i == 3:
                rep += "\n"
            if self.tiles[i] != 'n':
                rep += "[{}]".format(self.tiles[i])
            else:
                rep += "[ ]"

        return rep
    
    def update_tiles(self, state):
        
        if state[1] == 7:
            (mloc,cloc) = self.state_to_int(state)
        else:
            mloc = state[0]
            cloc = state[1]
    
        for i in range(len(self.tiles)):
            self.tiles[i] = 'n'
        self.tiles[mloc] = 'm'
        self.mouse_loc = mloc
        self.tiles[cloc] = 'c'

        return
    
    def start_sim(self, trial):
        for state in trial.Qvalues.keys():
            self.update_tiles((state[0], 7))
            print(self)

        return

    def next_state(self, cat_loc):
        cat_loc = int(cat_loc)
        if (cat_loc == 1 or cat_loc > 5 or cat_loc < 0): 
            print("Invalid Move")
            print(self)
            return
        state = (self.mouse_loc, cat_loc)
        mouse_mov = self.trial.policy(self.state_to_char(state))
        new_mouse_loc = self.policy_interpreter(mouse_mov)

        new_state = (new_mouse_loc, cat_loc)
        self.update_tiles(new_state)
        
        return print(self)

    def policy_interpreter(self, policy):
        # all_actions = ["N", "L", "R", "U", "D"]
        mloc = self.mouse_loc
        match policy:
            case "N":
                mloc += 0
            case "L":
                mloc -= 1
            case "R":
                mloc += 1
            case "U":
                mloc -= 3
            case "D":
                mloc += 3

        return mloc
            
    def state_to_int(self, state):

        mloc = state[0][0]
        cloc = state[0][1]

        state_dict = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5}

        return (state_dict[mloc],state_dict[cloc])
        
    def state_to_char(self, state):

        mloc = state[0]
        cloc = state[1]

        state_dict = ['A', 'B', 'C', 'D', 'E', 'F']

        for i in range(len(state_dict)):
            if i == mloc:
                mloc = state_dict[i]
            if i == cloc:
                cloc = state_dict[i]

        return mloc+cloc