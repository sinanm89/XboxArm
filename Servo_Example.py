#!/usr/bin/python
import xbox
import time
import math
from Adafruit_PWM_Servo_Driver.Adafruit_PWM_Servo_Driver import PWM

# Initialise the PWM device using the default address
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

# def setServoPulse(channel, pulse):
#     pulseLength = 1000000                   # 1,000,000 us per second
#     pulseLength /= 60                       # 60 Hz
#     print "%d us per period" % pulseLength
#     pulseLength /= 4096                     # 12 bits of resolution
#     print "%d us per bit" % pulseLength
#     pulse *= 1000
#     pulse /= pulseLength
#     return pulseLength, channel

def init_pwm():
    pwm = PWM(0x40)  # Initialise the PWM device using the default address
    # pwm.setPWM(channel, 0, pulse)
    pwm.setPWMFreq(60)
    return pwm

def wait_for_motors_to_catch_up(joy):
    joy.refresh()
    # time.sleep(1)

def run_input_debugger():
    joy = xbox.Joystick()

    print "Xbox controller sample: Press Back button to exit"
    # Loop until back button is pressed
    pwm = init_pwm()
    while not joy.Back():
        wait_for_motors_to_catch_up(joy)
        # Show connection status
        if not joy.connected():
            print "WTF",

        if joy.A():
            # Change speed of continuous servo on channel O
            pwm.setPWM(0, 0, servoMin)

        if joy.B():
            print "B",

        if joy.X():
            # Change speed of continuous servo on channel O
            pwm.setPWM(0, 0, servoMax)
            print "X",

        if joy.Y():
            print "Y",

        if joy.dpadUp():
            print "U",

        if joy.dpadDown():
            print "D"

        if joy.dpadLeft():
            print "L",

        if joy.dpadRight():
            print "R",

    # Close out when done
    joy.close()


if __name__ == '__main__':
    run_input_debugger()
