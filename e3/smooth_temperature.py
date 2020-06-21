import sys
from datetime import timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

filename = sys.argv[1]

cpu_data = pd.read_csv(filename, sep=',', parse_dates=['timestamp'])

# Loess Smoothing

cpu_data['tmp'] = cpu_data['timestamp'].apply(pd.to_datetime)
timestamp = cpu_data['tmp'].apply(np.datetime64)
temperature = cpu_data['temperature']

loess_smoothed = lowess(temperature, timestamp, frac=0.01)
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)

# Kalman Smoothing
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.8, 0.7, 0.5, 0.1]) ** 2
transition_covariance = np.diag([0.1, 0.1, 0.1, 0.1]) ** 2
transition = [[0.97, 0.5, 0.2, -0.001], [0.1, 0.4, 2.2, 0], [0, 0, 0.95, 0], [0, 0, 0, 1]]

kf = KalmanFilter(initial_state_mean=initial_state,
                  initial_state_covariance=observation_covariance,
                  observation_covariance=observation_covariance,
                  transition_covariance=transition_covariance,
                  transition_matrices=transition)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Loess Smoothed', 'CPU temperature', 'Kalman Smoothed'])
plt.title('CPU temperature')
plt.xlabel('Time')
plt.ylabel('Temperature')
# plt.show()
plt.savefig('cpu.svg')