/**
 * LayaLog - Internationalization (i18n) Module
 * Supported Languages: 'en' (Default), 'pt-br', 'cn' (Simplified Chinese)
 */

const translations = {
  en: {
    // Topbar & Navigation
    "app.title": "LayaLog — Intelligent Log Observability & AI Diagnosis",
    "nav.brand": "LayaLog",
    "nav.currentFile": "Current File",
    "nav.noActiveLog": "No active log",
    "nav.groupObservability": "Observability",
    "nav.triage": "Error Triage",
    "nav.logExplorer": "Log Explorer",
    "breadcrumb.root": "LayaLog",
    "breadcrumb.triage": "Triage",
    "breadcrumb.selectFile": "Select a file",
    "search.placeholder": "Search errors and logs...",
    "btn.importLog": "Import Log",
    "btn.exportMd": "Export MD",
    "btn.tour": "Tour Guide",
    "btn.tourShort": "Tour",
    "history.defaultOption": "-- Analysis History --",
    "history.title": "Saved Analysis History",
    "history.emptyTitle": "No analyses saved in history",
    "history.emptyDesc": "Import a log file to analyze incidents with Laya AI intelligence.",
    "history.open": "Open",
    "history.delete": "Permanently Delete",
    "history.activeBadge": "Active",
    "history.lines": "lines",
    "history.errors": "errors",
    "history.critical": "critical",
    "history.unavail": "unavailability",
    "btn.close": "Close",
    "btn.cancel": "Cancel",
    "btn.confirmDelete": "Delete Permanently",
    
    // KPI Cards
    "kpi.linesLabel": "Processed Lines",
    "kpi.linesMeta": "Total log volume",
    "kpi.errorsLabel": "Error Occurrences",
    "kpi.errorsMeta": "Classified events",
    "kpi.criticalLabel": "Critical Errors",
    "kpi.criticalMeta": "High response priority",
    "kpi.unavailLabel": "Unavailability Rate",
    "kpi.unavailMeta": "Direct operational impact",
    
    // Filters
    "filter.all": "All",
    "filter.critical": "Critical",
    "filter.high": "High",
    "filter.medium": "Medium",
    "filter.low": "Low",
    "filter.hint": "Use the filters above to focus on immediate diagnosis",

    // Incident List & Detail
    "incident.listTitle": "Identified Errors",
    "incident.listHint": "Click to inspect",
    "incident.emptyListTitle": "No file loaded",
    "incident.emptyListDesc": "Import a log file or select a previous analysis at the top.",
    "incident.noErrorsTitle": "No errors found",
    "incident.noErrorsDesc": "The analyzed log file contains no recorded errors or failures.",
    "incident.detailTitle": "Diagnosis & Details",
    "incident.waitingTitle": "Waiting for selection",
    "incident.waitingDesc": "Details and AI semantic analysis will appear here when you select an incident.",
    "incident.sector": "Sector",
    "incident.failure": "Failure",
    "incident.firstSeen": "First seen",
    "incident.affectsUnavail": "Affects System Availability",
    "incident.noUnavail": "No General Outage",
    "incident.profileCalibration": "Calibration Profile",
    "incident.diagSummary": "Diagnostic Summary",
    "incident.recommendation": "Suggested Action / Recommendation",
    "incident.occurrences": "Occurrences",
    "incident.occurrencesHint": "Click to inspect",
    "incident.jumpFirst": "1st",
    "incident.jumpGo": "Go",
    "incident.jumpPlaceholder": "Go to line...",
    "incident.evidenceTitle": "Evidence / Stacktrace",
    "incident.copy": "Copy",
    "incident.copied": "Copied!",
    "incident.occurrencesCount": "occurrence(s)",
    "incident.line": "Line",

    // Log Viewer Section
    "viewer.title": "Full Log Explorer",
    "viewer.meta": "Virtualized Stream · 200 lines/chunk",
    "viewer.emptyTitle": "No log loaded",
    "viewer.emptyDesc": "Select an analysis from history or import a log file.",

    // Profiles Modal
    "profile.modalTitle": "Gravity Profiles & Laya Calibration",
    "profile.modalSubtitle": "Define how the AI engine assesses severity (Low, Medium, Critical) for each stack",
    "profile.available": "Available Profiles",
    "profile.btnNew": "+ New",
    "profile.titleNew": "New Gravity Profile",
    "profile.titleEdit": "Edit Profile",
    "profile.badgeBuiltin": "Built-in",
    "profile.badgeCustom": "Custom",
    "profile.badgeBuiltinNotice": "Built-in (Creates copy on save)",
    "profile.btnDuplicate": "📑 Duplicate",
    "profile.btnSave": "💾 Save Profile",
    "profile.btnSaveNew": "💾 Save As New Profile",
    "profile.btnSaveEdit": "💾 Save Changes",
    "profile.btnDelete": "🗑️ Delete Profile",
    "profile.fieldName": "Profile Name",
    "profile.fieldDesc": "Short Description",
    "profile.fieldContext": "Operational System Context (Optional - Laya State)",
    "profile.critLow": "🟢 Criteria for LOW Severity (1)",
    "profile.critMed": "🟡 Criteria for MEDIUM Severity (2)",
    "profile.critHigh": "🔴 Criteria for CRITICAL Severity (3)",
    "profile.promptClone": "Name for profile copy:",
    "profile.confirmDelete": "Are you sure you want to delete this custom profile?",

    // Processing & Confirmation Modals
    "process.title": "Log Processing",
    "process.statusParsing": "Parsing and grouping log signatures...",
    "process.statusClassifying": "Classifying with Laya System One...",
    "process.statusCompleted": "Analysis completed successfully!",
    "process.btnCancel": "Cancel",
    "confirm.deleteTitle": "Confirm Analysis Deletion",
    "confirm.deleteMsg": 'Are you sure you want to permanently delete "{filename}"? This action will completely remove the history record and physical log file from the server.',

    // Tour Steps (Driver.js)
    "tour.step1Title": "🎯 Gravity Profiles",
    "tour.step1Desc": "Calibrate Laya AI semantic criteria for your technology stack (e.g. Web App, Keycloak IAM, Payments).",
    "tour.step2Title": "📥 Import Logs",
    "tour.step2Desc": "Upload any server log file (.txt, .log) with drag-and-drop or file picker to trigger real-time AI classification.",
    "tour.step3Title": "📊 Operational KPIs",
    "tour.step3Desc": "Instantly monitor total processed lines, error counts, critical incidents, and system unavailability impact.",
    "tour.step4Title": "🔍 Error Triage & Quiet AI",
    "tour.step4Desc": "Smart cryptographic grouping of incidents. Click any error to inspect root cause explanations, recommendations, and stack traces.",
    "tour.step5Title": "⚡ Virtualized Log Explorer",
    "tour.step5Desc": "High-speed stream viewer handling millions of lines smoothly with real-time text highlight and line jumps.",
    "tour.step6Title": "🕒 History & Export",
    "tour.step6Desc": "Access previous analyses anytime or export full diagnostic reports in Markdown format.",
    "tour.btnNext": "Next →",
    "tour.btnPrev": "← Previous",
    "tour.btnDone": "Got it! 🎉"
  },

  "pt-br": {
    // Topbar & Navigation
    "app.title": "LayaLog — Observabilidade & Diagnóstico Inteligente com IA",
    "nav.brand": "LayaLog",
    "nav.currentFile": "Arquivo Atual",
    "nav.noActiveLog": "Nenhum log ativo",
    "nav.groupObservability": "Observabilidade",
    "nav.triage": "Triagem de Erros",
    "nav.logExplorer": "Explorador de Log",
    "breadcrumb.root": "LayaLog",
    "breadcrumb.triage": "Triagem",
    "breadcrumb.selectFile": "Selecione um arquivo",
    "search.placeholder": "Buscar erros e logs...",
    "btn.importLog": "Importar Log",
    "btn.exportMd": "Exportar MD",
    "btn.tour": "Guia do Sistema",
    "btn.tourShort": "Guia",
    "history.defaultOption": "-- Histórico de Análises --",
    "history.title": "Histórico de Análises Salvas",
    "history.emptyTitle": "Nenhuma análise salva no histórico",
    "history.emptyDesc": "Importe um arquivo de log para analisar incidentes com a inteligência Laya.",
    "history.open": "Abrir",
    "history.delete": "Excluir Definitivamente",
    "history.activeBadge": "Ativo",
    "history.lines": "linhas",
    "history.errors": "erros",
    "history.critical": "críticos",
    "history.unavail": "indisponibilidade",
    "btn.close": "Fechar",
    "btn.cancel": "Cancelar",
    "btn.confirmDelete": "Excluir Definitivamente",
    
    // KPI Cards
    "kpi.linesLabel": "Linhas Processadas",
    "kpi.linesMeta": "Volume total do log",
    "kpi.errorsLabel": "Ocorrências de Erro",
    "kpi.errorsMeta": "Eventos classificados",
    "kpi.criticalLabel": "Erros Críticos",
    "kpi.criticalMeta": "Alta prioridade de resposta",
    "kpi.unavailLabel": "Taxa de Indisponibilidade",
    "kpi.unavailMeta": "Impacto operacional direto",
    
    // Filters
    "filter.all": "Todos",
    "filter.critical": "Crítica",
    "filter.high": "Alta",
    "filter.medium": "Média",
    "filter.low": "Baixa",
    "filter.hint": "Use os filtros acima para focar no diagnóstico imediato",

    // Incident List & Detail
    "incident.listTitle": "Erros Identificados",
    "incident.listHint": "Clique para inspecionar",
    "incident.emptyListTitle": "Nenhum arquivo carregado",
    "incident.emptyListDesc": "Importe um arquivo de log ou selecione uma análise prévia no topo da página.",
    "incident.noErrorsTitle": "Nenhum erro encontrado",
    "incident.noErrorsDesc": "O arquivo de log analisado não apresenta erros ou falhas registradas.",
    "incident.detailTitle": "Diagnóstico e Detalhes",
    "incident.waitingTitle": "Aguardando seleção",
    "incident.waitingDesc": "Os detalhes e a análise semântica da IA aparecerão aqui ao selecionar um incidente.",
    "incident.sector": "Setor",
    "incident.failure": "Falha",
    "incident.firstSeen": "1ª vez",
    "incident.affectsUnavail": "Afeta Disponibilidade do Sistema",
    "incident.noUnavail": "Sem Indisponibilidade Geral",
    "incident.profileCalibration": "Perfil de Calibração",
    "incident.diagSummary": "Resumo do Diagnóstico",
    "incident.recommendation": "Ação Sugerida / Recomendação",
    "incident.occurrences": "Ocorrências",
    "incident.occurrencesHint": "Clique para inspecionar",
    "incident.jumpFirst": "1ª",
    "incident.jumpGo": "Ir",
    "incident.jumpPlaceholder": "Ir p/ linha...",
    "incident.evidenceTitle": "Evidência / Stacktrace",
    "incident.copy": "Copiar",
    "incident.copied": "Copiado!",
    "incident.occurrencesCount": "ocorrência(s)",
    "incident.line": "Linha",

    // Log Viewer Section
    "viewer.title": "Explorador de Log Completo",
    "viewer.meta": "Stream Virtualizado · 200 linhas/chunk",
    "viewer.emptyTitle": "Nenhum log carregado",
    "viewer.emptyDesc": "Selecione uma análise no histórico ou importe um arquivo de log.",

    // Profiles Modal
    "profile.modalTitle": "Perfis de Gravidade & Calibração Laya",
    "profile.modalSubtitle": "Defina como o motor de IA avalia a gravidade (Baixa, Média, Crítica) para cada stack",
    "profile.available": "Perfis Disponíveis",
    "profile.btnNew": "+ Novo",
    "profile.titleNew": "Novo Perfil de Gravidade",
    "profile.titleEdit": "Editar Perfil",
    "profile.badgeBuiltin": "Nativo",
    "profile.badgeCustom": "Customizado",
    "profile.badgeBuiltinNotice": "Nativo (Gera Cópia ao Salvar)",
    "profile.btnDuplicate": "📑 Duplicar",
    "profile.btnSave": "💾 Salvar Perfil",
    "profile.btnSaveNew": "💾 Salvar Como Novo Perfil",
    "profile.btnSaveEdit": "💾 Salvar Alterações",
    "profile.btnDelete": "🗑️ Excluir Perfil",
    "profile.fieldName": "Nome do Perfil",
    "profile.fieldDesc": "Descrição Curta",
    "profile.fieldContext": "Contexto Operacional do Sistema (Opcional - Laya State)",
    "profile.critLow": "🟢 Critério para Gravidade BAIXA (1)",
    "profile.critMed": "🟡 Critério para Gravidade MÉDIA (2)",
    "profile.critHigh": "🔴 Critério para Gravidade CRÍTICA (3)",
    "profile.promptClone": "Nome para a cópia do perfil:",
    "profile.confirmDelete": "Tem certeza que deseja excluir este perfil customizado?",

    // Processing & Confirmation Modals
    "process.title": "Processamento de Log",
    "process.statusParsing": "Parsing e agrupamento de assinaturas do log...",
    "process.statusClassifying": "Classificando com Laya System One...",
    "process.statusCompleted": "Análise concluída com sucesso!",
    "process.btnCancel": "Cancelar",
    "confirm.deleteTitle": "Confirmar Exclusão de Análise",
    "confirm.deleteMsg": 'Tem certeza de que deseja excluir permanentemente "{filename}"? Esta ação removerá definitivamente o registro do histórico e o arquivo físico de log do servidor.',

    // Tour Steps (Driver.js)
    "tour.step1Title": "🎯 Perfis de Gravidade",
    "tour.step1Desc": "Calibre os critérios semânticos da IA Laya para cada stack técnica (ex: Web App, Keycloak IAM, Pagamentos).",
    "tour.step2Title": "📥 Importação de Log",
    "tour.step2Desc": "Envie arquivos de log (.txt, .log) via arrastar-e-soltar ou botão para iniciar a classificação inteligente.",
    "tour.step3Title": "📊 Painel de Métricas (KPIs)",
    "tour.step3Desc": "Acompanhe em tempo real volume de linhas, contagem de erros, criticidade e taxa de indisponibilidade.",
    "tour.step4Title": "🔍 Triagem de Erros & Quiet AI",
    "tour.step4Desc": "Agrupamento inteligente de incidentes. Clique em qualquer erro para ver diagnósticos, causas-raiz e recomendações.",
    "tour.step5Title": "⚡ Explorador de Log Virtualizado",
    "tour.step5Desc": "Visualizador de alto desempenho capaz de rolar milhões de linhas com buscas instantâneas e saltos de linha.",
    "tour.step6Title": "🕒 Histórico & Exportação",
    "tour.step6Desc": "Acesse análises anteriores a qualquer momento ou exporte relatórios técnicos completos em Markdown.",
    "tour.btnNext": "Próximo →",
    "tour.btnPrev": "← Anterior",
    "tour.btnDone": "Entendido! 🎉"
  },

  cn: {
    // Topbar & Navigation
    "app.title": "LayaLog — 智能日志可观测性与AI诊断系统",
    "nav.brand": "LayaLog",
    "nav.currentFile": "当前文件",
    "nav.noActiveLog": "无活动日志",
    "nav.groupObservability": "可观测性",
    "nav.triage": "错误分类排查",
    "nav.logExplorer": "日志浏览器",
    "breadcrumb.root": "LayaLog",
    "breadcrumb.triage": "分类",
    "breadcrumb.selectFile": "选择日志文件",
    "search.placeholder": "搜索错误与日志...",
    "btn.importLog": "导入日志",
    "btn.exportMd": "导出 MD",
    "btn.tour": "使用指南",
    "btn.tourShort": "指南",
    "history.defaultOption": "-- 历史分析记录 --",
    "history.title": "已保存的分析历史",
    "history.emptyTitle": "暂无已保存的分析记录",
    "history.emptyDesc": "导入日志文件以使用 Laya AI 智能引擎分析事件。",
    "history.open": "打开",
    "history.delete": "永久删除",
    "history.activeBadge": "当前",
    "history.lines": "行",
    "history.errors": "错误",
    "history.critical": "严重",
    "history.unavail": "不可用率",
    "btn.close": "关闭",
    "btn.cancel": "取消",
    "btn.confirmDelete": "确认永久删除",
    
    // KPI Cards
    "kpi.linesLabel": "处理总行数",
    "kpi.linesMeta": "日志总数据量",
    "kpi.errorsLabel": "错误发生次数",
    "kpi.errorsMeta": "已归类错误事件",
    "kpi.criticalLabel": "严重错误数",
    "kpi.criticalMeta": "高优先级响应事件",
    "kpi.unavailLabel": "不可用率影响",
    "kpi.unavailMeta": "对系统运行的直接影响",
    
    // Filters
    "filter.all": "全部",
    "filter.critical": "严重",
    "filter.high": "高",
    "filter.medium": "中",
    "filter.low": "低",
    "filter.hint": "使用上方严重级别过滤器快速聚焦关键问题",

    // Incident List & Detail
    "incident.listTitle": "识别到的错误事件",
    "incident.listHint": "点击以展开详细分析",
    "incident.emptyListTitle": "尚未加载日志文件",
    "incident.emptyListDesc": "请在页面顶部导入日志文件或选择历史分析记录。",
    "incident.noErrorsTitle": "未发现错误",
    "incident.noErrorsDesc": "当前分析的日志文件中未发现错误或异常记录。",
    "incident.detailTitle": "AI诊断与详细信息",
    "incident.waitingTitle": "等待选择",
    "incident.waitingDesc": "在左侧选择具体错误事件后，此处将展示语义分析与AI诊断。",
    "incident.sector": "所属架构",
    "incident.failure": "故障类型",
    "incident.firstSeen": "首次发生",
    "incident.affectsUnavail": "影响系统可用性",
    "incident.noUnavail": "未造成全局不可用",
    "incident.profileCalibration": "校准配置",
    "incident.diagSummary": "诊断摘要",
    "incident.recommendation": "建议处理方案 / 修复措施",
    "incident.occurrences": "发生频次",
    "incident.occurrencesHint": "点击行号快速定位",
    "incident.jumpFirst": "首行",
    "incident.jumpGo": "前往",
    "incident.jumpPlaceholder": "输入行号...",
    "incident.evidenceTitle": "技术证据 / 堆栈追踪",
    "incident.copy": "复制",
    "incident.copied": "已复制!",
    "incident.occurrencesCount": "次",
    "incident.line": "行",

    // Log Viewer Section
    "viewer.title": "完整日志流浏览器",
    "viewer.meta": "虚拟化滚动流 · 每批次200行",
    "viewer.emptyTitle": "尚未加载日志",
    "viewer.emptyDesc": "从历史记录中选择或导入新的日志文件。",

    // Profiles Modal
    "profile.modalTitle": "严重性配置与 Laya AI 校准",
    "profile.modalSubtitle": "针对不同技术栈自定义评估严重级别（低、中、严重）的语义标准",
    "profile.available": "可用配置列表",
    "profile.btnNew": "+ 新建",
    "profile.titleNew": "新建严重性配置",
    "profile.titleEdit": "编辑配置",
    "profile.badgeBuiltin": "内置",
    "profile.badgeCustom": "自定义",
    "profile.badgeBuiltinNotice": "系统内置（保存时将自动生成副本）",
    "profile.btnDuplicate": "📑 复制副本",
    "profile.btnSave": "💾 保存配置",
    "profile.btnSaveNew": "💾 保存为新配置",
    "profile.btnSaveEdit": "💾 保存修改",
    "profile.btnDelete": "🗑️ 删除配置",
    "profile.fieldName": "配置名称",
    "profile.fieldDesc": "简短描述",
    "profile.fieldContext": "系统运行环境与上下文 (可选 - Laya State)",
    "profile.critLow": "🟢 低级别严重性标准 (1)",
    "profile.critMed": "🟡 中级别严重性标准 (2)",
    "profile.critHigh": "🔴 严重级别判定标准 (3)",
    "profile.promptClone": "请输入新配置副本名称:",
    "profile.confirmDelete": "确认要删除此自定义配置吗？",

    // Processing & Confirmation Modals
    "process.title": "日志智能处理",
    "process.statusParsing": "正在解析日志结构与特征签名...",
    "process.statusClassifying": "正在使用 Laya System One 进行分类...",
    "process.statusCompleted": "日志分析成功完成!",
    "process.btnCancel": "取消",
    "confirm.deleteTitle": "确认删除历史记录",
    "confirm.deleteMsg": '确定要永久删除 "{filename}" 吗？此操作将彻底删除数据库记录及物理日志文件。',

    // Tour Steps (Driver.js)
    "tour.step1Title": "🎯 严重性配置 (Gravity Profiles)",
    "tour.step1Desc": "针对不同的技术栈（如 Web应用、Keycloak认证、支付系统等）校准 Laya AI 的语义分析标准。",
    "tour.step2Title": "📥 导入日志文件",
    "tour.step2Desc": "支持直接拖拽或点击导入 .txt / .log 日志文件，立即触发实时 AI 分类与错误分析。",
    "tour.step3Title": "📊 运行指标与KPI看板",
    "tour.step3Desc": "实时监控日志总行数、错误频次、高危致命错误数以及系统不可用性影响率。",
    "tour.step4Title": "🔍 错误分类排查与 Quiet AI",
    "tour.step4Desc": "基于特征结构聚合错误事件。点击任意事件即可查看由 AI 生成的故障根因、修复建议及堆栈。",
    "tour.step5Title": "⚡ 虚拟化日志流浏览器",
    "tour.step5Desc": "极致流畅渲染百万行级日志流，支持关键词即时高亮与精准行号直达跳转。",
    "tour.step6Title": "🕒 历史记录与导出",
    "tour.step6Desc": "随时加载过往分析快照，并可一键导出排版完备的 Markdown 诊断报告。",
    "tour.btnNext": "下一步 →",
    "tour.btnPrev": "← 上一步",
    "tour.btnDone": "开始使用! 🎉"
  }
};

let currentLang = localStorage.getItem("layalog_lang") || "en";

function t(key, fallback = "") {
  const dict = translations[currentLang] || translations["en"];
  if (dict && dict[key] !== undefined) {
    return dict[key];
  }
  const defaultDict = translations["en"];
  return (defaultDict && defaultDict[key] !== undefined) ? defaultDict[key] : (fallback || key);
}

function getCurrentLang() {
  return currentLang;
}

function setLanguage(lang) {
  if (!translations[lang]) lang = "en";
  currentLang = lang;
  localStorage.setItem("layalog_lang", lang);
  document.documentElement.lang = lang === "pt-br" ? "pt-BR" : (lang === "cn" ? "zh-CN" : "en");
  applyTranslations();
  
  // Sync select element if present
  const langSelect = document.getElementById("v2LangSelect");
  if (langSelect && langSelect.value !== lang) {
    langSelect.value = lang;
  }
}

function applyTranslations() {
  document.title = t("app.title");

  // Translate all elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key) {
      el.textContent = t(key);
    }
  });

  // Translate all elements with data-i18n-placeholder
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key) {
      el.placeholder = t(key);
    }
  });

  // Translate all elements with data-i18n-title
  document.querySelectorAll("[data-i18n-title]").forEach(el => {
    const key = el.getAttribute("data-i18n-title");
    if (key) {
      el.title = t(key);
    }
  });

  // Dispatch event for components to update dynamically rendered texts
  window.dispatchEvent(new CustomEvent("layalog-language-changed", { detail: { lang: currentLang } }));
}

// Global exports
window.LayaI18n = {
  t,
  setLanguage,
  getCurrentLang,
  applyTranslations,
  translations
};
