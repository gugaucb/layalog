# 03: Integração do Driver.js e Tour Guiado Interativo Multilíngue

**What to build:** Integração da biblioteca [Driver.js](https://driverjs.com/) (usando a skill `driverjs`), criando um tour passo a passo interativo que apresenta as principais funcionalidades do LayaLog nos 3 idiomas (`en`, `pt-br`, `cn`).

**Blocked by:** 02 (Sistema de Internacionalização i18n)

**Status:** resolved

- [x] Inclusão dos assets do Driver.js (`driver.js.iife.js` e `driver.css`) no HTML
- [x] Definição do tour interativo de 6 passos (Perfis de Gravidade, Upload de Log, KPIs, Triagem & Laya AI, Visualizador de Log, Histórico & Exportação)
- [x] Textos e botões de navegação do tour (Next, Prev, Done, Close) 100% integrados ao sistema de i18n
- [x] Acionamento do tour via botão na barra superior (`#v2TourBtn`) e opção de iniciar automaticamente no primeiro acesso
