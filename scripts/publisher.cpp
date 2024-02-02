/**
 * @file publisher.cpp
 * @author Shantanu Parab (sparab@umd.edu)
 * @brief Main application file for the project
 * @version 0.1
 * @date 2024-02-02
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "rclcpp/rclcpp.hpp"
#include <project_legion/project.hpp>
#include <iostream>

/**
 * @brief main function entry point
 * 
 * @param argc 
 * @param argv 
 * @return int 
 */

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<KeyboardTeleop>());
    rclcpp::shutdown();
    return 0;
}
