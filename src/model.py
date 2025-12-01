import pandas as pd
import numpy as np


class MovieRecommender:
    """Simple movie recommendation system."""

    def __init__(self, movies_df, ratings_df):
        self.movies = movies_df
        self.ratings = ratings_df
        self.movie_stats = self._compute_stats()

    def _compute_stats(self):
        """Compute average ratings per movie."""
        stats = self.ratings.groupby('movie_id').agg(
            avg_rating=('rating', 'mean'),
            num_ratings=('rating', 'count')
        ).reset_index()
        return self.movies.merge(stats, on='movie_id', how='left').fillna(0)

    def recommend_by_genre(self, genre, top_n=5):
        """Recommend top movies by genre."""
        genre_movies = self.movie_stats[self.movie_stats['genre'] == genre]
        return genre_movies.nlargest(top_n, 'avg_rating')[['title', 'year', 'rating', 'avg_rating']]

    def recommend_similar(self, movie_id, top_n=5):
        """Recommend similar movies based on genre and year."""
        movie = self.movies[self.movies['movie_id'] == movie_id].iloc[0]
        similar = self.movie_stats[
            (self.movie_stats['genre'] == movie['genre']) &
            (self.movie_stats['movie_id'] != movie_id)
            ]
        return similar.nlargest(top_n, 'avg_rating')[['title', 'year', 'rating', 'avg_rating']]

    def get_top_rated(self, top_n=10):
        """Get top rated movies overall."""
        return self.movie_stats.nlargest(top_n, 'rating')[['title', 'genre', 'year', 'rating']]

    def get_genre_stats(self):
        """Get statistics by genre."""
        return self.movie_stats.groupby('genre').agg(
            count=('movie_id', 'count'),
            avg_rating=('rating', 'mean'),
            avg_budget=('budget_million', 'mean')
        ).round(2).reset_index()