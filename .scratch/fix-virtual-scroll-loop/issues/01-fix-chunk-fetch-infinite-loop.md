# 01: Fix Chunk Fetch Infinite Loop and White Screen

**What to build:**
Eliminar o loop infinito de requisições assíncronas no `v2-log-viewer.js` e `virtual-scroll.js`. Adicionar conjunto de controle de ranges solicitados (`attemptedRanges`), garantia de preenchimento de todas as chaves em `lineCache` mesmo quando o backend retorna array vazio, renderização segura via `requestAnimationFrame` e tratamento robusto no backend para linhas legadas.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `attemptedRanges` adicionado para prevenir requisições duplicadas do mesmo chunk
- [x] Todas as linhas do intervalo solicitado são marcadas no `lineCache` evitando chamadas recursivas
- [x] Renderização otimizada com `requestAnimationFrame` sem travar a thread principal
- [x] Visualizadores V1 e V2 protegidos contra telas brancas ou congelamento
