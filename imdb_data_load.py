
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.exc import IntegrityError
import traceback
from imdb_scrapping_functions import create_combined_data_frames

import pandas as pd

imdb_combined_gener_movies = create_combined_data_frames()

imdb_data_load = imdb_combined_gener_movies.drop_duplicates(subset='movie_name')

engine = create_engine("mysql+pymysql://root:root@localhost:3306/imdb")

Base = declarative_base()

class ImdbMovies(Base):
    __tablename__ = 'imdb_movies'
    movie_name = Column(String(255), primary_key=True, nullable=False)
    genre = Column(String(255), nullable=False)
    ratings = Column(Float)
    voting_counts = Column(Integer)
    duration = Column(Float)
    
# Create the table in the database
Base.metadata.create_all(engine)

try:
    imdb_data_load.to_sql('imdb_movies', con=engine, index=False, if_exists='replace')
    print("Inserted the data successfully")

except IntegrityError as e:
    print("Exception occured while inserting records due to duplicate")
    print(e._message)

except Exception as e:
    print("other exception")
    traceback.print_exc()
      