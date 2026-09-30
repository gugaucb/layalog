# ⚡ LayaLog — Observabilidade Semântica & Diagnóstico de Logs com IA

<p align="center">
  <strong>Transforme logs de servidor brutos em diagnósticos estruturados por IA, identificação de causa-raiz e observabilidade em tempo real.</strong>
</p>

<p align="center">
  <a href="README.md"><strong>🇺🇸 English</strong></a> •
  <a href="README.pt-BR.md"><strong>🇧🇷 Português</strong></a> •
  <a href="README.zh-CN.md"><strong>🇨🇳 简体中文</strong></a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://github.com/typesafe-ai/laya"><img src="https://img.shields.io/badge/Laya%20AI-System%20One-7928CA?logo=openai&logoColor=white" alt="Laya AI" /></a>
  <a href="https://driverjs.com/"><img src="https://img.shields.io/badge/Driver.js-Guia%20Interativo-FF5722?logo=javascript&logoColor=white" alt="Driver.js" /></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-Testes%20E2E%20Aprovados-2EAD33?logo=playwright&logoColor=white" alt="Playwright" /></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Pytest-100%25%20Aprovado-brightgreen?logo=pytest&logoColor=white" alt="Pytest" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## 📖 Visão Geral

O **LayaLog** é uma plataforma moderna de observabilidade e triagem inteligente projetada para equipes de engenharia de software e SRE que lidam com logs corporativos volumosos. Em vez de inspeções manuais exaustivas com `grep` em arquivos de texto de centenas de megabytes, o LayaLog reúne:

1. **Agrupamento Inteligente por Assinatura (Smart Clustering)**: Agrupa criptograficamente rastros de pilha repetidos, timestamps, UUIDs e assinaturas de log antes da inferência, reduzindo o consumo de tokens e chamadas de LLM em mais de 98%.
2. **Motor Laya AI (System One)**: Fornece julgamentos semânticos tipados (`Choice`, `Score`, `Noul`) para classificar causas-raiz, níveis de gravidade (Baixa, Média, Crítica) e recomendar planos de ação imediatos.
3. **Quiet UI & Arquitetura Master-Detail**: Painel de alta densidade visual, focado em clareza operacional e produtividade.
4. **Explorador de Log Virtualizado (60 FPS)**: Motor de renderização virtual em lotes com paginação assíncrona que processa milhões de linhas sem estresse de memória no navegador.
5. **Tour Interativo Integrado ([Driver.js](https://driverjs.com/))**: Guia passo a passo completo pelas principais funcionalidades do sistema.
6. **Internacionalização Completa (i18n)**: Troca instantânea em tempo real entre Inglês (`en`), Português do Brasil (`pt-br`) e Chinês Simplificado (`cn`).

---

## 📸 Screenshots

### 1. Perfis de Gravidade e Estúdio de Calibração
Crie, personalize, clone e gerencie perfis de calibração especializados por tecnologia (*Aplicações Web, Keycloak / IAM, Gateways de Pagamento, Bancos de Dados, Filas Assíncronas*) que guiam os critérios de severidade da IA Laya.

<p align="center">
  <img src="docs/assets/02-perfis-gravidade.png" alt="Modal de Perfis de Gravidade" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

### 2. Explorador de Log Virtualizado de Alto Desempenho
Visualizador de stream virtualizado com tipografia monoespelhada (*JetBrains Mono*), saltos diretos de linha e realce em tempo real de termos pesquisados.

<p align="center">
  <img src="docs/assets/03-explorador-logs.png" alt="Visualizador de Log Virtualizado" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

---

## 🎯 7 Perfis Nativos de Gravidade Laya AI

O LayaLog inclui 7 perfis nativos pré-calibrados prontos para ambientes de produção:

| Perfil | Foco de Domínio | Gatilho de Severidade Crítica (Nota 3) |
| :--- | :--- | :--- |
| **Aplicação Web / Monólito** | APIs REST, MVC, requisições HTTP | Falhas 5xx massivas, banco inacessível, quebra de checkout |
| **Keycloak / IAM / OAuth2** | SSO, Realms, LDAP, tokens JWT | Realm travado, pool de conexões do Keycloak esgotado, token forjado |
| **Gateway de Pagamentos** | Transações financeiras, PIX, cartões | Queda de transações, timeout no adquirente, quebra de idempotência |
| **Microsserviços / Event-Driven** | Kafka, RabbitMQ, gRPC | Overflow de Dead-letter queue, split-brain, consumer group travado |
| **Workers Assíncronos / Queues** | Celery, Redis, background jobs | Bloqueio de pipeline, estouro de memória (OOM), falha em lote de faturamento |
| **Bancos de Dados & Storage** | Postgres, MySQL, Redis, S3 | Esgotamento de conexões, lock wait timeout, corrupção de dados |
| **Edge / Gateway / Infraestrutura** | Nginx, Traefik, Envoy, DNS | Todos os upstreams fora do ar, certificado SSL expirado, saturação de rede |

---

## 🚀 Funcionalidades Principais

- **⚡ Streaming NDJSON com Cancelamento em Tempo Real**: Upload e processamento com barra de progresso e cancelamento via `AbortController`.
- **🎯 Calibração Dinâmica de Gravidade**: Ajuste de critérios semânticos a qualquer momento e duplicação rápida de perfis nativos.
- **🧭 Guia Interativo de Produto**: Construído com [Driver.js](https://driverjs.com/) para ambientar o usuário no primeiro acesso.
- **🌐 Motor de Internacionalização com 3 Idiomas**: Troca fluida entre Inglês, Português e Chinês sem recarregar a página.
- **📊 Painel de Métricas Operacionais (KPIs)**: Total de linhas, eventos classificados, criticidade alta e impacto na disponibilidade.
- **📝 Exportação Executiva em Markdown**: Relatórios detalhados estruturados prontos para anexar em issues ou documentações post-mortem.
- **💾 Histórico Persistido em SQLite**: Armazenamento leve e local com abertura imediata de análises passadas e exclusão física com confirmação.

---

## 🛠️ Instalação e Execução Rápida

### Pré-requisitos
- Python 3.9 ou superior
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### 1. Clonar o Repositório e Configurar o Ambiente

```bash
# Clonar repositório
git clone https://github.com/gugaucb/layalog.git
cd layalog

# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # No macOS/Linux
# ou: .venv\Scripts\activate  # No Windows

# Instalar dependências
pip install -r requirements.txt
pip install -e .
```

### 2. Iniciar o Servidor Web

```bash
python run.py
```

Abra o navegador e acesse: **[http://localhost:8100](http://localhost:8100)**

---

## 🧪 Testes Automatizados

O LayaLog conta com cobertura completa de testes unitários e testes ponta a ponta (E2E) no navegador utilizando **Playwright**:

```bash
# Executar suíte de testes backend (unitários + integração)
pytest

# Executar testes E2E automatizados com Playwright
python scripts/run_e2e_tests.py

# Executar em modo detalhado
pytest -v
```

---

## 🔌 Referência de Endpoints da API REST

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/analyze-stream` | Streaming NDJSON de upload de log e classificação em tempo real |
| `POST` | `/api/analyze` | Análise síncrona com retorno consolidado |
| `GET` | `/api/analyses` | Lista o histórico de análises salvas |
| `GET` | `/api/analyses/{id}` | Recupera os detalhes completos de uma análise |
| `GET` | `/api/analyses/{id}/lines` | Paginação sob demanda de linhas para o visualizador virtual |
| `GET` | `/api/analyses/{id}/export-md` | Download do relatório executivo em formato Markdown |
| `DELETE`| `/api/analyses/{id}` | Exclui definitivamente o registro de histórico e o arquivo do servidor |
| `GET` | `/api/profiles` | Lista todos os perfis de gravidade disponíveis |
| `POST` | `/api/profiles` | Cria um novo perfil customizado |
| `PUT` | `/api/profiles/{id}` | Atualiza um perfil customizado existente |
| `DELETE`| `/api/profiles/{id}` | Remove um perfil customizado |
| `POST` | `/api/profiles/{id}/clone` | Clona um perfil criando uma cópia editável |

---

## 📁 Arquitetura do Projeto

```
layalog/
├── layalog/
│   ├── app.py              # Servidor FastAPI, rotas REST e montagem da SPA
│   ├── classifier.py       # Motor de classificação semântica com Laya AI
│   ├── database.py         # Persistência SQLite e snapshots de auditoria
│   ├── exporter.py         # Gerador de relatórios executivos em Markdown
│   ├── models.py           # Esquemas e modelos de dados Pydantic
│   ├── parser.py           # Parsing de logs e agrupamento por assinatura
│   ├── profiles.py         # 7 Perfis nativos e CRUD de calibração
│   └── static/             # Frontend da aplicação (Single Page Application)
│       ├── css/v2.css      # Sistema de design Quiet UI e tema Driver.js
│       ├── js/i18n.js      # Dicionário de tradução multilíngue (EN, PT-BR, CN)
│       ├── js/tour.js      # Tour guiado interativo com Driver.js
│       ├── js/v2-app.js    # Controlador da aplicação e estado reativo
│       ├── js/v2-log-viewer.js # Motor de log virtualizado em 60 FPS
│       └── index.html      # Ponto de entrada HTML5 responsivo
├── tests/                  # Suíte de testes unitários e integração com pytest
│   ├── e2e/                # Testes automatizados de navegador com Playwright
├── docs/                   # Registros arquiteturais (ADRs) e assets visuais
├── pyproject.toml          # Configuração do pacote Python
├── requirements.txt        # Dependências do projeto
└── run.py                  # Script de inicialização (porta 8100)
```

---

## 🤝 Contribuição

Contribuições da comunidade são muito bem-vindas!

1. Crie um Fork do projeto (`git checkout -b feature/minha-feature`)
2. Faça commit das suas alterações (`git commit -m "feat: adiciona nova funcionalidade"`)
3. Garanta que todos os testes passem (`pytest && python scripts/run_e2e_tests.py`)
4. Envie para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request detalhado

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte [`LICENSE`](LICENSE) para mais informações.
