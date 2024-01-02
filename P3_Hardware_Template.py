ip_address = '172.17.42.73' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P3A or P3B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *

hardware = True
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
if project_identifier == 'P3A':
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    table = servo_table(ip_address,QLabs,None,hardware)
else:
    speed = 0.1 # in m/s
    bot = qbot(speed,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import time

def transfer_container():
    # Activate line following, color, and stepper motor sensors
    bot.activate_line_following_sensor()
    bot.activate_color_sensor()
    bot.activate_stepper_motor()

    # Infinite while loop continously runs the code in its body which transfer the Qbot to the drop off bin location
    while True:
        # Using try and except statements to account for the delay of the color sensors reading
        try:
            # Getting and storing the color the Qbot reads using the color sensor into a variable
            detected_color = bot.read_color_sensor()[1]
            #print(detected_color)
            # If the color the Qbot is reading is between 165 to 255 then Qbot is in front of the red colored bin
            if detected_color[0] > 165 and detected_color[0] < 255:
                # The following code drops of its load (containers in the hopper) inside the bin 
                bot.stop()
                bot.rotate_stepper_ccw(2)
                time.sleep(1.0)
                bot.rotate_stepper_cw(-2)
                bot.deactivate_stepper_motor()
                bot.forward_distance(0.15)
                # Once the Qbot has dropped of the containers into the bin, break out of the infinite loop
                break
        # except block used to account for the color sensor delay
        except:
            # pass to the next iteration
            pass
        # Getting the ir values from the Qbot's IR sensor and storing both the left and right readings in separate variables
        get_ir_readings = bot.line_following_sensors()
        left_ir_reading = get_ir_readings[0]
        right_ir_reading = get_ir_readings[1]

        # if condition checking if both left and right IR sensors sense the yellow line then set both of the Qbots motor speeds the same
        if (left_ir_reading == 1 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05*1.5,0.05*1.5])
        # elif conditon is checking if left IR sensor is sensing the line but not the right, then turn Qbot to the right
        elif (left_ir_reading == 1 and right_ir_reading == 0):
            bot.set_wheel_speed([0.01,0.05])
        # elif condition is checking if right IR sensor is sensing the line but not the left, then turn Qbot to the left
        elif (left_ir_reading == 0 and right_ir_reading == 1):
            bot.set_wheel_speed([0.05,0.01])
        # if every other condition fails, run the else condition which turns the Qbot to the right
        else:
            bot.set_wheel_speed([0.01, 0.05])
            
# Deactivate line following and color sensors
bot.deactivate_line_following_sensor()
bot.deactivate_color_sensor()

def main():
    # The transfer container function, transfer the containers in the Qbot to the red bin
    transfer_container()
main()



#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

