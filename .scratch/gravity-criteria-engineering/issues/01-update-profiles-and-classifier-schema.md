# 01: Engenharia de Critérios Observáveis e Schema de Gravidade no LayaClassifier

**What to build:**
Atualizar `layalog/profiles.py` com critérios operacionais baseados em evidências técnicas observáveis para todos os perfis embutidos. Atualizar a pergunta `gravidade` em `layalog/classifier.py` com as novas instruções e suporte a choices `LOW`, `MEDIUM`, `CRITICAL`, `Baixa`, `Média`, `Crítica`.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Critérios de todos os perfis em `layalog/profiles.py` reescritos com foco em evidências técnicas e exemplos concretos
- [x] `LayaClassifier.build_questions` configurado com novas instruções e choices (`LOW`, `MEDIUM`, `CRITICAL`)
- [x] `LayaClassifier.classify_incident` mapeia `LOW` -> 1, `MEDIUM` -> 2, `CRITICAL` -> 3 mantendo retrocompatibilidade

## Comments
Todos os 7 perfis embutidos foram atualizados em `layalog/profiles.py` com critérios ricos em evidências técnicas e exemplos concretos. O `LayaClassifier` foi configurado com as novas instruções e suporte a choices `LOW`, `MEDIUM`, `CRITICAL` e `Baixa`, `Média`, `Crítica`.
