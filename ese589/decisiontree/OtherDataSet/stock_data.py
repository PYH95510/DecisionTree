import numpy as np
file=open("data/kohkiloyeh.csv")

read_dtypes = \
[
    ('degree', '<S16'), 
    ('caprice', '<S16'), 
    ('topic', '<S16'),
    ('limit', '<S16'),
    ('stopLossOrder', '<S16'),
    ('pricetoBook', '<S16'),
]


# Replace the above routine with the generalized routine below
# Create empty array
dtypes = [None] * len(read_dtypes)
for index, read_dtype in enumerate(read_dtypes):
    if read_dtype[1] != np.float32 and read_dtype[1] != np.int32:
        dtypes[index] = (read_dtype[0], np.int32) # type: ignore
    else:
        dtypes[index] = read_dtype


lines = file.readlines()
read_table = np.zeros(shape=(len(lines)), dtype=read_dtypes)

for index, line in enumerate(lines):
    cols = line.split(',')
    if len(cols) == 0:
        continue
    
    cols = [col.strip() for col in cols]

    entry = np.array(
        [(
            cols[0], 
            cols[1], 
            cols[2], 
            cols[3], 
            cols[4], 
            cols[5], 
        )],
        dtype=read_dtypes)
    read_table[index] = entry

data_table = np.zeros_like(read_table, dtype=dtypes)



# Replace the above routine with the generalized routine below
for read_dtype in read_dtypes:
    if (read_dtype[1] != np.int32 and read_dtype[1] != np.float32):
        _, data_table[read_dtype[0]] = np.unique(read_table[read_dtype[0]], return_inverse=True)
    else:
        data_table[read_dtype[0]] = read_table[read_dtype[0]]

print(data_table)