import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
from nltk.stem.porter import PorterStemmer

# Wczytanie danych
movies_df = pd.read_csv('C:\\Users\\weron\\Desktop\\uczelnia\\Semestr_6\\ai\\tmdb_5000_movies.csv')
credits_df = pd.read_csv('C:\\Users\\weron\\Desktop\\uczelnia\\Semestr_6\\ai\\tmdb_5000_credits.csv')

# Ustawienia wyświetlania dla DataFrame'ów
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

# Funkcja do przekształcania list słowników w listę nazw
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Przygotowanie danych
movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)

# Funkcja do rekomendacji filmów
def recommend(movie):
    # Inicjalizacja stemmera
    ps = PorterStemmer()
    
    # Przekształcenie list na łańcuchy znaków
    movies_df['genres'] = movies_df['genres'].apply(lambda x: ' '.join(x))
    movies_df['keywords'] = movies_df['keywords'].apply(lambda x: ' '.join(x))
    movies_df['cast'] = movies_df['cast'].apply(lambda x: ' '.join(x))
    movies_df['crew'] = movies_df['crew'].apply(lambda x: ' '.join(x))
    
    # Przygotowanie tagów
    movies_df['tags'] = movies_df['overview'] + ' ' + movies_df['genres'] + ' ' + movies_df['keywords'] + ' ' + movies_df['cast'] + ' ' + movies_df['crew']
    movies_df['tags'] = movies_df['tags'].apply(lambda x: x.lower())
    movies_df.dropna(subset=['tags'], inplace=True)
    movies_df['tags'] = movies_df['tags'].apply(lambda x: ' '.join([ps.stem(word) for word in x.split()]))
    
    # Wektoryzacja tagów
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    
    # Obliczenie podobieństwa
    similarity = cosine_similarity(vectors)
    
    # Wyszukanie rekomendowanych filmów
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies_df.iloc[i[0]]['title'] for i in movies_list]
    
    return recommended_movies

# Przykładowe użycie
recommended_movies = recommend('Avatar')
print(recommended_movies)
