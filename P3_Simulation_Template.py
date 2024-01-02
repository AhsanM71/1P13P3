ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P3A or P3B

# SERVO TABLE CONFIGURATION
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.20 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.20
bin2_color = [0,1,0]
bin2_metallic = False

bin3_offset = 0.20
bin3_color = [0,0,1]
bin3_metallic = False

bin4_offset = 0.2
bin4_color = [0,1,1]
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
# Importing random and math library
import random
import math

# Declaring and initialzing some variables
material = ""
mass_total = 0
target_bins = []
container_count = 0
bin_check = True
loading = True
staring_x_pos = 0
starting_y_pos = 0
starting_z_pos = 0
flag = True

# The release_container function dispenses a new container onto the servo table
def release_container():
    # Declaring global variables
    global material, mass_total, target_bins, container_count, bin_num, mass
    #global flag
    get_target_bin = ""
    # Generating a random number from 1 to 6 which represents the container ID 
    container_id = random.randint(1,6)

    # Dispensing a new container onto the servo table and extracting it's properties and storing them in their respective varibales
    material, mass, get_target_bin = table.dispense_container(container_id,True)
    # Extracting the containers bin drop off loaction from the string with the syntax Bin## and converting that string number into a int
    bin_num = int((get_target_bin[len(get_target_bin) - 1]))
    # Appending the designated bin drop off location to a list caleed target_bins
    target_bins.append(bin_num)
    # Incrementing the number of container's to be loaded into the hopper 
    container_count = container_count + 1
    # Adding the currently dispensed container's mass
    mass_total = mass_total + mass

    # Printing out the containers properties
    print("\n\tMaterial:", material)
    print("\tMass:    ", mass)
    print("\tBin Location:", bin_num)

# The load_container function only get's called when a container has met all the requirements. This function loads the container into the hopper
def load_container():
    # Setting the loading variable to global
    global loading
    # Setting the valid_container variable's initial value to True
    valid_container = True
    # This while loop is only true if a container that is to be loaded from the servo table onto the hopper has valid properties compared to the original container already
    # inside the hopper. Note for the very first container being dispensed from each run will get loaded into the hopper no matter what
    while valid_container:
        if (container_count == 1):
            # Qarm commands used to load the container into the hopper
            arm.move_arm(0.659,0.0,0.279)
            time.sleep(1)
            arm.control_gripper(35)
            time.sleep(3)
            arm.move_arm(0.04,-0.566,0.564)
            time.sleep(2)
            arm.rotate_base(-10)
            time.sleep(1)
            arm.rotate_wrist(10) # added this, may need to change
            time.sleep(1)
            arm.control_gripper(-15)
            time.sleep(3)
            arm.rotate_shoulder(-40)
            time.sleep(0.5)
            arm.home()
            # Setting loading variable to true, which tells the program the container has been loaded and the next container can be dispensed
            loading = True
            # Setting the valid_container to false because the main function of this if condition is to load the first container from every run
            valid_container = False
            return loading
        
        # The elif condition compares the properties of the newly dispensed container with the already loaded container
        elif (container_count < 4 and mass_total < 91 and target_bins[0] == target_bins[(container_count) - 1]):
            # if these conditions are met then the container is valid and can be loaded into the hopper
            # Therefore setting the valid_container variable to true
            valid_container = True
            # These Qarm commands load the container into the hopper
            arm.move_arm(0.659,0.0,0.279)
            time.sleep(1)
            arm.control_gripper(35)
            time.sleep(3)
            arm.move_arm(0.04,-0.566,0.564)
            time.sleep(1)
            arm.rotate_wrist(5) # added this, may need to change
            time.sleep(2)
            # if the container being loaded is the second one then drop it off in the hopper to the right from the first one
            if (container_count == 2):
                arm.rotate_base(-7.5)
                time.sleep(1)
                arm.control_gripper(-15)
                time.sleep(3)
            # if the container being loaded is the thrid one then drop it off in the hopper to the right from the second container
            else:
                arm.rotate_base(-3.5)
                time.sleep(1)
                arm.control_gripper(-15)
                time.sleep(3)
            arm.rotate_shoulder(-40)
            time.sleep(0.5)
            arm.home()
            # Setting the flag variable to true since the next container has been loaded into the hopper, which tells the program the next container can be dispensed
            flag = loading
            return loading
        # The else condition get's executed if the container on the servo table's properties don't meet the requirements
        else:
            # Printing out to the user conditions of the container were not satisfied and setting/returning the loading variable to false
            print("Conditions are not satisfied, container cannot be loaded")
            loading = False
            return loading
            break

# The transfer_container function transport's the loaded trash in the hopper to the containers designated bin number/drop off location. 
def transfer_container():
    # Setting bin_check as a global variable
    global bin_check
    # Activating color and line following sensors
    bot.activate_line_following_sensor()
    bot.activate_color_sensor()
    # Rotating Qbot to the correct orientation
    bot.rotate(95)
    # This while loop will run as long as the Qbot isn't next to the bin
    while bin_check:
        # Getting the ir readings from the ir sensor
        get_ir_readings = bot.line_following_sensors()
        left_ir_reading = get_ir_readings[0]
        right_ir_reading = get_ir_readings[1]
        # Using a helper function called reached_bin() to check if teh Qbot is next to the correct bin
        bin_check = reached_bin()
        # if condition checking if both left and right IR sensors sense the yellow line then set both of the Qbots motor speeds the same
        if (left_ir_reading == 1 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05*1.5,0.05*1.5])
        # elif conditon is checking if left IR sensor is sensing the line but not the right, then turn Qbot to the right
        elif (left_ir_reading == 1 and right_ir_reading == 0):
            bot.set_wheel_speed([0.05*0.2,0.05])
        # elif condition is checking if right IR sensor is sensing the line but not the left, then turn Qbot to the left 
        elif (left_ir_reading == 0 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05,0.05*0.2])
    # Once Qbot has arrived at the correct bin loaction then stop the Qbot and deactivate all previous activated sensors
    bot.stop()
    bot.deactivate_line_following_sensor()
    bot.deactivate_color_sensor()

# The deposit_container function desposits the containers by activating the stepper motor and rotating the hopper
def deposit_container():
    # activating the stepper motor
    bot.activate_stepper_motor()
    # if the trash in the hopper's drop off location was bin 1 (red) execute the code inside the if condition
    if target_bins[0] == 1:
        bot.forward_distance(0.25)
        time.sleep(1)
        bot.rotate(-20)
        time.sleep(1)
        bot.rotate_hopper(25)
        time.sleep(0.5)
        bot.rotate_hopper(50)
        time.sleep(0.5)
        bot.rotate_hopper(90)
        time.sleep(1)
        bot.rotate_hopper(0)
    # if the trash in the hopper's drop off location was bin 2 (green) execute the code inside the if condition
    elif target_bins[0] == 2:
        bot.forward_distance(0.25)
        time.sleep(1)
        bot.rotate_hopper(25)
        time.sleep(0.5)
        bot.rotate_hopper(50)
        time.sleep(0.5)
        bot.rotate_hopper(90)
        time.sleep(1)
        bot.rotate_hopper(0)
    # if the trash in the hopper's drop off location was bin 3 (blue) execute the code inside the if condition
    elif target_bins[0] == 3:
        bot.forward_distance(0.30)
        time.sleep(1)
        bot.rotate(-20)
        time.sleep(1)
        bot.rotate_hopper(25)
        time.sleep(0.5)
        bot.rotate_hopper(50)
        time.sleep(0.5)
        bot.rotate_hopper(90)
        time.sleep(1)
        bot.rotate_hopper(0) 
    # if the trash in the hopper's drop off location was bin 4 (turquoise) execute the code inside the if condition
    elif target_bins[0] == 4:
        bot.forward_distance(0.25)
        time.sleep(0.5)
        bot.rotate_hopper(25)
        time.sleep(0.5)
        bot.rotate_hopper(50)
        time.sleep(0.5)
        bot.rotate_hopper(90)
        time.sleep(1)
        bot.rotate_hopper(0)
    # Once the containers have been deposited deactivate the stepper motor
    bot.deactivate_stepper_motor()

# The reached_bin helper function checks if the Qbot has arrived at the correct bin drop off location
def reached_bin():
    # The target_bins is a list which contains the bin drop off bin location
    # if the Qbot is supposed to stop at bin 1 run the code below
    if target_bins[0] == 1:
        # if the color sensor reads red return false, else return true
        if bot.read_color_sensor()[0][0] == 1:
            return False
        else:
            return True
    # if the Qbot is supposed to stop at bin 1 run the code below
    elif target_bins[0] == 2:
        # if the color sensor reads green return false, else return true
        if bot.read_color_sensor()[0][1] == 1:
            return False
        else:
            return True
    # if the Qbot is supposed to stop at bin 1 run the code below
    elif target_bins[0] == 3:
        # if the color sensor reads blue return false, else return true
        if bot.read_color_sensor()[0][2] == 1:
            return False
        else:
            return True
    # if the Qbot is supposed to stop at bin 1 run the code below
    elif target_bins[0] == 4:
        # if the color sensor reads turquoise return false, else return true
        if bot.read_color_sensor()[0][1] == 1 and bot.read_color_sensor()[0][2] == 1:
            return False
        else:
            return True

# The return_home function moves the Qbot back to the home position once it has desposited the containers into the correct bin location
def return_home():
    # reactivate the line following sensor
    bot.activate_line_following_sensor()
    # initalizing deafult values for the current Qbot's position
    moving_x_pos = 0
    moving_y_pos = 0

    # While the Qbot isn't at its home position execute code below
    # This while loop condition takes the Qbot's moving xand y positions and subtracts it from the home x and y positions respectively,
    # then it takes the absolute value of that and compares it with a range of 0.1, what this basically does is, if the Qbot is in the relative range of 0.1 from the original
    # x and y position from home then it has arrived at home. 
    while (abs(moving_x_pos - starting_x_pos) > 0.1 or abs(moving_y_pos - starting_y_pos) > 0.1):
        # Get Qbot's current moving positions and ir readings
        moving_x_pos, moving_y_pos,z = bot.position()
        get_ir_readings = bot.line_following_sensors()
        left_ir_reading = get_ir_readings[0]
        right_ir_reading = get_ir_readings[1]

        # if condition checking if both left and right IR sensors sense the yellow line then set both of the Qbots motor speeds the same
        if (left_ir_reading == 1 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05*1.5,0.05*1.5])
        # elif conditon is checking if left IR sensor is sensing the line but not the right, then turn Qbot to the right
        elif (left_ir_reading == 1 and right_ir_reading == 0):
            bot.set_wheel_speed([0.05*0.2,0.05])
        # elif condition is checking if right IR sensor is sensing the line but not the left, then turn Qbot to the left 
        elif (left_ir_reading == 0 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05,0.05*0.2])
    # Hard coded some comands to get the Qbot closer to home position
    time.sleep(1)
    bot.rotate(15)
    time.sleep(1)
    bot.forward_distance(0.1)
    time.sleep(1)
    bot.rotate(-15)
    time.sleep(1)
    bot.rotate(-15)
    bot.stop()
    # Deactivate line following sensor and print our home position reaached
    bot.deactivate_line_following_sensor()
    print("Home Position Reached")

# The reset_variable function, set's all the variables that were manipulated to their deafult settings so the alogirthm and run infinitely many times. 
def reset_variables():
    global container_count, target_bins, mass_total, bin_check, loading, material, bin_num, mass, flag
    # Setting container_count to 1 because the first container is the default container that needs to be loaded from the servo table to the hopper
    container_count = 1
    # Setting the rest of the variables to theit default values
    target_bins = []
    mass_total = mass
    bin_check = True
    loading = True
    material = ""
    # Once the target_bin list has ben wiped from the last run the bin drop off location for the already dispensed container get's appended to the list
    target_bins.append(bin_num)
    flag = False

    
def main():
    # Declaring global variables
    global loading, starting_x_pos, starting_y_pos, flag
    print("\tBin # 1: RED")
    print("\tBin # 2: GREEN")
    print("\tBin # 3: BLUE")
    print("\tBin # 4: TURQUOISE")
    # Getting Qbot's home position
    starting_x_pos, starting_y_pos, z = bot.position()
    # infinite while loop
    while True:
        # Rotate Qbot sideways so loading the container is easier
        time.sleep(0.5)
        bot.rotate(-95)
        time.sleep(5)
        # This while loop is true only if a valid container (all required conditions are met) can be loaded into the Qbot's hopper. 
        while loading:
            # This flag variable is used temporarily to always dispense a new container even if the condition's are not met for loading
            if flag:
                # The release_container function is called to dispense a new container onto the empty servo table
                release_container()
            # Setting flag to True
            flag = True
            # Calling the load_container function which loads the container from the servo table to the hopper using the Qarm
            # This function also returns a boolean condition that get's stored into the loading function which basically determines if the newly dispensed container
            # on the servo table can be loaded into the hopper
            loading = load_container()
        # Once the Qbot reaches it's maximum carrying capacity the following functions get executed. 
        transfer_container()
        deposit_container()
        return_home()
        reset_variables()
main()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

