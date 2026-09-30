# Spec: Testes Automatizados E2E com Playwright para o LayaLog

## Objetivo
Criar uma suíte completa e robusta de testes ponta a ponta (E2E) com Playwright e Pytest para validar todas as funcionalidades, fluxos visuais, interações e resiliência do sistema LayaLog.

## Escopo dos Testes E2E
1. **Infraestrutura e Fixtures de Teste**:
   - Inicialização e encerramento automático do servidor FastAPI em porta dedicada/isolada.
   - Banco de dados SQLite isolado por sessão/teste (`/tmp` ou fixture temporária) pré-populado ou inicializado limpo.
   - Fixtures do Playwright (`page`, `context`, `browser`) com suporte a headless e headed/CDP.
   - Page Object / Helpers para ações comuns (upload, navegação de abas, filtros, criação de perfis, etc.).

2. **Fluxo de Upload e Análise de Logs**:
   - Upload de arquivo `.txt` ou `.log` via input/drag-and-drop.
   - Seleção de Gravity Profile no dropdown.
   - Validação da barra de progresso durante a análise.
   - Validação do botão de cancelamento de análise.
   - Renderização dos cards de métricas (Total de Linhas, Erros, Warnings, Avisos de Indisponibilidade).

3. **Visualizador de Logs (Log Viewer V2) e Filtros**:
   - Alternância entre abas de log level (ALL, ERROR, WARN, INFO).
   - Busca textual e highlight em tempo real.
   - Virtual scroll / renderização de grandes volumes de linhas sem travamento.
   - Expansão de detalhes e stack traces ao clicar na linha.

4. **Incidentes, Evidências da IA Laya e Exportação**:
   - Agrupamento inteligente de incidentes e badges de severidade (Baixa, Média, Crítica).
   - Abertura de modal/painel de evidências e auditoria da IA Laya.
   - Exportação de relatórios em JSON, Markdown e CSV, validando a integridade dos dados exportados.

5. **Gestão de Gravity Profiles**:
   - Listagem dos perfis do sistema (presets protegidos contra edição/exclusão).
   - Criação de novo perfil customizado com validação de campos.
   - Edição de perfil customizado existente.
   - Duplicação/clonagem de preset para custom profile.
   - Exclusão de perfil customizado.

6. **Histórico de Análises e Exclusão**:
   - Listagem de análises prévias com seus respectivos snapshots de perfil.
   - Carregamento de análise prévia direto para o visualizador/dashboard.
   - Exclusão de análise histórica com confirmação via modal.

7. **Execução e Relatórios Unificados**:
   - Execução via `pytest tests/e2e`.
   - Geração de relatório HTML e gravação de artefatos de diagnóstico.
