/**
 * @file project.hpp
 * @author Shantanu Parab (sparab@umd.edu)
 * @brief Header file for the project library
 * @version 0.1
 * @date 2024-02-02
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#pragma once

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include <iostream>
#include <unistd.h>
#include <termios.h>

#define KEYCODE_W 'W'
#define KEYCODE_A 'A'
#define KEYCODE_S 'S'
#define KEYCODE_D 'D'
#define KEYCODE_Q 'Q'
#define KEYCODE_E 'E'
#define LIN_VEL_STEP_SIZE  10
#define ANG_VEL_STEP_SIZE  0.1

int kfd = 0;
struct termios cooked, raw;

void set_terminal_raw();

void reset_terminal_mode();

int read_key();


class KeyboardTeleop : public rclcpp::Node
{
public:
    KeyboardTeleop();
    int test_function(int a, int b);

private:
    
    void publish_message();

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr vel_publisher_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr pos_publisher_;
    double velocity;
    double rotation;
};


