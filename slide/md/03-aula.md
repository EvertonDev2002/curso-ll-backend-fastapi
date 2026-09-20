---
marp: true
paginate: true
lang: pt-BR

theme: minimalist
---

![bg left 99%](../../imgs/01-aula/kanna.png)

# Formação Backend: Python & FastAPI — O Caminho Sannin de Orochimaru

## Projeto Mushi Bingo

---

# Aula Anterior

- Revisão de Banco de Dados
- Boas práticas de nomenclatura de banco de dados
- Apresentação do projeto: diagrama ER, regras de negócio e endpoints sugeridos
- Estrutura de pastas do projeto

![bg right 80%](../../imgs/03-aula/grimmer.jpg)

---

## Recapitulando: ORM, SQLAlchemy e Alembic

- **ORM:** manipular tabelas e registros como classes e objetos Python
- **SQLAlchemy:** o ORM que vamos utilizar no projeto
- **Alembic:** ferramenta de migrations, integrada ao SQLAlchemy

---

## Enum

Enum (abreviação de enumeration, ou "enumeração") é um tipo de dado que representa um conjunto fixo e finito de valores constantes e nomeados.

```Python
# app/enums/anime_status.py

from enum import Enum as PyEnum


class AnimeStatus(str, PyEnum):
    PLANEJO_ASSISTIR = 'planejo assistir'
    ASSISTINDO = 'assistindo'
    ASSISTIDO = 'assistido'
    PARADO = 'parado'
```

---

## Schemas

Um schema Pydantic é uma classe que descreve a forma dos dados que entram e saem da sua `API`. É a camada de contrato entre o mundo externo (`JSON` do cliente) e o mundo interno (objetos `ORM` do `SQLAlchemy`).

- Schema Pydantic = validação + serialização + documentação automática

Quando instalamos o `FastAPI` com [standard], todos os pacotes complementares foram instalados juntos, o `pydantic-*` é um deles.

- Certifique que possui instalado com `uv pip list`

---

### Criando Schema: Anime Base

```Python
# app/schema/anime.py

from pydantic import BaseModel, Field, model_validator
from typing import Optional, Self
from app.enums.anime_status import AnimeStatus


class AnimeBase(BaseModel):
    name: str = Field(..., max_length=150)
    episodes: int = Field(default=0, ge=0)
    episodes_watched: int = Field(default=0, ge=0)
    score: Optional[float] = Field(default=None, ge=0, le=10)
    status: AnimeStatus = AnimeStatus.PLANEJO_ASSISTIR
    cover: Optional[str] = None
    author_id: Optional[int] = None
    studio_id: Optional[int] = None

    @model_validator(mode='after')
    def validar_watched(self) -> Self:
        if self.episodes_watched > self.episodes:
            raise ValueError('episodes_watched não pode ser maior que episodes')
        if self.status == AnimeStatus.PLANEJO_ASSISTIR and self.score is not None:
            raise ValueError('score deve ser nulo quando o status for planejo assistir')
        return self
```

- `ge`: O valor deve ser maior ou igual a esse número
- `le`: O valor deve ser menor ou igual a esse número

---

### Criando Schema: Anime Public

```python
from datetime import datetime
from pydantic import ConfigDict


class AnimePublic(AnimeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

### Criando Schema: Anime List

```Python
class AnimeList(BaseModel):
    animes: list[AnimePublic]
```

### Criando Schema: Anime Schema

```Python
class AnimeCreate(AnimeBase):
    pass
```

---

## Configurando ambiente do banco de dados

A classe `Settings` fica responsavel por carregar as configurações do arquivo `.env`.

```python
# app/settings.py

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str = Field(init=False)
```

Em `.env` adicione `DATABASE_URL="sqlite:///database.db"`

---

### Criando Model: base

```python
# app/models/base.py

from sqlalchemy.orm import registry

table_registry = registry()
```

---

### Criando o Model: Anime

```python
# app/models/anime.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from app.enums.anime_status import AnimeStatus
from app.models.base import table_registry

if TYPE_CHECKING:
    from .author import Author
    from .studio import Studio


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

    author_id: Mapped[int | None] = mapped_column(
        ForeignKey('author.id'), default=None, nullable=True
    )
    studio_id: Mapped[int | None] = mapped_column(
        ForeignKey('studio.id'), default=None, nullable=True
    )
    author: Mapped[Author | None] = relationship(
        back_populates='animes', default=None
    )
    studio: Mapped[Studio | None] = relationship(
        back_populates='animes', default=None
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), init=False,
    )
```

---

### Tornando Models em um pacote

O `__init__.py` é um arquivo especial que marca um diretório como um pacote Python. Sem ele (na forma tradicional), o Python não reconhece a pasta como um pacote importável.

```python
# app/models/__init__.py

from app.models.anime import Anime
from app.models.base import table_registry

```

---

## Alembic: Configuração Inicial

Em `migrations/env.py`, aponte o `target_metadata` para os models do projeto:

```python
# migrations/env.py

from app.models import table_registry
from app.settings import Settings

config = context.config
config.set_main_option('sqlalchemy.url', Settings().DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = table_registry.metadata
```

---

## Alembic: Gerando e Aplicando Migrations

```bash
# Gera o script de migration comparando os models com o banco

uv run alembic revision --autogenerate -m "cria tabela anime"
```

```bash
# Aplica a migration, criando as tabelas de fato

uv run alembic upgrade head
```

**Dica:** Sempre revise o arquivo gerado antes de aplicar a migration.

---

## Configurando o SQLAlchemy

Criamos o `engine` (conexão com o banco) e a `Session` (unidade de trabalho para consultas e alterações).

```python
# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


Session = sessionmaker(bind=engine, autoflush=False)
```

---

### Persistindo os dados no banco (POST)

O `database = []` sai de cena, agora os endpoints usam a `Session` do SQLAlchemy.

```python
# app/routers/animes.py

@router.post("/", status_code=HTTPStatus.CREATED, response_model=AnimePublic)
def create_anime(anime: AnimeCreate):
    with Session() as session:
        db_anime = Anime(**anime.model_dump())
        session.add(db_anime)
        session.commit()
        session.refresh(db_anime)

        return db_anime
```

**Aviso**: _Não esqueça de fazer os imports em database, models e schema._

---

### Consultando o banco de dados por `id` (GET)

```python
@router.get('/{anime_id}', response_model=AnimePublic)
def read_anime(anime_id: int):
    with Session() as session:
        anime = session.get(Anime, anime_id)
        if anime is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Anime não encontrado'
            )
        return anime
```

---

![bg left:35%](../../imgs/common/nana-question.png)

**Atividade**

- Siga o mesmo padrão de `/animes` para implementar `/authors` e `/studios`
- Teste os endpoints pelo Swagger (`/docs`) e confira se os dados estão sendo salvos no `database.db`
- Fique livre para criar filtros ou endpoints extras que fizerem sentido para o seu projeto

---

# Próximos tópicos

- Injeção de Dependência (`Depends`)
- `RedirectResponse`
- Middleware
- Router
- Tratamento de exceções mais robusto

---

## Referencias

- [SQLAlchemy — ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [SQLAlchemy — Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic — Validators ](https://pydantic.dev/docs/validation/dev/concepts/validators/)
- [Pydantic — Constrainst (Restrições)](https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-2)
- [Pydantic — Fields](https://pydantic.dev/docs/validation/latest/api/pydantic/fields/)
- [Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/?h=Query)
- [Python - typing](https://docs.python.org/pt-br/3.14/library/typing.html)
- [Python - dataclasses](https://docs.python.org/pt-br/3.14/library/dataclasses.html)
- [Curso de Type Hints](https://www.youtube.com/playlist?list=PLbIBj8vQhvm04EuddtleOAoEmfU9vwQlN)

---

<!-- _paginate: skip -->

![bg fit ](../../imgs/common/fim.png)
