# 01: Estrutura HTML da Modal de Processamento com Canvas e Pastas

**What to build:** Atualizar a estrutura HTML da modal `#v2LoadingModal` nos templates `layalog/static/index.html` e `layalog/static/v2.html` para incluir a área do Canvas da animação Laya, cabeçalho de progresso, barra linear e os 3 cards/mini-pastas de contagem (Low, Medium, High).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] Incluir o `<canvas id="v2ProcessingCanvas">` dentro do container da modal `#v2LoadingModal`
- [x] Incluir os 3 cards de pastas/prioridades (`.processing-folders` com Low, Medium e High) com seus respectivos contadores
- [x] Preservar os elementos essenciais `#v2ProgressPercent`, `#v2ProgressFilename`, `#v2ProgressFill`, `#v2ProgressStatus` e `#v2BtnCancelProcess`
- [x] Sincronizar as alterações entre `layalog/static/index.html` e `layalog/static/v2.html`
