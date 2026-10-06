# Spec: GitHub Action para Docker Hub (gugaucb/layalog)

## Objetivo
Criar a configuração de build e empacotamento Docker da aplicação LayaLog e automatizar a publicação da imagem no Docker Hub através do GitHub Actions no repositório `gugaucb/layalog`.

## Requisitos
1. **Dockerfile & .dockerignore:**
   - Imagem base Python slim (`python:3.11-slim` ou similar).
   - Instalação de dependências via `pyproject.toml` / `requirements.txt`.
   - Exposição da porta `8100`.
   - Execução do serviço usando `python run.py` ou `uvicorn layalog.app:app`.
2. **GitHub Actions Workflow:**
   - Localização: `.github/workflows/docker-publish.yml`.
   - Disparador: `push` na branch `main` ou `master`.
   - Autenticação Docker Hub utilizando os secrets `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`.
   - Tags publicadas: `latest` e `${{ github.sha }}` no repositório `gugaucb/layalog`.
3. **Git & Deploy Key:**
   - Configuração do controle de versão com chave SSH Deploy Key gerada.
   - Commit e push das alterações para o GitHub.
