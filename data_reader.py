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
    lines = lines[1:104]

    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('age', np.int32), 10),
        AttributeHeader(False, ('sex', '<S16'), 11),
        AttributeHeader(False, ('ethnicity','<S16'), 12),
        AttributeHeader(False, ('jundice', '<S16'), 13),
        AttributeHeader(False, ('autism', '<S16'), 14),
        AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        AttributeHeader(False, ('relation', '<S16'), 19)

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
    lines = lines[26:729]

    # Too little data. Only use the A scores for this
    attrib_headers = [
        AttributeHeader(False, ('age', np.int32), 10),
        AttributeHeader(False, ('sex', '<S16'), 11),
        AttributeHeader(False, ('ethnicity','<S16'), 12),
        AttributeHeader(False, ('jundice', '<S16'), 13),
        AttributeHeader(False, ('autism', '<S16'), 14),
        AttributeHeader(False, ('countryOfResidence', '<S16'), 15),
        AttributeHeader(False, ('relation', '<S16'), 19)
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

def census_income_dataset():
    file = open('data/census-income.data')
    lines = file.readlines()
    lines = lines[1:199523]


    attrib_headers = [
        AttributeHeader(False, ('age', np.int32), 0),
        AttributeHeader(False, ('occupation', '<S16'), 1),
        AttributeHeader(False, ('education', '<S16'), 4),
        AttributeHeader(False, ('maritalStatus', '<S16'), 7),
        AttributeHeader(False, ('ethnicity', '<S16'), 10),
        AttributeHeader(False, ('sex', '<S16'), 12),
        AttributeHeader(False, ('originCountry', '<S16'), 35)
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def creditcard_client_dataset():
    file = open('data/default of credit card clients.csv')
    lines = file.readlines()
    lines = lines[1:30000]


    attrib_headers = [
        AttributeHeader(False, ('amountofGivenCredit', np.float32), 1),
        AttributeHeader(False, ('sex', np.float32), 2),
        AttributeHeader(False, ('education', np.float32), 3),
        AttributeHeader(False, ('maritalStatus', np.float32), 4),
        AttributeHeader(False, ('age', np.float32), 5)

  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def diabetes_dataset():
    file = open('data/diabetes_data_upload.csv')
    lines = file.readlines()
    lines = lines[1:521]


    attrib_headers = [
        AttributeHeader(False, ('age', '<S16'), 0),
        AttributeHeader(False, ('sex', '<S16'), 1),
        AttributeHeader(False, ('Polyuria', '<S16'), 2),
        AttributeHeader(False, ('suddenWeightLoss', '<S16'), 4),
        AttributeHeader(False, ('weakness', 'S16'), 5),
        AttributeHeader(False, ('visualBlurring', '<S16'), 8),
        AttributeHeader(False, ('Obesity', '<S16'), 15),
        AttributeHeader(False, ('class', 'S16'), 16)
    
    
    
    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    


def stock_dataset():
    file = open('data/kohkiloyeh.csv')
    lines = file.readlines()
    lines = lines[1:101]


    attrib_headers = [
        AttributeHeader(False, ('degree', '<S16'), 0),
        AttributeHeader(False, ('caprice', '<S16'), 1),
        AttributeHeader(False, ('topic', '<S16'), 2),
        AttributeHeader(False, ('limit', '<S16'), 4),
        AttributeHeader(False, ('stopLossOrder', '<S16'), 5),
        AttributeHeader(False, ('pricetoBook', '<S16'), 8)
    
     
    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    



def obs_network_dataset():
    file = open('data/OBS-Network-DataSet_2_Aug27.arff')
    lines = file.readlines()
    lines = lines[1:1075]


    attrib_headers = [
        AttributeHeader(False, ('node', np.float32),  0),
        AttributeHeader(False, ('packet_Size_Bite', np.float32), 1),
        AttributeHeader(False, ('packet_Transmitted', np.float32), 2),
        AttributeHeader(False, ('nodeStatus', '<S16'), 4),
        AttributeHeader(False, ('class', '<S16'), 5)

     

    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    



def page_block_dataset():
    file = open('data/page-blocks.data')
    lines = file.readlines()
    lines = lines[1:5473]


    attrib_headers = [
        AttributeHeader(False, ('height', np.float32),  0),
        AttributeHeader(False, ('length', np.float32), 1),
        AttributeHeader(False, ('area', np.float32), 2),
        AttributeHeader(False, ('blackPixels', np.float32), 8),
        AttributeHeader(False, ('blackAnd', np.float32), 9),
        AttributeHeader(False, ('whiteBlackTransition', np.float32), 10)

     

    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table    


def risk_factors_dataset():
    file = open('data/risk_factors_cervical_cancer.csv')
    lines = file.readlines()
    lines = lines[2:859]


    attrib_headers = [
        AttributeHeader(False, ('Age', np.float32),  0),
        AttributeHeader(False, ('numberofSexualPartners', np.float32), 1),
        AttributeHeader(False, ('firstSexualIntercourse', np.float32), 2),
        AttributeHeader(False, ('numberofPregnancies', np.float32), 3),
        AttributeHeader(False, ('Smokes', np.float32), 4),
        AttributeHeader(False, ('smokeYears', np.float32), 5),
        AttributeHeader(False, ('smokePacksPerYears', np.float32), 6)
        

    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table



def student_academic_performance_dataset():
    file = open('data/Sapfile1.arff')
    lines = file.readlines()
    lines = lines[28:158]


    attrib_headers = [
        AttributeHeader(False, ('sex', '<S16'),  0),
        AttributeHeader(False, ('testNotPerformed','<S16'), 2),
        AttributeHeader(False, ('township', '<S16'), 3),
        AttributeHeader(False, ('independentAssessment', '<S16'), 4),
        AttributeHeader(False, ('extrasensoryperception', '<S16'), 5),
        AttributeHeader(False, ('maritalStatus', '<S16'), 7),
        AttributeHeader(False, ('fatheroccupation', '<S16'), 14),
        AttributeHeader(False, ('motheroccupation', '<S16'), 15),
        AttributeHeader(False, ('attendance', '<S16'), 21)
        

    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def pixel_image_dataset():
    file = open('data/segmentation.data')
    lines = file.readlines()
    lines = lines[6:215]


    attrib_headers = [
        AttributeHeader(False, ('regionalCentroidCol', np.float32),  0),
        AttributeHeader(False, ('regionCentroidRow', np.float32), 1),
        AttributeHeader(False, ('regionPixelCount', np.float32), 2),
        AttributeHeader(False, ('shortLineDensity', np.float32), 3),
        AttributeHeader(False, ('hueMean', np.float32), 17)

    
    
  
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table



def seismic_bumps_dataset():
    file = open('data/seismic-bumps.arff')
    lines = file.readlines()
    lines = lines[155:2738]


    attrib_headers = [
        AttributeHeader(False, ('seismic', '<S16'),  0),
        AttributeHeader(False, ('seismoacoustic', '<S16'), 1),
        AttributeHeader(False, ('genergy', '<S16'), 2),
        AttributeHeader(False, ('gpuls', np.float32), 3),
        AttributeHeader(False, ('gdenergy', np.float32), 4),
        AttributeHeader(False, ('gdpuls', np.float32), 5),
        AttributeHeader(False, ('ghazard', '<S16'), 6),
        AttributeHeader(False, ('class', np.float32), 18)
    
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def somerville_happiness_dataset():
    file = open('data/SomervilleHappinessSurvey2015.csv')
    lines = file.readlines()
    lines = lines[2:144]


    attrib_headers = [
        AttributeHeader(False, ('happyUnhappy', np.float32),  0),
        AttributeHeader(False, ('cityService', np.float32), 1),
        AttributeHeader(False, ('costofHousing', np.float32), 2),
        AttributeHeader(False, ('qualityofPubSchool', np.float32), 3),
        AttributeHeader(False, ('trustofPolice', np.float32), 4),
        AttributeHeader(False, ('maintenanceofRoads', np.float32), 5),
        AttributeHeader(False, ('socialEvents', np.float32), 6)
        
    
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table


def spambase_dataset():
    file = open('data/spambase.data')
    lines = file.readlines()
    lines = lines[1:4601]


    attrib_headers = [
        AttributeHeader(False, ('freqMake', np.float32),  0),
        AttributeHeader(False, ('freqAddress', np.float32), 1),
        AttributeHeader(False, ('freqAll', np.float32), 2),
        AttributeHeader(False, ('freq3D', np.float32), 3),
        AttributeHeader(False, ('freqOur', np.float32), 4),
        AttributeHeader(False, ('freqOver', np.float32), 5),
        AttributeHeader(False, ('freqRemove', np.float32), 6),
        AttributeHeader(False, ('freqInternet', np.float32), 7),
        AttributeHeader(False, ('freqOrder', np.float32), 8)
    
    ]
    
    data_table = _read_dataset(lines, attrib_headers)
    return attrib_headers, data_table