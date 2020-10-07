from Servo import ServoS90
import time


print("Starting test")
s = ServoS90(17)

s.set_position(45)
time.sleep(0.2)
s.set_position(90)
time.sleep(0.2)
s.set_position(45)
time.sleep(0.2)
s.set_position(90)
time.sleep(0.2)
s.set_position(45)
print("Test end")