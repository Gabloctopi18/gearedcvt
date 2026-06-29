# Geared, Bi-directional CVT
A continously variable transmission that is fully geared and is bi-directional. I was heavily inspired by RatioZero.
Here is the link to the CAD: [https://cad.onshape.com/documents/c369754a085e1b437744081a/w/8784f23027b47ba880d55ef1/e/7f96dc46c879863ea30c1be9?renderMode=0&uiState=6a407643a70a739b238820a7](url)

Here is my project on stardance: [https://stardance.hackclub.com/projects/4431](url)

<img width="785" height="737" alt="image" src="https://github.com/user-attachments/assets/25d12f0b-6e16-4e5c-a0bb-49445688ba56" />

## Context
### What is a CVT? Why CVT?
A CVT (continously variable transmission) is a gearbox which allows an infinite, continuous range of gear ratios. Unlike normal gearboxes or gear switchers, which have fixed gear ratios and sharp switching between them, a CVT allows any gear ratio between it's mechanical limits (dependent on the mechanical design). For automotive industries, CVTs are used to keep engines at optimal efficiency RPM (deviations greatly reduce efficiency) and instead change speed by varying the gear ratio. However, my CVT is meant to be used in robotics: instead of compromising between speed and torque, a CVT allows both torque and speed modes in one gearbox. Robots that are used in a wide range of scenarios and load conditions benefit from it: it can choose the optimal gear ratio for each desired action.
### Why geared? Why bi-directional?
I chose to design a geared CVT mainly becaues I thought it looked really cool. Theoretically, geared CVTs are more efficient than typical belted CVTs because gears are inherently more efficient than belts. Furthermore, belted CVTs rely solely on friction, while geared CVTs rely on the mechanical interlocking of gears, redicuing manufacturing costs. One really good and popular Geared CVT design is the RatioZero. However, that gearbox is not bi-directional because it relies on one-way bearings: when you spin the input in reverse, the ouput doesn't spin. This also implies that there is no inherent braking mechanism. In many robotics applications, it is not feasible to use another actuator as a brake, and it is often necessary for the gearbox to be able to spin in both ways (think of a robotic arm or a mecanum drivetrain for example). My CVT is fully geared and bi-directional.

## How it works

Here is a brief overview of how the whole thing works. I recommend taking a look at the CAD because it's hard to explain stuff with only images.

### Rotation Splitting
The key idea for the geared CVT is rotation splitting. The blue gear is the input gear, belted to an actuator (the belt or pulley isn't shown in the picture). Note that the input coaxial but NOT attached to the hex shaft in the center. The input gear meshes with the two gray gears. Attatched to the gray gears is an arm, which slides up and down in the slot of the gray gear. The other end is attached to another shaft. The sliding up and down is resposible for the gear shifting. When the arm is close the the center of the gray gear, the radius is small, which lowers the speed during one full rotation (the speed is $2\pi r\omega$, $\omega$ is fixed). As a result, the output torque is magnified (think of it like a seesaw, where the driven end is much shorter than the driving end). The opposite happens when the arms moves further from the center of the gray gear; the speed is increased and the torque decreases. Therefore, the gear ratio is determined by the distance from the arm to the center of the gray gear. The way the distance is changed will be explained later. Interestingly, note that the arm could move to the center of the gray gear, which implies the gear ratio is 0:1 and the output is completely independent of the input.

The second stage (other end of the arm) is designed to have 95 degrees of range. You may also note that the motion is somewhat sinusoidal (not exactly because the pushing and pulling isn't symmetric, see the math folder for that). The four gray gears have their slots 90 degrees offset from eachother. The output gear is driven only during a quarter of the gray gear's period, in the middle of the wave. Therefore, the output gear is always moving in the same direction and hardly oscillates. This is why it's called rotation splitting.

<img width="758" height="739" alt="image" src="https://github.com/user-attachments/assets/eff67895-d4a6-4171-a2fb-d955d1b8453b" />

### the Selector
As mentioned previously, the second stage only drives the output during a quarter of it's period. Since all four gears are offset in phase by 90 degrees, the driven gear is constantly powered. The selection of which gear to mesh is done with a perependicular cam (I couldn't find or come up with a better name for it). On the other side of the second stage from the last section are four gears which are coaxial but NOT attatched to the second stage of shafts (one for each gear). These gears have dog clutch teeth. The gears are constantly meshed to the orange gear in the center, which is live axle onto the main center shaft. Right next to it are two dog clutches, each pointing to the gears mentioned above. The dog clutch is mounted on a linear bearing which is live axle to the second stage of shafts. 

For one gray gear tube (it's mirrored on the other side) the slots are 180 degrees offset. Each of the gears on the same side is offset by 90 degrees.

The dog clutch is linked to a linear cam. The linear cam is powered by a third gear meshing with the input. The dog clutches from each side come to sandwich the cam between two bearings, which makes the dog clutches move along with the shape of the cam. The bearing sandwich from the dog clutches on each side meet at a 90 degree angle, which means the positions between those two dog clutches are 90 degrees offset from eachother. Since the thickness of the cam says the same, the two dog clutches on one side of the gearbox are 180 degrees offset from eachother. This combination means only one gear will mesh with the output gear at a time, each for a quarter of the period. This is combined with the gear shifting described in the previous section so the output gear can vary its gear ratio.

<img width="607" height="600" alt="image" src="https://github.com/user-attachments/assets/114c1926-8470-40e0-aa93-f05c770173de" /> <img width="682" height="503" alt="image" src="https://github.com/user-attachments/assets/e60f847c-d52e-4de8-a508-bcc6f7feab1d" /> <img width="729" height="374" alt="image" src="https://github.com/user-attachments/assets/d4966215-95e7-472f-b469-61c03e102ef5" />

### the Gear Shifter
This section covers how the arm changes radius. This was a challenge because it also has to rotate on it's axis. Inside the tubes of the gray gears is a linear CAM. moving the cam causes a rider (the blue part), secured with two linear bearings mounted to dowel pins, to move up and down. The linear cam is attached to a ring outside the tube, which is sandwiched between two bearings. The bearings are attached to a lead screw nut mounted on a leadscrew. This way, the linear can can rotate about it's axis, but when the lead screw turns, it moves the linear cam, causing the gear ratio to change. Note that the cam is mirrored to the other side: this way, each of the riders are at the same position in the slot.
<img width="930" height="618" alt="image" src="https://github.com/user-attachments/assets/8de19e06-7882-4395-a7f3-71b49374341b" />
<img width="1115" height="812" alt="image" src="https://github.com/user-attachments/assets/34ad5f46-88b4-4fe8-b4fb-055087a3d982" />



