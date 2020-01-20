# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 00:08:05 2018

@author: Александр
"""

import numpy as np 

def interpolateRow(y):
    nans = np.isnan(y)
    if sum(~nans) == 0:
        y = np.nan
    else:
        y[nans] = np.interp(nans.nonzero()[0], (~nans).nonzero()[0], y[~nans])
    return y

def interpolatePN(y, empty_fill_val=0):
    np.apply_along_axis(interpolateRow,0,y)
    return y