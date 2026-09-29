# Ticket 03: Implementar Scroll Infinito e Carregamento sob Demanda no Frontend

**Status:** resolved  
**Type:** task  
**Feature:** infinite-scroll-log-viewer  
**Blocked by:** 01, 02  

## Descrição
Substituir o carregamento estático do log por um mecanismo de **scroll infinito / windowing** que consome o endpoint `/api/analyses/{id}/lines` conforme o usuário rola o painel esquerdo.

## Requisitos
1. No arquivo `layalog/static/js/virtual-scroll.js` (ou `log-stream.js`):
   - Inicializar o visualizador com o número total de linhas (`total_lines`).
   - Carregar o chunk inicial de linhas (ex: linhas 1 a 200).
   - Detectar rolagem próxima às bordas superior/inferior para carregar novos blocos sob demanda via `fetch`.
   - Manter um cache em memória das linhas já buscadas na sessão.
   - Mostrar indicador discreto de carregamento enquanto novos blocos são recuperados.

## Critérios de Aceite
- Ao abrir uma análise de 13.000 linhas, o navegador carrega apenas o primeiro bloco inicial imediatamente.
- Rolar para baixo carrega automaticamente os blocos seguintes sem travar a interface.
- Busca no log / filtragem de texto rápida.
