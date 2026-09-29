# 02: Visão de Triagem: KPIs e Lista de Incidentes com Micro-animações

**What to build:**
Implementar a visualização de Triagem (`Triage View`) na V2. Deve conter até 4 KPI cards limpos (Total de Linhas, Total de Erros, Erros Críticos, Taxa de Indisponibilidade) com números grandes e tipografia forte, barra de filtros por severidade com contadores interativos (Critical, High, Medium, Low) e lista de erros/incidentes de alta densidade visual. Cada item deve apresentar título humano em destaque, contexto técnico em linha secundária, badges semânticos discretos e microinterações de hover e seleção animadas via GSAP/CSS.

**Blocked by:** 01: Setup do Shell V2 e Design System Foundations

**Status:** resolved

- [x] Até 4 KPI cards estruturados e atualizados com os dados de `stats` da análise
- [x] Barra horizontal de filtros rápidos por severidade com contadores atualizados em tempo real
- [x] Lista compacta de incidentes (densidade confortável para scan rápido, sem poluição)
- [x] Micro-animações de ordenação, hover e seleção de itens (GSAP Flip / CSS transitions)
- [x] Campo de busca rápida com atalho de teclado `⌘K` / `Ctrl+K`
