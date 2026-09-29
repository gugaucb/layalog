# 02: Corrigir schema Pydantic de criação (422) e formatação de erros

**What to build:** Tornar o campo `id` opcional no modelo `GravityProfile` para geração automática de ID no backend ao criar perfil sem erro 422, e formatar respostas de erro no frontend para nunca exibir [object Object].

**Blocked by:** None (can start immediately)

**Status:** done

- [x] `id: Optional[str] = None` no modelo Pydantic `GravityProfile`
- [x] Backend gera `custom-{uuid}` automaticamente se `id` não for fornecido no payload
- [x] Função `formatErrorMessage` no frontend descompactando arrays de erro de validação do FastAPI
- [x] Testes de criação sem ID no payload
