import helloworld as hw
from mpi4py import MPI

null = MPI.COMM_NULL
hw.sayhello(null)

comm = MPI.COMM_WORLD
hw.sayhello(comm)

try:
    hw.sayhello(list())
except:
    pass
else:
    assert 0, "exception not raised"
