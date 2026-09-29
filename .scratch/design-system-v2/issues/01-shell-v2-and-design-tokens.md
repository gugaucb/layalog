# 01: Setup do Shell V2 e Design System Foundations

**What to build:**
Criar a fundação da interface V2 (`layalog/static/v2.html` e `layalog/static/css/v2.css`) e expor a rota `/v2` no backend FastAPI, mantendo a versão V1 intacta. Implementar o sistema completo de tokens CSS (Quiet UI, escala tipográfica Inter/JetBrains Mono, escala de espaçamento 4px-48px, raio de bordas e sombras sutis), estrutura de layout com Sidebar fixa de 224px, Topbar de 56px, navegação por seções (Overview, Triagem, Logs, Incidentes) e seletor/carregador de histórico de análises já integrado à API `/api/analyses`.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Rota `/v2` exposta no FastAPI retornando `v2.html` e versão atual (`/`) 100% preservada
- [x] Tokens CSS definidos no `:root` seguindo estritamente `layalog_design_system.md`
- [x] Sidebar fixa de 224px com logo, seletor de histórico, navegação (Overview, Triage, Logs) e link para alternar versões
- [x] Topbar de 56px com breadcrumb dinâmico, status de saúde da IA e botões compactos de ação
- [x] Responsividade básica e estrutura grid de 12 colunas pronta para os módulos
