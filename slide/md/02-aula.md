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

- Definição de back-end
- Definição de API
- Definição do protocolo HTTP
  - Verbos HTTP
  - Status Code
- Definição de Endpoints
- Ambiente de Desenvolver
- CRUD

![bg right 99%](../../imgs/02-aula/naruto.png)

---

## Boas práticas em Python

### Estilo e legibilidade

- Indentação com 4 espaços
- Linha deve ter no máximo 79 caracteres
- Declarações
  - variáveis e funções em snake_case
  - classes em PascalCase
  - constantes em UPPER_SNAKE

**Dica:** Utilize ferramentas com `ruff` para garantir as boas práticas em Python

---

## Banco de Dados (Revisão) - SGBD

É um conjunto organizado de dados relacionados, armazenado e gerenciado de forma que permita inserção, consulta, atualização e remoção.

**Modelagem de Dados:**

- conceitual
- lógico
- físico

**Normalização:**

- 1FN
- 2FN
- 3FN

---

### Boas práticas para banco de dados

#### Nomenclatura: Regras Gerais

- Padrão Snake Case:
  - _Correto:_ `data_nascimento`
  - _Incorreto:_ `DataNascimento`, `dataNascimento`
- Idioma Unificado
- Caracteres Permitidos
- Palavras Reservadas

---

#### Nomenclatura: Tabelas

- Sempre no Singular:
  - _Correto:_ `cliente`, `item_pedido`
- Evite prefixos como `tb_` ou `tbl_`.
  - _Correto:_ `usuario`
  - _Incorreto:_ `tb_usuario`

---

### Nomenclatura: Atributos (Colunas)

- Sempre no Singular:
  - _Correto:_ `nome`, `preco_unitario`
- Evite Redundância
  - _Correto:_ `nome`, `cpf`
  - _Incorreto:_ `nome_cliente`, `cpf_cliente`
- Seja Descritivo e Claro
  - _Correto:_ `quantidade_estoque`
  - _Incorreto:_ `qtd_est`

---

### Nomenclatura: Chaves (PK e FK)

- Chave Primária (PK): Utilizar simplesmente `id`.
- Chave Estrangeira (FK): Deve seguir a regra estrita de usar o nome da tabela referenciada no singular, seguido do sufixo `_id`.
  - _Exemplo em uma tabela de pedidos:_ `cliente_id`, `produto_id`.

---

## O projeto Mushi Bingo

Objetivo: Criar uma versão simplificada do MyAnimeList, permitindo cadastrar animes e acompanhar o status de cada um (assistindo, parado, assistido, planejo assistir).

![bg right 70%](../../imgs/02-aula/ginko.jpg)

---

### Diagrama RE

É uma representação visual que descreve a estrutura lógica de um banco de dados, facilitando a compreensão das regras de negócio pela equipe.

**Componentes fundamentais:**

- Entidades (tabelas)
- Atributos (colunas)
- Relacionamentos

---

```mermaid
%%{
  init: {
    "theme": "base",
    "themeVariables": {
      "primaryColor": "#FFFFFF",
      "primaryBorderColor": "#000000",
      "primaryTextColor": "#000000",
      "lineColor": "#000000",
      "background": "#FFFFFF"
    }
  }
}%%

erDiagram
    AUTHOR {
        int id PK
        string name
    }
    STUDIO {
        int id PK
        string name
    }
    ANIME {
        int id PK
        string name
        int episodes
        int episodes_watched
        float score
        string status
        string cover
        int author_id FK
        int studio_id FK
        timestamp created_at
        timestamp updated_at
    }
    AUTHOR ||--o{ ANIME : "writes"
    STUDIO ||--o{ ANIME : "produces"

```

---

### Regras de negócio: Fluxo de Status

**Fluxo de progresso:**

- `planejo assistir` -> `assistindo` -> `assistido`
  - _Regra:_ Um anime só pode ser marcado como `assistido` depois de já ter passado por `assistindo`.
  - _Regra:_ Só é possível marcar como `assistido` quando `episodes_watched` for igual a `episodes`.

**Fluxo de pausa:**

- `assistindo` -> `parado` -> `assistindo`
  - _Regra:_ Um anime `parado` pode voltar a `assistindo` a qualquer momento.

---

### Regras de negócio: Nota

- A nota é opcional e vai de `0` a `10` (aceita casas decimais, ex: `8.5`).
- Só faz sentido atribuir nota quando o status for `assistindo` ou `assistido`.
  - _Regra:_ Se o status for `planejo assistir`, a nota deve ser nula.

---

### Regras de negócio: Cadastro

- O campo `name` do anime é obrigatório.
- `author_id` e `studio_id` são opcionais (nem todo anime tem essa informação cadastrada), mas quando informados devem referenciar um registro existente em `author`/`studio`.
- O campo `name` em `author` e `studio` deve ser único, evitando cadastros duplicados do mesmo autor ou estúdio.
- O campo `episodes` representa o total de episódios da obra (não o progresso assistido).

---

### Regras de negócio: Cadastro

- O campo `episodes_watched` representa quantos episódios o usuário já assistiu, começa em `0` na criação do anime.
  - _Regra:_ `episodes_watched` nunca pode ser maior que `episodes`.
  - _Regra:_ só faz sentido incrementar `episodes_watched` quando o status for `assistindo`.
- `created_at` é preenchido automaticamente na criação do registro.
- `updated_at` é atualizado automaticamente a cada modificação do registro.
- O campo `cover` é opcional e armazena apenas o caminho/URL da imagem salva no servidor.

---

### Endpoints (Sugestão): Autores

- `GET /authors` : Lista autores.
- `GET /authors/{id}` : Retorna um autor com os animes vinculados.
- `POST /authors` : Cria um novo autor.
- `PATCH /authors/{id}` : Atualiza dados do autor.

---

### Endpoints (Sugestão): Estúdios

- `GET /studios` : Lista estúdios.
- `GET /studios/{id}` : Retorna um estúdio com os animes vinculados.
- `POST /studios` : Cria um novo estúdio.
- `PATCH /studios/{id}` : Atualiza dados do estúdio.

---

### Endpoints (Sugestão): Animes

- `GET /animes` : Lista animes (Filtros: `?status=`, `?author_id=`, `?studio_id=`).
- `GET /animes/{id}` : Retorna um anime específico.
- `POST /animes` : Cria um novo anime.
- `PATCH /animes/{id}` : Atualiza dados (incluindo status, nota e episodes_watched).
- `DELETE /animes/{id}` : Remove um anime da lista.
- `POST /animes/{id}/cover` : Recebe a imagem de capa do anime e salva o caminho no campo `cover`.

---

## Estrutura de Pasta (Projeto)

```

mushi_bingo
├── app
│   ├── main.py
│   ├── models
│   ├── routers
│   ├── enums
│   ├── schema
│   └── settings.py
├── database.db
└── .env
```

---

## ORM (Object-Relational Mapping)

É uma técnica de programação (ferramenta) que permite interagir diretamente com um banco de dados usando o paradigma de Orientação a Objetos da sua linguagem de programação, em vez de escrever consultas SQL puras.
<br>

- Abstração de banco de dados
- Segurança
- Eficiência no desenvolvimento

---

### SQLAlchemy

É o ORM mais robusto e tradicional do ecossistema Python. Ele abstrai a complexidade do banco de dados relacional, permitindo que você manipule tabelas e registros como se fossem classes e objetos Python nativos.

- Mapeamento Objeto-Relacional
- Abstração de Dialeto
- Gerenciamento de Sessão

**Para instalar**

```
# No linux e Windows
uv add sqlalchemy
```

---

### Migrations

É o conceito de controle de versão aplicado ao esquema (estrutura) do banco de dados. As migrações registram cada evolução da estrutura em arquivos de código ordenados cronologicamente.

- Histórico de Evolução
- Consistência de Ambientes
- Preservação de Dados

---

### Alembic

É a ferramenta oficial de migração de banco de dados projetada especificamente para funcionar em conjunto com o SQLAlchemy. Ele automatiza o processo de criação e aplicação das migrações.

- Autogeração de scripts
- Controle de direção (Upgrade/Downgrade)
- Automação de deploy

**Para instalar**

```
# No linux e Windows
uv add alembic
uv run alembic init migrations
```

---

![bg left:35%](../../imgs/common/nana-question.png)

**Ativdade**

- Leia as regras de negócios e tente implementar os recursos (endpoints)
- Tente criar por si mesmo as tabelas do banco de dados
- Tente refazer o diagrama do banco de dados conforme seu gosto (assim como as regras de negócio e endpoints)

---

# Próximos tópicos

- Conectar Banco de Dados
- Criar Recursos
- RedirectResponse
- Injeção de Dependência
- Middleware

---

## Referencias

- [FastAPI do Zero](https://fastapidozero.dunossauro.com/4.0)
- [FastAPI](https://fastapi.tiangolo.com/)
- [UV](https://docs.astral.sh/uv/)
- [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/)
- [Métodos de requisição HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Methods)
- [REST: Princípios e boas práticas](https://www.alura.com.br/artigos/rest-principios-e-boas-praticas)
- [5 dicas para fazer APIs melhores](https://www.youtube.com/watch?v=UEbm9mqFLTY)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Ambiente Python Moderno 2025: UV, Ruff, Pyright, pyproject.toml e VS Code](https://www.youtube.com/watch?v=HuAc85cLRx0)
- [Curso de Modelagem de Dados](https://www.youtube.com/playlist?list=PLucm8g_ezqNoNHU8tjVeHmRGBFnjDIlxD)

---

<!-- _paginate: skip -->

![bg fit ](../../imgs/common/fim.png)
