import random

default_angle = 0.1


def get_center(*points):
    return 1 / 3 * sum(points[::2]), 1 / 3 * sum(points[1::2])


def sign(point, l_start, l_end):
    return (point[0] - l_end[0]) * (l_start[1] - l_end[1]) - (l_start[0] - l_end[0]) * (point[1] - l_end[1])


def point_in_sector(point, sector):
    x1, y1, x2, y2, x3, y3 = sector
    s1 = sign(point, (x1, y1), (x2, y2))
    s2 = sign(point, (x2, y2), (x3, y3))
    s3 = sign(point, (x3, y3), (x1, y1))
    negative = (s1 < 0) or (s2 < 0) or (s3 < 0)
    positive = (s1 > 0) or (s2 > 0) or (s3 > 0)
    return not (negative and positive)


def get_rand_rotation():
    rand = random.random()
    angle = random.uniform(-default_angle, default_angle) if rand > 0.9 else 0.0
    return angle
