# 03: Desacoplamento da Carga e Fechamento Confiável da Modal

**What to build:** Fechar a modal de progresso assim que o processamento do stream receber os dados finais (`hideLoadingOverlay()`), garantindo parsing do stream resiliente contra buffers remanescentes e orquestrando o carregamento da visualização via `requestAnimationFrame` sem bloquear a UI.

**Blocked by:** 02-chunked-incident-rendering-and-animation-limit.md

**Status:** closed

- [x] Tratar qualquer resto no `buffer` de NDJSON após término da stream (`done: true`)
- [x] Ocultar a modal de carregamento antes de disparar o parse pesado e renderização
- [x] Orquestrar atualização assíncrona do log viewer e painel de incidentes
- [x] Tratar erros de evento `error` propagando corretamente para o catch externo
