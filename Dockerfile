# Dockerfile
#
# Baseado na imagem oficial do Marp CLI: já vem com Chromium configurado
# (necessário para o --pdf), evitando ter que lidar com sandbox/libs na mão.
# Compatível com `docker build` e `podman build` sem flags extras.

FROM marpteam/marp-cli:latest

USER root
WORKDIR /home/marp/app

COPY package.json pnpm-lock.yaml* .npmrc* ./
RUN npm install -g pnpm@11 \
    && pnpm install --frozen-lockfile

COPY . .