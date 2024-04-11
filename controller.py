from time import sleep
import pygame
import busio
import board
from adafruit_servokit import ServoKit

pygame.init()
pygame.joystick.init()

i2c = busio.I2C(3, 2)
kit = ServoKit(channels=16, i2c=i2c)

try:
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        while True:
            pygame.event.pump()
            
            # Get joystick axes values
            x_axis = joystick.get_axis(0)  # Steering control (left/right)
            y_axis = joystick.get_axis(1)  # Throttle control (forward/backward)
            
            # Invert y-axis for intuitive control (pushing forward should be positive)
            y_axis = -y_axis
            
            print("X-axis: {:.2f}, Y-axis: {:.2f}".format(x_axis, y_axis))
            
            # Map joystick values to servo angles for throttle and steering
            throttle_angle = ((y_axis + 1) / 2) * 180  # Map y-axis to throttle servo angle
            steering_angle = ((x_axis + 1) / 2) * 180  # Map x-axis to steering servo angle
            
            # Set servo angles for throttle and steering
            # Assuming servo channels 0 and 1 for throttle control
            kit.servo[0].angle = throttle_angle  # Set left motor angle
            kit.servo[1].angle = throttle_angle  # Set right motor angle
            
            # Assuming servo channel 15 for steering control
            kit.servo[15].angle = steering_angle
            
            sleep(0.1)  # Small delay for smoother control
            
    else:
        print("No joystick found.")
except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
