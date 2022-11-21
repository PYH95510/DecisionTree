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
        # Too many attributes
        # AttributeHeader(False,  ('nativeCountry', '<S16'),      13),
        AttributeHeader(False,  ('more50K', '<S16'),            14)
    ]

    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_autism_adolescent_dataset():
    file = open('data/Autism-Adolescent-Data.arff')
    lines = file.readlines()
    
    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('a1', np.int32), 0),
        AttributeHeader(False, ('a2', np.int32), 1),
        AttributeHeader(False, ('a3', np.int32), 2),
        AttributeHeader(False, ('a4', np.int32), 3),
        AttributeHeader(False, ('a5', np.int32), 4),
        AttributeHeader(False, ('a6', np.int32), 5),
        AttributeHeader(False, ('a7', np.int32), 6),
        AttributeHeader(False, ('a8', np.int32), 7),
        AttributeHeader(False, ('a9', np.int32), 8),
        AttributeHeader(False, ('a10', np.int32), 9)

        # AttributeHeader(True, ('age', np.float32), 10),
        # AttributeHeader(False, ('gender', '<S8'), 11),
        # AttributeHeader(False, ('ethnicity', '<S16'), 12),
        # AttributeHeader(False, ('jundice', '<S8'), 13),
        # AttributeHeader(False, ('autism', '<S8'), 14),
        # AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        # AttributeHeader(False, ('relation', '<S16'), 19),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_autism_adult_dataset():
    file = open('data/Autism-Adult-Data.arff')
    lines = file.readlines()

    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('a1', np.int32), 0),
        AttributeHeader(False, ('a2', np.int32), 1),
        AttributeHeader(False, ('a3', np.int32), 2),
        AttributeHeader(False, ('a4', np.int32), 3),
        AttributeHeader(False, ('a5', np.int32), 4),
        AttributeHeader(False, ('a6', np.int32), 5),
        AttributeHeader(False, ('a7', np.int32), 6),
        AttributeHeader(False, ('a8', np.int32), 7),
        AttributeHeader(False, ('a9', np.int32), 8),
        AttributeHeader(False, ('a10', np.int32), 9)

        # AttributeHeader(True, ('age', np.float32), 10),
        # AttributeHeader(False, ('gender', '<S8'), 11),
        # AttributeHeader(False, ('ethnicity', '<S16'), 12),
        # AttributeHeader(False, ('jundice', '<S8'), 13),
        # AttributeHeader(False, ('autism', '<S8'), 14),
        # AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        # AttributeHeader(False, ('relation', '<S16'), 19),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_balance_scale_dataset():
    file = open('data/balance-scale.data')
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(False,  ('leftWeight', np.int32),   1),
        AttributeHeader(False,  ('leftDist', np.int32),     2),
        AttributeHeader(False,  ('rightWeight', np.int32),  3),
        AttributeHeader(False,  ('rightDist', np.int32),    4),
        AttributeHeader(False,  ('class', '<S1'),        0)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)

    np.random.seed(1)
    np.random.shuffle(data_table)

    return attrib_headers, data_table

def read_breast_cancer_dataset():
    file = open('data/breast-cancer.data')
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(False,  ('age', '<S16'),        1),
        AttributeHeader(False,  ('menopuase', '<S16'),  2),
        AttributeHeader(False,  ('tumorSize', '<S16'),  3),
        AttributeHeader(False,  ('invNodes', '<S16'),   4),
        AttributeHeader(False,  ('class', '<S16'),      0)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    np.random.seed(1)
    np.random.shuffle(data_table)

    return attrib_headers, data_table

def read_credit_approval_data():
    file = open('data/crx.data')
    lines = file.readlines()

    # Note that the attribute names have been obfuscated to protect confidentiality
    attrib_headers = [
        AttributeHeader(False,  ('a1', '<S16'),     0),
        AttributeHeader(True,   ('a2', np.float32), 1),
        AttributeHeader(True,   ('a3', np.float32), 2),
        AttributeHeader(False,  ('a4', '<S16'),     3),
        AttributeHeader(False,  ('a5', '<S16'),     4),
        AttributeHeader(False,  ('a6', '<S16'),     5),
        AttributeHeader(False,  ('a7', '<S16'),     6),
        AttributeHeader(True,   ('a8', np.float32), 7),
        AttributeHeader(False,  ('a9', '<S16'),     8),
        AttributeHeader(False,  ('class', '<S16'), 15)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)

    return attrib_headers, data_table

def read_credit_card_client_dataset():
    file = open('data/default of credit card clients.csv')
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(True,   ('amountofGivenCredit', np.float32),    1),
        AttributeHeader(False,  ('sex', np.int32),                      2),
        AttributeHeader(False,  ('education', np.int32),                3),
        AttributeHeader(False,  ('maritalStatus', np.int32),            4),
        AttributeHeader(True,   ('age', np.float32),                    5),
        AttributeHeader(False,  ('defaulted', np.int32),                24)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def read_diabetes_dataset():
    file = open('data/diabetes_data_upload.csv')
    lines = file.readlines()
    lines = lines[1:]

    attrib_headers = [
        AttributeHeader(True,   ('age', np.float32),             0),
        AttributeHeader(False,  ('sex', '<S16'),                 1),
        AttributeHeader(False,  ('Polyuria', '<S16'),            2),
        AttributeHeader(False,  ('suddenWeightLoss', '<S16'),    4),
        AttributeHeader(False,  ('weakness', 'S16'),             5),
        AttributeHeader(False,  ('visualBlurring', '<S16'),      8),
        AttributeHeader(False,  ('Obesity', '<S16'),             15),
        AttributeHeader(False,  ('class', 'S16'),                16)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    

def read_obs_network_dataset():
    file = open('data/OBS-Network-DataSet_2_Aug27.arff')
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(True, ('utilizedBandwidthRate', np.float32), 1),
        AttributeHeader(True, ('packetDroprate', np.float32), 2),
        AttributeHeader(True, ('fullBandwidth', np.float32), 3),
        AttributeHeader(True, ('avgDelayTime', np.float32), 4),
        AttributeHeader(True, ('percentLostPacketRate', np.float32), 5),
        AttributeHeader(True, ('percentLostByteRate', np.float32), 6),
        AttributeHeader(False, ('class', '<S16'), 21)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    

def read_cervical_cancer_dataset():
    file = open('data/risk_factors_cervical_cancer.csv')
    lines = file.readlines()
    lines = lines[1:]

    attrib_headers = [
        AttributeHeader(True,   ('age', np.float32),                    0),
        AttributeHeader(True,   ('numberofSexualPartners', np.float32), 1),
        AttributeHeader(True,   ('firstSexualIntercourse', np.float32), 2),
        AttributeHeader(True,   ('numberofPregnancies', np.float32),    3),
        AttributeHeader(False,  ('smokes', np.int32),                   4),
        AttributeHeader(False,  ('hormonalContraceptive', np.int32),    7),
        AttributeHeader(False,  ('iud', np.int32),                      9),
        AttributeHeader(False,  ('std', np.int32),                      11),
        AttributeHeader(False,  ('class', np.int32),                    35),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_student_academic_performance_dataset():
    file = open('data/Sapfile1.arff')
    lines = file.readlines()
    lines = lines[27:157]

    attrib_headers = [
        AttributeHeader(False, ('sex', '<S16'),  0),
        AttributeHeader(False, ('caste','<S16'), 1),
        AttributeHeader(False, ('internalAssessmentPercentage', '<S16'), 4),
        AttributeHeader(False, ('maritalStatus', '<S16'), 7),
        AttributeHeader(False, ('townOrVillage', '<S16'), 8),
        AttributeHeader(False, ('fatheroccupation', '<S16'), 14),
        AttributeHeader(False, ('motheroccupation', '<S16'), 15),
        AttributeHeader(False, ('attendance', '<S16'), 21),
        AttributeHeader(False, ('endSemesterPercentage', '<S16'), 5),
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_pixel_image_dataset():
    file = open('data/segmentation.data')
    lines = file.readlines()
    lines = lines[5:]

    attrib_headers = [
        AttributeHeader(True,   ('rawRedMean', np.float32),     11),
        AttributeHeader(True,   ('rawBlueMean', np.float32),    12),
        AttributeHeader(True,   ('rawGreenMean', np.float32),   13),
        AttributeHeader(True,   ('valueMean', np.float32),      17),
        AttributeHeader(True,   ('saturationMean', np.float32), 18),
        AttributeHeader(True,   ('hueMean', np.float32),        19),
        AttributeHeader(False,  ('class', '<S16'),              0)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_seismic_bumps_dataset():
    file = open('data/seismic-bumps.arff')
    lines = file.readlines()
    lines = lines[154:]

    attrib_headers = [
        AttributeHeader(False,  ('seismic', '<S1'),         0),
        AttributeHeader(False,  ('seismoacoustic', '<S1'),  1),
        AttributeHeader(False,  ('shift', '<S1'),           2),
        AttributeHeader(True,   ('gdenergy', np.float32),   3),
        AttributeHeader(True,   ('gdpuls', np.float32),     4),
        AttributeHeader(False,  ('ghazard', '<S1'),         7),
        AttributeHeader(False,  ('class', np.int32),        18)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_somerville_happiness_dataset():
    file = open('data/SomervilleHappinessSurvey2015.csv')
    lines = file.readlines()
    lines = lines[1:]
 
    attrib_headers = [
        AttributeHeader(True,   ('cityService', np.int32),          1),
        AttributeHeader(True,   ('costofHousing', np.int32),        2),
        AttributeHeader(True,   ('qualityofPubSchool', np.int32),   3),
        AttributeHeader(True,   ('trustofPolice', np.int32),        4),
        AttributeHeader(True,   ('maintenanceofRoads', np.int32),   5),
        AttributeHeader(True,   ('socialEvents', np.int32),         6),
        AttributeHeader(False,  ('happyUnhappy', np.int32),         0)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table

def read_spambase_dataset():
    file = open('data/spambase.data')
    lines = file.readlines()

    attrib_headers = [
        AttributeHeader(True,   ('freqMake', np.float32),       1),
        AttributeHeader(True,   ('freqAddress', np.float32),    2),
        AttributeHeader(True,   ('freqAll', np.float32),        3),
        AttributeHeader(True,   ('freq3D', np.float32),         4),
        AttributeHeader(True,   ('freqOur', np.float32),        5),
        AttributeHeader(True,   ('freqOver', np.float32),       6),
        AttributeHeader(True,   ('freqRemove', np.float32),     7),
        AttributeHeader(True,   ('freqInternet', np.float32),   8),
        AttributeHeader(True,   ('freqOrder', np.float32),      9),
        AttributeHeader(False,  ('isSpam', np.float32),         0)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table
