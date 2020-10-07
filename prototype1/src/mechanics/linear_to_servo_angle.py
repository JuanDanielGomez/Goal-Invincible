def linear_to_servo_angle(absciss, min_absciss, max_absciss, min_angle, max_angle):
    return min_angle + absciss * (max_angle - min_angle) / (max_absciss - min_absciss)
