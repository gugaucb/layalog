# Relatório de Análise de Log - LayaLog

**Arquivo Analisado:** `log1.txt`  
**Data da Análise:** 2026-09-28 14:30:00  
**Total de Linhas:** 13.620  
**Total de Erros Detectados:** 48  
**Índice de Indisponibilidade Estimado:** 33.3%  

---

## 1. Sumário Executivo

| Métrica | Valor |
|---|---|
| **Erros Críticos (Severidade Alta)** | 16 |
| **Erros Médios (Severidade Média)** | 24 |
| **Erros Baixos / Avisos** | 8 |
| **Setor Mais Impactado** | Integrações Externas / E-mail / APIs |
| **Impacto em Disponibilidade** | Parcial (Falhas em notificações e autenticação) |

### Distribuição por Setor
- **Integrações Externas / E-mail / APIs:** 22 ocorrências (45.8%)
- **Negócio / Regras da Aplicação:** 14 ocorrências (29.2%)
- **Autenticação / Segurança:** 8 ocorrências (16.7%)
- **Infraestrutura / Banco de Dados:** 4 ocorrências (8.3%)

---

## 2. Erros Priorizados por Criticidade

### [CRÍTICO] #1 - The Response content must be a string or object implementing __toString()
- **Setor Responsável:** Negócio / Regras da Aplicação
- **Tipo de Falha:** Null Pointer / Type Error
- **Gravidade:** 3 / 3 (Crítica)
- **Causa Indisponibilidade do Sistema:** Sim
- **Total de Ocorrências:** 12 vezes
- **Primeira Ocorrência:** Linha 6 (`2026-09-25 09:26:32`)
- **Linhas no Log:** 6, 45, 120, 310...
- **Resumo Técnico:** A rota de API retornou um objeto `stdClass` bruto não serializado para a resposta HTTP Symfony/Laravel, gerando erro HTTP 500 para o usuário final durante a autenticação/requisição Keycloak.

#### Trecho do Log / Stacktrace:
```
[2026-09-25 09:26:32] production.ERROR: The Response content must be a string or object implementing __toString(), "object" given. {"userId":"MA8500075","email":"taiana.ribeiro@trf1.jus.br","exception":"[object] (UnexpectedValueException(code: 0): The Response content must be a string or object implementing __toString(), \"object\" given. at /var/www/html/sistema/eavs-api/vendor/symfony/http-foundation/Response.php:399)
[stacktrace]
#0 /var/www/html/sistema/eavs-api/vendor/laravel/framework/src/Illuminate/Http/Response.php(45): Symfony\Component\HttpFoundation\Response->setContent(Object(stdClass))
#1 /var/www/html/sistema/eavs-api/vendor/symfony/http-foundation/Response.php(206): Illuminate\Http\Response->setContent(Object(stdClass))
```

---

### [MÉDIO] #2 - Erro no envio de e-mail e/ou na criação da notificação: Trying to get property 'seccional_id' of non-object
- **Setor Responsável:** Integrações Externas / E-mail / APIs
- **Tipo de Falha:** Null Pointer / Type Error
- **Gravidade:** 2 / 3 (Média)
- **Causa Indisponibilidade do Sistema:** Não (Degradação de Notificação)
- **Total de Ocorrências:** 28 vezes
- **Primeira Ocorrência:** Linha 1 (`2026-09-25 00:01:13`)
- **Linhas no Log:** 1, 2, 3, 4, 5...
- **Resumo Técnico:** Tentativa de acesso à propriedade `seccional_id` em um objeto nulo ao disparar notificação por e-mail em background/fila. Não derruba o sistema principal, mas impede a entrega de mensagens.

#### Trecho do Log / Stacktrace:
```
[2026-09-25 00:01:13] production.ERROR: Erro no envio de e-mail e/ou na criação da notificação: Trying to get property 'seccional_id' of non-object
```

---

## 3. Recomendações de Ação

1. **Correção Imediata (API Response):** Tratar o retorno dos handlers e middlewares no repositório `eavs-api` para garantir retorno em JSON (`response()->json(...)`) em vez de instâncias diretas de `stdClass`.
2. **Correção de Notificação (E-mail):** Adicionar verificação de nulidade (`$usuario->seccional_id ?? null`) antes do disparo das notificações por e-mail.
3. **Monitoramento:** Configurar alertas em tempo real para erros 500 originados na camada de autenticação Keycloak.
