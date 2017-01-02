#!/usr/bin/python

import time
import math
from Adafruit_I2C import Adafruit_I2C

# ============================================================================
# Adafruit PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM :
    # Registers/etc.
    __MODE1              = 0x00
    __MODE2              = 0x01
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALL_LED_ON_L       = 0xFA
    __ALL_LED_ON_H       = 0xFB
    __ALL_LED_OFF_L      = 0xFC
    __ALL_LED_OFF_H      = 0xFD

    # Bits
    __RESTART            = 0x80
    __SLEEP              = 0x10
    __ALLCALL            = 0x01
    __INVRT              = 0x10
    __OUTDRV             = 0x04

    general_call_i2c = Adafruit_I2C(0x00)

    @classmethod
    def softwareReset(cls):
        "Sends a software reset (SWRST) command to all the servo drivers on the bus"
        cls.general_call_i2c.writeRaw8(0x06)        # SWRST

    def __init__(self, address=0x40, debug=False):
        self.i2c = Adafruit_I2C(address)
        self.i2c.debug = debug
        self.address = address
        self.debug = debug
        if (self.debug):
            print "Reseting PCA9685 MODE1 (without SLEEP) and MODE2"
        self.setAllPWM(0, 0)
        self.i2c.write8(self.__MODE2, self.__OUTDRV)
        self.i2c.write8(self.__MODE1, self.__ALLCALL)
        time.sleep(0.005)                                       # wait for oscillator

        mode1 = self.i2c.readU8(self.__MODE1)
        mode1 = mode1 & ~self.__SLEEP                 # wake up (reset sleep)
        self.i2c.write8(self.__MODE1, mode1)
        time.sleep(0.005)                             # wait for oscillator

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print "Setting PWM frequency to %d Hz" % freq
            print "Estimated pre-scale: %d" % prescaleval
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print "Final pre-scale: %d" % prescale

        oldmode = self.i2c.readU8(self.__MODE1);
        newmode = (oldmode & 0x7F) | 0x10             # sleep
        self.i2c.write8(self.__MODE1, newmode)        # go to sleep
        self.i2c.write8(self.__PRESCALE, int(math.floor(prescale)))
        self.i2c.write8(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.i2c.write8(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.i2c.write8(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.i2c.write8(self.__LED0_ON_H+4*channel, on >> 8)
        self.i2c.write8(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.i2c.write8(self.__LED0_OFF_H+4*channel, off >> 8)

    def setAllPWM(self, on, off):
        "Sets a all PWM channels"
        self.i2c.write8(self.__ALL_LED_ON_L, on & 0xFF)
        self.i2c.write8(self.__ALL_LED_ON_H, on >> 8)
        self.i2c.write8(self.__ALL_LED_OFF_L, off & 0xFF)
        self.i2c.write8(self.__ALL_LED_OFF_H, off >> 8)

#!/usr/bin/python
# from Adafruit_PWM_Servo_Driver import PWM
# import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength

def setup_pwm():
    pwm = PWM(0x40)
    pwm.setPWM(channel, 0, pulse)

    pwm.setPWMFreq(60)
    return pwm

def wait_for_motors_to_catch_up():
    time.sleep(1)

import xbox

def run_input_debugger():
    joy = xbox.Joystick()

    print "Xbox controller sample: Press Back button to exit"
    # Loop until back button is pressed
    pwm = setup_pwm()
    while not joy.Back():
        wait_for_motors_to_catch_up()
        # Show connection status
        if not joy.connected():
            print "WTF",

        if joy.A():
            # Change speed of continuous servo on channel O
            pwm.setPWM(0, 0, servoMin)
            # time.sleep(1)
            # pwm.setPWM(0, 0, servoMax)
            # time.sleep(1)
            # print "A",

        if joy.B():
            pwm.setPWM(0, 0, servoMax)
            # print "B",

        if joy.X():
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
