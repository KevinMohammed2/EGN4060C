#!/usr/bin/python

import sys
import time
import math

sys.path.append('../lib/python/amd64')
import robot_interface as sdk

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
    state = sdk.HighState()
    cmd = sdk.HighCmd()
    udp.InitCmdData(cmd)

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime += 1

        udp.Recv()
        udp.GetRecv(state)

        cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType = 0
        cmd.speedLevel = 0
        cmd.footRaiseHeight = 0
        cmd.bodyHeight = 0
        cmd.euler = [0, 0, 0]
        cmd.velocity = [0, 0]
        cmd.yawSpeed = 0.0
        cmd.reserve = 0
        
        # Adjust these values based on joystick input mapping
        throttle = map_value(joystick.get_axis(2), -1, 1, -1, 1)  # Throttle control on axis 2
        steering = map_value(joystick.get_axis(3), -1, 1, -1, 1)  # Steering control on axis 3
        
        if motiontime > 1000 and motiontime < 3500:
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [throttle, 0]  # Adjust throttle control
            cmd.yawSpeed = -steering  # Adjust steering control
            cmd.footRaiseHeight = 0.1
            print("walk\n")
        
        if motiontime > 3500:
            cmd.mode = 0
            cmd.velocity = [0, 0]
            print("idle\n")
            
        udp.SetSend(cmd)
        udp.Send()
