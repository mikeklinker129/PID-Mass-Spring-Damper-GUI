## PID-Mass-Spring-Damper-GUI

This is a simple GUI that includes a mass-spring-damper system, and a bang-bang or PID controller to control the masses position.

# Installation
First, you must run the installation script to install the necessary packages. It requires Python 2.7 and pip.

```
./install_requirements.sh
```

# Operation

The python gui is ran using the following arguments:
1. controller: options are 'bangbang' or 'pid'
2. dynamics: The default operation is no spring and no damper. If you want to include either of these systems, include enter 'spring' or 'damper' or 'spring damper' to activate each of the respective modes
3. time: enter an integer (seconds) that you want the simulation to run for

# Example Operation
```
$ python pid_gui.py bangbang 10  # This will run just the mass with a bangbang controller for 10 seconds. 
$ python pid_gui.py pid spring 5 # This will run the mass-spring system with a pid controller for 5 seconds. 
$ python pid_gui.py pid spring damper 20 # This will run the mass-spring-damper system with a pid controller for 20 seconds. 
```

After the time completes, a MatPlotLib window will show the system response. 
