# 03: Criar GitHub Action de publicação no Docker Hub

**What to build:** Workflow em `.github/workflows/docker-publish.yml` para compilar e enviar a imagem para `gugaucb/layalog`.

**Blocked by:** 01-dockerfile

**Status:** resolved

- [x] Workflow criado em .github/workflows/docker-publish.yml
- [x] Autenticação no Docker Hub via DOCKERHUB_USERNAME e DOCKERHUB_TOKEN
- [x] Build e push utilizando docker/build-push-action
- [x] Tags latest e SHA configuradas
