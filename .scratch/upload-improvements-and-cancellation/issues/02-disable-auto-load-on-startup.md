# Ticket 02: Desativar Auto-Carregamento na Inicialização da Aplicação

**Status:** resolved  
**Type:** task  
**Feature:** upload-improvements-and-cancellation  
**Blocked by:** none  

## Descrição
Ao abrir a aplicação no navegador, o sistema tentava carregar automaticamente a primeira análise do histórico. Se a análise não existisse ou houvesse qualquer inconsistência, a tela congelava no modal de carregamento. A aplicação deve inicializar limpa e somente carregar quando o usuário explicitamente selecionar no dropdown ou fizer upload.

## Requisitos
1. No arquivo `layalog/static/js/app.js`:
   - Remover a chamada automática `loadAnalysisById(items[0].id)` de dentro de `loadHistory()`.
   - Inicializar a interface no estado vazio (painel de log com mensagem de orientação e cards zerados).
   - Adicionar tratamento de erro seguro no `loadAnalysisById` para que, caso a análise não seja encontrada (HTTP 404), exiba um aviso elegante, remova o item inválido do dropdown e feche o overlay sem travar.

## Critérios de Aceite
- Ao abrir `http://localhost:8100/`, a página carrega instantaneamente sem modal de loading ou tentativas automáticas de carregar logs antigos.
- O dropdown de histórico exibe `-- Histórico de Análises --` como opção selecionada padrão.
- Selecionar uma análise no dropdown carrega os dados normalmente.
