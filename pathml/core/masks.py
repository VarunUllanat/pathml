"""
Copyright 2021, Dana-Farber Cancer Institute and Weill Cornell Medicine
License: GNU GPL 2.0
"""

import os
import reprlib
from collections import OrderedDict
from pathlib import Path

import h5py
import numpy as np
import pathml.core.h5managers


class Masks:
    """
    Object wrapping a dict of masks.

    Args:
        h5manager(pathml.core.h5pathManager)
        masks(dict): dictionary of np.ndarray objects representing ex. labels, segmentations.
    """

    def __init__(self, h5manager, masks=None):
        assert isinstance(
            h5manager, pathml.core.h5managers.h5pathManager
        ), f"expecting type pathml.core.h5pathManager but passed type {type(h5manager)}"
        self.h5manager = h5manager
        # if masks are supplied, add them to the h5manager
        if masks:
            if not isinstance(masks, dict):
                raise ValueError(
                    f"masks must be passed as dicts of the form key1:mask1,key2:mask2,..."
                )
            for val in masks.values():
                if not isinstance(val, np.ndarray):
                    raise ValueError(
                        f"can not add {type(val)}, mask must be of type np.ndarray"
                    )
            for key in masks.keys():
                if not isinstance(key, str):
                    raise ValueError(
                        f"can not add {type(key)}, key must be of type str"
                    )
            self._masks = OrderedDict(masks)
        else:
            self._masks = OrderedDict()
        for mask in self._masks:
            self.h5manager.add_mask(mask, self._masks[mask])
        del self._masks

    def __repr__(self):
        rep = f"{len(self.h5manager.h5['masks'])} masks: {reprlib.repr(list(self.h5manager.h5['masks'].keys()))}"
        return rep

    def __getitem__(self, tile, item):
        return self.h5manager.get_mask(tile, item)

    def __setitem__(self, tile, key, mask):
        self.h5manager.update_mask(tile, key, mask)

    @property
    def keys(self):
        return list(self.h5manager.h5["masks"].keys())

    def add(self, key, mask):
        """
        Add mask indexed by key to self.h5manager.

        Args:
            key (str): key
            mask (np.ndarray): array of mask. Must contain elements of type int8
        """
        self.h5manager.add_mask(key, mask)

    def remove(self, key):
        """
        Remove mask.

        Args:
            key(str): key indicating mask to be removed
        """
        self.h5manager.remove_mask(key)
