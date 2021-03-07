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
from sklearn.linear_model import LinearRegression
<<<<<<< HEAD
=======

>>>>>>> cde5595d369e43cc5ff7d9480de15b421d70595d
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
<<<<<<< HEAD
print(df.head())
'''
=======
#print(df.head())

>>>>>>> cde5595d369e43cc5ff7d9480de15b421d70595d
X= np.array(df.drop(['label'], 1))
y = np.array(df['label'])

X = preprocessing.scale(X)
X = X[:-forecast_out+1]
#df.dropna(inplace=True)
y = np.array(df['label'])
<<<<<<< HEAD
=======
#
# 
from sklearn.model_selection import KFold, cross_validate
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor

#X, y = load_boston(return_X_y=True)
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True)

model = LinearRegression()
scoring=('r2', 'neg_mean_squared_error')
>>>>>>> cde5595d369e43cc5ff7d9480de15b421d70595d

cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring, return_train_score=False)

print(cv_results)
#
'''
X_train, X_test, y_train, y_test = cross_validate.train_test_split(X, y, test_size=0.2)
clf= LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)
<<<<<<< HEAD
'''
=======
''' 
>>>>>>> cde5595d369e43cc5ff7d9480de15b421d70595d
## end of file
