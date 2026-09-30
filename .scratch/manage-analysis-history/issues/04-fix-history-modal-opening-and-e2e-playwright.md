# 04: Correção de abertura da modal de histórico e testes E2E Playwright

**What to build:** Correção de erro de sintaxe no JavaScript do cliente (`v2-app.js`) que bloqueava o registro do listener do botão "Gerenciar Histórico". Implementação de suporte a fechamento por clique no backdrop e tecla `Escape`. Adição de `pointer-events: none` aos ícones SVG internos de botões. Validação ponta a ponta com simulação do Playwright no navegador real.

**Blocked by:** 03-centralized-history-management-modal

**Status:** ready-for-agent

- [x] Corrigido fechamento da iteração `navBtns.forEach` em `v2-app.js`
- [x] Adicionado fechamento da modal por clique no backdrop e tecla `Escape`
- [x] Adicionado `pointer-events: none` para filhos de `.btn` no CSS para evitar perda de evento de clique em SVGs
- [x] Simulação de teste E2E com Playwright executada com sucesso validando abertura, visibilidade, listagem e fechamento da modal
