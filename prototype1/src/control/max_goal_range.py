# test servo library
from Servo import ServoS90
import time


print("Starting test")
s = ServoS90(17)
s.set_position(45)
time.sleep(10)

s.set_position(135)
time.sleep(10)
s.set_position(0)
print("Test end")
