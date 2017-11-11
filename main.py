from selenium import webdriver
from movie import *
from random import randint
import os.path
import plotly.plotly as py
import plotly.graph_objs as go

verbose = False
nummovies = 5

browser = webdriver.PhantomJS()
movies = []


def truncate(string, length):
	if len(string) == length:
		return string
	elif len(string) < length:
		diff = length - len(string)
		for i in range(0, diff):
			string += ' '
		return string
	else:
		return string[:length-3] + "..."

for i in range(2017, 2006, -1):
	print("Selecting {0} random movies from {1}...".format(nummovies, i))
	f = open("res/{0}.txt".format(i))
	lines = f.readlines()
	f.close()
	selected = [None]
	while len(movies) - (2017 - i) * nummovies < nummovies:
		title = None
		m = None
		
		while m is None:
			while title in selected:
				title = lines[randint(0, len(lines) - 1)][:-1]
			m = movie_by_name(browser, title + " (" + str(i) + ")")
			print("\tChecking \"" + title + "\"...", end="")
		
		n = m.get_num_ratings(browser, verbose)
		if verbose:
			print("\n\t{0} ratings\n\t".format(n), end="")
		print("Done!")
		if n >= 5000:
			movies.append(m)
			selected.append(m.title)
			print("\tSelected \"{0}\"".format(title))
	print("Done!")

fnum = 0
while os.path.exists("log{:03}.csv".format(fnum)):
	fnum += 1

f = open("log{:03}.csv".format(fnum), "w")

titles = []
imdb_ids = []
ratings = []
ten_stars = []
one_stars = []
differences = []

print("Title,IMDb ID,Rating,10 Star,1 Star,Difference", file=f)
for m in movies:
	title = m.get_title(browser, verbose).replace(',', '-')
	titles.append(title)
	imdb_id = m.imdb_id
	imdb_ids.append(imdb_id)
	rating = m.get_rating(browser, verbose)
	ratings.append(rating)
	ten_star = m.get_n_star(browser, 10, verbose)
	ten_stars.append(ten_star)
	one_star = m.get_n_star(browser, 1)
	one_stars.append(one_star)
	difference = float("{0:.1f}".format((ten_star * 10 + one_star) / (ten_star + one_star)))
	differences.append(difference)
	
	print("{0},{1},{2},{3},{4},{5}".format(title, imdb_id, rating, ten_star, one_star, difference), file=f)
	print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(truncate(title, 15), imdb_id, rating, ten_star, one_star, difference))

"""
layout = go.Layout(
	title="Rating vs Difference",
	xaxis=dict(
		title="Rating"
	),
	yaxis=dict(
		title="Difference"
	)
)
trace = go.Scatter(
	x=ratings,
	y=differences,
	text=titles,
	mode="markers"
)
fig = go.Figure(data=[trace], layout=layout)
py.plot(fig, filename="graph{:03}".format(fnum))
"""

browser.quit()
