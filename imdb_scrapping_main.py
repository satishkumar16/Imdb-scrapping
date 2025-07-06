import time
import pandas as pd
from selenium import webdriver
from imdb_scrapping_functions import search_movies


driver = webdriver.Chrome()

base_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres={genre}"

genre_list = ['action','animation','biography']

for genre in genre_list:
         imdb_url = base_url.format(genre=genre)
         driver.get(imdb_url)
         time.sleep(10)
         process_imdb_data(genre,driver)

driver.quit()