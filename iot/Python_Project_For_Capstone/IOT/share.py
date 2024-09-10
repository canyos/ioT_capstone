from multiprocessing import shared_memory
import array
import numpy as np
# a = np.array([0,1,2,3,4,5])
# shm = shared_memory.SharedMemory(create=True, size = a.nbytes)

# b = np.ndarray(a.shape, dtype = a.dtype, buffer=shm.buf)
# b[:] = a[:]



a = np.array([0,1,2,3,4,5])
shm = shared_memory.SharedMemory(create=True, size = a.nbytes)

# b = np.ndarray(a.shape, dtype = a.dtype, buffer=shm.buf)
b = shm
# b[:] = a[:]

print(b)

shm.close()
shm.unlink()