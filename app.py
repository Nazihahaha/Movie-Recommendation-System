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
    sig_scores = [i for i in sig_scores if i[1] > min_similarity][1:6]

    # Movie indices
    #movie_indices = [i[0] for i in sig_scores]

    # Get recommendations with posters
    recommendations = []
    posters = []
    
    for i, score in sig_scores[1:]: #skip self
        if i[1] > min_similarity:
            movie_id = movies.iloc[i]['id']  # Assuming your DataFrame has TMDB IDs
            poster = fetch_movie_poster(movie_id)
            movie_data = movies.iloc[i[0]]
            movie_genres = set(movie_data['genres'])
            if poster:  # Only include movies with posters
                recommendations.append(movies.iloc[i]['original_title'])
                posters.append(poster)
    
    return recommendations, posters




st.title('Movie Recommendation System')



selected_movie_name = st.selectbox('Select a movie you like',
                    movies['original_title'].values)



if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
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
    with col6:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])

