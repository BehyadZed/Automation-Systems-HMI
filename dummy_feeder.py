import time
from threading import Thread
import numpy as np

class Dummy_feeder:
    def __init__(self, no_of_random_states=3, no_of_controlled_states=3):
        self.no_of_random_states = no_of_random_states
        self.no_of_controlled_states = no_of_controlled_states
        self.random_states = np.zeros(no_of_random_states , dtype=int)
        self.controlled_states = np.ones(no_of_controlled_states , dtype=int)*2

        Thread(target=self.shuffle).start()
        
    def turn_on(self, controlled_state_no):
        self.controlled_states[controlled_state_no] = 1 

    def turn_off(self, controlled_state_no):
        self.controlled_states[controlled_state_no] = 0

    def rotate(self, controlled_state_no, delay = 1):
        Thread(target=self.rotate_handler, args=(controlled_state_no,delay,)).start()

    def rotate_handler(self, no, delay):
        self.controlled_states[no] = 1
        time.sleep(delay)
        self.controlled_states[no] = 0
    
    def shuffle(self):
        counter = True
        while True:
            if counter == True:
                for i in range(self.no_of_random_states):
                    self.random_states[i] = int(np.round(np.random.rand()))
                counter = False
                time.sleep(20)

            elif counter == False:
                time.sleep(20)
                counter == True   