import pandas as pd

# get data
totals = pd.read_csv('D:/Code/Python3/CMPT353/Ass1/e1/totals.csv').set_index(keys=['name'])
counts = pd.read_csv('D:/Code/Python3/CMPT353/Ass1/e1/counts.csv').set_index(keys=['name'])

# Which city had the lowest total precipitation over the year?
lowest_city = totals.sum(1).idxmin(1)
# print(lowest_city)

# Determine the average precipitation in these locations for each month.
month_ppt_avg = totals.sum(axis = 0) / counts.sum(axis = 0)
# print(month_ppt_avg)

# give the average precipitation (daily precipitation averaged over the month) for each city by printing the array.
city_ppt_avg = totals.sum(axis = 1) / counts.sum(axis = 1)
# print(city_ppt_avg)

print("City with lowest total precipitation:\n", lowest_city)
print("Average precipitation in each month:\n", month_ppt_avg)
print("Average precipitation in each city:\n", city_ppt_avg)










