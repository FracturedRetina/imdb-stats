from selenium import webdriver
from movie import *

browser = webdriver.PhantomJS()

movie = movie_by_name(browser, input("Enter a movie title: "))
#movie = Movie(input("Enter a movie id: "))

for i in range(10, 0, -1):
	print("{0}: {1}".format(i, movie.get_n_star_ratings(browser, i)))

browser.quit()
