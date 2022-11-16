# note
"""
This file computes SSPD trajectory distance matrix for given spatial data
"""
# COMPUTING ON  MULTIPLE CORE

import time
from multiprocessing import Pool

import numpy as np
import traj_dist.distance as tdist

from utils.path import (
    EXITED_DISTANCE_MATRIX,
    EXITED_TRAJECTORY_FILENAME,
    GROUND_DISTANCE_MATRIX,
    GROUND_TRAJECTORY_FILENAME,
    RESULT_DIR,
    TRAJ_DIR,
    NUMBER_OF_TRAJS,
)

G_trajectories = np.load(TRAJ_DIR + GROUND_TRAJECTORY_FILENAME, allow_pickle=True)[
    :NUMBER_OF_TRAJS
]
E_trajectories = np.load(TRAJ_DIR + EXITED_TRAJECTORY_FILENAME, allow_pickle=True)[
    :NUMBER_OF_TRAJS
]

"First compute ground trajectories"
traj_list = np.copy(G_trajectories)


def task(index_i, index_j):
    traj_list_i = traj_list[index_i]
    traj_list_j = traj_list[index_j]
    return tdist.sspd(traj_list_i, traj_list_j)


# initial parameters
traj_count = len(traj_list)
M = np.zeros(sum(range(traj_count)))
im = 0
index_list = []
for i in range(traj_count):
    for j in range(i + 1, traj_count):
        index_list.append((i, j))

print(
    f"Confugured {len(M)} distanses for {traj_count} trajectories\nComputation starts"
)

st = time.time()
with Pool() as pool:
    print("Pool created")
    for result in pool.starmap(task, index_list, chunksize=1):
        M[im] = result
        im += 1
et = time.time()

print(f"G matrix was computed in {(et-st)/60/60} hours")

# Save data
np.save(RESULT_DIR + GROUND_DISTANCE_MATRIX, M)


# Then compute exited trajectories
traj_list = np.copy(E_trajectories)


# initial parameters
traj_count = len(traj_list)
M = np.zeros(sum(range(traj_count)))
im = 0
index_list = []
for i in range(traj_count):
    for j in range(i + 1, traj_count):
        index_list.append((i, j))

print(
    f"Confugured {len(M)} distanses for {traj_count} trajectories\nComputation starts"
)

st = time.time()
with Pool() as pool:
    print("Pool created")
    for result in pool.starmap(task, index_list, chunksize=1):
        M[im] = result
        im += 1
et = time.time()

print(f"E matrix was computed in {(et-st)/60/60} hours")

# Save data
np.save(RESULT_DIR + EXITED_DISTANCE_MATRIX, M)
