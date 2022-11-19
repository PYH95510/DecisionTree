from typing import Tuple, Union, List, Type
import numpy as np

class AttributeHeader:
    is_continuous: bool
    attribute_names: Union[np.ndarray, None]
    read_dtype: Tuple[str, Union[str, Type[np.float32], Type[np.int32]]]
    csv_col_index: int

    def __init__(
        self,
        is_continuous: bool, 
        read_dtype: Tuple[str, Union[str, Type[np.float32], Type[np.int32]]],
        csv_col_index: int
        ):
        self.is_continuous = is_continuous
        self.attribute_names = None
        self.read_dtype = read_dtype
        self.csv_col_index = csv_col_index


def _read_dataset(csv: List[str], attrib_headers: List[AttributeHeader]):
    read_dtypes = [attrib_header.read_dtype for attrib_header in attrib_headers]

    # Create empty array
    dtypes = [None] * len(read_dtypes)

    # Create dtype list with string attributes replaced with int attributes
    for index, read_dtype in enumerate(read_dtypes):
        if attrib_headers[index].is_continuous:
            dtypes[index] = read_dtype # type: ignore
        else:
            dtypes[index] = (read_dtype[0], np.int32) # type: ignore

    read_table = np.zeros(shape=(len(csv)), dtype=read_dtypes)

    for index, line in enumerate(csv):
        cols = line.split(',')
        if len(cols) == 0:
            continue
        
        cols = [col.strip() for col in cols]
        entry = tuple([cols[attrib_header.csv_col_index] for attrib_header in attrib_headers])
        entry = np.array([entry], dtype=read_dtypes)
        read_table[index] = entry

    data_table = np.zeros_like(read_table, dtype=dtypes)

    # Convert string columns to int (enum) columns
    for read_dtype, attrib_header in zip(read_dtypes, attrib_headers):
        if attrib_header.is_continuous:
            data_table[read_dtype[0]] = read_table[read_dtype[0]]
        else:
            attrib_header.attribute_names, data_table[read_dtype[0]] = \
                np.unique(read_table[read_dtype[0]], return_inverse=True)

    return data_table

def read_adult_dataset():
    file = open("data/adult.data")
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(True,   ('age', np.float32),            0),
        AttributeHeader(False,  ('workClass', '<S16'),          1),
        AttributeHeader(False,  ('education', '<S16'),          3),
        AttributeHeader(True,   ('educationNum', np.float32),   4),
        AttributeHeader(False,  ('maritalStatus', '<S16'),      5),
        AttributeHeader(False,  ('occupation', '<S16'),         6),
        AttributeHeader(False,  ('relationship', '<S16'),       7),
        AttributeHeader(False,  ('race', '<S16'),               8),
        AttributeHeader(False,  ('sex', '<S16'),                9),
        AttributeHeader(True,   ('hoursPerWeek', np.float32),   12),
        AttributeHeader(False,  ('nativeCountry', '<S16'),      13),
        AttributeHeader(False,  ('more50K', '<S16'),            14)
    ]

    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table
