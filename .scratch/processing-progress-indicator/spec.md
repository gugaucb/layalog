# Especificação: Indicador de Progresso em Tempo Real na Modal de Processamento

## 1. Visão Geral
Durante o upload e análise de arquivos de log, a classificação semântica com o modelo Laya pode levar alguns segundos dependendo do número de incidentes únicos encontrados. Atualmente, o modal de carregamento exibe apenas um spinner com mensagem estática ("Classificando com Laya AI...").

O objetivo é transformar essa experiência exibindo:
- **Barra de progresso animada** com porcentagem numérica de 0% a 100%.
- **Status descritivo da etapa atual** (ex: *"Efetuando parsing de 13.620 linhas..."*, *"Classificando incidente 4 de 12 com Laya AI..."*, *"Salvando análise e gerando métricas..."*).

## 2. Arquitetura da Solução

### 2.1 Backend (Streaming com Server-Sent Events / SSE ou NDJSON)
- Endpoint `POST /api/analyze-stream` (ou `POST /api/analyze` com streaming):
  - Etapa 1: Parsing do arquivo e extração de blocos (`0% -> 15%`).
  - Etapa 2: Agrupamento por assinatura (`15% -> 25%`).
  - Etapa 3: Classificação semântica progressiva via `classifier.classify_incident` para cada incidente único (`25% -> 90%`), emitindo eventos de progresso:
    ```json
    {"type": "progress", "percent": 45, "message": "Classificando incidente 3 de 8 com Laya AI...", "current": 3, "total": 8}
    ```
  - Etapa 4: Cálculo de estatísticas e persistência em banco (`90% -> 100%`).
  - Evento final:
    ```json
    {"type": "complete", "data": { ... AnalysisRecord ... }}
    ```

### 2.2 Frontend (UI da Modal de Processamento)
- Atualizar `#loadingOverlay` no `index.html` e `style.css`:
  - Barra de progresso com gradiente cyan/indigo e brilho suave.
  - Indicador numérico em destaque (`45%`).
  - Mensagem de status dinâmica atualizada em tempo real conforme os eventos do backend chegam.
  - No `app.js`, consumir o stream de resposta e atualizar o DOM continuamente até a conclusão.

## 3. Lista de Tickets
1. **Ticket 01**: Implementar backend de análise com streaming progressivo (`/api/analyze-stream`).
2. **Ticket 02**: Atualizar modal de carregamento no frontend com barra de progresso, porcentagem e integração ao stream.
