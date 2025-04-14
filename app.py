from flask import Flask, request, jsonify, render_template
import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import sigmoid_kernel
import requests
import ast

app = Flask(__name__)


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

def recommend(title, min_similarity=0.5, sig=sig):
    # Get the index corresponding to original_title
    idx = movies[movies['original_title'] == title].index[0]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = [i for i in sig_scores if i[1] > min_similarity][1:21]

    # Movie indices
    #movie_indices = [i[0] for i in sig_scores]

    # Get recommendations with posters
    recommendations = []
    posters = []
        # Get the genre data
    target_genre = movies[movies['original_title'] == title]['genres'].iloc[0]

    # If it's stored as a string (not list), convert it first:
    if isinstance(target_genre, str):
        target_genre = ast.literal_eval(target_genre)

    # Extract the genre names
    target_genre_names = [genre['name'] for genre in target_genre]
    
    print("target",target_genre_names)
    for i, scores in sig_scores: #skip self
        if scores > min_similarity:
            movie_id = movies.iloc[i]['id']  # Assuming your DataFrame has TMDB IDs
            poster = fetch_movie_poster(movie_id)

            movie_data = movies.iloc[i]['genres']
            if isinstance(movie_data, str):
                movie_data = ast.literal_eval(movie_data)
            genre_names = [genre['name'] for genre in movie_data]
            #print(genre_names)
            target_genres_set = set(target_genre_names)
            movie_genres_set = set(genre_names)
            common_genres = target_genres_set & movie_genres_set #checking common genres
            if len(common_genres) >= 2:
                recommendations.append(movies.iloc[i]['original_title'])
                posters.append(poster)
                
    
    return recommendations, posters

'''st.title('Movie Recommendation System')



selected_movie_name = st.selectbox('Select a movie you like',
                    movies['original_title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    if recommended_movie_names:
        # Split recommendations into chunks of 5
        for i in range(0, len(recommended_movie_names), 5):
            # Create a row of up to 5 columns
            cols = st.columns(5)
            
            # Fill this row with up to 5 recommendations
            for j in range(5):
                if i + j < len(recommended_movie_names):
                    with cols[j]:
                        st.text(recommended_movie_names[i + j])
                        if i + j < len(recommended_movie_posters):
                            st.image(recommended_movie_posters[i + j])
                else:
                    with cols[j]:
                        st.empty()  # Empty space if less than 5 in this row
    else:
        st.warning("No recommendations available")'''

@app.route('/', methods=['GET', 'POST'])
def home():
    movie_list = movies['original_title'].values
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        return render_template(
            'index.html',
            movie_list=movie_list,
            selected_movie=selected_movie,
            recommended=zip(recommended_movie_names, recommended_movie_posters)
        )

    return render_template('index.html', movie_list=movie_list)

if __name__ == '__main__':
    app.run(debug=True)
