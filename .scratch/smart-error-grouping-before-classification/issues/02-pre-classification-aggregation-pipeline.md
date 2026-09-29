# Ticket 02: Pipeline de Clusterização Prévia e Otimização de Avaliações Laya

**Status:** resolved  
**Type:** task  
**Feature:** smart-error-grouping-before-classification  
**Blocked by:** 01-enhanced-error-normalization-and-clustering.md  

## Descrição
Garantir que a análise de logs agrupe e consolide todas as ocorrências de erro por assinatura raiz antes de disparar qualquer avaliação ou inferência no Laya. Dessa forma, se um log tiver 500 linhas de erro distribuídas em 4 causas raízes, o Laya realizará apenas 4 avaliações e não 500, multiplicando as ocorrências, severidade e linhas consolidadas nos relatórios.

## Requisitos
1. No pipeline de processamento (`layalog/app.py` / `layalog/parser.py`):
   - Agrupar e consolidar incidentes (`group_incidents`) primeiro em memória.
   - Enviar apenas o erro representativo de cada grupo consolidado para o Laya classificar.
   - Atualizar o progresso do modal informando a quantidade real de grupos únicos avaliados (ex: "Avaliando padrão 1 de 4").
   - Atribuir o resultado da classificação do grupo a todas as ocorrências associadas.
2. Criar testes unitários e de integração validando que o número de chamadas ao Laya é igual à quantidade de grupos únicos.

## Critérios de Aceite
- O Laya só é invocado para assinaturas únicas (grupos de erros).
- A contagem de ocorrências, linhas afetadas e dashboards refletem o total real de erros do log.
- O progresso no modal exibe a contagem de clusters/padrões únicos sendo avaliados.
- Testes automatizados cobrindo a agregação prévia com 100% de sucesso.
