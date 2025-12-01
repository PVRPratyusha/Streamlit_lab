import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_generator import generate_movie_data, generate_user_ratings, save_data
from model import MovieRecommender


@st.cache_data
def load_data():
    """Load or generate movie data."""
    movies = generate_movie_data(n_movies=100)
    ratings = generate_user_ratings(n_users=50, n_movies=100)
    save_data(movies, ratings)
    return movies, ratings


def main():
    st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

    st.title("🎬 Movie Recommendation Dashboard")
    st.markdown("---")

    # Load data
    movies, ratings = load_data()
    recommender = MovieRecommender(movies, ratings)

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Recommendations", "Analytics"])

    if page == "Home":
        show_home(movies, recommender)
    elif page == "Recommendations":
        show_recommendations(movies, recommender)
    else:
        show_analytics(movies, recommender)


def show_home(movies, recommender):
    """Display home page."""
    st.header("Top Rated Movies")
    top_movies = recommender.get_top_rated(10)
    st.dataframe(top_movies, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Movies", len(movies))
    col2.metric("Avg Rating", f"{movies['rating'].mean():.1f}")
    col3.metric("Genres", movies['genre'].nunique())


def show_recommendations(movies, recommender):
    """Display recommendations page."""
    st.header("Get Recommendations")

    tab1, tab2 = st.tabs(["By Genre", "Similar Movies"])

    with tab1:
        genre = st.selectbox("Select Genre", movies['genre'].unique())
        num_recs = st.slider("Number of recommendations", 3, 10, 5)

        if st.button("Get Recommendations", key="genre_btn"):
            recs = recommender.recommend_by_genre(genre, num_recs)
            st.subheader(f"Top {num_recs} {genre} Movies")
            st.dataframe(recs, use_container_width=True)

    with tab2:
        movie_title = st.selectbox("Select Movie", movies['title'].tolist())
        movie_id = movies[movies['title'] == movie_title]['movie_id'].values[0]

        if st.button("Find Similar", key="similar_btn"):
            similar = recommender.recommend_similar(movie_id, 5)
            st.subheader(f"Movies similar to {movie_title}")
            st.dataframe(similar, use_container_width=True)


def show_analytics(movies, recommender):
    """Display analytics page."""
    st.header("Movie Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Movies by Genre")
        genre_counts = movies['genre'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        st.subheader("Ratings Distribution")
        fig2, ax2 = plt.subplots()
        ax2.hist(movies['rating'], bins=15, edgecolor='black')
        ax2.set_xlabel('Rating')
        ax2.set_ylabel('Count')
        st.pyplot(fig2)

    st.subheader("Genre Statistics")
    genre_stats = recommender.get_genre_stats()
    st.dataframe(genre_stats, use_container_width=True)


if __name__ == "__main__":
    main()