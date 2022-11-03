cimport numpy as np
import numpy as np

cpdef double perpendicular_distanse(np.ndarray point, np.ndarray line_start_point, np.ndarray line_end_point):
    # function for baseline y = ax + b
    cdef double point_x = point[0]
    cdef double point_y = point[1]
    cdef double start_x = line_start_point[0]
    cdef double start_y = line_start_point[1]
    cdef double end_x = line_end_point[0]
    cdef double end_y = line_end_point[1]

    # find slope of line
    cdef double a = (end_y - start_y) / (end_x - start_x)

    # find offset of line
    cdef double b = start_y - a * start_x

    # line equation in general form
    # ax + by + c = 0
    # in our case:
    # ax - y + b = 0
    cdef double d = abs(a * point_x + (-1) * point_y + b) / (a**2 + 1) ** 0.5
    return d

cpdef np.ndarray[np.float64_t,ndim=1] RDP(np.ndarray[np.float64_t,ndim=2] line, double epsilon):
    cdef int start_idx = 0
    cdef int end_idx = len(line) - 1
    cdef double max_dist = 0  # var to store furthest point dist
    cdef int max_id = 0  # var to store furthest point index

    cdef int i = 0
    cdef double d
    cdef np.ndarray[np.float64_t,ndim=2] l, r, results
    
    for i from (start_idx + 1) <= i < (end_idx):
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


cpdef double perpendicular_distanse_tuple((double,double) point, (double,double) line_start_point, (double,double) line_end_point):
    # function for baseline y = ax + b
    cdef double point_x = point[0]
    cdef double point_y = point[1]
    cdef double start_x = line_start_point[0]
    cdef double start_y = line_start_point[1]
    cdef double end_x = line_end_point[0]
    cdef double end_y = line_end_point[1]

    # find slope of line
    cdef double a = (end_y - start_y) / (end_x - start_x)

    # find offset of line
    cdef double b = start_y - a * start_x

    # line equation in general form
    # ax + by + c = 0
    # in our case:
    # ax - y + b = 0
    cdef double d = abs(a * point_x + (-1) * point_y + b) / (a**2 + 1) ** 0.5
    return d

# cpdef ((double, double)) RDP_tuple(np.ndarray[np.float64_t,ndim=2] line, double epsilon):
#     cdef int start_idx = 0
#     cdef int end_idx = len(line) - 1
#     cdef double max_dist = 0  # var to store furthest point dist
#     cdef int max_id = 0  # var to store furthest point index

#     cdef int i = 0
#     cdef double d
#     cdef ((double, double)) l, r, results

#     line = tuple(map(tuple, line))
    
#     for i from (start_idx + 1) <= i < (end_idx):
#         d = perpendicular_distanse_tuple(line[i], line[start_idx], line[end_idx])
#         if d > max_dist:
#             max_dist = d  # overwrite max distance
#             max_id = i  # overwrite max index

#     if max_dist > epsilon:
#         l = RDP_tuple(line[start_idx : max_id + 1], epsilon)
#         r = RDP_tuple(line[max_id:], epsilon)

#         results = l[:-1] + r
#         return results

#     else:
#         results = (line[0],) + (line[end_idx],)
#         return results

cpdef tuple RDP_tuple(tuple line, double epsilon):
    cdef int start_idx = 0
    cdef int end_idx = len(line) - 1
    cdef double max_dist = 0  # var to store furthest point dist
    cdef int max_id = 0  # var to store furthest point index

    cdef int i = 0
    cdef double d
    cdef tuple l, r, results
    
    for i from (start_idx + 1) <= i < (end_idx):
        d = perpendicular_distanse_tuple(line[i], line[start_idx], line[end_idx])
        if d > max_dist:
            max_dist = d  # overwrite max distance
            max_id = i  # overwrite max index

    if max_dist > epsilon:
        l = RDP_tuple(line[start_idx : max_id + 1], epsilon)
        r = RDP_tuple(line[max_id:], epsilon)

        results = l[:-1] + r
        return results

    else:
        results = (line[0],) + (line[end_idx],)
        return results