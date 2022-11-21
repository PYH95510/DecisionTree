import numpy as np

def gen_bipartition(array: np.ndarray):
    assert(array.shape[0] < 31)

    max_iter = np.uint32(1) << np.uint32(array.shape[0])

    for i in range(0, max_iter):
        sel_mask = np.unpackbits(np.array([i], dtype=np.uint32).view(np.uint8), bitorder='little')[:array.shape[0]]
        sel_mask = sel_mask.astype(np.bool8)
        yield array[sel_mask], array[np.logical_not(sel_mask)]

def num_bipartition(array: np.ndarray):
    return 1 << array.shape[0]
