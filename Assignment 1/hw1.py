# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW
    ratings = defaultdict(list)
    for line in open(f):
        movie, rating, _ = line.split("|")
        ratings[movie.strip()].append(float(rating.strip()))  
    return ratings

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW
    genres = {}
    for line in open(f):
        genre, _, movie = line.split("|")
        genres[movie.strip()] = genre.strip()
    return genres


# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW
    genres_swap = defaultdict(list)
    for key in d:
        genres_swap[d[key]].append(key)
    return genres_swap

# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    averages = {}
    for key in d:
        averages[key] = sum(d[key])/len(d[key])
    return averages


# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW
    topn = {}
    temp = d.copy()
    if len(temp) < n:
        count = len(temp)
    else:
        count = n
    for i in range(count) :
        toprating = 0
        for key in temp:
            if temp[key] >= toprating:
                topkey = key
                toprating = temp[key]
        if topkey not in topn:
            topn[topkey] = temp.pop(topkey, None)
    return topn
   
# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    filtered = {}
    for key in d:   
        if d[key] >= thres_rating:
            filtered[key] = d[key]
    return filtered
 
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    topn = {}
    targetmovies = genre_to_movies[genre]
    if len(targetmovies) < n:
        count = len(targetmovies)
    else:
        count = n
    for i in range(count):
        toprating = 0
        for movie in targetmovies:
            if movie_to_average_rating[movie] >= toprating and movie not in topn:
                topkey = movie
                toprating = movie_to_average_rating[movie]
        topn[topkey] = toprating
    return topn

# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    # WRITE YOUR CODE BELOW
    targetmovies = genre_to_movies[genre]
    genreratings = [movie_to_average_rating[movie] for movie in targetmovies]
    genreaverage = sum(genreratings)/len(genreratings)
    return genreaverage
    
    
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    # WRITE YOUR CODE BELOW
    topn = {}
    if len(genre_to_movies) < n:
        count = len(genre_to_movies)
    else:
        count = n
    for i in range(count):
        toprating = 0
        for genre in genre_to_movies:
            genreaverage = get_genre_rating(genre, genre_to_movies, movie_to_average_rating)
            if genreaverage >= toprating and genre not in topn:
                toprating = genreaverage
                topgenre = genre
        topn[topgenre] = toprating
    return topn


# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    # WRITE YOUR CODE BELOW
    userratings = defaultdict(list)
    for line in open(f):
        movie, rating, id = line.split("|")
        userratings[int(id)].append((movie, float(rating)))
    return userratings
    
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW
    #1. get dict of user genres to ratings
    usergenres = defaultdict(list)
    usermovies = user_to_movies[user_id]
    for tup in usermovies:
        usergenres[movie_to_genre[tup[0]]].append(tup[1])
    #2. find out which genre has the highest average rating
    toprating = 0
    for genre in usergenres:
        if sum(usergenres[genre])/len(usergenres[genre]) >= toprating:
            toprating = sum(usergenres[genre])/len(usergenres[genre])
            topgenre = genre
    return topgenre
    
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    usergenre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    allgens = create_genre_dict(movie_to_genre)
    targetgen = allgens[usergenre]
    userrated = user_to_movies[user_id]
    top3 = {}
    for val in userrated:
        if val[0] in targetgen:
            targetgen.remove(val[0])
    while not len(top3) == 3 and not len(targetgen) == 0:
        toprating = 0
        for movie in targetgen:
            if movie_to_average_rating[movie] >= toprating:
                topmovie = movie
                toprating = movie_to_average_rating[movie]
        top3[topmovie] = movie_to_average_rating.pop(topmovie)
        targetgen.remove(topmovie)
    return top3


# -------- main function for your testing -----
def main():


# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()

    
