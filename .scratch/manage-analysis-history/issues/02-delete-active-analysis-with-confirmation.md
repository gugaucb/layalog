# 02: Exclusão com confirmação segura e feedback visual

**What to build:** Modal de confirmação seguro no padrão Design System V2 ("Excluir Análise") alertando o usuário sobre a perda irreversível dos dados e do arquivo de log original. Botão de exclusão da análise ativa no cabeçalho. Ao confirmar, executa a requisição DELETE, limpa o visualizador de logs/dashboard se a análise excluída for a atual, exibe toast/notificação de sucesso e atualiza a listagem do seletor.

**Blocked by:** 01-complete-analysis-deletion-backend

**Status:** ready-for-agent

- [x] Modal de confirmação reutilizável ou específico estilizado com Design System V2 (com botão "Cancelar" e botão destrutivo "Excluir Definitivamente")
- [x] Botão de exclusão rápida (ícone de lixeira) no cabeçalho próximo ao seletor de histórico e botão de exportar
- [x] Validação de confirmação explícita antes de chamar a API
- [x] Limpeza do estado visual (dashboard e visualizador de logs) caso a análise removida seja a que estava em exibição
- [x] Recarregamento automático do seletor de histórico
