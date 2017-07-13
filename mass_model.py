import numpy as np



class MassModel(object):
    def __init__(self,parent,X,dt):

        self.USE_DAMPER = parent.USE_DAMPER
        self.USE_SPRING = parent.USE_SPRING

        self._M = 1.0 #kg
        self._b = 0.3*self.USE_DAMPER+.2 #N s/m # Need .2 of extra damping to make the sim numerical integration work. 
        self._k = 10.0*self.USE_SPRING #N/m

        self._dt = dt
        self.t = 0

        self.X = X #  [x, dx] Initial State


    def step_time_forward(self,F_input):

        d2x = -self._k/self._M*self.X[0]  - self._b/self._M*self.X[1] + F_input/self._M

        #X_K+1 = X_k + dx_k*dt
        x =  self.X[0] + self.X[1]*self._dt
        dx = self.X[1] + d2x*self._dt

        self.X = [x, dx]

        self.t+=self._dt












