import sys
import pandas as pd
import matplotlib.pyplot as plt

print(sys.argv)

filename1 = sys.argv[1]
filename2 = sys.argv[2]

# read the data
data1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
                    names=['lang', 'page', 'views', 'bytes'])
data2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
                    names=['lang', 'page', 'views', 'bytes'])

data1_sorted = data1.sort_values(by='views', ascending=False)

data1['views2'] = data2['views']

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(data1_sorted['views'].values)
plt.title('distribution of views')
plt.xlabel('rank')
plt.ylabel('views')

plt.subplot(1, 2, 2)
plt.plot(data1['views'], data1['views2'], 'b.')
plt.title('daily views')
plt.xlabel('day 1')
plt.ylabel('day 2')
plt.xscale('log')
plt.yscale('log')

plt.savefig('wikipedia.png')


