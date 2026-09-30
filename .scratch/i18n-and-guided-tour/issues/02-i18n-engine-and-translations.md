# 02: Sistema de Internacionalização i18n (`en`, `pt-br`, `cn`) com Troca Dinâmica

**What to build:** Sistema completo de internacionalização frontend com dicionários para `en` (padrão), `pt-br` e `cn` (chinês simplificado), traduzindo todos os componentes da interface em tempo real e persistindo a preferência em `localStorage`.

**Blocked by:** 01 (Reformulação do Design da Barra Superior)

**Status:** resolved

- [x] Criação de `layalog/static/js/i18n.js` com dicionário completo de traduções para `en`, `pt-br` e `cn`
- [x] Implementação da função global `t(key)` e `setLanguage(lang)` atualizando o DOM dinamicamente
- [x] Tradução de todos os componentes da UI: Topbar, Sidebar, KPIs, Filtros, Cards de Incidentes, Modais (Perfis, Histórico, Confirmação, Progresso de Upload) e Painel de Evidências Laya AI
- [x] Persistência da preferência em `localStorage` (padrão: `en`)
