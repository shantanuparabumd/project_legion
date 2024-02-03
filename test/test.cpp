/**
 * @file test.cpp
 * @author Shantanu Parab (sparab@umd.edu)
 * @brief Test file for the project
 * @version 0.1
 * @date 2024-02-02
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#include <gtest/gtest.h>
#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <project_legion/project.hpp>

/**
 * @brief Test Suite for the project
 * 
 */
class MyTestSuite : public ::testing::Test {
protected:
    std::shared_ptr<KeyboardTeleop> robot;
    // Set up the test environment
    void SetUp() override {
        std::cout << "Setting up the test" << std::endl;
    }

    // Tear down the test environment
    void TearDown() override {
        std::cout << "Tearing down the test" << std::endl;
    }
};

/**
 * @brief Construct a new test f object
 * 
 */
TEST_F(MyTestSuite, Test1) {
    robot = std::make_shared<KeyboardTeleop>();
    int res = robot->test_function(2,8);
    ASSERT_EQ(2 + 8, res);
}



// Run the tests
int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    ::testing::InitGoogleTest(&argc, argv);
    int result = RUN_ALL_TESTS();
    rclcpp::shutdown();
    return result;
}
