from typing import Tuple, Union, List, Type
import numpy as np

class AttributeHeader:
    is_continuous: bool
    attribute_names: Union[np.ndarray, None]
    data_col_index: int
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
        self.data_col_index = -1
        self.read_dtype = read_dtype
        self.csv_col_index = csv_col_index


def _read_dataset(csv: List[str], attrib_headers: List[AttributeHeader]):
    read_dtypes = [attrib_header.read_dtype for attrib_header in attrib_headers]

    # Create empty array
    dtypes = [None] * len(read_dtypes)

    # Create dtype list with string attributes replaced with int attributes
    for index, attrib_header in enumerate(attrib_headers):
        if attrib_headers[index].is_continuous:
            dtypes[index] = attrib_header.read_dtype # type: ignore
        else:
            dtypes[index] = (attrib_header.read_dtype[0], np.int32) # type: ignore

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
    for i, attrib_header in enumerate(attrib_headers):
        read_dtype = attrib_header.read_dtype
        attrib_header.data_col_index = i
        
        if attrib_header.is_continuous:
            data_table[read_dtype[0]] = read_table[read_dtype[0]]
        else:
            attrib_header.attribute_names, data_table[read_dtype[0]] = \
                np.unique(read_table[read_dtype[0]], return_inverse=True)

    return data_table

def read_adult_dataset():
    file = open('data/adult.data')
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

def read_autism_adolescent_dataset():
    file = open('data/Autism-Adolescent-Data.arff')
    lines = file.readlines()
    lines = lines[25:128]

    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('a1Score', np.int32), 0),
        AttributeHeader(False, ('a2Score', np.int32), 1),
        AttributeHeader(False, ('a3Score', np.int32), 2),
        AttributeHeader(False, ('a4Score', np.int32), 3),
        AttributeHeader(False, ('a5Score', np.int32), 4),
        AttributeHeader(False, ('a6Score', np.int32), 5),
        AttributeHeader(False, ('a7Score', np.int32), 6),
        AttributeHeader(False, ('a8Score', np.int32), 7),
        AttributeHeader(False, ('a9Score', np.int32), 8),
        AttributeHeader(False, ('a10Score', np.int32), 9),
        # AttributeHeader(True, ('age', np.float32), 10),
        # AttributeHeader(False, ('gender', '<S8'), 11),
        # AttributeHeader(False, ('ethnicity', '<S16'), 12),
        # AttributeHeader(False, ('jundice', '<S8'), 13),
        # AttributeHeader(False, ('autism', '<S8'), 14),
        # AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        # AttributeHeader(False, ('relation', '<S16'), 19),
        AttributeHeader(False, ("class", '<S8'), 20),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_autism_adult_dataset():
    file = open('data/Autism-Adult-Data.arff')
    lines = file.readlines()
    lines = lines[25:728]

    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('a1Score', np.int32), 0),
        AttributeHeader(False, ('a2Score', np.int32), 1),
        AttributeHeader(False, ('a3Score', np.int32), 2),
        AttributeHeader(False, ('a4Score', np.int32), 3),
        AttributeHeader(False, ('a5Score', np.int32), 4),
        AttributeHeader(False, ('a6Score', np.int32), 5),
        AttributeHeader(False, ('a7Score', np.int32), 6),
        AttributeHeader(False, ('a8Score', np.int32), 7),
        AttributeHeader(False, ('a9Score', np.int32), 8),
        AttributeHeader(False, ('a10Score', np.int32), 9),
        # AttributeHeader(True, ('age', np.float32), 10),
        # AttributeHeader(False, ('gender', '<S8'), 11),
        # AttributeHeader(False, ('ethnicity', '<S16'), 12),
        # AttributeHeader(False, ('jundice', '<S8'), 13),
        # AttributeHeader(False, ('autism', '<S8'), 14),
        # AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        # AttributeHeader(False, ('relation', '<S16'), 19),
        AttributeHeader(False, ("class", '<S8'), 20),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table
