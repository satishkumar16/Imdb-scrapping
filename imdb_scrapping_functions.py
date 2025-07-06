
from selenium.webdriver.common.by import By
import pandas as pd

combined_genre_data = []

def format_voting_count(vote_value):
       vote_value =vote_value.replace('(', '').replace(')', '').strip().lower().replace(',', '')
       if vote_value.endswith('k'):
              return int(float(vote_value[:-1]) * 1000)
       elif vote_value.endswith('m'):
            return int(float(vote_value[:-1]) * 1000000)
       else:
            return int(float(vote_value))

def format_duration(duration_value):
    
    duration_value = duration_value.lower().strip()

    if 'h' in duration_value and 'm' in duration_value:
        parts = duration_value.split(' ')
        hours = int(parts[0].replace('h', ''))
        minutes = int(parts[1].replace('m', ''))
        return round(hours + minutes / 60, 2)

    elif 'h' in duration_value:
         return round(int(duration_value.replace('h', '').strip()), 2)


    elif 'm' in duration_value:
        minutes = int(duration_value.replace('min', '').replace('m', ''))
        return round(minutes / 60, 2)
    else:
        return 0              

def create_data_frames(titles, genres, ratings, votes, durations):
        df = pd.DataFrame({
        "movie_name": titles,
        "genre": genres,    
        "ratings": ratings,
        "voting_counts": votes,
        "duration": durations
    })   

        df['movie_name'] = df['movie_name'].astype(str).str.replace(r'^\d+\.\s*', '', regex=True)
        df['voting_counts'] = df['voting_counts'].apply(format_voting_count)
        df['duration'] = df['duration'].apply(format_duration)

        filename = f"imdb_{genres[0]}_movies.csv"
        df.to_csv(filename, index=False)
        print("Completed scrapping for genre:",genres[0])       

def process_imdb_data(genre,driver):

    titles, durations, ratings, genres,votes = [], [], [], [],[]
    movie_details = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item__tc")

    for movie_detail in movie_details:
            
            title = movie_detail.find_element(By.CSS_SELECTOR, ".ipc-title__text.ipc-title__text--reduced").text 

            duration_values = movie_detail.find_elements(By.XPATH, ".//span[contains(@class, 'dli-title-metadata-item')]")
            duration = duration_values[1].text

            rating = movie_detail.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text

            vote = movie_detail.find_element(By.CLASS_NAME,"ipc-rating-star--voteCount").text

            titles.append(title)
            durations.append(duration)
            votes.append(vote)
            ratings.append(rating)
            genres.append(genre)    

    create_data_frames(titles, genres, ratings, votes, durations)


def create_combined_data_frames():
        
        genre_list = ['action','animation','biography']
        for genre in genre_list:
            filename = f'imdb_{genre}_movies.csv'      
            imdb_data = pd.read_csv(filename)
            combined_genre_data.append(imdb_data)
        
        return pd.concat(combined_genre_data,ignore_index=True)
