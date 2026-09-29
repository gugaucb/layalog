# Especificação: Agrupamento Prévio e Otimização da Quantidade de Classificações no Laya

## 1. Problema Identificado
Durante o upload e análise de logs, o sistema realizava muitas inferências no Laya (ex: dezenas de avaliações individuais) para erros que representavam o mesmo problema raiz com pequenas variações dinâmicas (ex: JSON context com IDs de usuários diferentes, query strings `?offset=...`, timestamps ou URLs distintas).

Como a função de assinatura (`generate_signature`) não normalizava adequadamente payloads JSON embutidos e parâmetros de query, incidentes da mesma falha técnica recebiam hashes diferentes, gerando grupos duplicados e sobrecarregando o modelo Laya com avaliações redundantes.

## 2. Solução e Nova Arquitetura

### 2.1 Normalização Aprofundada e Extração de Padrão Raiz
- Extrair o **tipo da exceção** e a **mensagem central** descartando metadados dinâmicos:
  - Contextos JSON (`{"userId": "...", ...}`, `{"url": "...", ...}`).
  - Query strings e parâmetros codificados (`?payload=%5B...`, `?offset=...`, `?ano=...`).
  - Números de linha em stacktraces (`:113`, `:45`, etc.).
  - Variáveis de ambiente, IPs, hashes, tokens e caminhos dinâmicos.
- Identificar a primeira chamada de código de domínio no stacktrace (ignorando frames genéricos de framework como `Pipeline.php`, `Router.php`).

### 2.2 Agrupamento Prévio (Clusterização antes do Laya)
- Executar o agrupamento completo das entradas de log **antes** de qualquer chamada ao Laya.
- O pipeline de análise enviará ao Laya apenas as assinaturas únicas reais (reduzindo um log com milhares de ocorrências a apenas 3 ~ 8 avaliações essenciais).
- As métricas de frequência, lista de linhas e severidade multiplicam-se pelo total de ocorrências de cada cluster.

## 3. Lista de Tickets
1. **Ticket 01**: Implementar normalização avançada de logs e extração do padrão raiz de exceções (`layalog/parser.py`).
2. **Ticket 02**: Garantir pipeline de clusterização prévia antes da inferência no Laya com testes de agregação (`layalog/app.py` e `tests/test_parser.py`).
