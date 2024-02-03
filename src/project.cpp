#include "../include/project_legion/project.hpp"


void set_terminal_raw()
{
    tcgetattr(kfd, &cooked);
    memcpy(&raw, &cooked, sizeof(struct termios));
    raw.c_lflag &= ~(ICANON | ECHO);
    // Setting a new line, then end of file
    raw.c_cc[VEOL] = 1;
    raw.c_cc[VEOF] = 2;
    tcsetattr(kfd, TCSANOW, &raw);
}

void reset_terminal_mode()
{
    tcsetattr(kfd, TCSANOW, &cooked);
}

int read_key()
{
    char c;
    if (read(kfd, &c, 1) < 0)
    {
        perror("read():");
        exit(-1);
    }
    return c;
}


/**
 * @brief Construct a new Keyboard Teleop:: Keyboard Teleop object
 * 
 */

KeyboardTeleop::KeyboardTeleop(): Node("keyboard_teleop"), velocity(0.0), rotation(0.0)
    {
        pos_publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/joint_position_controller/commands", 10);
        vel_publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/joint_velocity_controller/commands", 10);
        set_terminal_raw();

        puts("Reading from keyboard");
        puts("---------------------------");
        puts("Use 'WASD' to control the robot");
        puts("Use 'Q' to quit");

        timer_ = this->create_wall_timer(std::chrono::milliseconds(100), std::bind(&KeyboardTeleop::publish_message, this));
    }


/**
 * @brief Tets function to test the project
 * 
 * @param a 
 * @param b 
 * @return int 
 */
int KeyboardTeleop::test_function(int a, int b){
    return a + b;
}

/**
 * @brief Function to publish the message to the velocity and position controllers
 * after reading the key from the keyboard
 */
void KeyboardTeleop::publish_message(){
    char c = read_key();
    switch (c)
    {
    case KEYCODE_W:
        velocity += LIN_VEL_STEP_SIZE;
        break;
    case KEYCODE_S:
        velocity -= LIN_VEL_STEP_SIZE;
        break;
    case KEYCODE_A:
        rotation += ANG_VEL_STEP_SIZE;
        break;
    case KEYCODE_D:
        rotation -= ANG_VEL_STEP_SIZE;
        break;
    case KEYCODE_Q:
        velocity = 0.0;
        rotation = 0.0;
        reset_terminal_mode();
        rclcpp::shutdown();
        break;
    default:
        velocity = 0.0;
        rotation = 0.0;
        break;
    }

    auto wheel_velocities = std_msgs::msg::Float64MultiArray();
    auto joint_positions = std_msgs::msg::Float64MultiArray();
    wheel_velocities.data = {velocity,-velocity,velocity,-velocity};
    joint_positions.data = {rotation,rotation,0.0,0.0};
    vel_publisher_->publish(wheel_velocities);
    pos_publisher_->publish(joint_positions);
}