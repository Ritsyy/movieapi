Movie API

An API interface to search and find movies by names, directors and genres.

It uses data from imdb.json

## Setting up project and initializing data
```
# create a virtualenv 
virtualenv env_movie
source env_movie/bin/activate
pip install -r reuqirements.txt
./manage.py migrate
./manage.py runserver 7001
./manage.py import_db
```


API request examples
GET Movies

base API url
https://rocky-ravine-28021.herokuapp.com/movies/

search by name (full text search)
https://rocky-ravine-28021.herokuapp.com/movies/?name=wizard

search by movie name and director name
https://rocky-ravine-28021.herokuapp.com/movies/?name=wizard&director=victor

search by genre name
https://rocky-ravine-28021.herokuapp.com/movies/?genre=family


POST a movie
/movies/
  {
    "popularity": 83.0,
    "director": "richa rupela",
    "score": 8.3,
    "name": "test",
    "genres": ["Comedy"]
  }

PUT a movie

/movies/

  {
    "popularity": 83.0,
    "director": "richa rupela",
    "score": 8.3,
    "name": "test yo",
    "genres": ["Comedy"],
    "id": "255"
  }

