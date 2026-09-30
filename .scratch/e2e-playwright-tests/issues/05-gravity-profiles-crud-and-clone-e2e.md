# 05: Testes E2E de Gestão de Gravity Profiles (CRUD & Clonagem)

**What to build:** Testes E2E para toda a aba de Gestão de Perfis de Gravidade: verificação de proteção dos presets nativos, criação de novos perfis com validação de campos obrigatórios, edição de perfis customizados, clonagem de preset e exclusão de perfil customizado.

**Blocked by:** 01 (Setup do ambiente de testes E2E com Playwright & Pytest Fixtures)

**Status:** ready-for-agent

- [x] Teste de navegação até a aba/seção de Perfis e conferência dos presets do sistema (sem botões de exclusão)
- [x] Teste de criação de perfil customizado preenchendo nome, contexto e critérios de severidade (Baixa, Média, Crítica)
- [x] Teste de edição de perfil customizado e validação de persistência
- [x] Teste de duplicação/clonagem de preset para gerar novo perfil customizado
- [x] Teste de exclusão de perfil customizado e atualização imediata da lista

