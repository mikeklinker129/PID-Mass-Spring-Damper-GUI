import numpy as np
import Tkinter
import time
import sys
import datetime
import matplotlib.pyplot as plt

from mass_model import MassModel
from pid_controller import PID_Controller
from bangbang_controller import BB_Controller

class PID_GUI():


    def __init__(self,controller,spring,damper, time_r = 10):
        self.master = Tkinter.Tk()
        self.master.title("PID Mass-Spring-Damper")



        self.w_width = 850
        self.w_height = 400

        self.init_pos = [400,100]
        self.ref=0
        self.last_x = 0

        self.USE_SPRING = spring
        self.USE_DAMPER = damper
        self.MODE = controller
        self.TIME_RUN = time_r
        
        self.w = Tkinter.Canvas(self.master,width=self.w_width,height=self.w_height)

        x0 = self.init_pos[0]
        y0 = self.init_pos[1]
        self.block = self.w.create_rectangle(x0-40,y0-40, x0+40, y0+40, fill="black")

        if self.MODE == 'pid':
            self.c_p = self.w.create_line(x0,300,x0+5,300,fill='green', width='8')
            self.c_i = self.w.create_line(x0,300,x0+5,300,fill='blue', width='8')
            self.c_d = self.w.create_line(x0,300,x0+5,300,fill='red', width='8')
        elif self.MODE == 'bangbang':
            self.c_p = self.w.create_line(x0,300,x0+5,300,fill='purple', width='8')

        self.draw_background()
        self.Spring = SpringDamper(self.master,self.w,self.USE_SPRING,self.USE_DAMPER,50,75,self.init_pos[0])
        self.draw_labels()

        Tkinter.Label(self.master, text="Built by Mike Klinker 2017").place(x=650, y=10)

        self.initial_mass_state = [0,0]
        self.update_mass(self.initial_mass_state)

        self.slide_ref  = Tkinter.Scale(self.master,label='Reference Location', from_=-3,to=3,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
        self.slide_init = Tkinter.Scale(self.master,label='Initial Location', from_=-3,to=3,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
        self.slide_init.set(0)
        self.slide_ref.set(1)

        if self.MODE == 'pid':
            self.slide_p = Tkinter.Scale(self.master,label='P Gain', from_=0,to=25,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
            self.slide_i = Tkinter.Scale(self.master,label='I Gain', from_=0,to=2,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
            self.slide_d = Tkinter.Scale(self.master,label='D Gain', from_=0,to=25,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
            self.slide_p.set(20)
            self.slide_i.set(.5)
            self.slide_d.set(10)
        elif self.MODE == 'bangbang':
            self.slide_F = Tkinter.Scale(self.master,label='Force In Newtons', from_=0,to=25,length=200, resolution=0.1, orient=Tkinter.HORIZONTAL)
            self.slide_F.set(5)



        self.start_button = Tkinter.Button(self.master, text='Start Controls Simulation',command=self.run_sim)

        self.w.pack()

        self.slide_init.pack()
        self.slide_ref.pack()

        Tkinter.Frame(self.master,relief=Tkinter.RIDGE,height=2,width = 500, bg='black').pack(pady=10)

        if self.MODE == 'pid':
            self.slide_p.pack()
            self.slide_i.pack()
            self.slide_d.pack()
        elif self.MODE == 'bangbang':
            self.slide_F.pack()

        self.start_button.pack()


    def manage_inputs(self):
        self.initial_mass_state = [self.slide_init.get(),0]
        self.ref = self.slide_ref.get()

    def draw_labels(self):
        Tkinter.Label(self.master, text="0m").place(x=self.init_pos[0]-10, y=255)
        Tkinter.Label(self.master, text="1m").place(x=self.init_pos[0]-10+100, y=255)
        Tkinter.Label(self.master, text="2m").place(x=self.init_pos[0]-10+200, y=255)
        Tkinter.Label(self.master, text="3m").place(x=self.init_pos[0]-10+300, y=255)
        Tkinter.Label(self.master, text="-1m").place(x=self.init_pos[0]-10-100, y=255)
        Tkinter.Label(self.master, text="-2m").place(x=self.init_pos[0]-10-200, y=255)
        Tkinter.Label(self.master, text="-3m").place(x=self.init_pos[0]-10-300, y=255)

        if self.MODE == 'pid':
            label1 = Tkinter.Label(self.master, text="Proportional Control Effort",fg='purple')
            label2 = Tkinter.Label(self.master, text="Integral Control Effort",fg='blue')
            label3 = Tkinter.Label(self.master, text="Derivative Control Effort",fg='red')
            base = 290
            label1.place(x=25,y=base)
            label2.place(x=25,y=base+20)
            label3.place(x=25,y=base+40)

        elif self.MODE == 'bangbang':
            label1 = Tkinter.Label(self.master, text="Control Effort",fg='purple')
            label1.place(x=25,y=290)

        #Makes the sim too slow.
    # def time_label(self):
    #     #label = Tkinter.Label(self.master, text="Time Ellapsed: %.2f sec" %self.mass.t)
    #     var = Tkinter.StringVar()
    #     varstr = 'Time Ellapsed: %.1f sec' %self.mass.t
        
    #     var.set(varstr)    
    #     label = Tkinter.Label(self.master, textvariable = var)
    #     label.place(x=25, y=25)



    def draw_background(self):
        floor = 250
        ceiling = 50
        self.w.create_line(50,ceiling ,50,floor,width=3)
        self.w.create_line(50,floor,self.w_width-50,floor,width=3)
        self.w.create_line(self.init_pos[0],floor,self.init_pos[0],ceiling,dash=(5,5))

    def draw_reference(self,ref):
        try:
            self.w.delete(self.ref_line)
            self.w.delete(self.ref_label)
        except:
            pass

        floor = 250
        ceiling = 50
    
        self.ref_line = self.w.create_line(self.init_pos[0]+ref*100,floor,self.init_pos[0]+ref*100,ceiling,fill='green')

        self.ref_label = Tkinter.Label(self.master, text="Reference\nlocation",fg='green')
        ref_pix = self.init_pos[0]+100
        self.ref_label.place(x=ref_pix,y=ceiling-30)


    def update_mass(self,X):


        #Conversion is 1m = 100 pixels. 
        width = 75
        height = 75
        dx = X[0]*100 - self.last_x

        self.last_x+=dx
        self.w.move(self.block,dx,0)
        self.Spring.update(X[0]*100+self.init_pos[0])


    def draw_control_effort(self,control_output):

        if self.MODE=='pid':
            p = control_output[0]*10
            i = control_output[1]*10
            d = control_output[2]*10

            x0 = self.init_pos[0]
            self.w.delete(self.c_p)
            self.w.delete(self.c_i)
            self.w.delete(self.c_d)
            self.c_p = self.w.create_line(x0,300,x0+p,300,fill='purple', width='8')
            self.c_i = self.w.create_line(x0,300+20,x0+i,300+20,fill='blue', width='8')
            self.c_d = self.w.create_line(x0,300+40,x0+d,300+40,fill='red', width='8')

        elif self.MODE == 'bangbang':
            p = control_output[0]*10
            x0 = self.init_pos[0]

            self.w.delete(self.c_p)
            self.c_p = self.w.create_line(x0,300,x0+p,300,fill='purple', width='8')



    def step_info(self,t,yout,ref):
        step_size = np.abs(yout[0]-ref)
        #print "OS: %f%s"%( ((yout.max()-yout[0]-step_size)/step_size) *100,'%' )
        #print "Tr: %fs"%(t[next(i for i in range(0,len(yout)-1) if yout[i]>yout[-1]*.90)]-t[0])
        #print "Ts: %fs"%(t[next(len(yout)-i for i in range(2,len(yout)-1) if abs(yout[-i]/yout[-1])>1.02)]-t[0])

        os_str = 'Overshoot: %.1f ' %(((yout.max()-yout[0]-step_size)/step_size)*100) +'%'
        Tkinter.Label(self.master,text = os_str, font=("Helvetica", 16)).place(x=550,y=320)
        tr_str = 'Rise Time: %.2f sec' %(t[next(i for i in range(0,len(yout)-1) if yout[i]>yout[-1]*.90)]-t[0])
        Tkinter.Label(self.master,text = tr_str, font=("Helvetica", 16)).place(x=550,y=350)
        sse_str = 'Steady State Error: %.1f ' %( (yout[-1]-ref)/step_size *100  ) +'%'
        Tkinter.Label(self.master,text = sse_str, font=("Helvetica", 16)).place(x=550,y=380)


    def run_sim(self):
        dt = .02
        self.manage_inputs()
        self.mass = MassModel(self,self.initial_mass_state,dt)

        if self.MODE=='pid':
            controller = PID_Controller(self,dt)
        else:
            controller = BB_Controller(self,dt)

        ref = self.ref #meters
        self.draw_reference(ref)    

        xt = [self.mass.X[0],self.mass.X[0]]
        tt = [-1,0]
        rt = [self.initial_mass_state[0],self.initial_mass_state[0]]
        ut = [0,0]

        t_end = self.TIME_RUN #seconds

        count = 0

        while self.mass.t<t_end:

            count+=1
            if (count%10)==0:
                print "time: %.2f" %self.mass.t

            t0 = datetime.datetime.now()

            tt.append(self.mass.t)
            xt.append(self.mass.X[0])
            ut.append(sum(controller.control_output))
            rt.append(ref)

            gui.update_mass(self.mass.X)
            controller.run(self.mass.X,ref)
            control = controller.control_output
            self.draw_control_effort(control)

            self.mass.step_time_forward(sum(control))
            self.master.update_idletasks()
            self.master.update()

            t1 = datetime.datetime.now()
            dt_actual = (t1-t0).total_seconds()
            if dt_actual<dt:
                time.sleep(dt-dt_actual)
            else:
                time.sleep(.005)

        self.step_info(np.array(tt),np.array(xt),ref)

        line1, = plt.plot(tt,xt, label='Block Location X(t)')
        line2, = plt.plot(tt,rt,'g--',label='Reference Command R(t)')
        plt.ylabel('x(t) (meters)')
        plt.xlabel('Time (seconds)')
        #plt.axis([-1, t_end, -.5, 1.5])
        plt.legend(handles=[line1,line2])
        plt.show()




class SpringDamper(object):
    def __init__(self,master,canvas,USE_SPRING,USE_DAMPER,x0,y0,x1):
        self.master = master
        self.w = canvas

        self.USE_SPRING = USE_SPRING
        self.USE_DAMPER = USE_DAMPER

        self.x0 = x0
        self.y0 = y0
        self.spring_lines = []
        spring = self.update(x1)



    def update(self,x1):

        y0 = self.y0
        y1 = self.y0+30

        sections = 4

        x0 = self.x0

        for line in self.spring_lines:
            self.w.delete(line)


        for i in range(0,sections):
            st = (x1-x0)/sections*i+x0
            sp = (x1-x0)/sections*(i+1)+x0
            
            if self.USE_SPRING:
                line1 = self.w.create_line(st,y0,sp,y1)
                line2 = self.w.create_line(sp,y0,sp,y1)
                self.spring_lines.append(line1)
                self.spring_lines.append(line2)

        if self.USE_DAMPER:
            damper1 = self.w.create_line(x0,y0+40,x1-30,y0+40,width=6)
            damper2 = self.w.create_line(x0,y0+40,x0+75,y0+40,width=12) #(x1-x0)/2+x0

        
            self.spring_lines.append(damper1)
            self.spring_lines.append(damper2)






if __name__ == "__main__":
    print("Executing as main program")

    args = sys.argv

    spring = 0
    damper = 0

    controller = args[1]

    print args
    if 'spring' in args:
        spring=1
    if 'damper' in args:
        damper=1

    #Last arg has to be time. 
    time_r = int(args[-1])

    if time_r<1:
        print 'PUT A REAL TIME IN PLEASE (last argument must a number of seconds more than 1'
        time_r=10

    dt = 0.01
    

    gui = PID_GUI(controller,spring,damper,time_r)
    # mass = MassModel(dt)
    # controller = PID_Controller(gui,dt)

    # ref = 2 #meters
    # gui.draw_reference(ref)

    while 1:
        time.sleep(.1)

    # while mass.t<10:
    #     gui.update_mass(mass.X)
    #     controller.run(mass.X,ref)
    #     control = controller.control_output
    #     gui.draw_control_effort(control)

    #     mass.step_time_forward(sum(control))
        gui.master.update_idletasks()
        gui.master.update()
    #     time.sleep(mass._dt/playback_multi)























