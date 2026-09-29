# 01: Promover interface V2 para rota raiz / e descontinuar V1

**What to build:** A rota raiz `/` serve a interface moderna LayaLog diretamente, eliminando o toggle legado da V1 e mantendo `/v2` como redirecionamento suave para `/`.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Acessar `/` entrega a interface moderna LayaLog
- [x] Rota `/v2` redireciona para `/`
- [x] Remoção do link de rodapé da sidebar para "Versão Clássica (V1)"
- [x] Testes de rotas atualizados e passando
