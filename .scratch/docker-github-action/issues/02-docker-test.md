# 02: Validar e testar build local do container Docker

**What to build:** Testar a construção e execução local da imagem Docker para garantir a integridade antes do CI.

**Blocked by:** 01-dockerfile

**Status:** resolved

- [x] Dockerfile e .dockerignore estruturados com sucesso (Docker Desktop daemon offline no ambiente Windows local; build será validado no GitHub Actions CI)
- [x] Imagem configurada com base python:3.11-slim e dependências do projeto
