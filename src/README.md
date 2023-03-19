Overview - Learn by Dueling

This project was a showcase of all programming and hardware skills acquired over the last two quarters of our Mechatronics education. The goal of the project was to integrate motor control, sensors, communication protocols, and inspire creativity with an open-ended design.

The competition goal was to create a machine that uses a thermal camera to direct a nerf dart to an opponent in the shortest amount of time. The rules were simple - each time has five seconds to rotate their machine from rear facing to front facing, acquire a target, and ten seconds to fire. The first time to land a hit scored three points, the second team to hit scored one point, any misses subtracted a point, and any subsequent hits did not affect the score.

This exercise is an early study on the possibility of targetting embers falling through the sky and precisely extinguishing them before they have a chance to cause further wildfire damage. In theory, a network of these machines that use thermal data for targetting can prevent the spread of fires.


Mechanical Hardware

The machine is actuated by two 200rpm 24v encoded motors to control rotation and pitch. With an internal gearing of 50:1 and an external gearing of 4:1, the machine is able to rotate about either axis at 1 revolution per second. Two 24v 12,000rpm motors with 5" diameter flywheels enthusiastically send darts down a lightweight 12" aluminum barrel. A maximum of 12 Nerf Accustrike darts are fed from a factory magazine, which are pushed between the flywheels by a 25kg 180deg hobby servo linked by pin and slot mechanism to a custom machined 3/8" firing rod. A custom 3D printed receiver supports the magazine, firing rod, and rear of the barrel.

The support structure is a combination of laser cut 12g steel and 3D printed pivot mechanisms. All pivots are supported by 1/4" steel D shaft on bearings pressed into place. Heatset inserts were used extensively in the 3D printed parts in M3 and M4 sizes to fassten parts.

The base of the machine is an 8" lazy Susan ball bearing unit. It is bolted to a bespoke wooden base with adequate clearance for the yaw gearing. This is further supported by a brake disc to prevent slipping and under-rotation of the turret. 

To add to the overall aesthetic of the design, a 3.3-24V alarm and three 5V pre-resisted red LEDs alert to the opponent of their approaching fate. 

![Figure 1: Full system render (Fusion 360).](/imgFullTurret.png)

![Figure 2: Motors and gear system.](/imgMotorsAndGearing.png)

![Figure 3: Front firing group assembly.](/imgForwardFiringGroup.png)

![Figure 4: Rear firing group assembly.](/imgRearFiringGroup.png)


Electronic Hardware

All electronics are secured to a custom 3D printed electronics control box. They are powered by a 24V 15A power supply with an emergency stop and 15A fuse. This is stepped down to provide 7.9V to the hobby servo and 5V to the control logic, encoders, and LEDs. 

The 24V motors are powered by two Dual L298 DC Motor drivers. A limit switch on a tether is used as a "start" button to signal the machine to start a new round. A Melexis MLX90640 thermal camera mounted to the barrel provides machine vision.

![Figure 5: Control box rendering.](/imgControlBox.png)

![Figure 6: Wiring diagram.](/imgWiringDiagram.png)


Software

An overview of the software design. This should be brief and general, with a link to your Doxygen pages -- the pages describe the details of the software, so there's no need to repeat that here.

**dylan and jonathan**

![Figure 7: Nucleo pinout.](/imgPinout.png)


Results

A discussion of the results.  How did you test your system?  How well has your system performed in these tests?

**dylan and jonathan**

![Figure 8: Final production unit.](/imgRealFullTurret.jpeg)

![Figure 9: Front view.](/imgRealTurretFront.jpeg)

![Figure 10: Topdown view.](/imgRealTopDown.jpeg)

Takeaways

A brief discussion of what you've learned about the project and recommendations for anyone who would like to build upon your work. This does not mean a discussion of what you learned about mechatronics in general; that belongs in other places.  It is a discussion of what worked well and what didn't for this device.

**dylan and jonathan**


Links

**docugen**

**links to all parts in discord**
