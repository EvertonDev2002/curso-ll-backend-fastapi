from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from app.models import Anime
from app.schema.anime import AnimeCreate, AnimePublic
from app.database import Session

router = APIRouter(prefix="/anime", tags=['animes'])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AnimePublic)
def create_anime(anime: AnimeCreate):
    with Session() as session:
        db_anime = Anime(**anime.model_dump())
        session.add(db_anime)
        session.commit()
        session.refresh(db_anime)
        return db_anime

@router.get('/{anime_id}', response_model=AnimePublic)
def read_anime(anime_id: int):
    with Session() as session:
        anime = session.get(Anime, anime_id)
        if anime is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Anime não encontrado'
            )
        return anime
