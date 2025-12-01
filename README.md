# Streamlit Lab: Movie Recommendation Dashboard

An interactive ML dashboard built with Streamlit for movie recommendations.

## Project Structure
```
Streamlit_Lab/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
├── models/
└── src/
    ├── __init__.py
    ├── app.py
    ├── data_generator.py
    └── model.py
```

## Features
- Browse top rated movies
- Get recommendations by genre
- Find similar movies
- View analytics and visualizations

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
streamlit run src/app.py
```

## Technologies
- Python 3.12
- Streamlit
- Scikit-learn
- Pandas
- Matplotlib