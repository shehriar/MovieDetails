# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, id, title, year):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, id, title, year, num, avg):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = num
    self._Avg_Rating = avg

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, id, title, r_date, runtime, lang, budget, revenue, num, avg_rating, tagline):
    self._Movie_ID = id;
    self._Title = title
    self._Release_Date = r_date
    self._Runtime = runtime
    self._Original_Language = lang
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = num
    self._Avg_Rating = avg_rating
    self._Tagline = tagline
    self._Genres = [];
    self._Production_Companies = [];

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title
  
  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime
  
  @property
  def Original_Language(self):
    return self._Original_Language
  
  @property
  def Budget(self):
    return self._Budget
  
  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  
  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  try:
    sql = "select count(*) from movies;"
    row = datatier.select_one_row(dbConn, sql)[0]
    return row
  except Exception as err:
    print("Error: num_movies failed", err)
    return -1
  pass


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  try:
    sql = "select count(*) from ratings;"
    row = datatier.select_one_row(dbConn, sql)[0]
    return row
  except Exception as err:
    print("Error: num_reviews failed", err)
    return -1
  pass


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by movie id; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  try:
    sql = "select movie_id, title, strftime('%Y', release_date) from movies where title like ? group by movie_id order by movie_id asc;"
    rows = datatier.select_n_rows(dbConn, sql, [pattern])
    resultList = []
    
    for row in rows:
      resultList.append(Movie(row[0], row[1], row[2]))
      
    return resultList
    
  except Exception as err:
    print("Error: get_movies failed", err)
  pass

##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  try:
    sqlMain = "select movies.movie_id, movies.title, strftime('%Y-%m-%d', movies.release_date) as rDate, movies.runtime, movies.original_language, movies.budget, movies.revenue, count(ratings.movie_id) as numRatings, sum(ratings.rating) as sumRatings, movie_taglines.tagline from Movies left join ratings on movies.movie_id = ratings.movie_id left join movie_taglines on movies.movie_id = movie_taglines.movie_id where movies.movie_id = ? group by movies.movie_id order by movies.movie_id;"
    row = datatier.select_one_row(dbConn, sqlMain, [movie_id])
    if row == None:
      return None
      
    id = row[0]
    title = row[1]
    date = row[2]
    runtime = row[3]
    language = row[4]
    budget = row[5]
    revenue = row[6]
    
    numRatings = row[7]
    if numRatings == 0:
      numRatings = 0
      avgRating = 0
    else:
      avgRating = row[8]/numRatings
      
    tagline = row[9]
    if tagline == None:
      tagline = ""

    res = MovieDetails(id, title, date, runtime, language, budget, revenue, numRatings, avgRating, tagline)

    sqlGenre = "select genre_name from genres join movie_genres on movie_genres.genre_id = genres.genre_id where movie_genres.movie_id = ? group by genre_name order by genre_name;"
    genreRows = datatier.select_n_rows(dbConn, sqlGenre, [movie_id])
    if genreRows != None:
      for row in genreRows:
        res._Genres.append(row[0])
    
    sqlProduction = "select company_name from companies join movie_production_companies on companies.company_id = movie_production_companies.company_id where movie_production_companies.movie_id = ? group by company_name order by company_name;"
    productionRows = datatier.select_n_rows(dbConn, sqlProduction, [movie_id])
    if productionRows != None:
      for row in productionRows:
        res._Production_Companies.append(row[0])
        
    return res
    
  except:
    return None
  pass
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  try:
    sql = "select movies.movie_id, movies.title, strftime('%Y', movies.Release_date), count(ratings.movie_id), avg(ratings.rating) from Movies left join Ratings on movies.movie_id = ratings.movie_id group by movies.movie_Id having count(ratings.movie_id) >= ? order by avg(ratings.rating) desc limit ?;"
    rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
    result = []
    
    if rows == None:
      return result

    for row in rows:
      result.append(MovieRating(row[0], row[1], row[2], row[3], row[4]))

    return result
  except:
      return []
  pass


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  try:
    sqlFindMovie = "select 1 from movies where movie_id = ?"
    row1 = datatier.select_one_row(dbConn, sqlFindMovie, [movie_id])
    if row1[0] != 1:
      return 0
    
    sql = "insert into ratings(movie_id, rating) values (?, ?);"
    row = datatier.perform_action(dbConn, sql, [movie_id, rating])
    
    if row == -1:
      return 0
      
    return 1
    
  except:
    return 0
  pass


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  try:
    sqlFindMovie = "select 1 from movies where movie_id = ?"
    row1 = datatier.select_one_row(dbConn, sqlFindMovie, [movie_id])
    if int(row1[0]) != 1:
      return 0

    sqlIsTagline = "select 1 from Movie_Taglines where movie_id = ?"
    row2 = datatier.select_one_row(dbConn, sqlIsTagline, [movie_id])
    
    if not row2:  # No existing tagline, so add one
      sqlInsert = "insert into movie_taglines(movie_id, tagline) values (?, ?);"
      row3 = datatier.perform_action(dbConn, sqlInsert, [movie_id, tagline])
      
      if row3 == -1:
        return 0
        
      return 1
    
    # Tagline exists, so update it
    sqlUpdate = "update movie_taglines set tagline = ? where movie_id = ?"
    row4 = datatier.perform_action(dbConn, sqlUpdate, [tagline, movie_id])
    
    if row4 == -1:
      return 0
    return 1
    
  except:
    return 0
