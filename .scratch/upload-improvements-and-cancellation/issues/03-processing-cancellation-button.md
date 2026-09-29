# Ticket 03: Adicionar Botão de Cancelamento no Modal de Processamento

**Status:** resolved  
**Type:** task  
**Feature:** upload-improvements-and-cancellation  
**Blocked by:** none  

## Descrição
Adicionar um botão de cancelamento visível e interativo no modal de progresso de processamento, permitindo que o usuário aborte a operação a qualquer momento sem precisar recarregar a página.

## Requisitos
1. No `layalog/static/index.html`:
   - Adicionar botão `<button id="btnCancelProcess" class="btn btn-secondary btn-sm" ...>❌ Cancelar</button>` no footer da modal de progresso.
2. No `layalog/static/js/app.js`:
   - Criar uma instância global de `currentAbortController = new AbortController()` antes de iniciar o `fetch("/api/analyze-stream", { signal: currentAbortController.signal, ... })`.
   - No evento de clique em `#btnCancelProcess`, executar `currentAbortController.abort()`, fechar a modal de progresso (`#loadingOverlay.style.display = "none"`), resetar o input de arquivo e restaurar o estado da UI.
   - Capturar `AbortError` no `catch` sem exibir alerta de erro desnecessário, mostrando uma notificação suave de cancelamento.

## Critérios de Aceite
- Durante o processamento de um arquivo, o usuário pode clicar em "Cancelar".
- A requisição é abortada imediatamente no navegador e a modal fecha sem travar a tela.
- O usuário pode enviar outro arquivo em seguida normalmente.
