import numpy as np

# get data
data = np.load('D:/Code/Python3/CMPT353/Ass1/e1/monthdata.npz')
totals = data['totals']
counts = data['counts']

# which city had the lowest total precipitation over the year?
# Hints: sum across the rows (axis 1);
# use argmin to determine which row has the lowest value. Print the row number.

# sum across the rows
city_ppt_sum = totals.sum(axis = 1)
# find row of lowest value by argmin
lowest_city = np.argmin(city_ppt_sum, axis = 0)
# Print(lowest_city)

# Determine the average precipitation in these locations for each month

month_ppt_avg = totals.sum(axis = 0) / counts.sum(axis = 0)
# print(month_ppt_avg)

# Do the same for the cities: give the average precipitation (daily precipitation
# averaged over the month) for each city by printing the array.
city_obs_sum = counts.sum(axis = 1)
city_ppt_avg = totals_sum / counts_sum
# print(city_ppt_avg)

# Calculate the total precipitation for each quarter in each city
n = totals.shape[0]
qrter = totals.reshape(4*n, 3)
qrter_sum = qrter.sum(axis = 1)
qrter_ppt = qrter_sum.reshape(n,4)
# print(qrter_ppt)

print ("Row with lowest total precipitation:\n",lowest_city)

print("Average precipitation in each month:\n",month_ppt_avg)

print("Average precipitation in each city:\n",city_ppt_avg)

print("Quarterly precipitation totals:\n",qrter_ppt)