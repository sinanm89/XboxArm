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

oneTick = 50
halfTick = oneTick / 25

one_tick = (servoMax - servoMin) / 2
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

def wait_for_motors_to_catch_up(joy, sleep=None):
    # joy.refresh()
    if sleep:
        time.sleep(sleep)
    else:
        time.sleep(0.6)

def run_input_debugger():
    joy = xbox.Joystick()

    print "Xbox controller sample: Press Back button to exit"
    # Loop until back button is pressed
    pwm = init_pwm()
    pos = servoMin
    pwm.setPWM(0, 0, servoMin)
    time.sleep(0.6)
    pwm.setPWM(0, 0, servoMax)
    time.sleep(0.6)
    pwm.setPWM(0, 0, servoMin + 50)
    time.sleep(0.6)
    while not joy.Back():
        wait_for_motors_to_catch_up(joy)
        # Show connection status
        if not joy.connected():
            print "WTF",

        if joy.A():
            # Change speed of continuous servo on channel O
            print "A",
            pos += halfTick
            pwm.setPWM(0, 0, pos)
            # wait_for_motors_to_catch_up(joy, 0.2)

        if joy.B():
            print "B",
            pos -= halfTick
            pwm.setPWM(0, 0, pos)

        if joy.X():
            # Change speed of continuous servo on channel O
            print "X",
            pwm.setPWM(0, 0, servoMax)

        if joy.Y():
            print "Y (Reset)",
            time.sleep(1)
            pwm.setPWM(0, 0, servoMax)
            time.sleep(1)
            pwm.setPWM(0, 0, servoMin)

        if joy.dpadUp():
            print "U",

        if joy.dpadDown():
            print "D"

        if joy.dpadLeft():
            print "L",

        if joy.rightX():
            import ipdb; ipdb.set_trace()
            print "Right Y axis move",

        if joy.rightY():
            print "Right X axis move",

        if joy.leftX():
            print "Left X axis move",

        if joy.leftY():
            print "Left Y axis move",

        if joy.dpadRight():
            print "R",

    # Close out when done
    joy.close()


if __name__ == '__main__':
    run_input_debugger()
