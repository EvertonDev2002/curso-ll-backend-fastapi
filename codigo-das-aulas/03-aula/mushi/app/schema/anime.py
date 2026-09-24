from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, Self
from app.enums.anime_status import AnimeStatus

class AnimeBase(BaseModel):
    name: str = Field(..., max_length=150)
    episodes: int = Field(default=0, ge=0)
    episodes_watched: int = Field(default=0, ge=0)
    score: Optional[float] = Field(default=None, ge=0, le=10)
    status: AnimeStatus = AnimeStatus.PLANEJO_ASSISTIR
    cover: Optional[str] = None
    #author_id: Optional[int] = None
    #studio_id: Optional[int] = None

    @model_validator(mode="after")
    def validar_watched(self)-> Self:
        if self.episodes_watched > self.episodes:
            raise ValueError("episodes_watched não pode ser maior que episodes")
        if self.status == AnimeStatus.PLANEJO_ASSISTIR and self.score is not None:
            raise ValueError('score deve ser nulo quando status for planejo assistir')
        return self

class AnimePublic(AnimeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnimeList(BaseModel):
    animes: list[AnimePublic]

class AnimeCreate(AnimeBase):
    pass
