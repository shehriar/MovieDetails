import objecttier
import sqlite3

#########################################################
## Command 1
## Output all movie details about the movies similar to user input
def command1(dbConn):
  userInput = input("Enter movie name (wildcards _ and % supported): ")
  print()

  # use function from objecttier
  rows = objecttier.get_movies(dbConn, userInput)
  # check if there are no rows
  if rows is None:
    print("# of movies found: 0", end = "\n")
    return;

  print("# of movies found:", len(rows), end = "\n\n")

  # check if there are too many rows
  if len(rows) > 100:
    print("There are too many movies to display, please narrow your search and try again...", end = "\n")
    return;

  # printing values
  for row in rows:
    print(row.Movie_ID, ":", row.Title, "("+row.Release_Year+")", end = "\n")
  print()

#########################################################
## Command 2
## Gets all movie details about the movie that has the same ID as user input
def command2(dbConn):
  userInput = int(input("Enter movie id: "))
  print()
  rows = objecttier.get_movie_details(dbConn, userInput)
  # If there are no rows fetched
  if not rows:
    print("No such movie...", end = "\n")
    return;

  # printing values
  print(rows.Movie_ID, ":", rows.Title, end = "\n")
  print("  Release date:", rows.Release_Date, end = "\n")
  print("  Runtime:", rows.Runtime, end = " (mins)\n")
  print("  Orig language:", rows.Original_Language, end = "\n")
  print("  Budget: $"+ f"{rows.Budget:,}", end = " (USD)\n")
  print("  Revenue: $"+ f"{rows.Revenue:,}", end = " (USD)\n")
  print("  Num reviews:", rows.Num_Reviews, end = "\n")
  print("  Avg rating:", "%.2f" % rows.Avg_Rating, end = " (0..10)\n")
  print("  Genres:", end = " ")
  # printing the items in genre list
  for genre in rows.Genres:
    print(genre+",", end = " ")
  print()
  
  print("  Production companies:", end = " ")
  # printing the items in production companies list
  for company in rows.Production_Companies:
    print(company+",", end = " ")
  print()

  print("  Tagline:", rows.Tagline, end = "\n")
  print()

#########################################################
## Command 3
## Get the top N number of movies based on average rating. Movies also have to have a minimum number of reviews.
def command3(dbConn):
  userN = int(input("N? "))
  # Check boundaries of N
  if(userN < 1):
    print("Please enter a positive value for N...", end = "\n\n")
    return
  
  userMin = int(input("min number of reviews? "))
  # Check boundaries of minimum number of reviews
  if(userMin < 1):
    print("Please enter a positive value for min number of reviews...", end = "\n\n")
    return

  rows = objecttier.get_top_N_movies(dbConn, userN, userMin)
  
  print()

  # printing values
  for row in rows:
    print(row.Movie_ID, ":", row.Title, "("+str(row.Release_Year)+"),", "avg rating =", "%.2f" % row.Avg_Rating, "("+str(row.Num_Reviews), "reviews)", end = "\n")
  print()
  
#########################################################
## Command 4
## Insert a new rating into the database
def command4(dbConn):
  userRating = int(input("Enter rating (0..10): "))
  if(userRating < 0 or userRating > 10):
    print("Invalid rating...", end = "\n")
    print()
    return
  
  userID = int(input("Enter movie id: "))
  # add using objecttier function
  insertRating = objecttier.add_review(dbConn, userID, userRating)

  if not insertRating:
    print()
    print("No such movie...")
    print()
    return
  print()
  print("Review successfully inserted")
  print()

#########################################################
## Command 5
## update the tagline of a movie into the database
def command5(dbConn):
  userTagline = input("tagline? ")

  userID = int(input("movie id? "))
  # update using objecttier function
  updateTagline = objecttier.set_tagline(dbConn, userID, userTagline)

  if not updateTagline:
    print()
    print("No such movie...")
    print()
    return
  print()
  print("Tagline successfully set")
  print()

# Prints the General statistics of the database
def startingPrint(dbConn):
  print("** Welcome to the MovieLens app **", end = "\n\n")

  print("General stats:", end = "\n")
  numMovies = objecttier.num_movies(dbConn)
  print("  # of movies:", f"{numMovies:,}", end = "\n")
  
  numReviews = objecttier.num_reviews(dbConn)
  print("  # of reviews:", f"{numReviews:,}", end = "\n\n")

# for user to determine which command they want
def whichCommand(dbConn):
  userInput = input("Please enter a command (1-5, x to exit): ")
  print()
  
  while(userInput !='x'):
    match userInput:
      case '1':
        command1(dbConn)
      case '2':
        command2(dbConn)
      case '3':
        command3(dbConn)
      case '4':
        command4(dbConn)
      case '5':
        command5(dbConn)
      case 'x':
        break
      case _:
        break
    userInput = input("Please enter a command (1-5, x to exit): ")
    print()
  pass
  
#########################################################
## Main
dbConn = sqlite3.connect('MovieLens.db')
startingPrint(dbConn)

whichCommand(dbConn)
dbConn.close()