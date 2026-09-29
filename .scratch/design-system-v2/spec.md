# Spec: LayaLog Design System V2 (Clean Observability)

## Overview
Implementar uma nova interface (V2) para o LayaLog baseada estritamente nas especificações de `layalog_design_system.md` (Quiet UI, alta densidade com baixa sensação de poluição, paleta neutra com cores semânticas de severidade, tipografia Inter + JetBrains Mono, sidebar de 224px, painel Master-Detail e visualizador de logs de alta densidade).
A versão atual (`/` ou `index.html`) deve ser mantida intacta e acessível, enquanto a nova versão é servida em `/v2` (e `v2.html`) consumindo as mesmas APIs e dados do backend FastAPI.

## Architectural Decisions
1. **Coexistência de Versões**:
   - `layalog/static/index.html` e seus assets atuais continuam disponíveis para a versão V1.
   - `layalog/static/v2.html` (e assets dedicados `layalog/static/css/v2.css`, `layalog/static/js/v2-app.js`, `layalog/static/js/v2-log-viewer.js`) passam a implementar a versão V2.
   - Rota no FastAPI em `layalog/app.py` para `/v2` servindo `v2.html`.
   - Links discretos de alternância entre V1 e V2 no cabeçalho/sidebar.

2. **Design System & Quiet UI**:
   - CSS Tokens em `:root`: `--bg-app: #F5F7FA`, `--bg-sidebar: #F2F4F7`, `--bg-surface: #FFFFFF`, `--border-soft: #E6EAF0`, etc.
   - Cores semânticas para Severidade: Critical (`#DC2626` / `#EF4444` / `#FEF2F2`), High (`#EA580C` / `#F97316`), Medium (`#D97706` / `#F59E0B`), Low (`#2563EB` / `#3B82F6`), Success (`#059669` / `#10B981`).
   - Tipografia: Inter para interface, JetBrains Mono para logs e códigos.
   - Lucide Icons para iconografia técnica e consistente.
   - GSAP e CSS Transitions para microinterações elegantes.

3. **Visão de Triagem & Detalhes**:
   - Header com Breadcrumb e ações compactas.
   - Máximo de 4 KPI cards limpos.
   - Barra de filtros de severidade funcionais com badges com contagem.
   - Lista densa de incidentes com hover state e marcação de selecionado.
   - Detalhe Master/Detail com bloco nativo e calmo de *Laya AI Analysis* (`#F8FAFF`, sem neon), causa provável, impacto, sugestões e stack trace com salto direto para o log.

4. **Log Viewer de Alta Densidade**:
   - Scroll virtual integrado ao endpoint `/api/analyses/{id}/lines`.
   - Linhas de erro destacadas em `#FEF2F2` com borda lateral vermelha.
   - Destaque sutil de busca e salto direto via pills de incidentes.
