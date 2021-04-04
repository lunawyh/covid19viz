import pandas as pd
import numpy as np
from sklearn import linear_model

df = pd.read_csv("machine_learning_tutorial_03.csv")
print('1:', df)

import math
median_bedrooms = math.floor(df.bedrooms.median())
print('2:', median_bedrooms)

#clean your modul
df.bedrooms = df.bedrooms.fillna(median_bedrooms)
print('3:', df)

reg = linear_model.LinearRegression()
print('4:', reg)
#train your modul
reg.fit(df[['area', 'bedrooms', 'age']],df.price)
print('4:', reg)

print(reg.coef_)

print('5:', reg.intercept_)

reg.predict([[3000, 3, 40]])
print('6:', reg)

reg.predict([[2500, 4, 5]])
print('6:', reg)
