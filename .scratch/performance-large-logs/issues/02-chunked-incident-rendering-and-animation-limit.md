# 02: Renderização Otimizada da Lista de Incidentes e Limitação de GSAP

**What to build:** Otimizar a renderização da lista de incidentes com renderização em lote (`DocumentFragment` / chunks com `requestAnimationFrame`) e desativar animações escalonadas (`stagger`) do GSAP quando a lista de incidentes for grande (>20 itens) para evitar overhead na thread de renderização.

**Blocked by:** 01-dom-safeguard-occurrence-pills.md

**Status:** closed

- [x] Usar DocumentFragment para inserção única no DOM
- [x] Desativar ou limitar stagger no GSAP quando `incidents.length > 20`
- [x] Manter filtros rápidos de gravidade e busca funcionais sem recriação pesada
