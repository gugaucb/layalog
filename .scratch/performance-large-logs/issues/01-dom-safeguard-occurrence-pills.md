# 01: DOM Safeguard para Pílulas de Ocorrências em Detalhes

**What to build:** Quando um incidente possui centenas ou milhares de ocorrências (`inc.lines`), limitar a renderização inicial a 50 pílulas de salto de linha com botão para carregar o restante ou campo de busca rápido, evitando que o navegador aloque milhares de elementos DOM de uma vez e congele a UI.

**Blocked by:** None (can start immediately)

**Status:** closed

- [x] Limitar exibição de `inc.lines` a 50 itens inicialmente
- [x] Fornecer botão expansor `+N ocorrências restantes` quando exceder 50
- [x] Garantir navegação e salto para linhas no visualizador virtual
