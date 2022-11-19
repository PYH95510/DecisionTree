from typing import List, Union, Tuple, Any
import numpy as np
from data_reader import AttributeHeader

def _entropy_class(class_header: AttributeHeader, class_col: np.ndarray):
    assert(class_header.attribute_names is not None)

    entropy = 0.0
    total_count = class_col.shape[0]
    for class_id in range(0, class_header.attribute_names.shape[0]):
        class_count = np.count_nonzero(class_col[class_col == class_id])
        if class_count <= 0:
            continue
        entropy += -class_count / total_count * np.log2(class_count / total_count)

    return entropy

def _entropy_continuous(
    class_header: AttributeHeader, 
    data_col: np.ndarray, 
    class_col: np.ndarray
    ):
    sort_args = np.argsort(data_col)
    data_sort = data_col[sort_args]
    class_sort = class_col[sort_args]

    total_count = class_sort.shape[0]
    entropy_list = np.zeros(shape=(data_sort.shape[0]-1,), dtype=np.float32)
    for i, bisect_idx in enumerate(range(1, data_sort.shape[0])):
        class_left = class_sort[:bisect_idx]
        class_right = class_sort[bisect_idx:]
        entropy_list[i] = \
            class_left.shape[0] / total_count * _entropy_class(class_header, class_left) + \
            class_right.shape[0] / total_count * _entropy_class(class_header, class_right)
    
    min_entropy_idx = np.argmin(entropy_list)

    return entropy_list[min_entropy_idx], (data_sort[min_entropy_idx+1], data_sort[min_entropy_idx+2])

def _entropy_discrete(
    attrib_header: AttributeHeader, 
    class_header: AttributeHeader, 
    data_col: np.ndarray, 
    class_col: np.ndarray
    ):
    assert(attrib_header.attribute_names is not None and class_header.attribute_names is not None)

    entropy = 0.0
    total_count = data_col.shape[0]
    for attrib_id in range(0, attrib_header.attribute_names.shape[0]):
        attrib_count = np.count_nonzero(data_col == attrib_id)
        classes = class_col[data_col == attrib_id]

        attrib_entropy = 0.0
        for class_id in range(0, class_header.attribute_names.shape[0]):
            class_count = np.count_nonzero(classes == class_id)
            if class_count <= 0:
                continue
            
            attrib_entropy += -class_count / attrib_count * np.log2(class_count / attrib_count)

        entropy += attrib_count / total_count * attrib_entropy

    return entropy

def entropy(attrib_headers: List[AttributeHeader], data_table: np.ndarray) -> Tuple[int, Union[None, Tuple[Any, Any]]]:
    entropy_list = np.zeros(shape=(len(attrib_headers)-1,), dtype=np.float32)
    partition_val_list: List[Union[None, Tuple[Any, Any]]] = [None] * (len(attrib_headers) - 1)
    class_header = attrib_headers[-1]

    for i, attrib_header in enumerate(attrib_headers[:-1]):
        if attrib_header.is_continuous:
            entropy_list[i], partition_val_list[i] = _entropy_continuous(
                class_header, 
                data_table[attrib_header.read_dtype[0]],
                data_table[class_header.read_dtype[0]])
        else:
            entropy_list[i] = _entropy_discrete(
                attrib_header, 
                class_header, 
                data_table[attrib_header.read_dtype[0]],
                data_table[class_header.read_dtype[0]])

    class_entropy = _entropy_class(class_header, data_table[class_header.read_dtype[0]])
    gain_list = class_entropy - entropy_list
    max_gain_idx = np.argmax(gain_list)

    return int(max_gain_idx), partition_val_list[max_gain_idx]

def _test_entropy_discrete():
    attribs = np.concatenate([np.full(shape=(600,), fill_value=0, dtype=np.int32), np.full(shape=(400,), fill_value=1, dtype=np.int32)])
    classes = np.concatenate(
        [
            np.where(np.random.uniform(0, 1, size=(600,)) < 0.99, 0, 1),
            np.where(np.random.uniform(0, 1, size=(400,)) < 0.99, 1, 0)
        ])
    attrib_headers = [
        AttributeHeader(False, ('attrib0', np.int32), 0),
        AttributeHeader(False, ('class', np.int32), 0)
    ]
    attrib_headers[0].attribute_names = np.array(['zero', 'one'], dtype='<S8')
    attrib_headers[1].attribute_names = np.array(['class0', 'class1'], dtype='<S8')

    print(_entropy_class(attrib_headers[1], classes))
    print(_entropy_discrete(attrib_headers[0], attrib_headers[1], attribs, classes))

def _test_entropy_continuous():
    attribs = np.arange(0, 1000, dtype=np.int32)
    classes = np.concatenate(
        [
            np.where(np.random.uniform(0, 1, size=(200,)) < 0.99, 0, 1),
            np.where(np.random.uniform(0, 1, size=(800,)) < 0.99, 1, 0)
        ]) 
    attrib_headers = [
        AttributeHeader(False, ('attrib0', np.int32), 0),
        AttributeHeader(False, ('class', np.int32), 0)
    ]
    attrib_headers[0].attribute_names = None
    attrib_headers[1].attribute_names = np.array(['class0', 'class1'], dtype='<S8')

    print(_entropy_class(attrib_headers[1], classes))
    print(_entropy_continuous(attrib_headers[1], attribs, classes))
