import pandas as pd
import numpy as np
import os


def generate_movie_data(n_movies=100, seed=42):
    """Generate synthetic movie dataset."""
    np.random.seed(seed)

    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Thriller']

    titles = [f"Movie_{i + 1}" for i in range(n_movies)]

    data = {
        'movie_id': range(1, n_movies + 1),
        'title': titles,
        'genre': np.random.choice(genres, n_movies),
        'year': np.random.randint(1990, 2024, n_movies),
        'duration_min': np.random.randint(80, 180, n_movies),
        'rating': np.round(np.random.uniform(3.0, 9.5, n_movies), 1),
        'votes': np.random.randint(1000, 500000, n_movies),
        'budget_million': np.random.randint(5, 200, n_movies),
    }

    df = pd.DataFrame(data)
    df['revenue_million'] = (df['budget_million'] * np.random.uniform(0.5, 5, n_movies)).astype(int)

    return df


def generate_user_ratings(n_users=50, n_movies=100, seed=42):
    """Generate synthetic user ratings."""
    np.random.seed(seed)

    ratings = []
    for user_id in range(1, n_users + 1):
        n_rated = np.random.randint(5, 30)
        movies_rated = np.random.choice(range(1, n_movies + 1), n_rated, replace=False)
        for movie_id in movies_rated:
            ratings.append({
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': np.random.randint(1, 6)
            })

    return pd.DataFrame(ratings)


def save_data(movies_df, ratings_df, data_dir='data'):
    """Save dataframes to CSV."""
    os.makedirs(data_dir, exist_ok=True)
    movies_df.to_csv(f'{data_dir}/movies.csv', index=False)
    ratings_df.to_csv(f'{data_dir}/ratings.csv', index=False)
    return data_dir