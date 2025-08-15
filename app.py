import streamlit as st
import pickle
import pandas as pd
import requests
import time
from requests.exceptions import ConnectionError, Timeout, HTTPError



st.markdown("""
<style>
.title {
    font-family: "Better Minds" , cursive ;
    font-weight: bold;
    font-size: 50px;  
    color:  LightSalmon;
    text-align: center;
    animation: 
    glowShadow  2.5s infinite;

}
@keyframes glowShadow {
  0%, 100% { text-shadow: 0 0 5px LightSalmon, 0 0 10px Gold; }
  50% { text-shadow: 0 0 15px MediumPurple, 0 0 30px DeepSkyBlue; }
}


/* Background image */

[data-testid="stAppViewContainer"] {
    background: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4") center/cover fixed;
}


/* Center Recommend button and make text huge */

div.stButton {
    display: flex;
    justify-content: center;
}
div.stButton > button {
    font-size: 10px !important;
    font-family: "Better Minds", cursive;
    padding: 20px 40px !important;
}

/* Make selected text in search box big */

div[data-baseweb="select"] > div {
    font-size: 20px !important;
    font-family: "Better Minds", cursive;

}

/* Make dropdown list items big */

ul[role="listbox"] li {
    font-size: 50px !important;
    font-family: "Better Minds", cursive;
    color: yellow !important; /* Yellow font */
}
</style>
""", unsafe_allow_html=True)

# Persistent session for API requests

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

API_KEY = "2bbdeb88d13933eba9d83546ea498f09"  # TMDB API key

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    for attempt in range(3):
        try:
            response = session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except (ConnectionError, Timeout) as e:
            print(f"Connection issue (attempt {attempt + 1}/3): {e}")
            time.sleep(1)
        except HTTPError as e:
            print(f"HTTP error: {e}")
            break
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(poster_url)
        time.sleep(0.3)  # Prevent hitting API rate limits

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Display title
st.markdown('<div class="title">MOVIE RECOMMENDER SYSTEM</div>', unsafe_allow_html=True)

# Subtitle
st.markdown('<p style="font-size:20px; font-family: \'Better Minds\' ; font-weight: 400;color = yellow">DESIGNED BY NAVNEET</p>', unsafe_allow_html=True)

# Movie selection box
selected_movie_name = st.selectbox("", movies['title'].values)

# Recommend button and movie results

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])




