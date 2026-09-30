# 02: Testes E2E do Fluxo de Upload, Progresso e Cancelamento de Logs

**What to build:** Testes E2E automatizados cobrindo toda a jornada de upload de arquivos de log, seleção de Gravity Profile, feedback visual da barra de progresso / status de processamento, mecanismo de cancelamento de análise e renderização inicial do dashboard com os cards de métricas.

**Blocked by:** 01 (Setup do ambiente de testes E2E com Playwright & Pytest Fixtures)

**Status:** ready-for-agent

- [x] Teste de upload de arquivo `.txt`/`.log` selecionando perfil default e verificando início de processamento
- [x] Teste de verificação da barra de progresso e transição de estados (Parsing -> Classificação -> Concluído)
- [x] Teste de cancelamento de upload/análise via botão de cancelar e retorno ao estado inicial
- [x] Teste de verificação dos cards de resumo estatístico (total de linhas, erros, avisos e indisponibilidade)

