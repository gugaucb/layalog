# 03: Motor de Animação Canvas e Gerenciamento de Lifecycle

**What to build:** Implementar o motor de animação Canvas 2D em `layalog/static/js/v2-app.js` baseado em `log/exemplo_animation.html`, adaptado para o tamanho reduzido da modal, com Orb central "LAYA", física de curvas de Bézier em direção às 3 pastas, contadores em tempo real e controle estrito de ciclo de vida (`startProcessingAnimation()` e `stopProcessingAnimation()`).

**Blocked by:** 02-modal-css-and-responsive-styling.md

**Status:** ready-for-agent

- [x] Adaptar a classe `DocParticle` e função `drawOrb` para dimensões relativas ao canvas da modal (~540x220px)
- [x] Centralizar e posicionar os alvos das 3 pastas dinamicamente conforme a largura do canvas
- [x] Conectar o loop de `requestAnimationFrame` ao método `showLoadingOverlay()` e cancelamento via `cancelAnimationFrame` em `hideLoadingOverlay()` e no botão Cancelar
- [x] Resetar e atualizar contadores de itens Low, Medium e High dinamicamente
- [x] Prevenir memory leaks e uso de CPU quando a modal estiver oculta
