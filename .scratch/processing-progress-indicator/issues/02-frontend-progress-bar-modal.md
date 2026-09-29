# Ticket 02: Atualizar Modal de Carregamento com Barra de Progresso e Porcentagem

**Status:** resolved  
**Type:** task  
**Feature:** processing-progress-indicator  
**Blocked by:** 01  

## Descrição
Melhorar a modal/overlay de carregamento durante a importação e análise do log para exibir uma barra de progresso visual estilizada, porcentagem numérica e descrição da etapa atual.

## Requisitos
1. No `layalog/static/index.html`:
   - Atualizar a estrutura de `#loadingOverlay` com:
     - Título e spinner moderno.
     - Container da barra de progresso (`#progressBar` / `#progressFill`).
     - Rótulo de porcentagem (`#progressPercent`, ex: `45%`).
     - Mensagem de status detalhada (`#progressStatus`, ex: *"Classificando incidente 3 de 12..."*).
2. No `layalog/static/css/style.css`:
   - Estilização premium da barra de progresso (gradiente, bordas arredondadas, transição suave de largura, efeito de brilho e animação).
3. No `layalog/static/js/app.js`:
   - Atualizar a função `handleFileUpload` para consumir o stream de `/api/analyze-stream`.
   - Ler linha por linha do stream via `ReadableStreamDefaultReader`.
   - Atualizar dinamicamente a largura da barra (`width: X%`), o texto numérico (`X%`) e a mensagem de status.
   - Ao receber o evento `complete`, ocultar a modal e chamar `displayAnalysis(data)`.

## Critérios de Aceite
- Durante o upload de um log, a barra de progresso avança fluidamente de 0% a 100%.
- A porcentagem e a mensagem descritiva atualizam em tempo real na tela.
- Ao atingir 100%, a análise é renderizada normalmente.
