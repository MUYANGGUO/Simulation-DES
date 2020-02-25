[![Authors](https://img.shields.io/badge/authors:-Muyang_Guo,_Wei_Zhao,_Shushu_Zhao,_Wenyue_Wang-blue.svg)](https://github.com/MUYANGGUO/Simulation-DES/graphs/contributors/)
[![Licence](https://img.shields.io/badge/license-GPL--3.0-green.svg)](https://github.com/MUYANGGUO/Simulation-DES/blob/master/LICENSE) 
&emsp;&emsp;[![Buildwithpython](https://img.shields.io/badge/Build--With--Python3-9cf?style=for-the-badge&logo=Python)](https://www.python.org/)
# Simulation-DES project for Tech Square Intersection Traffic
> @Georgia Tech, Tech Square Intersection : [View on Google Map: Spring St NW & 5th St NW, Atlanta, GA](https://www.google.com/maps/place/5th+St+NW+%26+Spring+St+NW,+Atlanta,+GA+30308/@33.7768422,-84.3893492,19z/data=!3m1!4b1!4m5!3m4!1s0x88f50466f3bc5519:0x348198a2b5659d14!8m2!3d33.7768411!4d-84.388802)
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/CrossSection.png" width="400" height="400">
</p>

## Introduction

The intersection between Spring Street and 5th Street (Tech Square) has been one of the busiest area on Georgia Tech campus. Students are rushing to classrooms from main campus and vehicles are taking Spring Street to Interstate Highways. The traffics lights control is vital in this heavy traffics area for both protecting the safety of pedestrian and improving the efficiency of traffic flow. <br>
In 2018, a new traffic pattern is introduced by including a ["pedestrian scramble crossing"](https://en.wikipedia.org/wiki/Pedestrian_scramble) as known as Barnes Dance, where the major improvement is that introducing a "all-way-right cycle" for vehicles and pedestrians can cross this intersection in any direction. <br>
This project will simulate this new traffic pattern with a discrete events simulation (DES) to study and further improve current system of traffic control.
## Software Architecture

<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/BlockDiagram.png" width="600" height="400">
</p>

## Installation
1. Install the complete software package:
```bash
git clone git@github.com:MUYANGGUO/Simulation-DES.git
```
2. Install the visualization dependencies
```bash
cd ~/.../Simulation-DES/Visualization
npm install
```
**note:** <br>
The Visualization is a react.js web page application, it needs `node.js` installed. The dependency packages need to be installed with `npm install`. The Visualization also depends on the Simulation results. The simulation python software package will generate a test.json file which will overwrite the current test.json in Visualization folder.

## Run Simulation
```
cd ~/your location path/Simulation-DES
python3 simulator.py N P T
```
> N: Number of vehicle events within time duration, P: number of people events within time duration (unit is "crowd") ,T: Time duration (hr). <br> Note that you should come up with these two number starting with the expectation of the events/per unit time rate, as the model will apply a poisson random process to simulate the observed occurrence of events within the time duration. The sampled observed events rate will be close to the expectation rate. 

  help line for understanding the software inputs:
```
python3 simulator.py -h
```
And the helper function will show:

```
usage: simulator.py [-h] total_events total_people simulation_time

positional arguments:
  total_events     :indicate the total events would like to simulate,
                   requested here
  total_people     :indicate the total people would like to simulate,
                   requested here
  simulation_time  :indicate simulation duration time, unit is hour, requested
                   here

optional arguments:
  -h, --help       show this help message and exit
```

Run Example: 

```
python3 simulator.py 150 4 0.1 >output_test1.txt
```

The command window will print out the configurations info and reminders, once the program complete, an output folder will be generated for saving plots. <br>
If with `>output.txt` added, the system output will be saved in this text file. If without this, the system outputs will pop out in the command window. 

## Run Visualization

After getting the **test.json** (will be stored in the visualization folder) from running simulator.py in the upper level directory, cd to Visualization directory, and run the following command:

```bash
npm start
```
The localhost will be started, and a web browser with the visualization page will be shown up. 

### Animation speed setting:

The animation cycle time, looplenth should be based on your simulation time duration (unit: second). 
If you run the simulation over 1 hour, you should set this number at least 3600. 

The animation speed is the scaled up playback speedup. You can set any number to increase the time lapse speed for playback.

In app.js line 75. 

```javascript
  _animate() {
    const {
      loopLength = 360, // unit corresponds to the timestamp in source data
      animationSpeed = 2 // unit time per second
    } = this.props;
    const timestamp = Date.now() / 1000;
    const loopTime = loopLength / animationSpeed;

    this.setState({
      time: ((timestamp % loopTime) / loopTime) * loopLength
    });
    this._animationFrame = window.requestAnimationFrame(this._animate.bind(this));
  }
```


## Output Figures
> Output figures will be saved under generated outputs folder at the end of the simulation process.

**1. Initial Poisson Distribution of Events Generating**
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Events_Poisson.png" width="400" height="400">
</p>

**2. Initial Arrival Timestamps for actors**
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_Timestamps.png" width="400" height="400">
</p>

**3. Initial Each Lane Assigned for actors**
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_0_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_1_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_2_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_3_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_4_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Initial_lane_5_Timestamps.png" width="400" height="400">
</p>

**4. Final Each Lane Arrival Timestamps**
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_0_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_1_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_2_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_3_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_4_Timestamps.png" width="400" height="400">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Final_lane_5_Timestamps.png" width="400" height="400">
</p>

**5. Comparision Each Lane Arrival Timestamps** 
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_0_Timestamps.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_1_Timestamps.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_2_Timestamps.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_3_Timestamps.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_4_Timestamps.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/outputs/Comparison_lane_5_Timestamps.png" width="500" height="500">
</p>

## Discrete Event Flow Chart 
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/ped.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/withred.png"  width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/withoutred.png"  width="500" height="500">
</p>

## Visualization
Graphical playback of the simulation results can provide an intuitive and direct understanding of the discrete events happening. Although the events are discrete, we managed to visualize the simulation in continuous time span by placing the discrete time stamps into an unit time stepped visualization process. To achieve better playback visual effect, we chose to use javascript and react framework to render the events log in web browser. We chose to use deck.gl, a powerful open-sourced, web-GL based visualization platform to playback the logs. <br>
We added motion tracks to describe the car/pedestrain movements, mapped the event happening with real world longitude latitude coordinates in a zoomed interactive real map, by using mapbox's service. 
Shown below is a screenshot of our visualization. <br>

<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/vis1.png" width="500" height="500">
</p>
<p align="center">
<img src="https://github.com/MUYANGGUO/Simulation-DES/blob/master/README_FILES/vis2.png"  width="500" height="500">
</p>

The web page is 3D and interactive, user can zoom, pan, rotate to view the playback from any angle. The camera auto focused to the tech square intersection location. We used different color scheme to differentiate the lanes, for example, North lane running towards are red, east lane is green, west lane is purple, pedestrian as yellow. We also use tail length of the car's motion track to describe whether it is passing or waiting, waiting cars will have slow speed , short tails approaching to the intersection, while cars passing the intersection will have higher speed, longer tails motion track. 

**Video Demo**

<a href="https://www.youtube.com/watch?feature=player_embedded&v=nKSSbqjWDY8
" target="_blank"><img src="https://img.youtube.com/vi/nKSSbqjWDY8/0.jpg" 
alt="Demo"/></a>

## Result Table

Plese kindly visit out_sample.txt file to see the sample test results logs. 


## Analysis of Results








