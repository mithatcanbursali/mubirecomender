import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

filmInfos = []

r=requests.get("https://api.mubi.com/v4/collections/trending", headers={"Client-Country":"TR","Client":"web"})
films = r.json()["films"]
for film in films:
    orig_title = film["original_title"]
    mov_year = film["year"]

    rating_r = requests.get("http://www.omdbapi.com/?apikey=a122d346&t={film_title}&y={film_year}".format(film_title=orig_title, film_year=mov_year))
    film_imdb_rating = rating_r.json()
    mubiRating = float(film["average_rating_out_of_ten"])

    if not "Error" in film_imdb_rating:
        if film_imdb_rating["imdbRating"] != "N/A":
            imdbRating = float(film_imdb_rating["imdbRating"])
        filmImg = film["still_url"]
        filmDirector = film_imdb_rating["Director"]
        averageRating = (imdbRating + mubiRating) / 2.0
        averageRating_floated = "{:.2f}".format(averageRating)
        filmColor = film["average_colour_hex"]
        filmDuration = film["duration"]
        filmGenre = film["genres"]
        filmDescription = film["short_synopsis"]
        filmWebURL = film["web_url"]

        new_film = {"filmName": orig_title, "filmYear": mov_year, "mubiRating": mubiRating, "imdbRating":imdbRating, "averageRating":averageRating_floated, "filmImg":filmImg, "filmDirector":filmDirector, "filmGenre":filmGenre,"filmColor":filmColor,"fiLmDuration":filmDuration,"filmDescription":filmDescription,"filmWebUrl":filmWebURL}
        filmInfos.append(new_film)

@app.route('/films', methods=['GET'])
def get_films():
    return jsonify(filmInfos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


