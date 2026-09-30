# 05: Testes Automatizados Playwright E2E para i18n e Guided Tour

**What to build:** Testes E2E com Playwright cobrindo a alternância dinâmica entre os 3 idiomas (`en`, `pt-br`, `cn`), persistência no `localStorage`, tradução de componentes e execução do tour interativo com Driver.js.

**Blocked by:** 02 (Sistema de Internacionalização i18n), 03 (Integração do Driver.js e Tour Guiado)

**Status:** ready-for-agent

- [ ] Teste E2E em `tests/e2e/test_i18n_and_tour_e2e.py` validando o idioma padrão `en` e comutação para `pt-br` e `cn`
- [ ] Teste E2E verificando persistência do idioma após reload
- [ ] Teste E2E disparando o tour do Driver.js via `#v2TourBtn`, avançando pelos steps e concluindo o walkthrough
- [ ] Validação de compatibilidade com os testes E2E existentes
