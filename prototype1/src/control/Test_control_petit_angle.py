from Servo import ServoS90
import time

print("Starting test")
s = ServoS90(17)
angle = 90
pas_angle = 2
pas_temps = 0.01

s.set_position(angle)
time.sleep(pas_temps)

for i in range (2):
    for j in range (0, 45, pas_angle):
        angle += (-1)**i * pas_angle
        s.set_position(angle)
        time.sleep(pas_temps)
print("Test end")