#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			mapviz.py
#
#	visualize data in map
#
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import pandas as pandas
import quandl
import math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================
df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)
#print(df.head())

x= np.array(df.drop(['labe1'], 1))
y = np.array(df['labe1'])

x = preprocessing.scale(x)
x = x[:-forecast_out+1]
df.dropna(inplace=True)

y = np.array(df['label1'])
print(len(x), len(y))

''' '''
## end of file
