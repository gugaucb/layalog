# 04: Validação E2E e Testes Visuais de Não-Regressão

**What to build:** Executar a suíte de testes automatizados E2E Playwright (`tests/e2e/test_upload_flow_e2e.py` e testes de fluxo completo) para garantir que a nova modal e a animação do canvas funcionem perfeitamente sem quebrar nenhum fluxo existente.

**Blocked by:** 03-canvas-animation-engine.md

**Status:** ready-for-agent

- [x] Executar testes E2E e smoke tests com Playwright para validar integridade da modal
- [x] Validar que a estrutura de classes e elementos da modal `#v2LoadingModal` e cancelamento foram preservados
- [x] Validar que o loop de renderização do Canvas Canvas 2D e partículas funciona com ciclo de vida limpo e sem memory leaks
