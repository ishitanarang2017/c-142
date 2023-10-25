from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api to return list of liked movies



@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api to return list of popular movies
@app.route("/popular_movies")
def popular_movies():
    popularmd = []
    for i,r in output.iterrows():
        _p = {
            "original_title": r["original_title"],
            "poster_link": r["poster_link"],
            "release_date": r["release_date"]or "na",
            "duration": r["runtime"],
            "rating": r["weighted_rating"]/2
        }
        popularmd.append(_p)
    return jsonify({
        "data": popularmd,
        "status": "success"
    })
                                      



# api to return list of recommended movies
@app.route("/rec_movies")
def rec_movies():
    global liked_movies
    columnnames = ['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating' ]
    all_rec = pd.DataFrame(columns=columnnames)
    for l in liked_movies:
        output = get_recommendations(l["original_title"])
        all_rec=all_rec.append(output)
    all_rec.drop_duplicates(subset=["original_title"],inplace = True)
    recmd = []
    for i,r in all_rec.iterrows():
        _p = {
            "original_title": r["original_title"],
            "poster_link": r["poster_link"],
            "release_date": r["release_date"] or "na",
            "duration": r["runtime"],
            "rating": r["weighted_rating"]/2
        }
        recmd.append(_p)
    return jsonify({
        "data": recmd,
        "status": "success"
    })


if __name__ == "__main__":
  app.run()
