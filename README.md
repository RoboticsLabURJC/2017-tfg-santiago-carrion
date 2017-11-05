# 2017-tfg-santiago-carrion
# Scratch2JdeRobot

Tool that allows to program robots easily using Scratch 2.0. Performs the translation of the Scratch blocks to Python code for use on robots.

### Prerequisites

Operating system Ubuntu 16.04
Scratch 2.0

### Installation


### API Reference
* **Perceptive Blocks**

| Name        | Robot     | Param     | Return     | Description|
| ----------- |:---------:|:---------:| :---------:| :----------:|
| Pose3D x | Kobuki - Drone|--| Return his position on the x axis | Get the value of his 3d position
| Pose3D y | Kobuki - Drone|--| Return his position on the y axis | Get the value of his 3d position
| Pose3D z | Kobuki - Drone|--|Return his position on the z axis | Get the value of his 3d position
| Frontal laser distance | Kobuki   |--| The average measure of the frontal laser data|Get the average value for the values of the frontal laser |
| Size of object | Kobuki|--|  |   
| X position of object |Kobuki|-- | |   
| Y position of object | Kobuki|--| |   
| Drone size object | Drone|--|  |   
| Drone pos x center object |Drone|-- | |   
| Drone pos y center object | Drone|--| |  

*  **Movement Blocks**

| Name        | Robot     | Param    | Return     | Description|
| ----------- |:---------:|:--------:| :---------:| :---------:|
| stop robot-drone | Kobuki - Drone    |--     |  -- | Reset all velocity values |
| drone take off | Drone | --    | --  | Makes the drone take off|   
| drone land | Drone|  --  | --  | Makes the drone land |
| drone move {direction} speed {velocity} | Drone  | direction: forward, back, up, down, left, right / velocity: integer |    --  |  Gives the drone a speed in the indicated direction|
| drone turn {direction} speed {velocity} | Drone  | direction: left, right / velocity: integer |    --  |  Gives the drone a turning speed in the indicated direction|
| robot move {direction} speed {velocity} | Kobuki  | direction: forward, back, left, right / velocity: integer |    --  |  Gives  a speed in the indicated direction|
| robot turn {direction} speed {velocity} | Kobuki  | direction: left, right / velocity: integer |    --  |  Gives a turning speed in the indicated direction|
| robot move {direction} meters {meters} | Kobuki  | direction: left, right, forward, back / meters: integer |    --  |  Move robot the indicated meters in one direction|

##### Movement Blocks


### Tests
