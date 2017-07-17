from mpi4py import MPI
import numpy as np
import time
import cProfile

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = np.array([0])

def sleep_send(a):
    time.sleep(3)
    comm.Bcast(a, root = 0)
    return

def awake_receive(a):
    comm.Bcast(a, root = 0)
    return

if rank == 0:
    data = np.array([1])
    profileName = "time_sleep_rank"+str(rank)
    cProfile.run('sleep_send(data)',profileName)
else:
    profileName = "time_sleep_rank"+str(rank)
    cProfile.run('awake_receive(data)',profileName)

print "Rank = "+str(rank)+", data = "+str(data)