# USAGE
# python test_tracking.py --video babyvideo.mov
# python test_tracking.py
from lib_tracking import Tracker
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

tracker = Tracker()

# if a video path was not supplied, grab reference to webcam (option 1)
if not args.get("video", False):
    tracker.take_video(args, 1)
else:
    # else, take video from file (option 2)
    tracker.take_video(args, 2)

#dim = tracker.video_resolution()
# print(dim)

goal_ctrs = tracker.detect_goal()
if len(goal_ctrs) != 2:
    raise Exception(
        "Error in detection of goal, points detected: {}".format(len(goal_ctrs)))
else:
    goal1 = goal_ctrs.popleft()
    goal2 = goal_ctrs.popleft()
    print("goal location # 1 : {}".format(goal1))
    print("goal location # 2 : {}".format(goal2))

for b in tracker:
    print("ball center: {}".format(b))

print("goal location # 1 : {}".format(goal1))
print("goal location # 2 : {}".format(goal2))
