let currentAnalysis = null;
let logViewer = null;
let charts = {};
let currentUploadAbortController = null;

document.addEventListener("DOMContentLoaded", () => {
  initUI();
  loadHistory();
});

function initUI() {
  const container = document.getElementById("logViewer");
  logViewer = new VirtualLogViewer(container, { rowHeight: 22, buffer: 20 });

  // Upload button
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  uploadBtn.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  });

  // Cancel processing button
  const btnCancel = document.getElementById("btnCancelProcess");
  if (btnCancel) {
    btnCancel.addEventListener("click", () => {
      if (currentUploadAbortController) {
        currentUploadAbortController.abort();
        currentUploadAbortController = null;
      }
      document.getElementById("loadingOverlay").style.display = "none";
      document.getElementById("fileInput").value = "";
    });
  }

  // History selector
  const historySelect = document.getElementById("historySelect");
  historySelect.addEventListener("change", (e) => {
    if (e.target.value) {
      loadAnalysisById(e.target.value);
    }
  });

  // Export MD button
  const exportBtn = document.getElementById("exportBtn");
  exportBtn.addEventListener("click", () => {
    if (!currentAnalysis) {
      alert("Nenhuma análise ativa para exportar.");
      return;
    }
    window.location.href = `/api/analyses/${currentAnalysis.id}/export-md`;
  });

  // Log Search
  const logSearch = document.getElementById("logSearch");
  logSearch.addEventListener("input", (e) => {
    if (logViewer) {
      logViewer.setSearchQuery(e.target.value);
    }
  });

  // Incidents Search / Filter
  const incidentSearch = document.getElementById("incidentSearch");
  incidentSearch.addEventListener("input", (e) => {
    filterIncidents(e.target.value);
  });

  // Modal close handlers
  document.getElementById("modalClose").addEventListener("click", closeModal);
  document.getElementById("detailsModal").addEventListener("click", (e) => {
    if (e.target.id === "detailsModal") closeModal();
  });
}

async function loadHistory() {
  try {
    const res = await fetch("/api/analyses");
    if (!res.ok) return;
    const items = await res.json();
    const select = document.getElementById("historySelect");
    
    select.innerHTML = '<option value="">-- Histórico de Análises --</option>';
    items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item.id;
      opt.textContent = `${item.filename} (${item.created_at}) - ${item.total_errors} erros`;
      select.appendChild(opt);
    });
    // System intentionally starts clean without auto-loading old files
  } catch (err) {
    console.error("Erro ao carregar histórico:", err);
  }
}

function updateProgressUI(percent, statusText) {
  const pFill = document.getElementById("progressFill");
  const pPercent = document.getElementById("progressPercent");
  const pStatus = document.getElementById("progressStatus");

  if (pFill) pFill.style.width = `${percent}%`;
  if (pPercent) pPercent.textContent = `${percent}%`;
  if (pStatus && statusText) pStatus.textContent = statusText;
}

async function handleFileUpload(file) {
  const loadingOverlay = document.getElementById("loadingOverlay");
  const progressFilename = document.getElementById("progressFilename");
  
  if (progressFilename) progressFilename.textContent = file.name;
  updateProgressUI(0, "Iniciando upload e análise...");
  loadingOverlay.style.display = "flex";

  const formData = new FormData();
  formData.append("file", file);

  currentUploadAbortController = new AbortController();

  try {
    const res = await fetch("/api/analyze-stream", {
      method: "POST",
      body: formData,
      signal: currentUploadAbortController.signal
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Falha na análise" }));
      throw new Error(err.detail || "Falha na requisição de análise");
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";
    let completedData = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop(); // Retain incomplete line

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const event = JSON.parse(line);
          if (event.type === "progress") {
            updateProgressUI(event.percent, event.message);
          } else if (event.type === "complete") {
            completedData = event.data;
          } else if (event.type === "error") {
            throw new Error(event.message || "Erro durante o processamento do log");
          }
        } catch (parseErr) {
          console.error("Erro ao interpretar evento do stream:", parseErr, line);
        }
      }
    }

    if (completedData) {
      displayAnalysis(completedData);
      await loadHistory();
      document.getElementById("historySelect").value = completedData.id;
    } else {
      throw new Error("O servidor finalizou sem retornar os dados completos da análise.");
    }

  } catch (err) {
    if (err.name === "AbortError") {
      console.log("Processamento cancelado pelo usuário.");
      return;
    }
    alert(`Erro na análise: ${err.message}`);
    console.error(err);
  } finally {
    currentUploadAbortController = null;
    loadingOverlay.style.display = "none";
    document.getElementById("fileInput").value = "";
  }
}

async function loadAnalysisById(id) {
  const loadingOverlay = document.getElementById("loadingOverlay");
  const progressFilename = document.getElementById("progressFilename");
  
  if (progressFilename) progressFilename.textContent = "Carregando análise...";
  updateProgressUI(50, "Buscando dados da análise no banco...");
  loadingOverlay.style.display = "flex";

  try {
    const res = await fetch(`/api/analyses/${id}`);
    if (!res.ok) {
      throw new Error("Análise não encontrada no servidor.");
    }
    const data = await res.json();
    displayAnalysis(data);
  } catch (err) {
    alert(err.message);
    await loadHistory();
  } finally {
    loadingOverlay.style.display = "none";
  }
}

function displayAnalysis(data) {
  currentAnalysis = data;

  // 1. Update Metrics Cards
  const stats = data.stats;
  document.getElementById("metricTotalLines").textContent = Number(stats.total_lines).toLocaleString("pt-BR");
  document.getElementById("metricTotalErrors").textContent = Number(stats.total_errors).toLocaleString("pt-BR");
  document.getElementById("metricCritical").textContent = Number(stats.critical_errors).toLocaleString("pt-BR");
  document.getElementById("metricDept").textContent = stats.most_affected_department || "N/D";
  document.getElementById("metricUnavail").textContent = `${stats.unavailability_rate}%`;

  // 2. Render Charts
  renderCharts(stats);

  // 3. Populate Left Log Viewer with chunked stream
  if (logViewer && data.id) {
    logViewer.setAnalysis(data.id, data.total_lines);
  }

  // 4. Render Right Incidents List
  renderIncidents(data.incidents);

  // Enable export button
  document.getElementById("exportBtn").removeAttribute("disabled");
}

function renderCharts(stats) {
  // Destroy existing charts
  if (charts.severity) charts.severity.destroy();
  if (charts.dept) charts.dept.destroy();
  if (charts.types) charts.types.destroy();

  // Chart 1: Gravidade (Donut)
  const ctxSev = document.getElementById("chartSeverity").getContext("2d");
  charts.severity = new Chart(ctxSev, {
    type: "doughnut",
    data: {
      labels: ["Crítica", "Média", "Baixa"],
      datasets: [{
        data: [
          stats.severity_counts["Crítica"] || 0,
          stats.severity_counts["Média"] || 0,
          stats.severity_counts["Baixa"] || 0
        ],
        backgroundColor: ["#ef4444", "#f59e0b", "#10b981"],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#94a3b8", font: { size: 11 } } }
      },
      cutout: "68%"
    }
  });

  // Chart 2: Setor (Horizontal Bar)
  const deptLabels = Object.keys(stats.department_counts || {});
  const deptValues = Object.values(stats.department_counts || {});
  const ctxDept = document.getElementById("chartDept").getContext("2d");
  charts.dept = new Chart(ctxDept, {
    type: "bar",
    data: {
      labels: deptLabels,
      datasets: [{
        data: deptValues,
        backgroundColor: "#0ea5e9",
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#64748b" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } }
      }
    }
  });

  // Chart 3: Tipos de Falha (Vertical Bar)
  const typeLabels = Object.keys(stats.failure_type_counts || {});
  const typeValues = Object.values(stats.failure_type_counts || {});
  const ctxTypes = document.getElementById("chartTypes").getContext("2d");
  charts.types = new Chart(ctxTypes, {
    type: "bar",
    data: {
      labels: typeLabels,
      datasets: [{
        data: typeValues,
        backgroundColor: "#8b5cf6",
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#94a3b8", font: { size: 9 }, maxRotation: 25 }, grid: { display: false } },
        y: { ticks: { color: "#64748b" }, grid: { color: "rgba(255,255,255,0.05)" } }
      }
    }
  });
}

function renderIncidents(incidents) {
  const container = document.getElementById("incidentsList");
  container.innerHTML = "";

  if (!incidents || incidents.length === 0) {
    container.innerHTML = '<div style="padding:2rem;text-align:center;color:#64748b;">Nenhum erro detectado no arquivo.</div>';
    return;
  }

  incidents.forEach((inc, idx) => {
    const card = document.createElement("div");
    const gravClass = inc.gravidade === 3 ? "critical" : (inc.gravidade === 2 ? "medium" : "low");
    const badgeGravClass = inc.gravidade === 3 ? "badge-critical" : (inc.gravidade === 2 ? "badge-medium" : "badge-low");

    card.className = `incident-card ${gravClass}`;
    card.dataset.id = inc.id;
    card.dataset.text = (inc.title + " " + inc.setor + " " + inc.tipo_falha).toLowerCase();

    card.innerHTML = `
      <div class="incident-header">
        <div class="incident-title">#${idx + 1} ${escapeHTML(inc.title)}</div>
        <span class="badge ${badgeGravClass}">${inc.gravidade_label.toUpperCase()}</span>
      </div>

      <div class="incident-badges">
        <span class="badge badge-dept">🏢 ${escapeHTML(inc.setor)}</span>
        <span class="badge badge-type">🏷️ ${escapeHTML(inc.tipo_falha)}</span>
        ${inc.causa_indisponibilidade ? '<span class="badge badge-unavail">⚠️ Causa Indisponibilidade</span>' : ''}
        <span class="badge" style="background:rgba(255,255,255,0.08);color:#cbd5e1;">🔁 ${inc.total_occurrences}x ocorrências</span>
      </div>

      <div class="incident-summary">${escapeHTML(inc.technical_summary)}</div>

      <div class="incident-footer">
        <div class="incident-meta">
          1ª vez na <strong>Linha ${inc.first_seen_line}</strong> (${inc.first_seen_time || 'N/D'})
        </div>
        <div class="incident-actions">
          <button class="btn btn-secondary btn-sm btn-details" data-id="${inc.id}">🔍 Ver Detalhes</button>
          <button class="btn btn-primary btn-sm btn-jump" data-line="${inc.first_seen_line}">📍 Ir para Linha ${inc.first_seen_line}</button>
        </div>
      </div>
    `;

    container.appendChild(card);
  });

  // Attach card action buttons
  container.querySelectorAll(".btn-jump").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const line = parseInt(e.currentTarget.dataset.line, 10);
      if (logViewer) {
        logViewer.scrollToLine(line, true);
      }
    });
  });

  container.querySelectorAll(".btn-details").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const incId = e.currentTarget.dataset.id;
      const incident = incidents.find(i => i.id === incId);
      if (incident) {
        openModal(incident);
      }
    });
  });
}

function filterIncidents(query) {
  const q = (query || "").toLowerCase();
  const cards = document.querySelectorAll(".incident-card");
  cards.forEach(c => {
    const text = c.dataset.text || "";
    c.style.display = text.includes(q) ? "flex" : "none";
  });
}

function openModal(inc) {
  const modal = document.getElementById("detailsModal");
  document.getElementById("modalTitle").textContent = inc.title;
  
  const modalBody = document.getElementById("modalBody");
  
  const pillsHtml = inc.lines.map(l => 
    `<span class="line-pill" onclick="jumpFromModal(${l})">Linha ${l}</span>`
  ).join(" ");

  modalBody.innerHTML = `
    <div>
      <div class="detail-section-title">Classificação Semântica (Laya)</div>
      <div class="incident-badges" style="margin-bottom:0.5rem;">
        <span class="badge ${inc.gravidade === 3 ? 'badge-critical' : (inc.gravidade === 2 ? 'badge-medium' : 'badge-low')}">
          Gravidade: ${inc.gravidade_label} (${inc.gravidade}/3)
        </span>
        <span class="badge badge-dept">Setor: ${escapeHTML(inc.setor)}</span>
        <span class="badge badge-type">Tipo: ${escapeHTML(inc.tipo_falha)}</span>
        <span class="badge ${inc.causa_indisponibilidade ? 'badge-unavail' : 'badge-low'}">
          ${inc.causa_indisponibilidade ? 'Causa Indisponibilidade Geral' : 'Sem Indisponibilidade de Sistema'}
        </span>
      </div>
      <p style="font-size:0.875rem;color:#cbd5e1;line-height:1.5;">${escapeHTML(inc.technical_summary)}</p>
    </div>

    <div>
      <div class="detail-section-title">Recomendação de Correção</div>
      <div style="background:rgba(14,165,233,0.1);border-left:3px solid #0ea5e9;padding:0.75rem 1rem;border-radius:4px;font-size:0.875rem;color:#e0f2fe;">
        💡 ${escapeHTML(inc.recommendation || 'Verificar stacktrace e aplicar tratamento defensivo.')}
      </div>
    </div>

    <div>
      <div class="detail-section-title">Ocorrências no Log (${inc.lines.length} vezes) - Clique para ir à linha</div>
      <div class="lines-pills">${pillsHtml}</div>
    </div>

    <div>
      <div class="detail-section-title">Amostra do Log & Stacktrace</div>
      <div class="code-block">${escapeHTML(inc.sample_raw || inc.sample_stacktrace || 'Nenhum stacktrace disponível')}</div>
    </div>
  `;

  modal.classList.add("active");
}

function jumpFromModal(lineNumber) {
  closeModal();
  if (logViewer) {
    logViewer.scrollToLine(lineNumber, true);
  }
}

function closeModal() {
  document.getElementById("detailsModal").classList.remove("active");
}

function escapeHTML(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
