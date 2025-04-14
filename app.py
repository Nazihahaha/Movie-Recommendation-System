import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import sigmoid_kernel



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict) #Datafreame creation

# Load or compute similarity matrix
sig = pickle.load(open('similarity.pkl', 'rb'))


# Create reverse mapping of indices and movie titles
indices = pd.Series(movies.index, index=movies['original_title']).drop_duplicates()


def recommend(title, sig =sig):
    # Get the index corresponding to original_title
    idx = movies[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return movies['original_title'].iloc[movie_indices]




st.title('Movie Recommendation System')



selected_movie_name = st.selectbox('Select a movie you like',
                    movies['original_title'].values)


if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if not recommendations.empty:
        st.write("Recommended Movies:")
        st.write(recommendations)
    else:
        st.write("Movie not found in database")


