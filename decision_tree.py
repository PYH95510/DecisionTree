from typing import List, Any
import numpy as np
from data_reader import AttributeHeader
import attribute_selection
import data_reader


class TreeNode:
    _split_attrib_idx: int
    _threshold: float
    _children: List[Any]
    _class_id: int

    def __init__(self):
        self._split_attrib_idx = -1
        self._threshold = 0.0
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
        attrib_idx, split_neighbors = attribute_selection.entropy(attrib_headers, data_table)
        self._split_attrib_idx = attrib_headers[attrib_idx].data_col_index           

        attrib_headers_cpy = attrib_headers.copy()
        del attrib_headers_cpy[attrib_idx]
        
        split_attrib_col = data_table[attrib_headers[attrib_idx].read_dtype[0]]

        if attrib_headers[attrib_idx].is_continuous:
            assert(split_neighbors is not None)
            self._threshold = (split_neighbors[0] + split_neighbors[1]) / 2
            self._children = [TreeNode() for _ in range(0, 2)]

            self._build_child(
                attrib_headers_cpy, 
                data_table,
                leaf_nodes, 
                self._children[0], 
                split_attrib_col < self._threshold)
            self._build_child(
                attrib_headers_cpy, 
                data_table,
                leaf_nodes, 
                self._children[1], 
                split_attrib_col >= self._threshold)
        else:
            assert(attrib_headers[attrib_idx].attribute_names is not None)
            num_attribs = attrib_headers[attrib_idx].attribute_names.shape[0] # type: ignore
            self._children = [TreeNode() for _ in range(0, num_attribs)]

            for i in range(0, num_attribs):
                self._build_child(
                    attrib_headers_cpy, 
                    data_table,
                    leaf_nodes, 
                    self._children[i], 
                    split_attrib_col == i)

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
                    data_table[split_attrib_col < self._threshold], 
                    pred_classes,
                    indices[split_attrib_col < self._threshold])
                self._children[1].forward(
                    attrib_headers, 
                    data_table[split_attrib_col >= self._threshold], 
                    pred_classes,
                    indices[split_attrib_col >= self._threshold])
            else:
                assert(attrib_headers[self._split_attrib_idx].attribute_names is not None)
                num_attribs = attrib_headers[self._split_attrib_idx].attribute_names.shape[0] # type: ignore
                for i in range(0, num_attribs):
                    self._children[i].forward(
                        attrib_headers, 
                        data_table[split_attrib_col == i], 
                        pred_classes,
                        indices[split_attrib_col == i])
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
