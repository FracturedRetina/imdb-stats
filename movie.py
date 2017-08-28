from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

class Movie:
	def __init__(self, imdb_id):
		if imdb_id[:2] == "tt":
			imdb_id = imdb_id[2:]
		
		self.imdb_id = imdb_id
	
	def get_page(self, driver):
		if driver.current_url == "http://www.imdb.com/title/tt%s" % self.imdb_id:
			return "title"
		elif driver.current_url == "http://www.imdb.com/title/tt%s/ratings" % self.imdb_id:
			return "ratings"
	
	def load_page(self, driver, page, verbose=False):
		url = None
		if page == "ratings" and not self.get_page(driver) == "ratings":
			url = "http://www.imdb.com/title/tt%s/ratings" % self.imdb_id
		elif page == "title" and not self.get_page(driver) == "title":
			url = "http://www.imdb.com/title/tt%s" % self.imdub_id
		
		if url != None:
			if verbose:
				print("Accessing \"{0}\"...".format(url), end="")
			driver.get(url)
			if verbose:
				print("Done!")
	
	def has_ratings(self, driver, verbose=False):
		if self.get_page(driver) == "ratings":
			return len(driver.find_elements_by_xpath("//tbody[1]/tr")) >= 11
		else:
			self.load_page(driver, "ratings", verbose)
			return self.has_ratings(driver)
	
	def get_n_star(self, driver, stars, verbose=False):
		if self.has_ratings(driver):
			self.load_page(driver, "ratings", verbose)
		
			return driver.find_element_by_xpath("//tbody[1]/tr[{0}]/td".format(12 - stars)).get_attribute("innerText")
	
	def get_rating(self, driver, verbose=False):
		if self.get_page(driver) == "ratings":
			return driver.find_element_by_xpath("//div[@id=\"tn15content\"]/p/a[2]").get_attribute("innerText")
		else:
			self.load_page(driver, "ratings", verbose)
			return self.get_rating(driver, verbose)

def movie_by_name(driver, name):
	if not "imdb.com" in driver.current_url:
		driver.get("http://www.imdb.com")
	searchbar = driver.find_element_by_id("navbar-query")
	searchbar.clear()
	searchbar.send_keys(name)
	searchbar.submit()
	
	return Movie(WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "td.result_text > a"))).get_attribute("href")[26:35])
