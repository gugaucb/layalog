# 04: Log Viewer V2 de Alta Densidade com Destaque de Linhas Críticas

**What to build:**
Desenvolver o Log Viewer V2 (`layalog/static/js/v2-log-viewer.js`) com renderização de alta densidade e tipografia monoespacial (`JetBrains Mono`, 12.5px, line-height 20px). O visualizador consome a paginação em chunks de `/api/analyses/{id}/lines` com scroll virtual de alto desempenho, exibe colunas alinhadas para número de linha, timestamp e mensagem, destaca linhas de erro com background `#FEF2F2` e borda esquerda de 2px `#EF4444`, suporta busca em tempo real com realce de termos e integração com a funcionalidade de "Jump to Line" disparada a partir dos incidentes.

**Blocked by:** 01: Setup do Shell V2 e Design System Foundations

**Status:** resolved

- [x] Componente `V2LogViewer` estilizado de acordo com a seção 20 do design system
- [x] Renderização virtual fluida via `/api/analyses/{id}/lines` em chunks
- [x] Destaque elegante de linhas críticas (`#FEF2F2` + borda `#EF4444`) e warnings
- [x] Busca interna com highlights e contagem de correspondências
- [x] Método `scrollToLine` com animação suave e highlight temporário
