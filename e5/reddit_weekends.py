import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


def main():
	file1 = sys.argv[1]
	counts = pd.DataFrame(pd.read_json(file1, lines=True))
	counts['index'] = counts['date']
	counts = counts.set_index('index')
	counts = counts['2012':'2013']
	counts = counts[counts['subreddit'] == 'canada']
	counts['dayOfWeek'] = counts['date'].dt.dayofweek
	weekdays = counts[counts['dayOfWeek'] < 5].reset_index(drop=True)
	weekends = counts[counts['dayOfWeek'] > 4].reset_index(drop=True)

	norWeekdays = stats.normaltest(weekdays['comment_count']).pvalue
	norWeekends = stats.normaltest(weekends['comment_count']).pvalue
	
	levPvalue = stats.levene(weekdays['comment_count'], weekends['comment_count']).pvalue
	# print(lev_pvalue)
	# 0.04378740989202803

	# Fix1 transforming data might save us.
	# plt.hist(weekdays['comment_count'], alpha=0.5)
	# plt.hist(weekends['comment_count'], alpha=0.5)
	# plt.show()

	# np.log
	# logWeekdays = np.log(weekdays['comment_count'])
	# logWeekends = np.log(weekends['comment_count'])
	# plt.hist(logWeekdays, alpha=0.5)
	# plt.hist(logWeekends, alpha=0.5)
	# plt.show()

	# np.exp
	expWeekdays = np.exp(weekdays['comment_count'])
	expWeekends = np.exp(weekends['comment_count'])
	# plt.hist(expWeekdays, alpha=0.5)
	# plt.hist(expWeekends, alpha=0.5)
	# plt.show()
	print(expWeekdays)
	print(expWeekends)




if __name__ == '__main__':
	main()


