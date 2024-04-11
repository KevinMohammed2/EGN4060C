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
            
            # Read joystick axes
            x_axis = joystick.get_axis(0)
            y_axis = -joystick.get_axis(1)
            throttle_axis = -joystick.get_axis(2)  # Assuming throttle control is on axis 2
            steering_axis = joystick.get_axis(3)   # Assuming steering control is on axis 3
            
            print("X-axis: {:.2f}, Y-axis: {:.2f}, Throttle: {:.2f}, Steering: {:.2f}".format(x_axis, y_axis, throttle_axis, steering_axis))
            
            # Map joystick values to servo angles for steering
            steering_angle = ((steering_axis + 1) / 2) * 180
            kit.servo[0].angle = steering_angle  # Adjust as needed for your setup
            kit.servo[1].angle = steering_angle  # Adjust as needed for your setup
            
            # Map joystick values to servo angles for throttle control
            throttle_angle = ((throttle_axis + 1) / 2) * 180
            kit.servo[15].angle = throttle_angle  # Adjust as needed for your setup
            
            # Adjust other servos as needed for your specific setup
            
            sleep(0.1)  # Add a small delay to prevent excessive updates
    else:
        print("No joystick found.")
except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
