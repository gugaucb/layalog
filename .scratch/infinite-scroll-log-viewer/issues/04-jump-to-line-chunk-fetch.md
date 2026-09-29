# Ticket 04: Atualizar Funcionalidade "Ir para a Linha" com Carregamento sob Demanda

**Status:** resolved  
**Type:** task  
**Feature:** infinite-scroll-log-viewer  
**Blocked by:** 01, 03  

## Descrição
Ao clicar em "Ir para a Linha X" (seja no card do erro ou no modal de detalhes), a linha X pode não estar presente no buffer inicial carregado pelo scroll infinito. A funcionalidade deve ser adaptada para buscar a janela de linhas correspondente no backend se necessário, posicionar o scroll e aplicar o realce.

## Requisitos
1. No método `scrollToLine(lineNumber)` do visualizador:
   - Verificar se a linha `lineNumber` está no cache local de linhas.
   - Caso não esteja, disparar requisição para `/api/analyses/{id}/lines?start_line=max(1, lineNumber - 50)&limit=200`.
   - Atualizar o buffer renderizado com o bloco recuperado.
   - Posicionar a rolagem suave na linha `lineNumber`.
   - Aplicar a animação de realce (highlight temporário) na linha de erro.
2. Integrar os botões de salto tanto na lista de incidentes (lado direito) quanto nos pills de linhas do modal.

## Critérios de Aceite
- Clicar em "Ir para Linha 126" ou "Linha 13500" carrega o trecho sob demanda instantaneamente e destaca a linha com sucesso.
- O highlight temporário pisca suavemente na linha selecionada.
