from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

class Movie:
	def __init__(self, imdb_id, title=None):
		if str(imdb_id)[:2] == "tt":
			imdb_id = str(imdb_id[2:])
		
		self.imdb_id = imdb_id
		if title != None and re.search(r"(?! \()\d{4}(?=\)($|\n))", title) != None:
			self.year = re.search(r"(?! \()\d{4}(?=\)($|\n))", title)
			self.title = re.sub(r" \(\d{4}\)($|\n)", "", title)
		else:
			self.year = None
			self.title = title

	def get_page(self, driver):
		if driver.current_url == "http://www.imdb.com/title/tt%s" % self.imdb_id:
			return "title"
		elif driver.current_url == "http://www.imdb.com/title/tt%s/ratings" % self.imdb_id:
			return "ratings"
	
	def load_page(self, driver, page, verbose=False):
		url = None
		if page == "ratings" and not self.get_page(driver) == "ratings":
			url = "http://www.imdb.com/title/tt{0}/ratings".format(self.imdb_id)
		elif page == "title" and not self.get_page(driver) == "title":
			url = "http://www.imdb.com/title/tt{0}".format(self.imdb_id)
		if url != None:
			if verbose:
				print("Accessing \"{0}\"...".format(url), end="")
			driver.get(url)
			
			try:
				WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "navbar-query")))
			except TimeoutException:
				pass
			
			if verbose:
				print("Done!")
	
	def get_title(self, driver, verbose=False):
		if self.title == None:
			if self.get_page(driver, verbose) == "title":
				self.title = driver.find_elements_by_path("//h1[0]").get_attribute("innerText")
			else:
				self.load_page(driver, "title", verbose)
				self.title = self.get_title(driver, verbose)
		
		return self.title
	
	def has_ratings(self, driver, verbose=False):
		if self.get_page(driver) == "ratings":
			return len(driver.find_elements_by_xpath("//tbody[1]/tr")) >= 11
		else:
			self.load_page(driver, "ratings", verbose)
			return self.has_ratings(driver, verbose)
	
	def get_n_star(self, driver, stars, verbose=False):
		if self.has_ratings(driver):
			self.load_page(driver, "ratings", verbose)
		
			return int(driver.find_element_by_xpath("//tbody[1]/tr[{0}]/td[3]/div/div".format(12 - stars)).get_attribute("innerText").replace(',',""))
	
	def get_num_ratings(self, driver, verbose=False):
		if self.get_page(driver) == "ratings":
			if self.has_ratings(driver, verbose):
				num_ratings = 0
				for i in range (1, 11):
					num_ratings += self.get_n_star(driver, i, verbose)
				return num_ratings
			else:
				return 0
		elif self.get_page(driver) == "title":
			return int(driver.find_element_by_xpath("//*[@id=\"title-overview-widget\"]/div[2]/div[2]/div/div[1]/div[1]/a/ratings").get_attribute("innerText"))
		else:
			self.load_page(driver, "ratings", verbose)
			return self.get_num_ratings(driver, verbose)
	
	def get_rating(self, driver, verbose=False):
		if self.has_ratings(driver):
			if self.get_page(driver) == "ratings":
				return driver.find_element_by_xpath("//*[@name=\"ir\"]").get_attribute("data-value")
			elif self.get_page(driver) == "title":
				return driver.find_element_by_xpath("//*[@itemprop='ratingValue']").get_attribute("innerText")
			else:
				self.load_page(driver, "ratings", verbose)
				return self.get_rating(driver, verbose)

def movie_by_name(driver, name):
	if not "imdb.com" in driver.current_url:
		driver.get("http://www.imdb.com")
		try:
			WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "navbar-query")))
		except TimeoutException:
			return None
	try:
		searchbar = driver.find_element_by_id("navbar-query")
	except NoSuchElementException:
		return None
	
	searchbar.clear()
	searchbar.send_keys(name)
	searchbar.submit()
	
	try:
		return Movie(WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "td.result_text > a"))).get_attribute("href")[26:35], title=name)
	except TimeoutException:
		return None
