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

- Injeção de Dependência (`Depends`) para gerenciar a `Session` por requisição
- `RedirectResponse`
- Middleware
- Tratamento de exceções mais robusto (`exception_handler`)

<!-- imagem de destaque desta aula: ../../imgs/05-aula/<sua-imagem>.png -->

---

## UploadFile e File

O FastAPI oferece duas formas de receber arquivos:

- `bytes`: lê o arquivo inteiro na memória (simples, mas ruim para arquivos grandes)
- `UploadFile`: usa arquivo temporário em disco, expõe `filename`, `content_type` e é mais eficiente

Para o projeto, vamos usar `UploadFile` no upload da capa do anime.

---

### Endpoint de Upload

```python
# app/routers/animes.py

from pathlib import Path

from fastapi import UploadFile

PASTA_CAPAS = Path("static/capas")
PASTA_CAPAS.mkdir(parents=True, exist_ok=True)


@router.post("/{anime_id}/capa")
def upload_capa(anime_id: int, session: DbSession, arquivo: UploadFile):
    anime = session.get(Anime, anime_id)

    caminho = PASTA_CAPAS / f"{anime_id}_{arquivo.filename}"

    with open(caminho, "wb") as arquivo_salvo:
        arquivo_salvo.write(arquivo.file.read())

    anime.capa = str(caminho)
    session.commit()

    return {"capa": anime.capa}
```

---

### Validação de Arquivo

```python
# app/routers/animes.py

from http import HTTPStatus

from fastapi import HTTPException

TIPOS_PERMITIDOS = {"image/png", "image/jpeg", "image/webp"}
TAMANHO_MAXIMO_MB = 5


@router.post("/{anime_id}/capa")
def upload_capa(anime_id: int, session: DbSession, arquivo: UploadFile):
    if arquivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail="Formato de imagem não suportado.",
        )

    conteudo = arquivo.file.read()

    if len(conteudo) > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail="Arquivo maior que o permitido.",
        )

    # restante do código (salvar conteudo, atualizar anime.capa)
```

---

## Servindo arquivos estáticos

Para visualizar a capa depois do upload, expomos a pasta `static/` publicamente.

```python
# app/main.py

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

Com isso, uma capa salva em `static/capas/1_naruto.png` fica acessível em `/static/capas/1_naruto.png`.

---

## Revisão Geral do Projeto

- **Aula 1:** fundamentos de back-end, HTTP, CRUD em memória, Pydantic
- **Aula 2:** modelagem, normalização, diagrama ER e regras de negócio do projeto
- **Aula 3:** SQLAlchemy, models com relacionamentos, Alembic, APIRouter
- **Aula 4:** Injeção de Dependência, RedirectResponse, Middleware, tratamento de exceções
- **Aula 5:** upload e validação da capa, arquivos estáticos

---

![bg left:35%](../../imgs/common/nana-question.png)

**Atividade**

- Cadastre alguns animes, autores e estúdios pela API
- Faça upload de uma capa para cada anime cadastrado e confira o arquivo pelo `/static`
- Fique livre para adicionar novos recursos ao projeto (ex: filtros extras, novos campos, novos endpoints)

---

## Referencias

- [FastAPI — Request Files (UploadFile)](https://fastapi.tiangolo.com/tutorial/request-files/)
- [FastAPI — UploadFile Reference](https://fastapi.tiangolo.com/reference/uploadfile/)
- [FastAPI — Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
- [FastAPI do Zero](https://fastapidozero.dunossauro.com/4.0)

---

<!-- _paginate: skip -->

![bg fit ](../../imgs/common/fim.png)
