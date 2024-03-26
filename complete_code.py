import pandas as pd
import numpy as np

movies_df = pd.read_csv('C:\\Users\\weron\\Desktop\\uczelnia\\Semestr_6\\ai\\tmdb_5000_movies.csv')
credits_df = pd.read_csv('C:\\Users\\weron\\Desktop\\uczelnia\\Semestr_6\\ai\\tmdb_5000_credits.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

print(credits_df)         
# credits_df.head() - 5 pierwszych
# credits_df.tail() - 5 ostatnich

print(movies_df)

# łączenie dwóch ramek danych (DataFrames) w oparciu o wspólną kolumnę 'title'
movies_df = movies_df.merge(credits_df, on = 'title')

# zwraca rozmiar tabeli - liczbę wierszy i kolumn
movies_df.shape

movies_df.head()

''' Zwraca podsumowanie informacji o ramce danych movies_df, takie jak:
- liczbę wierszy (obserwacji) w ramce danych,
- liczbę kolumn w ramce danych,
- nazwy kolumn oraz typy danych w każdej kolumnie,
- liczbę niepustych wartości w każdej kolumnie,
- podsumowanie używanej pamięci przez ramkę danych.'''
movies_df.info()

# Nadpisanie poprzedniej tabeli, tabelą z wybranym zestawem kolumn
movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

movies_df.head()

movies_df.info()

# wykonuje zliczenie wartości brakujących w poszczególnych kolumnach ramki
movies_df.isnull().sum()

# Usuwanie wszystkich wierszy, które zawierają przynajmniej jedną wartość null z ramki
# inplace=False -> zwróci nową ramkę danych z usuniętymi wierszami, oryginalną zostawi bez zmian
movies_df.dropna(inplace=True)

# Zlicza zduplikowane wiersze w ramce danych
movies_df.duplicated().sum()

# Pobiera wartość w kolumnie "genres" dla pierwszego wiersza w ramce danych movies_df
movies_df.iloc[0].genres

# Importuje moduł ast, który jest potrzebny do przekształcania stringów zawierających literały struktur danych Pythona 
# na rzeczywiste struktury danych Pythona.
import ast

def convert(obj):   # Przyjmuje jeden argument obj, który jest stringiem reprezentującym listę słowników.
    L = []          # Tworzy pustą listę L, do której zostaną dodane nazwy z elementów przekształconej listy słowników.
    for i in ast.literal_eval(obj):     # wywołuje funkcję literal_eval() z modułu ast, która przekształca string obj na rzeczywistą listę
        L.append(i['name'])         #  Dla każdego słownika i w przekształconej liście, dodaje wartość pola 'name' do listy L.
    return L        #  Zwraca listę L, która zawiera nazwy z przekształconej listy słowników

movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)
movies_df.head()

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])     # Dodaje nazwę aktualnego słownika do listy, do osiągnięcia wartości 3
            counter +=1
        else:
            break
        return L        # zawiera nazwy z przetworzonych słowników, ograniczone do trzech pierwszych
    
movies_df['cast'] = movies_df['cast'].apply(convert3)

movies_df.head()

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
        return L
    
movies_df['crew'] = movies_df['crew'].apply(fetch_director)

movies_df

movies_df['overview'][0]

movies_df['overview']=movies_df['overview'].apply(lambda x:x.split())

movies_df['genres'] = movies_df['genres'].apply(lambda x:[i.replace(" "," ") for i in x])
movies_df['keywords'] = movies_df['keywords'].apply(lambda x:[i.replace(" "," ") for i in x])
#movies_df['cast'] = movies_df['cast'].apply(lambda x:[i.replace(" "," ") for i in x])
#movies_df['crew'] = movies_df['crew'].apply(lambda x:[i.replace(" "," ") for i in x])

movies_df

movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']

movies_df

new_df = movies_df[['movie_id','title','tags']]

new_df

# new_df['tags'] = new_df['tags'].apply(lambda x:' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)


new_df

new_df['tags'][0]

#new_df['tags'] = new_df['tags'].apply(lambda X:X.lower())
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower() if isinstance(x, str) else x)

new_df.head()

new_df.dropna(subset=['tags'], inplace=True)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features= 5000, stop_words='english')

cv.fit_transform(new_df['tags']).toarray().shape

vectors = cv.fit_transform(new_df['tags']).toarray()

vectors[0]

len(cv.get_feature_names_out())

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(vectors)

cosine_similarity(vectors).shape

similarity = cosine_similarity(vectors)

similarity[0]

similarity[0].shape

sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x:x[1])[1:6]

def recommend(movie):
    movie_index = new_df[new_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


