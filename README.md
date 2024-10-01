# ICRA2023 Transferability in Robotics Workshop 
## Augmenting Off-the-Shelf Grippers with Tactile Sensing
[Paper](https://doi.org/10.48550/arXiv.2306.05902) -- [Related work](https://doi.org/10.1109/LRA.2023.3284382)



The development of tactile sensing ad its fusion with computer vision is expected to enhance robotic systems in handling complex tasks like deformable object manipulation. However, readily available industrial grippers typically lack tactile feedback, which has led researchers to integrate and develop their own tactile sensors. This has resulted in a wide range of sensor hardware and difficulty in comparing tasksolving performance. We propose moving towards accessible open-source sensors and present a set of fingertips specifically designed for fine object manipulation, with readily interpretable data output. The fingertips are validated through two difficult tasks: cloth edge tracing and cable tracing. 

## Video material
Video material of the proof-of-concept experiments is provided in the videos folder.

## Hardware integration

<img align="right" width="400" src="https://github.com/RemkoPr/icra-2023-workshop-tactile-fingertips/blob/main/cad/3d/collapsed_view.png">

Currently the fingertips are designed for the Robotiq-2F85 gripper. This gripper can be mounted to various different collaborative robot arms by means of a tool flange. We provide a design for an intermediate flange, nestled between the Robotiq tool flange and the gripper itself, that provides external interfaces for the supply and ground pins otherwise reserved for the gripper. This way, the sensorised fingertips can draw their power straight from the robot arm. The intermediate flange consists of a pcb in the cad/pcb folder and two 3D printed parts in the cad/3d folder. Sensor readout is currently performed by an Arduino Nano 33 BLE externally mounted to the gripper via a 3D printed holder (see cad/3d), but we are in the process of integrating a microcontroller on our custom intermediate flange such that sensor readout and data transmission can also be done internally.  

<BR CLEAR="all">

## Software integration
Both Arduino firmware and python readout software is provided. Data is communicated between the arduino and a remote workstation via Bluetooth Low Energy. Further documentation on the software is provided in the code/python folder.

