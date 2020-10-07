from tracking.lib_tracking import Tracker
from mechanics.linear_to_servo_angle import linear_to_servo_angle
from predict.Predictor import Predictor
# from control.Servo import ServoS90
import argparse
from math import sqrt, floor


# parsing args
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-i", "--invert", action='store_true',
                help="swap the positions of the goal")
args = vars(ap.parse_args())


# ############## INITIALIZATION ################
scale = 0.00037037  # width of a pixel (in meters)
ball_tracker = Tracker()  # no args as defaults color are ok for our use case

# take camera or video input
# if a video path was not supplied, grab reference to webcam (option 1)
if not args.get("video", False):
    ball_tracker.take_video(args, 1)
else:
    # else, take video from file (option 2)
    ball_tracker.take_video(args, 2)


goal_pixels = list(ball_tracker.detect_goal())
if len(goal_pixels) != 2:
    raise Exception("Goal incorrectly detected")
goal = []
for p in goal_pixels:
    p_m = []
    for coo in p:
        print(coo, ",", end="")
        p_m.append(coo * scale)
    goal.append(p_m)
    print()
print(goal)
print("goal size:", sqrt((goal[0][0]-goal[1][0])
                         ** 2 + (goal[0][1]-goal[1][1])**2), " m")

# can take into args the goal position
predictor = Predictor(goal, high_freq=0.20)
predictor.sort_goal()  # so the order of the side of the goal is not random

if args.get("invert"):
    predictor.invert_goal()  # can be necessary if the camera is turned around or something
# servo = ServoS90(17)  # control pin 17

# ############# MAIN LOOP ##################
i = 0
for point in ball_tracker:
    i += 1
    # point is a tuple containing (x,y) in pixels
    # or None if nothing is recognized
    # print("point from tracker:", end="")
    # print(point)
    if point is None:
        # servo.default_position()
        continue

    # transform point into metric coordinates
    metric_point = point[0] * scale, point[1] * scale

    # get intersection absciss, in cm
    predictor.add(metric_point)
    goal_target = predictor.predict_cross()

    if goal_target is None:
        # servo.default_position()
        print("ball not on a path going towards the goal")
        continue
    else:
        # print("ball with cross goal line at " + str(floor(1000*goal_target)/1000) +
        # " m from the left-up most side of the goal")
        print(goal_target)

    #
    # transform goal absciss to servo angle
    angle = linear_to_servo_angle(goal_target, 0, 0.2, 45, 135)
    # servo.set_position(angle)
    # print(angle)


# ##### END #####
ball_tracker.close()
# servo.end()
