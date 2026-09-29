# Ticket 02: Corrigir Sobreposição de Linhas no CSS do Visualizador de Log

**Status:** resolved  
**Type:** task  
**Feature:** infinite-scroll-log-viewer  
**Blocked by:** none  

## Descrição
Conforme evidenciado no screenshot do usuário, o texto do log no painel esquerdo está ilegível com caracteres empilhados uns sobre os outros. Isso ocorre porque o CSS aplicava `white-space: pre-wrap; word-break: break-all;` em elementos com altura fixa e posicionamento absoluto.

## Requisitos
1. No arquivo `layalog/static/css/style.css`:
   - Configurar `.log-viewer-container` com `overflow-x: auto` e `overflow-y: auto`.
   - Ajustar `.log-line` para usar `white-space: pre;` (ou altura flexível/independente por linha), garantindo que textos longos não quebrem verticalmente invadindo a linha de baixo.
   - Adicionar estilização elegante para barra de rolagem horizontal e vertical.
   - Assegurar contraste visual, alinhamento monospaçado e legibilidade cristalina em telas de qualquer resolução.

## Critérios de Aceite
- Nenhuma linha de texto se sobrepõe à linha anterior ou posterior.
- Linhas longas de stacktrace podem ser roladas horizontalmente sem quebrar o layout.
- Numeração de linhas permanece perfeitamente alinhada com o respectivo texto.
