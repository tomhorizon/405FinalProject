# Overview - Learn by Dueling

![Figure 0: Early concept art of the turret (Fusion 360).](imgInitialRender.png)

This project was a showcase of all programming and hardware skills acquired over the last two quarters of our Mechatronics education. The goal of the project was to integrate motor control, sensors, communication protocols, and inspire creativity with an open-ended design.

The competition goal was to create a machine that uses a thermal camera to direct a nerf dart to an opponent in the shortest amount of time. The rules were simple - each time has five seconds to rotate their machine from rear facing to front facing, acquire a target, and ten seconds to fire. The first team to land a hit scored three points, the second team to hit scored one point, any misses subtracted a point, and any subsequent hits did not affect the score.

This exercise is an early study on the possibility of targetting embers falling through the sky and precisely extinguishing them before they have a chance to cause further wildfire damage. In theory, a network of these machines that use thermal data for targetting can prevent the spread of fires.

# Hardware
## Mechanical

The machine is actuated by two 200rpm 24v encoded motors to control rotation and pitch. With an internal gearing of 50:1 and an external gearing of 4:1, the machine is able to rotate about either axis at 1 revolution per second. Two 24v 12,000rpm motors with 5" diameter flywheels enthusiastically send darts down a lightweight 12" aluminum barrel. A maximum of 12 Nerf Accustrike darts are fed from a factory magazine, which are pushed into the path of the flywheels by a 25kg 180deg hobby servo linked by pin and slot mechanism to a custom machined 3/8" firing rod. A custom 3D printed receiver supports the magazine, firing rod, and rear of the barrel. The support structure is a combination of laser cut 12g steel and 3D printed pivot mechanisms. The base of the machine rotates on an 8" lazy Susan ball bearing unit. It is bolted to a bespoke wooden base with adequate clearance for the yaw gearing. This is further supported by a brake disc to prevent slipping and under-rotation of the turret. To add to the overall aesthetic of the design, a 3.3-24V alarm and three 5V pre-resisted red LEDs alert to the opponent of their approaching fate.


![Figure 1: Final system render.](/imgFullTurret2.png)

![Figure 2: Motors and gear system.](/imgMotorsAndGearing.png)

![Figure 3: Front firing group assembly.](/imgForwardFiringGroup.png)

![Figure 4: Rear firing group assembly.](/imgRearFiringGroup.png)

## Electronics

All electronics are secured to a custom 3D printed electronics control box. They are powered by a 24V 15A power supply with an emergency stop and 15A fuse. This is stepped down to provide 7.9V to the hobby servo and 5V to the control logic, encoders, and LEDs. 

The 24V motors are powered by two Dual L298 DC Motor drivers. A limit switch on a tether is used as a "start" button to signal the machine to start a new round. A Melexis MLX90640 thermal camera mounted to the barrel provides machine vision.

![Figure 5: Control box rendering.](/imgControlBox.png)

![Figure 6: Wiring diagram.](/imgWiringDiagram.png)


# Software

An overview of the software design. This should be brief and general, with a link to your Doxygen pages -- the pages describe the details of the software, so there's no need to repeat that here.

**dylan and jonathan**

Our software utilizes i2c communication to capture images from an infrared camera. 
The captured images are then processed using a targeting algorithm to detect human
targets. Once a target has been detected, a PID control algorithm is employed to 
control the encoder motors, which are used to fire a Nerf dart accurately towards
our target.

![Figure 7: Nucleo pinout.](/imgPinout.png)


# Results

A discussion of the results.  How did you test your system?  How well has your system performed in these tests?

**dylan and jonathan**

During the testing phase of the system, we ensured that the firing pin had a 
consistent and reliable range of motion, which was achieved by using a servo 
and linkage mechanism. We also tested the flywheels to ensure that they 
propelled the dart straight towards the target and did not draw too much 
current, which could affect the system's overall performance.

The pitch and yaw movement were tested to verify that the system was capable 
of accurately aiming the Nerf dart towards the target. The accuracy of the 
targeting algorithm was also tested to ensure that it correctly identified and 
tracked human targets, further enhancing the precision of the system. We
ended up fine tuning our algortihm with small offsets to pitch and yaw to ensure
it more frequently hit our human targets.

![Figure 8: Final production unit.](/imgRealFullTurret.jpg)

![Figure 9: Front view.](/imgRealTurretFront.jpg)

![Figure 10: Topdown view.](/imgRealTopDown.jpg)

## Takeaways

A brief discussion of what you've learned about the project and recommendations for anyone who would like to build upon your work. This does not mean a discussion of what you learned about mechatronics in general; that belongs in other places.  It is a discussion of what worked well and what didn't for this device.

**dylan and jonathan**

Overall, building our own system rather than relying on pre-existing Nerf hardware
was a success, as it allowed us to create a more intricate and finished design. 
We also had ample time to put into the project, which allowed us to thoroughly test
each subsystem and the system as a whole, which was critical in identifying issues 
and debugging them.

However, certain algorithms, such as the weighted average for targeting, did not 
work as well as we had hoped. Along with this, pure propotional control with a single
fixed setpoint caused constant overshooting, which affected the accuracy of the 
system. Additionally, the vibrations from the flywheels caused issues with the 
overall stability of the system and led to certain other systems failing or becoming
unreliable.

# Links
Compilation of duels conducted during on championship day (3/17/2023):
https://youtu.be/L2fNEF87ndI

Close-up view of turret during a duel:
https://youtu.be/JrsSzEOzaZ4

**docugen**

**links to all parts in discord**
