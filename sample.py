import xbox

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

joy = xbox.Joystick()

print "Xbox controller sample: Press Back button to exit"
# Loop until back button is pressed
while not joy.Back():
    # Show connection status
    if joy.connected():
        print "Connected",

    if joy.A():
        print "A",

    if joy.B():
        print "B",

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
