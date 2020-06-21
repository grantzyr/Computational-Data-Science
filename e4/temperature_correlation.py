import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stations = sys.argv[1]
city = sys.argv[2]
output = sys.argv[3]

# read data from station.json.gz
stations_data = pd.DataFrame(pd.read_json(stations, lines=True))

# change avg_tmax to avg_tmax/10
stations_data['avg_tmax'] = stations_data['avg_tmax'] / 10

# read data from city_data.csv
city_data = pd.DataFrame(pd.read_csv(city))

# drop rows with NaN
city_data = city_data.dropna(axis=0, how='any').reset_index(drop=True)
# calculate new area value
city_data['area'] = city_data['area'] / 1000000
# drop rows with area over 10000 km^2
city_data = city_data[city_data['area'] <= 10000].reset_index(drop=True)
# add population density to city data
city_data['density'] = city_data['population'] / city_data['area']


def distance(city, stations):
    # radius in km
    R = 6371
    cityLat = city['latitude']
    cityLon = city['longitude']
    stationLat = stations['latitude']
    stationLon = stations['longitude']
    a = np.square(np.sin((np.deg2rad(stationLat - cityLat)) / 2))
    b = np.cos(np.deg2rad(cityLat)) * np.cos(np.deg2rad(stationLat))
    c = np.square(np.sin((np.deg2rad(stationLon - cityLon)) / 2))
    result = 2 * R * np.arcsin(np.sqrt(a + b * c))
    return result

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    # print(stations)
    loc_tmax = stations['distance'].idxmin(axis=1)
    # print(loc_tmax)
    return stations.loc[loc_tmax, 'avg_tmax']


# final dataframe
city_data['avg_tmax'] = city_data.apply(best_tmax, axis=1, stations=stations_data)

plt.scatter(city_data['avg_tmax'], city_data['density'])
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.savefig(output)
