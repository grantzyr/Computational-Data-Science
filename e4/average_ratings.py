import numpy as np 
import pandas as pd 
import sys
import difflib

movie_list = sys.argv[1]
movie_ratings = sys.argv[2]
output = sys.argv[3]


# read file movie_list
data_movies = open(movie_list).readlines()
movies = pd.DataFrame(data_movies, columns=['title'])
movies = movies['title'].str.replace('\n', '')
movies = pd.DataFrame(movies, columns=['title'])

# read file movie_ratings
ratings = pd.read_csv(movie_ratings)

# def function to match title shows in both files
def match_title(data):
	match = difflib.get_close_matches(data, movies['title'])
	if len(match) !=0:
		return match[0]
	else:
		return None
match = np.vectorize(match_title)

ratings['title'] = ratings['title'].apply(match)

ratings = ratings.dropna()

ratings = ratings.groupby('title').mean().round(2)

# send data to csv
ratings.to_csv(output)


