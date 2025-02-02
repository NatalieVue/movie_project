import sqlalchemy as db
from sqlalchemy import select, MetaData, Table, Column, Integer, String, desc
from sqlalchemy.orm import sessionmaker, join
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

class Movie(BaseModel):
    Id: str  
    TitleType: str
    PrimaryTitle: str
    OriginalTitle: str
    IsAdult: str
    StartYear: str
    EndYear: str
    RuntimeMinutes: str
    Genres: str

def access_tables1():
   meta = MetaData()
   engine = db.create_engine('sqlite:///my_data.db') # ensure this is the correct path for the sqlite file. 

   ratings = Table(
      "Ratings",
      meta,
      Column('Id', String),
      Column('AverageRating', String),
      Column('NumVotes', String)
   )
   
   movies = Table(
      "Movies",
      meta,
      Column('Id', String),
      Column('TitleType', String),
      Column('PrimaryTitle', String),
      Column('OriginalTitle', String),
      Column('IsAdult', String),
      Column('StartYear', String),
      Column('EndYear', String),
      Column('RuntimeMinutes', String),
      Column('Genres', String)
   )
   meta.create_all(engine)
   conn = engine.connect()

   r = ratings.select().where(ratings.c.Id == 'tt0110357')
   # m = movies.select().where(and_(movies.c.PrimaryTitle=="The Lion King", movies.c.TitleType == 'movie')).order_by(movies.c.Id)
   m = movies.select().where(movies.c.Id == 'tt0110357')
   
   rating_result = conn.execute(r)
   result = conn.execute(m)
   
   rating_res = [rating for rating in rating_result]

   res = [movie for movie in result]
   
   # stmt = select().select_from(ratings).join(movies, movies.Id == ratings.Id)

   # session = sessionmaker(bind=engine)
   # results = session.execute(stmt) 
  
   # for row in results: 
   #    print(row)

   stmt = (
    select(movies)
    .select_from(join(movies, ratings, movies.Id))

)
   print(stmt)

   return res, rating_res


def access_tables():
   # meta = MetaData()
   engine = db.create_engine('sqlite:///my_data.db') # ensure this is the correct path for the sqlite file. 
   Base = declarative_base()
   class Ratings(Base):
      __tablename__ = "Ratings"
      Id = Column(String, primary_key=True)
      AverageRating = Column(Integer)
      NumVotes = Column(String(512))
   
   class Movies(Base):
      __tablename__ = "Movies"
      Id = Column(String, primary_key=True)
      TitleType = Column(String)
      PrimaryTitle = Column(String(512))
      OriginalTitle = Column(String)
      IsAdult = Column(String)
      StartYear = Column(String)
      EndYear = Column(String)
      RuntimeMinutes = Column(String)
      Genres = Column(String)

   Session = sessionmaker(bind = engine)
   session = Session()


   # movie_rowzzzzzz = session.query(
   #    Movies, Ratings
   #    ).join(Ratings, Movies.Id == Ratings.Id).filter(Movies.PrimaryTitle == 'The Lion King').all()
   # print(movie_rowzzzzzz[0])
   movie_rows = session.query(
      Movies.Id, 
      Movies.PrimaryTitle, 
      Ratings.AverageRating,
      Ratings.NumVotes
      ).join(Ratings, Movies.Id == Ratings.Id
      ).filter(Ratings.NumVotes > 10, Movies.StartYear.between('2015','2025'), Movies.TitleType == 'movie', Ratings.AverageRating > 7
         # Movies.PrimaryTitle == 'The Lion King', Movies.StartYear.between('2015','2025'), Movies.TitleType == 'movie'
      ).order_by(desc(Ratings.NumVotes)
      ).limit(10
      ).all()
   
   # print("MOVIES",movie_rows)
   return movie_rows
