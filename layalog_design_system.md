# LayaLog — Clean Observability Design System

> Design system inspirado nas melhores características visuais das referências fornecidas: dashboards claros, minimalistas, com alta legibilidade, navegação lateral discreta, cartões suaves, hierarquia tipográfica forte e uso contido de cor.

---

## 1. Objetivo visual

O LayaLog deve parecer uma ferramenta técnica premium, confiável e calma.

A interface precisa transmitir:

- **clareza antes de decoração**
- **alta densidade com baixa sensação de poluição**
- **hierarquia visual imediata**
- **cores usadas somente quando carregam significado**
- **componentes compactos, porém confortáveis**
- **sensação de produto SaaS moderno**
- **foco em diagnóstico, investigação e priorização**

A estética deve ficar entre:

- dashboard SaaS minimalista
- ferramenta profissional de observabilidade
- painel operacional para engenharia
- produto B2B premium

---

# 2. Princípios do sistema

## 2.1 Quiet UI

A interface base deve ser quase neutra.

Evitar:

- grandes blocos coloridos
- gradientes chamativos
- sombras pesadas
- bordas com alto contraste
- excesso de badges
- excesso de ícones
- muitos níveis de destaque simultâneos

A cor deve entrar principalmente para:

- criticidade
- status
- estados interativos
- indicadores de sucesso/erro
- ação primária

## 2.2 Progressive Disclosure

Mostrar primeiro somente o necessário.

```text
Erro
├─ título
├─ gravidade
├─ serviço
├─ ocorrências
└─ timestamp

Ao abrir:
├─ resumo
├─ causa provável
├─ impacto
├─ stack trace
├─ contexto
└─ ações
```

## 2.3 Data-first

Os dados são o elemento principal. A interface existe para facilitar leitura, comparação, triagem, investigação, priorização e ação.

## 2.4 Consistência espacial

Todos os módulos devem seguir o mesmo raio, borda, escala de espaçamento, escala tipográfica, lógica de estados e altura de controles.

---

# 3. Direção estética

## Características principais extraídas das referências

### Sidebar limpa

- largura fixa
- ícones pequenos
- texto compacto
- item ativo com fundo suave
- sem bordas pesadas
- grupos bem separados

### Conteúdo principal claro

- fundo geral levemente acinzentado
- cards brancos
- grande respiro entre blocos
- títulos pequenos e fortes

### Cards

- bordas muito suaves
- sombras discretas
- raio entre 10 e 14 px
- conteúdo alinhado em grid
- sem gradientes desnecessários

### Métricas

- número grande
- label pequena
- contexto secundário discreto

### Gráficos

- linhas finas
- eixos discretos
- grid quase invisível
- poucas cores
- destaque apenas no dado principal

### Listas

- linhas compactas
- avatar/ícone opcional
- descrição reduzida
- ação no hover
- separadores suaves

---

# 4. Foundations

## 4.1 Grid

Desktop principal:

```text
Sidebar: 224 px
Content: fluid
Max-width opcional: 1600 px
```

Grid recomendado:

```text
12 colunas
gutter: 24 px
page padding: 24 px
```

Para telas muito largas:

```text
page padding: 32 px
gutter: 24 px
```

## 4.2 Spacing Scale

| Token | Valor |
|---|---:|
| space-1 | 4 px |
| space-2 | 8 px |
| space-3 | 12 px |
| space-4 | 16 px |
| space-5 | 20 px |
| space-6 | 24 px |
| space-8 | 32 px |
| space-10 | 40 px |
| space-12 | 48 px |

Regra: não criar espaçamentos aleatórios como 13px, 18px, 27px etc.

---

# 5. Cores

## 5.1 Light Theme

```css
--bg-app: #F5F7FA;
--bg-sidebar: #F2F4F7;
--bg-surface: #FFFFFF;
--bg-surface-hover: #F8FAFC;
--bg-surface-selected: #EEF4FF;

--border-soft: #E6EAF0;
--border-default: #DDE3EA;
--border-strong: #CBD3DD;

--text-primary: #111827;
--text-secondary: #667085;
--text-muted: #98A2B3;
--text-disabled: #C2C8D0;

--brand-50: #EFF6FF;
--brand-100: #DBEAFE;
--brand-500: #3B82F6;
--brand-600: #2563EB;
--brand-700: #1D4ED8;
```

## 5.2 Semantic Colors

### Critical

```css
--critical-bg: #FEF2F2;
--critical-border: #FECACA;
--critical-text: #DC2626;
--critical-solid: #EF4444;
```

### High

```css
--high-bg: #FFF7ED;
--high-border: #FED7AA;
--high-text: #EA580C;
--high-solid: #F97316;
```

### Medium

```css
--medium-bg: #FFFBEB;
--medium-border: #FDE68A;
--medium-text: #D97706;
--medium-solid: #F59E0B;
```

### Low

```css
--low-bg: #EFF6FF;
--low-border: #BFDBFE;
--low-text: #2563EB;
--low-solid: #3B82F6;
```

### Success

```css
--success-bg: #ECFDF3;
--success-border: #A7F3D0;
--success-text: #059669;
--success-solid: #10B981;
```

### Info

```css
--info-bg: #F5F3FF;
--info-border: #DDD6FE;
--info-text: #7C3AED;
--info-solid: #8B5CF6;
```

---

# 6. Dark Theme opcional

```css
--bg-app: #0B0F17;
--bg-sidebar: #0E131D;
--bg-surface: #111827;
--bg-surface-hover: #161E2B;
--bg-surface-selected: #172554;

--border-soft: #1F2937;
--border-default: #273244;
--border-strong: #364152;

--text-primary: #F8FAFC;
--text-secondary: #A8B0BF;
--text-muted: #7C8798;
```

Não inverter todas as cores mecanicamente; manter a mesma hierarquia de contraste.

---

# 7. Tipografia

## Fonte principal

Preferência:

```text
Inter
```

Alternativas:

```text
Geist
SF Pro
Roboto
system-ui
```

Para logs/código:

```text
JetBrains Mono
IBM Plex Mono
SF Mono
```

## 7.1 Type Scale

```css
/* Display metric */
font-size: 32px;
line-height: 38px;
font-weight: 600;
letter-spacing: -0.02em;

/* Page title */
font-size: 22px;
line-height: 28px;
font-weight: 600;

/* Section title */
font-size: 15px;
line-height: 20px;
font-weight: 600;

/* Body */
font-size: 14px;
line-height: 20px;
font-weight: 400;

/* Small */
font-size: 12px;
line-height: 16px;
font-weight: 400;

/* Caption */
font-size: 11px;
line-height: 14px;
font-weight: 500;
```

Log:

```css
font-family: "JetBrains Mono", monospace;
font-size: 12.5px;
line-height: 20px;
```

---

# 8. Border Radius

```css
--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 14px;
--radius-pill: 999px;
```

Uso:

```text
inputs: 8px
buttons: 8px
cards: 12px
large panels: 14px
badges: pill
```

---

# 9. Shadows

Sombras devem ser quase invisíveis.

```css
--shadow-xs: 0 1px 2px rgba(16, 24, 40, 0.04);
--shadow-sm: 0 1px 3px rgba(16, 24, 40, 0.06), 0 1px 2px rgba(16, 24, 40, 0.03);
--shadow-md: 0 4px 10px rgba(16, 24, 40, 0.06);
```

Evitar sombras maiores em dashboards.

---

# 10. Sidebar

## Estrutura

```text
Logo
Workspace / contexto

Search

Principal
├─ Overview
├─ Triage
├─ Logs
├─ Services

Analysis
├─ Errors
├─ Patterns
├─ Incidents

System
├─ Settings
├─ Help
└─ Account
```

## Dimensões

```css
width: 224px;
padding: 16px 12px;
```

Item:

```css
height: 36px;
padding: 0 10px;
border-radius: 7px;
font-size: 13px;
```

Estado ativo:

```css
background: #FFFFFF;
box-shadow: 0 1px 2px rgba(16, 24, 40, .05);
color: var(--text-primary);
```

---

# 11. Topbar

```css
height: 56px;
```

Conteúdo:

```text
breadcrumb / título                     contexto  ações
```

Exemplo:

```text
Logs / production / log1.txt        Importar   Exportar   •••
```

Evitar barra cheia de botões, botões gigantes e múltiplas cores de CTA.

---

# 12. Buttons

## Primary

```css
height: 36px;
padding: 0 14px;
background: var(--brand-600);
color: #FFF;
border-radius: 8px;
font-weight: 500;
```

## Secondary

```css
background: #FFF;
border: 1px solid var(--border-default);
color: var(--text-primary);
```

## Ghost

```css
background: transparent;
border: 0;
```

Danger: somente para ações destrutivas.

---

# 13. Cards

```css
background: var(--bg-surface);
border: 1px solid var(--border-soft);
border-radius: 12px;
box-shadow: var(--shadow-xs);
padding: 16px;
```

Card grande:

```css
padding: 20px;
```

---

# 14. KPI Cards

Formato:

```text
LABEL
12,483
texto auxiliar
```

Regra:

- máximo 4 KPIs visíveis
- números grandes
- evitar cores no número salvo quando semanticamente necessário

---

# 15. Error Severity Summary

Preferir controles compactos:

```text
Critical  12
High      38
Medium   142
Low      893
```

Ou horizontal:

```text
● Critical 12   ● High 38   ● Medium 142   ● Low 893
```

Cada item funciona como filtro.

---

# 16. Error List

A lista de erros é um dos principais componentes do LayaLog.

```text
●  Database connection timeout
   payments-api · production

   HIGH      82 occurrences        14s ago
```

```css
min-height: 72px;
```

Hover:

```css
background: var(--bg-surface-hover);
```

Selecionado:

```css
background: var(--bg-surface-selected);
border-left: 2px solid var(--brand-600);
```

---

# 17. Badges

```css
height: 22px;
padding: 0 8px;
font-size: 11px;
font-weight: 600;
border-radius: 999px;
```

Evitar 3 ou mais badges coloridos na mesma linha.

---

# 18. Detail Panel

```text
Error title
metadata

Laya Analysis
├─ Summary
├─ Probable cause
├─ Impact
└─ Suggested action

Occurrences

Stack trace

Context
```

```css
min-width: 420px;
width: 40%;
max-width: 640px;
```

---

# 19. Laya AI Analysis

A IA deve parecer parte nativa do produto.

Não usar card neon, gradiente roxo, ícone enorme ou excesso de “AI”.

Usar:

```text
✦ Laya Analysis

Probable cause
...

Impact
...

Suggested action
...
```

```css
background: #F8FAFF;
border: 1px solid #E3E8FF;
```

---

# 20. Log Viewer

```text
line │ timestamp │ level │ message
```

Exemplo:

```text
2151 │ 00:01:14.201 │ INFO  │ Sync started
2152 │ 00:01:14.238 │ WARN  │ User already exists
2153 │ 00:01:14.283 │ ERROR │ Failed to update user
```

Linha crítica:

```css
background: #FEF2F2;
border-left: 2px solid #EF4444;
```

---

# 21. Search

```css
height: 36px;
border: 1px solid var(--border-default);
border-radius: 8px;
background: var(--bg-surface);
```

Placeholder:

```text
Search errors...
```

Atalho:

```text
⌘ K
```

---

# 22. Filters

Preferir chips/dropdowns:

```text
Severity ▾
Service ▾
Environment ▾
Time range ▾
```

Filtro ativo:

```text
Severity: Critical ×
```

---

# 23. Tables

Header:

```css
font-size: 11px;
font-weight: 600;
color: var(--text-muted);
text-transform: uppercase;
letter-spacing: .03em;
```

Linha:

```css
height: 44px;
border-bottom: 1px solid var(--border-soft);
```

Sem zebra striping por padrão.

---

# 24. Charts

Regras:

- usar no máximo 1 cor principal + tons derivados
- reservar cores semânticas para estados
- grid quase invisível
- labels pequenas
- tooltip simples
- sem 3D
- sem sombras em gráficos
- sem fundo colorido

Line chart:

```css
stroke-width: 1.5px;
```

Area chart:

```css
fill-opacity: 0.08;
```

---

# 25. Empty States

```text
Nenhum erro encontrado

Tente alterar os filtros ou carregar outro arquivo.

[ Importar log ]
```

Ícone simples, sem ilustração gigante.

---

# 26. Loading

Evitar spinners no centro da tela. Usar skeleton, progress bar e status textual.

```text
Processing log...
38%
```

---

# 27. Motion

```css
--motion-fast: 120ms;
--motion-default: 180ms;
--motion-slow: 260ms;
```

Easing:

```css
cubic-bezier(.2,.8,.2,1)
```

Usos recomendados:

```text
Hover: 120ms
Abrir painel: 180–220ms
Reordenar erros: 180–260ms
Expandir stack trace: 180ms
```

---

# 28. GSAP Flip

Usar GSAP Flip para:

- reorganizar lista por criticidade
- aplicar filtros
- mover erro entre grupos
- alterar prioridade
- inserir/remover resultados

Não usar para animação puramente decorativa.

---

# 29. Iconografia

Recomendação:

```text
Lucide Icons
```

Tamanhos:

```text
sidebar: 16px
buttons: 16px
status: 14px
empty state: 24px
```

Stroke:

```text
1.75
```

---

# 30. Accessibility

Obrigatório:

- WCAG AA
- contraste mínimo adequado
- foco visível
- navegação por teclado
- atalhos documentados
- não comunicar severidade apenas por cor
- usar ícone + label
- respeitar prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

# 31. Layout principal sugerido para LayaLog

```text
┌───────────────────────────────────────────────────────────────┐
│ Sidebar │ Topbar                                              │
│         ├─────────────────────────────────────────────────────┤
│         │ Summary / filters                                   │
│         ├─────────────────────┬───────────────────────────────┤
│         │ Error list          │ Error details                 │
│         │                     │                               │
│         │                     │ Laya analysis                 │
│         │                     │                               │
│         │                     │ Stack trace                   │
│         │                     │                               │
│         └─────────────────────┴───────────────────────────────┤
└───────────────────────────────────────────────────────────────┘
```

---

# 32. Estrutura de navegação recomendada

```text
Overview
Triage
Logs
Services
Incidents
Analytics

Settings
```

Página padrão após processamento:

```text
Triage
```

O usuário deve ver primeiro o que precisa investigar.

---

# 33. Responsive

## Desktop

```text
≥ 1280px
sidebar fixa
master/detail lado a lado
```

## Tablet

```text
768–1279px
sidebar colapsável
detail panel overlay
```

## Mobile

```text
< 768px
navegação bottom sheet/menu
lista → detalhe em tela cheia
```

---

# 34. CSS Tokens

```css
:root {
  --bg-app: #F5F7FA;
  --bg-sidebar: #F2F4F7;
  --bg-surface: #FFFFFF;
  --bg-surface-hover: #F8FAFC;
  --bg-surface-selected: #EEF4FF;

  --border-soft: #E6EAF0;
  --border-default: #DDE3EA;
  --border-strong: #CBD3DD;

  --text-primary: #111827;
  --text-secondary: #667085;
  --text-muted: #98A2B3;

  --brand-500: #3B82F6;
  --brand-600: #2563EB;

  --critical: #EF4444;
  --high: #F97316;
  --medium: #F59E0B;
  --low: #3B82F6;
  --success: #10B981;

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 14px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;

  --motion-fast: 120ms;
  --motion-default: 180ms;
  --motion-slow: 260ms;
}
```

---

# 35. Component Density

## Comfortable

Para overview/dashboard:

```text
row: 48–56px
padding: 16–20px
```

## Compact

Para logs e triagem:

```text
row: 36–44px
padding: 8–12px
```

---

# 36. Regras de consistência

## Sempre

- usar grid
- usar tokens
- usar hierarquia tipográfica
- usar espaçamento da escala
- usar cor com significado
- manter componentes compactos
- mostrar ações secundárias somente no hover quando possível

## Nunca

- mais de 2 CTAs primários por área
- gradientes decorativos em dashboard
- border radius diferente sem motivo
- shadows grandes
- cards dentro de cards excessivamente
- mais de 5 cores competindo na mesma tela
- badges gigantes
- títulos técnicos longos como primeira linha

---

# 37. Regra para títulos técnicos

Evitar:

```text
[org.keycloak.storage.ldap.LDAPStorageProviderFactory] Timer-2...
```

Preferir:

```text
User not updated during LDAP synchronization

org.keycloak.storage.ldap.LDAPStorageProviderFactory
```

A primeira linha deve ser humana. A segunda pode ser técnica.

---

# 38. Hierarquia ideal de uma tela

```text
1. Contexto
2. Problema
3. Gravidade
4. Impacto
5. Evidência
6. Ação
```

Não:

```text
1. Gráfico
2. Métrica
3. Decoração
4. Problema
```

---

# 39. Resultado esperado

O produto final deve passar a sensação de:

```text
SaaS dashboard minimalista
+
observability tooling
+
produto B2B premium
+
identidade própria do LayaLog
```

A identidade própria deve vir de:

- organização dos dados
- linguagem da IA
- tratamento de severidade
- interação com logs
- fluxo de triagem
- microinterações

---

# 40. Checklist de tela

- [ ] existe um foco visual claro?
- [ ] o usuário sabe o que fazer em até 3 segundos?
- [ ] existe apenas um CTA principal?
- [ ] a cor está comunicando significado?
- [ ] existe espaço visual suficiente?
- [ ] a tipografia segue a escala?
- [ ] os componentes seguem tokens?
- [ ] a tela funciona com teclado?
- [ ] funciona com reduced motion?
- [ ] as informações técnicas longas estão truncadas?
- [ ] ações secundárias estão discretas?
- [ ] estados loading/empty/error foram definidos?
- [ ] o layout funciona em 1280px?
- [ ] o layout continua legível em telas maiores?
- [ ] existe contraste suficiente?

---

# 41. Resumo rápido

```text
Sidebar
→ compacta e discreta

Cards
→ brancos, bordas suaves, pouco shadow

Tipografia
→ simples e altamente legível

Métricas
→ números grandes + labels pequenas

Gráficos
→ limpos e monocromáticos

Listas
→ densas e fáceis de escanear

Cores
→ neutras + semânticas

Layout
→ modular, com bastante respiro

Interações
→ rápidas e discretas
```

Esse deve ser o DNA visual do LayaLog.
