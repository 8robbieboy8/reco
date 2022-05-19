from flask import Flask, render_template, request
from datetime import date
import requests
import json
from fetch import movie, movie_collection


app = Flask(__name__)



@app.route('/', methods = ['GET', 'POST'])
#라우트 메서드는 
def home():
    if request.method =="GET":
        year = date.today().year
        url = f'http://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year={year}&sort_by=popularity.desc'
        top_year = movie_collection()
        top_year.results = []
        top_year.fetch(url)
        
        genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=da396cb4a1c47c5b912fda20fd3a3336&language=en-US").text)

        top_genre_collection = []
        for genre in genres['genres']:
            # print(genre['id'])
            genre_id = f'https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&with_genres={genre["id"]}&sort_by=popularity.desc'
            top_genre = movie_collection()
            top_genre.results = []
            top_genre.fetch(genre_id)
            top_genre_id = [top_genre.results, genre["name"]]
            top_genre_collection.append(top_genre_id)
    
    return render_template('home.html', message = 'success')

if __name__ == '__main__':
    app.run(debug = True)