import sys
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import stats

counts = pd.DataFrame(pd.read_json('reddit-counts.json.gz', lines=True))
counts['index'] = counts['date']
counts = counts.set_index('index')
counts = counts['2012':'2013']
counts = counts[counts['subreddit'] == 'canada']
counts['dayOfWeek'] = counts['date'].dt.dayofweek
Weekdays = counts[counts['dayOfWeek'] < 5].reset_index(drop=True)
Weekends = counts[counts['dayOfWeek'] > 4].reset_index(drop=True)