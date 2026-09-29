# Ticket 01: Implementar Normalização Avançada de Logs e Extração do Padrão Raiz

**Status:** resolved  
**Type:** task  
**Feature:** smart-error-grouping-before-classification  
**Blocked by:** none  

## Descrição
Melhorar a função de geração de assinatura de erro (`generate_signature`) para ignorar parâmetros dinâmicos (JSONs contextuais com IDs, query strings, URLs, números de linha, variáveis em queries) e identificar o padrão de falha raiz, unificando erros idênticos em uma única assinatura.

## Requisitos
1. No `layalog/parser.py`:
   - Tratar e normalizar payloads JSON anexados ao final da mensagem de erro (`{"userId": "...", ...}`).
   - Remover query strings de URLs (`?offset=0&ano=2027...`).
   - Normalizar stacktraces removendo números de linha específicos (`vendor/something.php:123` -> `vendor/something.php:<LINE>`).
   - Extrair e usar a mensagem de erro limpa principal + primeira linha relevante do stacktrace.
2. Adicionar testes unitários em `tests/test_parser.py` validando que erros idênticos com parâmetros diferentes geram a mesma assinatura.

## Critérios de Aceite
- Erros do mesmo tipo com IDs de usuário ou query strings diferentes geram a mesma assinatura SHA-256.
- Testes com `pytest` cobrindo logs Laravel, Guzzle e Oracle passando com 100% de sucesso.
