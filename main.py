from selenium import webdriver
from movie import *
from random import randint
import os.path

loadtype = 'r'
browser = webdriver.PhantomJS()

movies = []


if loadtype == 'f':
	for i in range(2017, 2007, -1):
		f = open("res/{0}.txt".format(i), "r")

		print("Loading movies from {0}...".format(i))
		for line in f:
			line = line[:-1]
			print("\tLoading \"{0}\"...".format(line), end="")
			movie = movie_by_name(browser, line)
			if movie != None:
				movies.append(movie)
				print("Done!")
			else:
				print("Error :(")
		print("Done!")
		
		print("IMDB id\trating\t10*\t1*")
		print("-------------------------------")
		for movie in movies:
			print("{0}\t{1}\t{2}\t{3}".format(movie.imdb_id, movie.get_rating(browser), movie.get_n_star(browser, 10), movie.get_n_star(browser, 1)))
elif loadtype == 'r':
	nummovies = 5
	for i in range(2017, 2007, -1):
		print("Selecting {0} random movies from {1}...".format(nummovies, i))
		f = open("res/{0}.txt".format(i))
		lines = f.readlines()
		f.close()
		selected = [None]
		while len(movies) - (2017 - i) * nummovies < nummovies:
			title = None
			while title in selected:
				title = lines[randint(0, len(lines) - 1)][:-1]
			m = movie_by_name(browser, title)
			if m.get_num_ratings(browser) >= 5000:
				movies.append(m)
				print("\tSelected \"{0}\"".format(title))
		print("Done!")
	
	fnum = 0
	while os.path.exists("log{:03}.csv".format(fnum)):
		fnum += 1
	
	f = open("log{:03}.csv".format(fnum), "w")
	
	print("Title,IMDb ID,Rating,10 Star,1 Star", file=f)
	for m in movies:
		title = m.get_title(browser)
		imdb_id = m.imdb_id
		rating = m.get_rating(browser)
		ten_star = m.get_n_star(browser, 10)
		one_star = m.get_n_star(browser, 1)
		print("{0},{1},{2},{3},{4}".format(title, imdb_id, rating, ten_star, one_star), file=f)
		print("{0}\t{1}\t{2}\t{3}\t{4}".format(title, imdb_id, rating, ten_star, one_star))
	
browser.quit()
