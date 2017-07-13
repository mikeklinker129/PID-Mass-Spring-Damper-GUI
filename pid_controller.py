import numpy as numpy



class PID_Controller():
    def __init__(self,parent_gui,dt):


        self.gui = parent_gui

        self.kp = self.gui.slide_p.get()
        self.kd = self.gui.slide_d.get()
        self.ki = self.gui.slide_i.get()

        self._dt = dt

        self.e_integrated = 0
        self.e_prev = None
        self.control_output = [0,0,0]

    def run(self,state,reference):
        error = reference - state[0]
        if self.e_prev==None:
            e_dot=0
        else:      
            e_dot = (error - self.e_prev) / self._dt
        self.e_integrated += error

        proportional =  self.kp * error
        integral =      self.ki * self.e_integrated
        derivative =    self.kd * e_dot

        self.e_prev = error

        #This is the force output!
        self.control_output = [proportional,integral,derivative]