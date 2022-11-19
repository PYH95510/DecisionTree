import numpy as np
file=open("data/default of credit card clients.csv")

read_dtypes = \
[
    ('amountofGivenCredit', np.float32), 
    ('sex', np.float32), 
    ('education', np.float32),
    ('maritalStatus', np.float32),
    ('age', np.float32)
]

# dtypes = \
# [
#     ('age', np.float32), 
#     ('workClass', np.int32), 
#     ('education', np.int32),
#     ('educationNum', np.float32),
#     ('maritalStatus', np.int32),
#     ('occupation', np.int32),
#     ('relationship', np.int32),
#     ('race', np.int32),
#     ('sex', np.int32),
#     ('hoursPerWeek', np.float32),
#     ('nativeCountry', np.int32),
#     ('more50K', np.int32)
# ]

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
            cols[1], 
            cols[2], 
            cols[3], 
            cols[4], 
            cols[5], 
        )],
        dtype=read_dtypes)
    read_table[index] = entry

data_table = np.zeros_like(read_table, dtype=dtypes)

# data_table['age'] = read_table['age']
# _, data_table['workClass'] = np.unique(read_table['workClass'], return_inverse=True)
# _, data_table['education'] = np.unique(read_table['education'], return_inverse=True)
# data_table['educationNum'] = read_table['educationNum']
# _, data_table['maritalStatus'] = np.unique(read_table['maritalStatus'], return_inverse=True)
# _, data_table['occupation'] = np.unique(read_table['occupation'], return_inverse=True)
# _, data_table['relationship'] = np.unique(read_table['relationship'], return_inverse=True)
# _, data_table['race'] = np.unique(read_table['race'], return_inverse=True)
# _, data_table['sex'] = np.unique(read_table['sex'], return_inverse=True)
# data_table['hoursPerWeek'] = read_table['hoursPerWeek']
# _, data_table['nativeCountry'] = np.unique(read_table['nativeCountry'], return_inverse=True)
# _, data_table['more50K'] = np.unique(read_table['more50K'], return_inverse=True)

# Replace the above routine with the generalized routine below
for read_dtype in read_dtypes:
    if (read_dtype[1] != np.int32 and read_dtype[1] != np.float32):
        _, data_table[read_dtype[0]] = np.unique(read_table[read_dtype[0]], return_inverse=True)
    else:
        data_table[read_dtype[0]] = read_table[read_dtype[0]]

print(data_table)