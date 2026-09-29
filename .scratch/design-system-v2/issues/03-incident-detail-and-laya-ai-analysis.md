# 03: Painel de Detalhes do Incidente e Bloco Nativo de Laya AI Analysis

**What to build:**
Construir o painel de detalhes do incidente (Master/Detail) com transição lateral deslizante e suave. O painel deve incorporar o bloco nativo de **Laya AI Analysis** com visual calmo e elegante (`#F8FAFF`, borda `#E3E8FF`, sem luzes neon ou gradientes excessivos), contendo Causa Provável, Impacto e Ação Sugerida. Deve exibir a lista de ocorrências com pills clicáveis para navegação direta de linha, bloco de stack trace com formatação JetBrains Mono, botão de cópia com feedback visual e botão de salto direto para a linha do log.

**Blocked by:** 02: Visão de Triagem: KPIs e Lista de Incidentes com Micro-animações

**Status:** resolved

- [x] Painel lateral de detalhes (Master/Detail) com abertura fluida e fechamento por `Esc` ou botão
- [x] Card estilizado de Laya AI Analysis respeitando a diretriz *Quiet UI*
- [x] Detalhamento de impacto, setor, tipo de falha e recomendação técnica
- [x] Lista de ocorrências em pills navegáveis e bloco de stack trace legível com botão de copiar
- [x] Ação primária clara para pular diretamente para a linha no visualizador de logs
