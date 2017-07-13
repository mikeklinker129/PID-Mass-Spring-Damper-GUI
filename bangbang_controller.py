import numpy as numpy



class BB_Controller():
    def __init__(self,parent_gui,dt):


        self.gui = parent_gui

        self.F = self.gui.slide_F.get()

        self._dt = dt

        self.control_output = [0,0,0]

    def run(self,state,reference):
        error = reference - state[0]

        deadband = 0.02

        if error>deadband:
            force = self.F

        elif error<-deadband:
            force = -self.F

        else:
            force = 0

        #This is the force output!
        self.control_output = [force,0,0]



