# 01: Botão de exclusão rápida direto nos itens da lista de perfis

**What to build:** Na barra lateral do modal de gerenciamento de perfis, cada perfil customizado exibe um botão de lixeira inline para exclusão imediata com confirmação, mantendo perfis nativos protegidos.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] Itens customizados na lista de perfis exibem botão inline 🗑️ de exclusão
- [x] Perfis nativos (is_builtin=True) não exibem botão de exclusão
- [x] Exclusão aciona confirmação, chama DELETE /api/profiles/{id} e atualiza lista e seletor principal
