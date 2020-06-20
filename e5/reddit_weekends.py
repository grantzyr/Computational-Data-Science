import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from datetime import date

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
	
	ttestPvalue = stats.ttest_ind(weekdays['comment_count'], weekends['comment_count']).pvalue
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
	# logNorWeekdays = stats.normaltest(logWeekdays).pvalue
	# logNorWeekends = stats.normaltest(logWeekends).pvalue 
	# logLevPvalue = stats.levene(logWeekdays, logWeekends).pvalue
	# print(logNorWeekdays)
	# print(logNorWeekends)
	# print(logLevPvalue)

	# np.exp
	# expWeekdays = np.exp(weekdays['comment_count'])
	# expWeekends = np.exp(weekends['comment_count'])
	# plt.hist(expWeekdays, alpha=0.5)
	# plt.hist(expWeekends, alpha=0.5)
	# plt.show()
	# print(expWeekdays)
	# print(expWeekends)
	# expNorWeekdays = stats.normaltest(expWeekdays).pvalue
	# expNorWeekends = stats.normaltest(expWeekends).pvalue
	# expLevPvalue = stats.levene(expWeekdays, expWeekends).pvalue
	# print(expNorWeekdays)
	# print(expNorWeekends)
	# print(expLevPvalue)

	# np.sqrt
	sqrtWeekdays = np.sqrt(weekdays['comment_count'])
	sqrtWeekends = np.sqrt(weekends['comment_count'])
	# plt.hist(sqrtWeekdays, alpha=0.5)
	# plt.hist(sqrtWeekends, alpha=0.5)
	# plt.show()
	sqrtNorWeekdays = stats.normaltest(sqrtWeekdays).pvalue 
	sqrtNorWeekends = stats.normaltest(sqrtWeekends).pvalue  
	sqrtLevPvalue = stats.levene(sqrtWeekdays, sqrtWeekends).pvalue 


	# counts**2
	# e2Weekdays = (weekdays['comment_count']) ** 2
	# e2Weekends = (weekends['comment_count']) ** 2
	# plt.hist(e2Weekdays, alpha=0.5)
	# plt.hist(e2Weekends, alpha=0.5)
	# plt.show()
	# e2NorWeekdays = stats.normaltest(e2Weekdays).pvalue 
	# e2NorWeekends = stats.normaltest(e2Weekends).pvalue 
	# e2LevPvalue = stats.levene(e2Weekdays, e2Weekends).pvalue 
	# print(e2NorWeekdays)
	# print(e2NorWeekends)
	# print(e2LevPvalue)

	# np.sqrt is the best

	# fix2: the central limit theorem might save us.
	weekOfYearWeekdays = weekdays['date'].apply(date.isocalendar).apply(pd.Series)
	weekOfYearWeekends = weekends['date'].apply(date.isocalendar).apply(pd.Series)
	weekdays = weekdays.join(weekOfYearWeekdays).rename(columns = {0:'year', 1:'week', 2:'day'})
	weekends = weekends.join(weekOfYearWeekends).rename(columns = {0:'year', 1:'week', 2:'day'})
	weekdaysMean = weekdays.groupby(['year', 'week'])['comment_count'].mean().reset_index() 
	weekendsMean = weekends.groupby(['year', 'week'])['comment_count'].mean().reset_index()


	norWeekdaysMean = stats.normaltest(weekdaysMean['comment_count']).pvalue 
	norWeekendsMean = stats.normaltest(weekendsMean['comment_count']).pvalue
	levMean = stats.levene(weekdaysMean['comment_count'],weekendsMean['comment_count']).pvalue
	ttestMean = stats.ttest_ind(weekdaysMean['comment_count'],weekendsMean['comment_count']).pvalue



	# fix3: a non-parametric test might save us
	utestPvalue = stats.mannwhitneyu(weekdays['comment_count'],weekends['comment_count']).pvalue
	

	print(OUTPUT_TEMPLATE.format(
	        initial_ttest_p=ttestPvalue,
	        initial_weekday_normality_p=norWeekdays,
	        initial_weekend_normality_p=norWeekends,
	        initial_levene_p=levPvalue,
	        transformed_weekday_normality_p=sqrtNorWeekdays,
	        transformed_weekend_normality_p=sqrtNorWeekends,
	        transformed_levene_p=sqrtLevPvalue,
	        weekly_weekday_normality_p=norWeekdaysMean,
	        weekly_weekend_normality_p=norWeekendsMean,
	        weekly_levene_p=levMean,
	        weekly_ttest_p=ttestMean,
	        utest_p=utestPvalue,
	    ))
if __name__ == '__main__':
	main()


