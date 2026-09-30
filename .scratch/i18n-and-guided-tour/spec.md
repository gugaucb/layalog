# Spec: Internacionalização i18n (EN, PT-BR, CN), Redesign do Topbar, Driver.js Tour e Documentação Multilíngue

## Objetivo
Implementar internacionalização (i18n) completa no LayaLog com suporte a 3 idiomas (`en` padrão, `pt-br`, `cn`), reformular a barra superior (topbar) para despoluir a interface e comportar o seletor de idiomas e botão de guia, adicionar um tour guiado interativo com a biblioteca [Driver.js](https://driverjs.com/) em todos os idiomas e prover documentação open source multilíngue (`README.md`, `README.pt-BR.md`, `README.zh-CN.md`).

---

## Escopo Funcional

### 1. Reformulação da Barra Superior (Topbar Layout)
- Agrupar e harmonizar os controles para evitar saturação visual.
- Estrutura limpa:
  - Esquerda: Breadcrumb contextual inteligente.
  - Centro: Busca Global (com atalho ⌘K).
  - Direita:
    - Botão "Importar Log" (destaque primário).
    - Seletor de Perfil + Botão de Configuração (unificado em dropdown/badge).
    - Seletor de Histórico + Botão de Gestão.
    - Seletor de Idioma (Toggle/Dropdown elegante com `EN`, `PT`, `CN` e bandeiras/ícones).
    - Botão de Ajuda / Tour Interativo (ícone ❓ / "Guia" / "Tour").
    - Botão de Exportação MD.

### 2. Sistema de Internacionalização i18n (`en`, `pt-br`, `cn`)
- Suporte a:
  - `en` (English - default)
  - `pt-br` (Português do Brasil)
  - `cn` (简体中文 - Chinese Simplified)
- Dicionário completo de strings cobrindo:
  - Topbar & Sidebar: Navegação, títulos, placeholders, badges.
  - KPIs: Labels, descrições, métricas.
  - Filtros: "All", "Critical", "High", "Medium", "Low" ("Todos", "Crítica", "Alta", "Média", "Baixa" / "全部", "严重", "高", "中", "低").
  - Modais: Gestão de Perfis de Gravidade, Histórico de Análises, Confirmação de Exclusão, Modal de Progresso/Cancelamento de Upload.
  - Painel de Detalhes da IA Laya: Resumos, recomendações, stacktrace, botões de cópia e salto de linha.
  - Mensagens de feedback, erros e toasts.
- Persistência da preferência em `localStorage.getItem('layalog_lang') || 'en'`.
- Troca de idioma em tempo real sem recarregar a página (`window.setLanguage(lang)`).

### 3. Tour Guiado Interativo com Driver.js
- Integração do CDN Driver.js (`driver.js.iife.js` e `driver.css`).
- Tour passo a passo:
  - Step 1: **Perfis de Gravidade** — Como a IA Laya calibra a severidade para cada stack técnica.
  - Step 2: **Importação de Logs** — Como enviar arquivos `.txt`/`.log`.
  - Step 3: **Painel de Métricas (KPIs)** — Contadores de linhas, erros e taxas de indisponibilidade.
  - Step 4: **Triagem de Erros & IA Laya** — Incidentes agrupados e diagnóstico inteligente com recomendações.
  - Step 5: **Explorador de Log Virtualizado** — Stream de alta performance e navegação rápida.
  - Step 6: **Histórico & Exportação** — Gestão de análises anteriores e relatórios em Markdown.
- Textos do tour e botões de navegação (Próximo/Next/下一步, Anterior/Prev/上一步, Concluir/Done/完成) dinamicamente traduzidos conforme o idioma selecionado.

### 4. Documentação Open Source Multilíngue
- `README.md` (Inglês como padrão global).
- `README.pt-BR.md` (Português).
- `README.zh-CN.md` (Chinês).
- Badges no topo permitindo alternar entre os arquivos de README com 1 clique.
- Seções completas: Visão Geral, Diferenciais da IA Laya, Demonstração, Instalação Rápida, Guia de Uso, Arquitetura, Perfis de Gravidade, Testes Automatizados E2E e Contribuição.

### 5. Testes E2E com Playwright
- Testes cobrindo troca dinâmica de idioma e verificação de strings renderizadas.
- Testes acionando e percorrendo o tour do Driver.js.
- Garantia de que a suíte completa de testes continua 100% verde.
