# https://github.com/melanieimfeld/Small-spatial-algorithms

import numpy as np


def perpendicular_distanse(point, line_start_point, line_end_point):
    # function for baseline y = ax + b
    point_x, point_y = point[0], point[1]
    start_x, start_y = line_start_point[0], line_start_point[1]
    end_x, end_y = line_end_point[0], line_end_point[1]

    # find slope of line
    a = (end_y - start_y) / (end_x - start_x)

    # find offset of line
    b = start_y - a * start_x

    # line equation in general form
    # ax + by + c = 0
    # in our case:
    # ax - y + b = 0
    d = abs(a * point_x + (-1) * point_y + b) / (a**2 + 1) ** 0.5
    return d


def RDP(line, epsilon):
    start_idx = 0
    end_idx = len(line) - 1
    max_dist = 0  # var to store furthest point dist
    max_id = 0  # var to store furthest point index

    for i in range(start_idx + 1, end_idx):
        d = perpendicular_distanse(line[i], line[start_idx], line[end_idx])
        if d > max_dist:
            max_dist = d  # overwrite max distance
            max_id = i  # overwrite max index

    if max_dist > epsilon:
        l = RDP(line[start_idx : max_id + 1], epsilon)
        r = RDP(line[max_id:], epsilon)

        results = np.vstack((l[:-1], r))
        return results

    else:
        results = np.vstack((line[0], line[end_idx]))
        return results
