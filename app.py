import streamlit as st
import pickle
import requests

# Load data
movies_list = pickle.load(open('movies.pkl', 'rb'))  
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_titles = movies_list['title'].values  

# TMDb API key (Replace with your actual key)
API_KEY = "facc59915e55876b4e5a42ddf776f30d"

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')
    return None  

# Function to recommend movies
def recommend(movie):
    if movie not in movies_list['title'].values:
        return [], []  
    
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_indices:
        movie_row = movies_list.iloc[i[0]]
        movie_title = movie_row.title
        movie_id = movie_row.movie_id  # Use the 'movie_id' column

        recommended_movies.append(movie_title)

        # Fetch movie poster using TMDb ID
        poster_url = fetch_poster(movie_id)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movie_titles  
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    if not recommended_movie_names:
        st.error("❌ Movie not found. Please check the title.")
    else:
        # Display recommendations in columns
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                if recommended_movie_posters[i]:
                    st.image(recommended_movie_posters[i])
                else:
                    st.text("No poster available")
