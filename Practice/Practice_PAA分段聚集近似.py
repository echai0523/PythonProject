# -*- coding: UTF-8 -*-

# from pyts.approximation import PiecewiseAggregateApproximation
# X = [[0, 4, 2, 1, 7, 6, 3, 5],
#      [2, 5, 4, 5, 3, 4, 2, 3]]
# transformer = PiecewiseAggregateApproximation(window_size=2)
# transformer.transform(X)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyts.approximation import PiecewiseAggregateApproximation

# Parameters
# n_samples, n_timestamps = 100, 48
# Toy dataset
# rng = np.random.RandomState(41)
# X = rng.randn(n_samples, n_timestamps)

rng = pd.read_csv('PAAtest.csv', encoding="utf-8")
# DateFrame转numpy的两种方式：
# X = np.array(rng)
X = rng.to_numpy()
# print(X, X.shape)

n_samples, n_timestamps = X.shape
# PAA transformation
window_size = 6
paa = PiecewiseAggregateApproximation(window_size=window_size)
X_paa = paa.transform(X)

# Show the results for the first time series
plt.figure(figsize=(6, 4))
plt.plot(X[0], 'o--', ms=4, label='Original')
plt.plot(np.arange(window_size // 2,
                   n_timestamps + window_size // 2,
                   window_size), X_paa[0], 'o--', ms=4, label='PAA')
plt.vlines(np.arange(0, n_timestamps, window_size) - 0.5,
           X[0].min(), X[0].max(), color='g', linestyles='--', linewidth=0.5)
plt.legend(loc='best', fontsize=10)
plt.xlabel('Time', fontsize=12)
plt.title('Piecewise Aggregate Approximation', fontsize=16)
plt.show()
