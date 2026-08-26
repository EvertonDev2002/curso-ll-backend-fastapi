# Formação Backend: Python & FastAPI — Slides

Ambiente de slides em Marp, com diagramas Mermaid renderizados via Kroki
self-hosted, rodando em container (Docker ou Podman).

## Estrutura

```
.
├── theme/
│   └── minimalist.css     # Tema Personalizado
├── slide/
│   ├── md/                # fonte dos slides (.md)
│   ├── html/               # gerado pelo modo watch (fora do --server)
│   └── pdf/                 # gerado por `pnpm run build`
├── imgs/                    # imagens usadas nos slides
├── compose.yaml
├── Dockerfile
├── .dockerignore
├── marp-engine.cjs        # engine customizado do Marp (integração com Kroki)
└──  package.json
```

## Como rodar

```bash
docker compose up --build

# Ou podman compose up --build
```

Sempre que mudar `compose.yaml`, `Dockerfile` ou `package.json`, refaça
do zero:

```bash
docker compose down
docker compose up --build
```

Slides disponíveis em `http://localhost:8080/slide/md/<arquivo>.md`.

## Gerar PDF

```bash
docker compose run --rm marp --html --engine ./marp-engine.cjs --theme-set ./theme/minimalist.css -I slide/md/ -o slide/pdf/ --pdf --allow-local-files
```

## Portas

| Porta   | Serviço   | Pra que serve                                                                 |
| ------- | --------- | ------------------------------------------------------------------------------ |
| `8080`  | `marp`    | Servidor HTTP do `--server` — é onde você abre os slides no navegador.        |
| `37717` | `marp`    | WebSocket de live-reload do `--watch`. Não se acessa direto (dá "Upgrade Required" se tentar) — os `.html` gerados já se conectam nele sozinhos pra recarregar a página quando um `.md` muda. |
| `8000`  | `kroki`   | HTTP do Kroki. É essa porta que o `marp-engine.cjs` usa (via `KROKI_ENTRYPOINT`) pra montar a URL de cada diagrama Mermaid. |

## Serviços

- **marp**: serve os slides em modo `--server`, lendo `slide/md/` a partir
  da raiz do projeto.
- **kroki** / **mermaid**: Kroki self-hosted, publicado em
  `localhost:8000`. O `marp-engine.cjs` aponta pra essa URL via
  `KROKI_ENTRYPOINT`

## Erros já resolvidos (se voltarem, é regressão)

- `failed switching to "1000:1000"` → não colocar `USER marp` no fim do
  Dockerfile; o entrypoint da imagem precisa iniciar como root.
- `Not found processable Markdown file(s)` → `command:` do compose
  precisa ser só os *flags* do marp (sem `pnpm run dev`) — o entrypoint
  já invoca o binário direto.
- `Cannot find module '@marp-team/marp-core'` → precisa estar declarado
  como devDependency no `package.json` (não é só transitiva do
  `marp-cli`).
- `error 500` do Kroki / mermaid não renderiza → instância pública
  (`kroki.io`) é instável; por isso o self-hosted.
- Imagens não carregam em modo `--server` → servir a raiz do projeto
  (`.`) com `--allow-local-files`, não só `slide/md/`.