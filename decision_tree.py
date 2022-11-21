from typing import List, Any, Union, Tuple
import pickle
import numpy as np
import sklearn.metrics
from data_reader import AttributeHeader
import attribute_selection
import data_reader


class TreeNode:
    _split_attrib_idx: int
    _split_criteria: Union[float, Tuple[np.ndarray, np.ndarray]]
    _children: List[Any]
    _class_id: int

    def __init__(self):
        self._split_attrib_idx = -1
        self._split_criteria = 0.0
        self._children = []
        self._class_id = -1

    def build_recursive(
        self, 
        attrib_headers: List[AttributeHeader], 
        data_table: np.ndarray, 
        leaf_nodes: List[Any]
    ):
        class_col = data_table[attrib_headers[-1].read_dtype[0]]
        if np.all(class_col[:] == class_col[0]) or \
            len(attrib_headers) <= 1 \
            :
            # Find the most frequent class in the set
            self._class_id = int(np.argmax(np.bincount(class_col)))
            leaf_nodes.append(self)
            return
        del class_col
        print(data_table.shape)

        # attrib_idx, split_result = attribute_selection.entropy(attrib_headers, data_table)
        attrib_idx, split_result = attribute_selection.gini_index(attrib_headers, data_table)

        self._split_attrib_idx = attrib_headers[attrib_idx].data_col_index           

        attrib_headers_cpy = attrib_headers.copy()
        del attrib_headers_cpy[attrib_idx]
        
        split_attrib_col = data_table[attrib_headers[attrib_idx].read_dtype[0]]

        if attrib_headers[attrib_idx].is_continuous:
            assert(split_result is not None)

            self._split_criteria = (split_result[0] + split_result[1]) / 2
            self._children = [TreeNode() for _ in range(0, 2)]

            self._build_child(
                attrib_headers_cpy, 
                data_table,
                leaf_nodes, 
                self._children[0], 
                split_attrib_col < self._split_criteria)
            self._build_child(
                attrib_headers_cpy, 
                data_table,
                leaf_nodes, 
                self._children[1], 
                split_attrib_col >= self._split_criteria)
        else:
            assert(attrib_headers[attrib_idx].attribute_names is not None)
            assert(split_result is not None)

            self._children = [TreeNode() for _ in range(0, 2)]
            self._split_criteria = split_result
            self._build_child(
                attrib_headers_cpy, 
                data_table, 
                leaf_nodes, 
                self._children[0], 
                np.isin(split_attrib_col, self._split_criteria[0]))
            self._build_child(
                attrib_headers_cpy, 
                data_table, 
                leaf_nodes, 
                self._children[1], 
                np.isin(split_attrib_col, self._split_criteria[1]))

    def _build_child(
        self, 
        attrib_headers: List[AttributeHeader], 
        data_table: np.ndarray, 
        leaf_nodes: List[Any],
        child,
        mask: np.ndarray
    ):
        if np.count_nonzero(mask) == 0:
            class_col = data_table[attrib_headers[-1].read_dtype[0]]
            # Find the most frequent class in the set
            child._class_id = np.argmax(np.bincount(class_col))
            leaf_nodes.append(child)
        else:
            child.build_recursive(
                attrib_headers, 
                data_table[mask], 
                leaf_nodes)

    def forward(self, attrib_headers: List[AttributeHeader], data_table: np.ndarray, pred_classes: np.ndarray, indices: np.ndarray):
        if data_table.shape[0] == 0:
            return
        
        if len(self._children) > 0:
            split_attrib_col = data_table[attrib_headers[self._split_attrib_idx].read_dtype[0]]
            if attrib_headers[self._split_attrib_idx].is_continuous:
                self._children[0].forward(
                    attrib_headers, 
                    data_table[split_attrib_col < self._split_criteria], 
                    pred_classes,
                    indices[split_attrib_col < self._split_criteria])
                self._children[1].forward(
                    attrib_headers, 
                    data_table[split_attrib_col >= self._split_criteria], 
                    pred_classes,
                    indices[split_attrib_col >= self._split_criteria])
            else:
                assert(attrib_headers[self._split_attrib_idx].attribute_names is not None)
                assert(type(self._split_criteria) is tuple)

                self._children[0].forward(
                    attrib_headers,
                    data_table[np.isin(split_attrib_col, self._split_criteria[0])],
                    pred_classes,
                    indices[np.isin(split_attrib_col, self._split_criteria[0])]
                )
                self._children[1].forward(
                    attrib_headers,
                    data_table[np.isin(split_attrib_col, self._split_criteria[1])],
                    pred_classes,
                    indices[np.isin(split_attrib_col, self._split_criteria[1])]
                )
        else:
            pred_classes[indices] = self._class_id


def build_tree(attrib_headers: List[AttributeHeader], data_table: np.ndarray):
    train_size = int(data_table.shape[0] * 0.7)
    train_data = data_table[:train_size]
    valid_data = data_table[train_size:]
    print(f"Train data size: {train_data.shape[0]}, Validation data size: {valid_data.shape[0]}")

    root = TreeNode()
    leaf_nodes = []
    root.build_recursive(attrib_headers, train_data, leaf_nodes)

    pred_classes = np.full(shape=(valid_data.shape[0],), fill_value=-1, dtype=np.int32)
    root.forward(attrib_headers, valid_data, pred_classes, np.arange(0, valid_data.shape[0]))
    
    print(np.count_nonzero(pred_classes == valid_data[attrib_headers[-1].read_dtype[0]]))
    print(pred_classes)

    return root

def save_tree(root_node: TreeNode, file_name: str):
    pickle.dump(root_node, open(file_name, 'wb'))

def load_tree(file_name: str):
    return pickle.load(open(file_name, 'rb'))

def accuracy(gt_y, pred_y):
    return np.count_nonzero(gt_y == pred_y) / gt_y.shape[0]

def precision(gt_y, pred_y, class_id):
    numerator = np.count_nonzero(gt_y == pred_y)
    denominator = numerator

    mask = pred_y == class_id
    # False positives
    denominator += np.count_nonzero(pred_y[mask] != gt_y[mask])

    return numerator / denominator

def recall(gt_y, pred_y, class_id):
    numerator = np.count_nonzero(gt_y == pred_y)
    denominator = numerator

    mask = gt_y == class_id
    denominator += np.count_nonzero(pred_y[mask] != gt_y[mask])

    return numerator / denominator

def predict(model_file_name, attrib_headers: List[AttributeHeader], data_table: np.ndarray):
    root_node = load_tree(model_file_name)
    train_size = int(data_table.shape[0] * 0.7)
    train_data = data_table[:train_size]
    valid_data = data_table[train_size:]

    assert(attrib_headers[-1].attribute_names is not None)
    num_classes = attrib_headers[-1].attribute_names.shape[0]

    train_gt = train_data[attrib_headers[-1].read_dtype[0]]
    valid_gt = valid_data[attrib_headers[-1].read_dtype[0]]

    train_pred = np.full(shape=(train_data.shape[0],), fill_value=-1, dtype=np.int32)
    valid_pred = np.full(shape=(valid_data.shape[0],), fill_value=-1, dtype=np.int32)

    root_node.forward(attrib_headers, train_data, train_pred, np.arange(0, train_data.shape[0]))
    root_node.forward(attrib_headers, valid_data, valid_pred, np.arange(0, valid_data.shape[0]))

    print(attrib_headers[-1].attribute_names)
    print(sklearn.metrics.confusion_matrix(valid_gt, valid_pred))

if __name__ == '__main__':
    # attribute_selection.use_gain_ratio = True
    # root_node = build_tree(*data_reader.read_balance_scale_dataset())
    # save_tree(root_node, 'models/gini/balance-scale.pickle')

    predict('models/gini/adult.pickle', *data_reader.read_adult_dataset())
