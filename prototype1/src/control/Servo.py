import RPi.GPIO as GPIO


class ServoS90:
    def __init__(self, pin):
        # set the servo pin, should be a valid GPIO out pin (eg: 17)
        self.servoPIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.p = GPIO.PWM(self.servoPIN, 50)  # 50 for 50Hz
        self.p.start(0)
        self.p.ChangeDutyCycle(0)

    def angle_to_percent(self, angle):
        if angle > 180 or angle < 0:
            return False
        start = 2.5
        end = 11
        ratio = (end - start)/180  # Calcul ratio from angle to percent
        angle_as_percent = angle * ratio
        return start + angle_as_percent

    def set_position(self, angle):
        # position should be  as an angle given in degrees (0<.<180)
        self.p.ChangeDutyCycle(self.angle_to_percent(angle))

    def default_position(self):
        self.p.ChangeDutyCycle(0)

    def end(self):
        self.p.stop()
        GPIO.cleanup()
