import sqlite3
import pandas as pd

conn = sqlite3.connect('my_data.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS temp_ratings (tconst text, averageRating int, numVotes int)''')
# c.execute('''CREATE TABLE IF NOT EXISTS temp_movies (tconst text, titleType text, primaryTitle text, originalTitle text, isAdult int, startYear text, endYear text, runtimeMinutes int, genres text)''')


# load the data into a Pandas DataFrame
ratings = pd.read_csv('title.ratings.tsv', sep='\t')

# write the data to a sqlite table
ratings.to_sql('temp_ratings', conn, if_exists='append', index = False)

c.execute('''
    CREATE TABLE IF NOT EXISTS Ratings AS
        SELECT
            tconst as Id, 
            averageRating as AverageRating,
            numVotes as NumVotes
        FROM temp_ratings
''')

# we're not doing this here
# c.execute('''
#     CREATE TABLE IF NOT EXISTS Movies AS
#         SELECT
#             tconst as Id,
#             titleType as TitleType,
#             primaryTitle as PrimaryTitle,
#             originalTitle as OriginalTitle,
#             isAdult as IsAdult,
#             startYear as StartYear,
#             endYear as EndYear,
#             runtimeMinutes as RuntimeMinutes,
#             genres as Genres
#         FROM temp_movies
# ''')
