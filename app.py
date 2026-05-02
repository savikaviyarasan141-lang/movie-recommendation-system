import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch poster
def fetch_poster(movie_id):
    api_key = "1aec4fa452fc4a76978a0787cfa56b37"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()

    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# UI
st.title("🎬 Movie Recommendation System")

# Select movie
selected_movie = st.selectbox(
    "Type or select a movie",
    movies['title'].values
)

# Button
if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])