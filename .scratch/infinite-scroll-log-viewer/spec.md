# Especificação: Visualizador de Log com Scroll Infinito, Chunking e Correção Visual

## 1. Problema Identificado
1. **Sobreposição de Texto (Impossível de ler)**: No visualizador de log (`virtual-scroll.js` e `style.css`), linhas longas sofrem quebra de linha (`white-space: pre-wrap`), ultrapassando a altura fixa de `22px`. Como os elementos tinham posição absoluta fixa em intervalos de 22px, linhas consecutivas se sobrepunham verticalmente criando o embaralhamento visual visível no screenshot.
2. **Estouro de Memória / Payload Gigante**: O endpoint de análise retornava todo o texto bruto do log (megabytes e milhares de linhas) de uma só vez no JSON, sobrecarregando a memória do navegador.

## 2. Nova Arquitetura & Requisitos

### 2.1 Backend (Chunking e Paginação de Linhas)
- Não trafegar mais o log completo no payload de análise (`/api/analyze` e `/api/analyses/{id}`).
- Criar endpoint dedicado: `GET /api/analyses/{id}/lines?start_line=1&limit=200` retornando as linhas solicitadas, `total_lines` e metadados.
- Persistir o log bruto no backend (SQLite) com indexação de linhas otimizada.

### 2.2 Frontend (Scroll Infinito & Correção de CSS)
- **Correção de CSS**: Utilizar `white-space: pre;` (sem wrapping forçado por cima de linhas seguintes) e barra de rolagem horizontal suave no visualizador, garantindo altura uniforme por linha e legibilidade perfeita.
- **Scroll Infinito / Windowing**: O cliente gerencia um buffer de linhas carregadas dinamicamente via AJAX ao rolar para cima ou para baixo.
- **Estratégia "Ir para a Linha"**: Ao clicar no botão de pular para a linha X:
  - Se a linha X já estiver no buffer, faz o scroll direto e highlight.
  - Se a linha X estiver fora do buffer atual, faz requisição ao backend para carregar a janela ao redor de X (ex: `start_line = max(1, X - 50)` com `limit = 200`), atualiza a view, posiciona o scroll na linha X e aplica o highlight animado.

## 3. Plano de Tickets
1. **Ticket 01**: Implementar endpoint de leitura de linhas paginadas no backend (`/api/analyses/{id}/lines`) e testes unitários.
2. **Ticket 02**: Corrigir estilos CSS do visualizador para eliminar sobreposição de texto e suportar rolagem horizontal/vertical limpa.
3. **Ticket 03**: Implementar scroll infinito dinâmico no visualizador frontend (`VirtualLogViewer` / `LogStreamViewer`).
4. **Ticket 04**: Atualizar a funcionalidade do botão "Ir para a linha" para buscar e renderizar a janela de linhas correspondente sob demanda.
