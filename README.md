# LayaLog - Inteligência e Classificação de Logs com IA

**LayaLog** é uma plataforma moderna e inteligente para análise, classificação semântica e visualização interativa de arquivos de log de sistemas corporativos. Utilizando a biblioteca **Laya** (`Router`), o LayaLog classifica automaticamente incidentes por **setor responsável**, **tipo de falha**, **nível de gravidade** e **impacto em disponibilidade do sistema**.

---

## 🚀 Funcionalidades

1. **Importação e Parsing Inteligente de Logs**:
   - Suporte nativo a logs no formato Monolog / Laravel e tracebacks genéricos.
   - Detecção precisa de linhas, timestamps, contexto e stacktraces multilinhas.
   - Agrupamento automático de ocorrências por assinatura de erro (deduplicação eficiente).

2. **Classificação Semântica com Laya AI**:
   - **Setor Responsável** (*Choice*): Infraestrutura / Banco de Dados, Autenticação / Segurança, Negócio / Regras da Aplicação, Integrações Externas / E-mail / APIs.
   - **Tipo de Falha** (*Choice*): Database Error, Null Pointer / Type Error, Network / Timeout, Permission / Auth, HTTP 5xx, Outros.
   - **Gravidade** (*Score*): Baixa (1), Média (2) ou Crítica (3).
   - **Impacto em Disponibilidade** (*Noul*): Avaliação se a falha acarreta indisponibilidade para os usuários finais.

3. **Dashboard Executivo & Gráficos**:
   - Indicadores numéricos em tempo real (Total de Linhas, Total de Erros, Erros Críticos, Setor Mais Afetado, Taxa de Indisponibilidade %).
   - Gráficos interativos com Chart.js: Distribuição por Gravidade (Donut), Volume por Setor (Barras Horizontais) e Principais Tipos de Falha.

4. **Split View com Virtual Scrolling & Sincronização**:
   - **Painel Esquerdo**: Visualizador de log de alta performance capaz de renderizar arquivos com dezenas de milhares de linhas a 60fps sem travar o navegador, com busca instantânea e numeração de linhas.
   - **Painel Direito**: Lista de cards de incidentes ordenados por gravidade e frequência.
   - **Navegação Sincronizada**: Clique em *"Ir para Linha"* para realizar scroll suave com destaque luminoso animado na linha correspondente no log.

5. **Modal de Detalhes Completos**:
   - Classificação semântica, resumo técnico, recomendações de ação personalizadas, stacktrace formatado e lista de todas as linhas de ocorrência para salto direto.

6. **Histórico Persistido em SQLite**:
   - Armazenamento local leve das análises processadas para alternância rápida no menu superior.

7. **Exportação de Relatório Executivo em Markdown**:
   - Exportação no padrão definido no modelo [exemplo-log.md](file:///Users/gustavoluiscosta/Downloads/projetos/LayaLog/exemplo-log.md).

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.9+
- Ambiente virtual (`venv`)

### 1. Clonar e Configurar Ambiente
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # No Linux/macOS
# ou: .venv\Scripts\activate  # No Windows

# Instalar dependências
pip install -r requirements.txt
pip install -e .
```

### 2. Iniciar o Servidor
```bash
python run.py
```
Acesse a aplicação no navegador em: **[http://localhost:8000](http://localhost:8000)**

---

## 🧪 Testes Automatizados

Para rodar a suíte de testes com `pytest`:
```bash
pytest
```

---

## 📁 Estrutura do Projeto

```
LayaLog/
├── layalog/
│   ├── app.py              # API FastAPI e montagem da SPA
│   ├── classifier.py       # Motor de classificação semântica com Laya
│   ├── database.py         # Persistência SQLite
│   ├── exporter.py         # Gerador de relatórios Markdown
│   ├── models.py           # Modelos de dados Pydantic
│   ├── parser.py           # Parser de logs e agrupamento por assinatura
│   └── static/             # Frontend da aplicação
│       ├── css/style.css
│       ├── js/app.js
│       ├── js/virtual-scroll.js
│       └── index.html
├── log/
│   └── log1.txt            # Log de exemplo para teste
├── tests/                  # Testes unitários e de integração
├── exemplo-log.md          # Modelo padrão de exportação Markdown
├── pyproject.toml          # Configuração de pacote Python
├── requirements.txt        # Dependências do projeto
└── run.py                  # Script de inicialização
```
