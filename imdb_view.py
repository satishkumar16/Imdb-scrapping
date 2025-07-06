import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns


genres =['All','Action','Musical','Biography','Animation']
columns = ["Title", "Genre", "ratings", "voting_counts", "Duration in hours"]
durations =['NA','<1 hr','<2 hrs','<3 hrs','>1 hr','>2 hrs','>3 hrs','1-2 hrs','2-3 hrs']
symbols =['>','=','<','>=','<=']
values = ['NA','1','2','3','4','5','6','7','8','9','10']
duration_map = {
    '<1 hr': "duration < 1",
    '<2 hrs': "duration < 2",
    '<3 hrs': "duration < 3",
    '=1 hr': "duration = 1",
    '=2 hrs': "duration = 2",
    '=3 hrs': "duration = 3",
    '>1 hr': "duration > 1",
    '>2 hrs': "duration > 2",
    '>3 hrs': "duration > 3",
    '1-2 hrs': "duration BETWEEN 1 AND 2",
    '2-3 hrs': "duration BETWEEN 2 AND 3"
}

def db_connection():
    try: 
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='imdb'
        )
        return conn        
    except Error:
        print("Error while connecting to MySQL")
        return None

st.set_page_config(layout="wide")

page = st.sidebar.radio("Select the Process", ["Search Movies"])

if page == "Search Movies":
    st.markdown(
        "<h1 style='text-align: center;'>IMDB Movies</h1>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

    with col1:
        st.markdown("<div style='font-weight:bold;'>Genre:</div>",unsafe_allow_html=True)   
        genre = st.radio(label="",options=genres)

    with col2:
        st.markdown("<div style='font-weight:bold;'>Rating:</div>",unsafe_allow_html=True)
        rate_criteria = st.selectbox(label="",options=symbols,key="rating_value")   
        rating = st.selectbox(label="",options=values)    

    with col3:
        st.markdown("<div style='font-weight:bold;'>Durations:</div>",unsafe_allow_html=True) 
        selected_durations = st.selectbox(label="",options=durations)

    with col4:
        st.markdown("<div style='font-weight:bold;'>Voting Count:</div>",unsafe_allow_html=True)
        vote_criteria = st.selectbox(label="",options=symbols,key="vote_value")
        voting_count =  st.text_input(
            label="", 
        placeholder="NA"
        )

    with col5:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        search_criteria = st.button('Search')    
    
    if search_criteria:    
        conn = db_connection()
        cursor = conn.cursor()
        if conn:
            query = "SELECT * FROM imdb_movies WHERE 1=1"
            params = []   

            if genre and genre != 'All':
                query += " AND Genre = %s"
                params.append(genre)

            if rating and rating != 'NA':
                query += f" AND ratings {rate_criteria} %s"
                params.append(rating)  

            if selected_durations and selected_durations != 'NA'and selected_durations in duration_map:
                query += f" AND {duration_map[selected_durations]}"
                
            if voting_count and voting_count !='NA':
                query += f" AND voting_counts {vote_criteria} %s"
                params.append(voting_count)
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            df = pd.DataFrame(results,columns=columns)
            st.write(df)

