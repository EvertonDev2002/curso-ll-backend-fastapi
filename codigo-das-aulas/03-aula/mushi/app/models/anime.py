from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import (
Mapped,
mapped_as_dataclass,
mapped_column,

)
from app.enums.anime_status import AnimeStatus
from app.models.base import table_registry
#if TYPE_CHECKING:
#from .author import Author
#from .studio import Studio
@mapped_as_dataclass(registry=table_registry)
class Anime:
    __tablename__ = 'anime'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150))
    episodes: Mapped[int] = mapped_column(default=0)
    episodes_watched: Mapped[int] = mapped_column(default=0)
    score: Mapped[float | None] = mapped_column(default=None)
    status: Mapped[AnimeStatus] = mapped_column(
    SQLEnum(AnimeStatus, native_enum=False, name='anime_status'),
    default=AnimeStatus.PLANEJO_ASSISTIR,
    )
    cover: Mapped[str | None] = mapped_column(default=None)
    #author_id: Mapped[int | None] = mapped_column(
    #ForeignKey('author.id'), default=None, nullable=True
    #)
    #studio_id: Mapped[int | None] = mapped_column(
    #ForeignKey('studio.id'), default=None, nullable=True
    #)
    #author: Mapped[Author | None] = relationship(
    #back_populates='animes', default=None
    #)
    #studio: Mapped[Studio | None] = relationship(
    #back_populates='animes', default=None
    #)
    created_at: Mapped[datetime] = mapped_column(
    server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
    server_default=func.now(), onupdate=func.now(), init=False,
    )
