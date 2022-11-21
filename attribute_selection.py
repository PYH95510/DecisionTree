from typing import List, Union, Tuple, Any
import numpy as np
from data_reader import AttributeHeader
import util

use_gain_ratio = False

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

    return entropy_list[min_entropy_idx], (data_sort[min_entropy_idx], data_sort[min_entropy_idx+1])

def _entropy_discrete(
    attrib_header: AttributeHeader, 
    class_header: AttributeHeader, 
    data_col: np.ndarray, 
    class_col: np.ndarray
):
    assert(attrib_header.attribute_names is not None and class_header.attribute_names is not None)

    attrib_ids = np.arange(0, attrib_header.attribute_names.shape[0])
    min_entropy  = np.Inf
    cur_partition = None
    total_count = class_col.shape[0]

    for i, (part_left, part_right) in enumerate(util.gen_bipartition(attrib_ids)):
        class_left = class_col[np.isin(data_col, part_left)]
        class_right = class_col[np.isin(data_col, part_right)]
        cur_entropy = 0
        if class_left.shape[0] > 0:
            cur_entropy += class_left.shape[0] / total_count * _entropy_class(class_header, class_left)
        if class_right.shape[0] > 0:
            cur_entropy += class_right.shape[0] / total_count * _entropy_class(class_header, class_right)
        if cur_entropy < min_entropy:
            min_entropy = cur_entropy
            cur_partition = (part_left, part_right)

    return min_entropy, cur_partition

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
            entropy_list[i], partition_val_list[i] = _entropy_discrete(
                attrib_header, 
                class_header, 
                data_table[attrib_header.read_dtype[0]],
                data_table[class_header.read_dtype[0]])

    class_entropy = _entropy_class(class_header, data_table[class_header.read_dtype[0]])
    gain_list = class_entropy - entropy_list

    if use_gain_ratio:
        for i, attrib_header in enumerate(attrib_headers[:-1]):
            if not attrib_header.is_continuous:
                assert(attrib_header.attribute_names is not None)
                data_col = data_table[attrib_header.read_dtype[0]]
                total_count = data_col.shape[0]
                split_info = 0.0
                for j in range(0, attrib_header.attribute_names.shape[0]):
                    attrib_count = np.count_nonzero(data_col == j)
                    if attrib_count > 0:
                        split_info += -attrib_count / total_count * np.log2(attrib_count / total_count)
                    if split_info > 0:
                        gain_list[i] /= split_info

    max_gain_idx = np.argmax(gain_list)

    return int(max_gain_idx), partition_val_list[max_gain_idx]

def _test_entropy_discrete():
    attribs = np.concatenate(
        [
            np.full(shape=(200,), fill_value=0, dtype=np.int32), 
            np.full(shape=(400,), fill_value=1, dtype=np.int32),
            np.full(shape=(400,), fill_value=2, dtype=np.int32)
        ])
    classes = np.concatenate(
        [
            np.where(np.random.uniform(0, 1, size=(200,)) < 0.99, 0, 1),
            np.where(np.random.uniform(0, 1, size=(400,)) < 0.99, 1, 0),
            np.where(np.random.uniform(0, 1, size=(400,)) < 0.99, 0, 1)
        ])
    attrib_headers = [
        AttributeHeader(False, ('attrib0', np.int32), 0),
        AttributeHeader(False, ('class', np.int32), 0)
    ]
    attrib_headers[0].attribute_names = np.array(['zero', 'one', 'two'], dtype='<S8')
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


def _gini_class(class_header: AttributeHeader, class_col: np.ndarray):
    assert(class_header.attribute_names is not None)

    gini_index = 0.0
    total_count = class_col.shape[0]
    for class_id in range(0, class_header.attribute_names.shape[0]):
        class_count = np.count_nonzero(class_col[class_col == class_id])
        gini_index += np.power(class_count / total_count, 2)
        
    gini_index = 1 - gini_index
    return gini_index

def _gini_discrete(    
    attrib_header: AttributeHeader, 
    class_header: AttributeHeader, 
    data_col: np.ndarray, 
    class_col: np.ndarray
):
    assert(attrib_header.attribute_names is not None and class_header.attribute_names is not None)

    attrib_ids = np.arange(0, attrib_header.attribute_names.shape[0])
    min_gini_index  = np.Inf
    cur_partition = None
    total_count = class_col.shape[0]

    for i, (part_left, part_right) in enumerate(util.gen_bipartition(attrib_ids)):
        class_left = class_col[np.isin(data_col, part_left)]
        class_right = class_col[np.isin(data_col, part_right)]
        cur_gini_index = 0.0
        if class_left.shape[0] > 0:
            cur_gini_index += class_left.shape[0] / total_count * _gini_class(class_header, class_left)
        if class_right.shape[0] > 0:
            cur_gini_index += class_right.shape[0] / total_count * _gini_class(class_header, class_right)

        if cur_gini_index < min_gini_index:
            min_gini_index = cur_gini_index
            cur_partition = (part_left, part_right)

    return min_gini_index, cur_partition

def _gini_continuous(
    class_header: AttributeHeader, 
    data_col: np.ndarray, 
    class_col: np.ndarray
    ):
    sort_args = np.argsort(data_col)
    data_sort = data_col[sort_args]
    class_sort = class_col[sort_args]

    total_count = class_sort.shape[0]
    gini_index_list = np.zeros(shape=(data_sort.shape[0]-1,), dtype=np.float32)
    for i, bisect_idx in enumerate(range(1, data_sort.shape[0])):
        class_left = class_sort[:bisect_idx]
        class_right = class_sort[bisect_idx:]
        gini_index_list[i] = \
            class_left.shape[0] / total_count * _gini_class(class_header, class_left) + \
            class_right.shape[0] / total_count * _gini_class(class_header, class_right)
    
    min_gini_idx = np.argmin(gini_index_list)

    return gini_index_list[min_gini_idx], (data_sort[min_gini_idx], data_sort[min_gini_idx+1])

def gini_index(attrib_headers: List[AttributeHeader], data_table: np.ndarray) -> Tuple[int, Union[None, Tuple[Any, Any]]]:
    gini_list = np.zeros(shape=(len(attrib_headers)-1,), dtype=np.float32)
    partition_val_list: List[Union[None, Tuple[Any, Any]]] = [None] * (len(attrib_headers) - 1)
    class_header = attrib_headers[-1]

    for i, attrib_header in enumerate(attrib_headers[:-1]):
        if attrib_header.is_continuous:
            gini_list[i], partition_val_list[i] = _gini_continuous(
                class_header, 
                data_table[attrib_header.read_dtype[0]],
                data_table[class_header.read_dtype[0]])
        else:
            gini_list[i], partition_val_list[i] = _gini_discrete(
                attrib_header, 
                class_header, 
                data_table[attrib_header.read_dtype[0]],
                data_table[class_header.read_dtype[0]])

    gini_class = _gini_class(class_header, data_table[class_header.read_dtype[0]])
    gain_list = gini_class - gini_list

    max_gain_idx = np.argmax(gain_list)

    return int(max_gain_idx), partition_val_list[max_gain_idx]
