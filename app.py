import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import sigmoid_kernel
import requests



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict) #Datafreame creation

# Load or compute similarity matrix
sig = pickle.load(open('similarity.pkl', 'rb'))


# Create reverse mapping of indices and movie titles
indices = pd.Series(movies.index, index=movies['original_title']).drop_duplicates()

# Your TMDB API key
API_KEY = "8216a29a0c1530dea56770df0beb9a07"

def fetch_movie_poster(movie_id):
    # Get movie details including poster path
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

def recommend(title, sig =sig):
    # Get the index corresponding to original_title
    idx = movies[movies['original_title'] == title].index[0]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:6]

    # Movie indices
    #movie_indices = [i[0] for i in sig_scores]

    movie_indices = []
    recommended_movies_posters = []
    for i in sig_scores:
        movie_id = i[0]
        # fetch movie poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        movie_indices.append(i[0])


    # Top 10 most similar movies
    return movies['original_title'].iloc[movie_indices], recommended_movies_posters




st.title('Movie Recommendation System')



selected_movie_name = st.selectbox('Select a movie you like',
                    movies['original_title'].values)



if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

