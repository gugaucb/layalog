# 03: Modal de Gerenciamento Centralizado do Histórico de Análises

**What to build:** Modal completo de gerenciamento de histórico acessível por botão dedicado (ex: ícone de relógio/histórico ou engrenagem ao lado do seletor). Exibe lista detalhada com cards/linhas de cada análise salva contendo nome do arquivo, data/hora, perfil associado, volume de linhas e métricas de erros. Cada item possui ações rápidas: "Carregar Análise" e "Excluir Análise" (com diálogo de confirmação).

**Blocked by:** 02-delete-active-analysis-with-confirmation

**Status:** ready-for-agent

- [x] Botão de abertura do modal de Histórico no cabeçalho (ao lado do select)
- [x] Modal moderno com tabela/lista de análises salvas, badges de perfil, status e métricas resumidas
- [x] Ação de carregar análise diretamente a partir da lista no modal
- [x] Ação de exclusão individual diretamente na lista com confirmação do usuário
- [x] Estado vazio elegante caso não haja análises gravadas
- [x] Atualização em tempo real da lista ao excluir ou importar novo log
