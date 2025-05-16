from fastapi import FastAPI, HTTPException
from database import engine
import models
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, models
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()


@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
       db_movie = models.Movie(
           title=movie.title,
           year=movie.year,
           director=movie.director
       )
       db.add(db_movie)
       db.commit()
       db.refresh(db_movie)

       for actor in movie.actors:
           db_actor = models.Actor(actor_name=actor.actor_name, movie_id=db_movie.id)
           db.add(db_actor)
       db.commit()
       db.refresh(db_movie)
       return db_movie


@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
       movie = db.query(models.Movie).options(joinedload(models.Movie.actors)).order_by(func.random()).first()
       if movie is None:
           raise HTTPException(status_code=404, detail="No movies found")
       return movie

@app.post("/add_movie", response_model=schemas.MoviePublic)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
       db_movie = models.Movie(
           title=movie.title,
           year=movie.year,
           director=movie.director
       )
       db.add(db_movie)
       db.commit()
       db.refresh(db_movie)

       for actor in movie.actors:
           db_actor = models.Actor(actor_name=actor.actor_name, movie_id=db_movie.id)
           db.add(db_actor)
       db.commit()
       db.refresh(db_movie)
       return db_movie

@app.get("/movies/{movie_id}/summary")
def generate_summary(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).options(joinedload(models.Movie.actors)).filter(models.Movie.id == movie_id).first()
    if movie is None:
        return {"error": f"Movie with id {movie_id} not found."}
    actor_names = [actor.actor_name for actor in movie.actors]
    summary = (
        f"'{movie.title}' ({movie.year}), directed by {movie.director}, "
        f"stars {', '.join(actor_names)}."
    )
    return {
        "id": movie.id,
        "title": movie.title,
        "actors": actor_names,
        "summary": summary
    }