from collections import deque
from math import sqrt
import numpy as np
from scipy import fftpack
from matplotlib import pyplot as plt


def distance(p1, p2):
    # Compute the distance between p1 and p2
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


class Predictor:
    # Class to predict the next position
    def __init__(self, goal=((0, 0), (0.2, 0)), high_freq=0.04, line_amort=4):
        self.positions = deque()
        self.filtered_positions = deque()
        self.line_amort = line_amort
        self.goal = goal
        self.high_freq = high_freq  # freq to filter noise, fps-independant

    def filter(self, previous_list, next_point):
        if len(previous_list) == 0:
            return next_point

        point_filtered = [0, 0]

        previous_list.appendleft(next_point)

        n = len(previous_list)
        high_freq = self.high_freq

        # For all the x and y coordinates, we use FFT to remove noise
        # from the video capture
        list_x = [x[0] for x in previous_list]
        sig_fft_x = fftpack.fft(list_x)
        sample_freq_x = fftpack.fftfreq(n, d=1)
        sig_fft_x[np.abs(sample_freq_x) > high_freq] = 0
        filtered_sig_x = fftpack.ifft(sig_fft_x)
        point_filtered[0] = np.real(filtered_sig_x[-1])

        list_y = [y[1] for y in previous_list]
        sig_fft_y = fftpack.fft(list_y)
        sample_freq_y = fftpack.fftfreq(n, d=1)
        sig_fft_y[np.abs(sample_freq_y) > high_freq] = 0
        filtered_sig_y = fftpack.ifft(sig_fft_y)
        point_filtered[1] = np.real(filtered_sig_y[-1])

        self.filtered_positions.append(point_filtered)

        return point_filtered

    def add(self, point):
        # Filter the point and add it to the current positions list
        point_filtered = self.filter(self.positions, point)
        self.positions.append(point_filtered)

    def invert_goal(self):
        self.goal = (self.goal[1], self.goal[0])

    def sort_goal(self):
        """give a direction to the goal: the up-left-most point (video-wise) is
        the reference (when it touches this side  the ball is at 0 cm"""
        a = self.goal[0][0] + self.goal[0][1]
        b = self.goal[1][0] + self.goal[1][1]

        if a > b:
            self.invert_goal()

    def get(self):
        # Return the last position
        return self.positions[-1]

    def check_goal_size(self):
        p1 = self.goal[0]
        p2 = self.goal[1]
        goal_size = distance(p1, p2)
        if goal_size < 0.15 or goal_size > 0.25:
            raise Exception("Goal size must be about 0.2m")
        return goal_size

    def approaching(self, point):
        # goal s to not move too much if the ball is going away
        # point is the intersection with the goal line

        if len(self.filtered_positions) <= 2:
            return True

        latest = self.filtered_positions[-1]
        old = self.filtered_positions[-2]

        d1 = distance(latest, point)
        d2 = distance(old, point)

        return d1 <= d2

    def predict_cross(self):
        # Predict if the ball is going to cross the goal line

        def line(p1, p2):
            # The equation of the line passing through p1 and p2
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C

        def intersect(L1, L2):
            # Check if the lines L1 and L2 are crossing
            D = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x, y
            else:
                return None
        goal_line = line(self.goal[0], self.goal[1])

        if len(self.filtered_positions) <= 1:
            return None

        # Check if the line made by the last two coordinates points crosses the goal line
        nb_average = self.line_amort  # has effect on delay

        # the position to consider the trajectory line
        position_before = [0, 0]
        # as, having only the precedent one multiply the noise amplification by distance
        if len(self.filtered_positions) < nb_average:
            position_before = self.positions[-2]
        else:
            x_average = sum([self.filtered_positions[-i][0]
                             for i in range(1, nb_average+1)])/nb_average
            y_average = sum([self.filtered_positions[-i][1]
                             for i in range(1, nb_average+1)])/nb_average
            position_before = [x_average, y_average]

        ball_line = line(position_before, self.filtered_positions[-1])
        intersection_point = intersect(goal_line, ball_line)

        if intersection_point is None:
            return None

        if not self.approaching(intersection_point):
            return None

        # we are sure the point is on the goal line
        v = self.goal[0][0] - \
            intersection_point[0], self.goal[0][1] - intersection_point[1]
        vgoal = self.goal[0][0] - \
            self.goal[1][0], self.goal[0][1] - self.goal[1][1]
        side = v[0]*vgoal[0] + v[1]*vgoal[1]
        if side < 0:
            return None

        v = self.goal[1][0] - \
            intersection_point[0], self.goal[1][1] - intersection_point[1]
        vgoal = self.goal[1][0] - \
            self.goal[0][0], self.goal[1][1] - self.goal[0][1]
        side = v[0]*vgoal[0] + v[1]*vgoal[1]
        if side < 0:
            return None

        # then the point is within th goal
        return ((intersection_point[0]-self.goal[0][0])**2 + (intersection_point[1]-self.goal[0][1])**2)**0.5
