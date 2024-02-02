
# Project Legion
<!-- 
[![codecov](https://codecov.io/gh/jayprajapati009/project_chakravyu/branch/main/graph/badge.svg?token=0C30FZ9SC6)](https://codecov.io/gh/jayprajapati009/project_chakravyu)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) -->

![Build Status](https://github.com/shantanuparabumd/project_legion/actions/workflows/project_legion_git_ci.yml/badge.svg)


![Project Legion](/images/robotaxi.jpg)

## Authors

|Name|ID|Email|
|:---:|:---:|:---:|
|Shantanu Parab|119208625|sparab@umd.edu|


## Introduction

 This project tries to replicate the Robotaxi project by Zoox. The fundmental goal of the project is to understand the working of autonomous vehicles and implement various neccessary algorithms such as path planning, perception and multi-agent systems. The project is a simulation of all these in Gazebo (Physics Simulation Engine) using ROS2.

## Dependencies

- OS: Ubuntu Linux 22.04
- ROS Version: ROS2 Galactic
- C++

## System Architecture

The essential task of the taxi is to pick a passenger randomly spawned in the world and drop it to a particular goal location.


## Documents

|AIP Backlog and Worklog Sheet|[Link](https://docs.google.com/spreadsheets/d/1OLjYREJhVSBwzK9YCMAjV7O8FSent7a0hvpAadGcQXk/edit?usp=sharing)|
<!-- |Sprint and Review Meeting Notes|[Link](https://docs.google.com/document/d/1zADA51S8-DCuGPjZB7dvrBzD6DiS--uvvF-nh4I-Mvw/edit?usp=sharing)| -->



# Dependeny Installation and Setup

Installing ROS Controller (Run this in home directory)

`sudo apt install ros-galactic-ros2-control ros-galactic-ros2-controllers ros-galactic-gazebo-ros2-control`

Install xacro module to read xacro files
`pip install xacro`

Launch gazebo using launch file and then run the below 2 commands to start the controllers
# Manually Starting Controllers (Top 2 Only)

`ros2 control load_controller --set-state start joint_state_broadcaster`

`ros2 control load_controller --set-state start velocity_controller`

`ros2 control load_controller --set-state start joint_position_controller`

# Check Topics

`ros2 topic list`

# Publish Velocity

`ros2 topic pub /velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [1.0,-1.0,1.0,-1.0],layout: {dim:[], data_offset: 1"}}`

`ros2 topic pub /joint_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.3,0.3,0.3,0.3],layout: {dim:[], data_offset: 1"}}`

# Joint State Publisher Gui Package
sudo apt-get install ros-galactic-joint-state-publisher-gui
