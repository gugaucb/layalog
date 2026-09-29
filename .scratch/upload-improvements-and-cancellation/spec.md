# Especificação: Armazenamento em Pasta de Upload, Cancelamento de Processamento e Desativação do Auto-Load

## 1. Problemas Identificados
1. **Auto-carregamento Indesejado ao Iniciar**: Ao abrir a aplicação, o JavaScript tentava carregar automaticamente a última análise do histórico (`loadAnalysisById(items[0].id)`). Caso o ID estivesse corrompido, vazio ou inconsistente, o sistema entrava em loop de carregamento e travava na tela. O comportamento correto é iniciar em estado neutro/limpo.
2. **Ausência de Cancelamento de Processamento**: Se o usuário enviar um arquivo por engano ou o processamento demorar, não havia como abortar a operação, deixando o modal de progresso preso.
3. **Armazenamento Volátil de Logs**: Os arquivos de upload não eram persistidos em disco em uma pasta estruturada (`uploads/`), dificultando a integridade dos dados e auditoria.

## 2. Requisitos e Soluções

### 2.1 Pasta de Upload de Arquivos (`uploads/`)
- Criar diretório dedicado `uploads/` na raiz do projeto (garantindo que exista na inicialização).
- Ao realizar upload via `/api/analyze-stream` ou `/api/analyze`, salvar o arquivo físico em `uploads/<analysis_id>_<safe_filename>`.
- Armazenar o caminho relativo do arquivo no banco de dados SQLite para leitura rápida de chunks diretamente do arquivo físico ou do banco.

### 2.2 Desativação do Auto-Carregamento na Inicialização
- No `layalog/static/js/app.js`, remover o trecho que chama `loadAnalysisById(items[0].id)` automaticamente no `loadHistory()`.
- A tela inicial deve exibir um estado vazio amigável ("Nenhum arquivo de log carregado. Importe um arquivo ou selecione do histórico.") até ação voluntária do usuário.

### 2.3 Botão de Cancelamento no Modal de Processamento
- Adicionar botão *"❌ Cancelar Processamento"* na modal de progresso (`#loadingOverlay`).
- No frontend, utilizar `AbortController` para cancelar a requisição `fetch` do stream instantaneamente quando o usuário clicar no botão de cancelamento.
- Fechar a modal, resetar o input de arquivo e restaurar a interface ao estado anterior.

## 3. Lista de Tickets
1. **Ticket 01**: Implementar armazenamento físico dos logs na pasta `uploads/` e vinculação no backend.
2. **Ticket 02**: Remover auto-carregamento no startup do frontend e tratar estado inicial limpo.
3. **Ticket 03**: Adicionar botão de cancelamento com `AbortController` na modal de processamento.
