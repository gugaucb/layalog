/**
 * LayaLog V2 App Controller
 * Implements Quiet UI Observability, Master-Detail, Laya AI Analysis, Profiles & Interactive Triage
 */

let currentAnalysis = null;
let selectedIncident = null;
let logViewerV2 = null;
let activeSeverityFilter = "all";
let uploadAbortController = null;

let allProfiles = [];
let selectedProfileId = "web-app-general";
let modalSelectedProfileId = null;

document.addEventListener("DOMContentLoaded", () => {
  initV2App();
  loadProfiles();
  loadHistory();
  setupKeyboardShortcuts();
  setupProfileModalHandlers();
});

function initV2App() {
  const viewerContainer = document.getElementById("v2LogViewerContainer");
  if (viewerContainer) {
    logViewerV2 = new V2LogViewer(viewerContainer, { rowHeight: 20, buffer: 25 });
  }

  // File Upload
  const fileInput = document.getElementById("v2FileInput");
  const uploadBtn = document.getElementById("v2UploadBtn");
  if (uploadBtn && fileInput) {
    uploadBtn.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileUpload(e.target.files[0]);
      }
    });
  }

  // Cancel Upload Button
  const cancelBtn = document.getElementById("v2BtnCancelProcess");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      if (uploadAbortController) {
        uploadAbortController.abort();
        uploadAbortController = null;
      }
      hideLoadingOverlay();
      if (fileInput) fileInput.value = "";
    });
  }

  // History selector
  const historySelect = document.getElementById("v2HistorySelect");
  if (historySelect) {
    historySelect.addEventListener("change", (e) => {
      if (e.target.value) {
        loadAnalysisById(e.target.value);
      }
    });
  }

  // History Manager Button
  const manageHistoryBtn = document.getElementById("v2ManageHistoryBtn");
  if (manageHistoryBtn) {
    manageHistoryBtn.addEventListener("click", () => {
      openHistoryModal();
    });
  }

  // Delete Current Active Analysis Button
  const deleteCurrentBtn = document.getElementById("v2DeleteCurrentAnalysisBtn");
  if (deleteCurrentBtn) {
    deleteCurrentBtn.addEventListener("click", () => {
      if (!currentAnalysis) return;
      deleteAnalysisWithConfirmation(currentAnalysis.id, currentAnalysis.filename);
    });
  }

  // History Modal Close Buttons
  const closeHistoryModalBtn = document.getElementById("v2CloseHistoryModalBtn");
  if (closeHistoryModalBtn) {
    closeHistoryModalBtn.addEventListener("click", closeHistoryModal);
  }
  const closeHistoryFooterBtn = document.getElementById("v2CloseHistoryFooterBtn");
  if (closeHistoryFooterBtn) {
    closeHistoryFooterBtn.addEventListener("click", closeHistoryModal);
  }

  // Profile Selector in Topbar
  const profileSelect = document.getElementById("v2ProfileSelect");
  if (profileSelect) {
    profileSelect.addEventListener("change", (e) => {
      selectedProfileId = e.target.value;
    });
  }

  // Export MD
  const exportBtn = document.getElementById("v2ExportBtn");
  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      if (!currentAnalysis) return;
      window.location.href = `/api/analyses/${currentAnalysis.id}/export-md`;
    });
  }

  // Search input
  const searchInput = document.getElementById("v2SearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const q = e.target.value;
      if (logViewerV2) logViewerV2.setSearchQuery(q);
      filterIncidentsList(q);
    });
  }

  // Severity Filter Chips
  const filterChips = document.querySelectorAll(".severity-chip");
  filterChips.forEach(chip => {
    chip.addEventListener("click", (e) => {
      filterChips.forEach(c => c.classList.remove("active"));
      const targetChip = e.currentTarget;
      targetChip.classList.add("active");
      activeSeverityFilter = targetChip.dataset.severity;
      filterIncidentsList(searchInput ? searchInput.value : "");
    });
  });

  // Navigation tabs (Sidebar)
  const navBtns = document.querySelectorAll(".nav-item-btn");
  navBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      navBtns.forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
    });
  });
}

function setupKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    // ⌘K or Ctrl+K -> Focus Search
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      const searchInput = document.getElementById("v2SearchInput");
      if (searchInput) searchInput.focus();
    }
    // Esc -> Close detail / blur search / close modal
    if (e.key === "Escape") {
      const searchInput = document.getElementById("v2SearchInput");
      if (document.activeElement === searchInput) {
        searchInput.blur();
      }
      closeProfileModal();
    }
  });
}

// ================= PROFILES CONTROLLER =================

async function loadProfiles(selectIdToSet = null) {
  try {
    const res = await fetch("/api/profiles");
    if (!res.ok) return;
    allProfiles = await res.json();

    const profileSelect = document.getElementById("v2ProfileSelect");
    if (!profileSelect) return;

    profileSelect.innerHTML = "";
    allProfiles.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = `${p.is_builtin ? '🔒' : '⚙️'} ${p.name}`;
      profileSelect.appendChild(opt);
    });

    if (selectIdToSet && allProfiles.some(p => p.id === selectIdToSet)) {
      selectedProfileId = selectIdToSet;
    } else if (!allProfiles.some(p => p.id === selectedProfileId)) {
      selectedProfileId = allProfiles.length > 0 ? allProfiles[0].id : "";
    }
    profileSelect.value = selectedProfileId;

  } catch (err) {
    console.error("Erro ao carregar perfis:", err);
  }
}

function setupProfileModalHandlers() {
  const manageBtn = document.getElementById("v2ManageProfilesBtn");
  const closeBtn = document.getElementById("v2CloseProfileModalBtn");
  const cancelBtn = document.getElementById("v2CancelProfileBtn");
  const newProfileBtn = document.getElementById("v2NewProfileBtn");
  const saveBtn = document.getElementById("v2SaveProfileBtn");
  const saveTopBtn = document.getElementById("v2SaveProfileTopBtn");
  const deleteBtn = document.getElementById("v2DeleteProfileBtn");
  const cloneBtn = document.getElementById("v2CloneProfileBtn");

  if (manageBtn) {
    manageBtn.addEventListener("click", () => openProfileModal());
  }

  if (closeBtn) closeBtn.addEventListener("click", () => closeProfileModal());
  if (cancelBtn) cancelBtn.addEventListener("click", () => closeProfileModal());

  if (newProfileBtn) {
    newProfileBtn.addEventListener("click", () => {
      modalSelectedProfileId = null;
      renderProfileForm(null);
    });
  }

  const handleSave = (e) => {
    e.preventDefault();
    saveProfileFromModal();
  };

  if (saveBtn) saveBtn.addEventListener("click", handleSave);
  if (saveTopBtn) saveTopBtn.addEventListener("click", handleSave);

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (!modalSelectedProfileId) return;
      deleteProfileFromModal(modalSelectedProfileId);
    });
  }

  if (cloneBtn) {
    cloneBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (!modalSelectedProfileId) return;
      cloneProfileFromModal(modalSelectedProfileId);
    });
  }
}

function openProfileModal() {
  const modal = document.getElementById("v2ProfileModal");
  if (!modal) return;
  modal.classList.add("active");
  renderProfileListInModal();

  const targetId = selectedProfileId || (allProfiles.length > 0 ? allProfiles[0].id : null);
  selectProfileInModal(targetId);
}

function closeProfileModal() {
  const modal = document.getElementById("v2ProfileModal");
  if (modal) modal.classList.remove("active");
}

function renderProfileListInModal() {
  const container = document.getElementById("v2ProfilesContainer");
  if (!container) return;
  container.innerHTML = "";

  allProfiles.forEach(p => {
    const item = document.createElement("div");
    item.className = `profile-list-item ${modalSelectedProfileId === p.id ? 'selected' : ''}`;
    item.dataset.id = p.id;

    const header = document.createElement("div");
    header.className = "profile-item-header";

    const nameSpan = document.createElement("span");
    nameSpan.className = "profile-item-name";
    nameSpan.textContent = p.name;
    header.appendChild(nameSpan);

    const actionsDiv = document.createElement("div");
    actionsDiv.className = "profile-item-actions";

    const badge = document.createElement("span");
    badge.className = `badge ${p.is_builtin ? 'badge-subtle' : 'badge-high'}`;
    badge.style.fontSize = "10px";
    badge.textContent = p.is_builtin ? 'Nativo' : 'Custom';
    actionsDiv.appendChild(badge);

    if (!p.is_builtin) {
      const delBtn = document.createElement("button");
      delBtn.className = "profile-item-delete-btn";
      delBtn.title = "Excluir perfil customizado";
      delBtn.innerHTML = "🗑️";
      delBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteProfileFromModal(p.id);
      });
      actionsDiv.appendChild(delBtn);
    }

    header.appendChild(actionsDiv);
    item.appendChild(header);

    const desc = document.createElement("div");
    desc.className = "profile-item-desc";
    desc.textContent = p.description || p.system_context || 'Sem descrição';
    item.appendChild(desc);

    item.addEventListener("click", () => {
      selectProfileInModal(p.id);
    });

    container.appendChild(item);
  });
}

function selectProfileInModal(profileId) {
  modalSelectedProfileId = profileId;
  renderProfileListInModal();

  const profile = allProfiles.find(p => p.id === profileId);
  renderProfileForm(profile);
}

function formatErrorMessage(errPayload, defaultMsg = "Erro na operação.") {
  if (!errPayload) return defaultMsg;
  if (typeof errPayload === "string") return errPayload;
  if (typeof errPayload.detail === "string") return errPayload.detail;
  if (Array.isArray(errPayload.detail)) {
    return errPayload.detail.map(d => {
      const field = d.loc && d.loc.length > 0 ? d.loc[d.loc.length - 1] : "";
      const fieldLabel = {
        "name": "Nome do Perfil",
        "criteria_baixa": "Critério Baixa",
        "criteria_media": "Critério Média",
        "criteria_critica": "Critério Crítica"
      }[field] || field;
      return fieldLabel ? `${fieldLabel}: ${d.msg}` : d.msg;
    }).join("\n");
  }
  if (errPayload.message) return errPayload.message;
  return defaultMsg;
}

function renderProfileForm(profile) {
  const titleEl = document.getElementById("v2ProfileFormTitle");
  const badgeEl = document.getElementById("v2ProfileBuiltinBadge");
  const cloneBtn = document.getElementById("v2CloneProfileBtn");
  const deleteBtn = document.getElementById("v2DeleteProfileBtn");
  const saveBtn = document.getElementById("v2SaveProfileBtn");
  const saveTopBtn = document.getElementById("v2SaveProfileTopBtn");

  const idInput = document.getElementById("v2FormProfileId");
  const nameInput = document.getElementById("v2FormProfileName");
  const descInput = document.getElementById("v2FormProfileDesc");
  const contextInput = document.getElementById("v2FormProfileContext");
  const baixaInput = document.getElementById("v2FormCriteriaBaixa");
  const mediaInput = document.getElementById("v2FormCriteriaMedia");
  const criticaInput = document.getElementById("v2FormCriteriaCritica");

  if (!profile) {
    // New profile mode
    if (titleEl) titleEl.textContent = "Novo Perfil de Gravidade";
    if (badgeEl) {
      badgeEl.textContent = "Customizado";
      badgeEl.className = "badge badge-high";
    }
    if (cloneBtn) cloneBtn.style.display = "none";
    if (deleteBtn) deleteBtn.style.display = "none";
    if (saveBtn) {
      saveBtn.style.display = "inline-flex";
      saveBtn.textContent = "💾 Criar Perfil";
    }
    if (saveTopBtn) {
      saveTopBtn.style.display = "inline-flex";
      saveTopBtn.innerHTML = "<span>💾 Criar Perfil</span>";
    }

    idInput.value = "";
    idInput.dataset.isBuiltin = "false";
    nameInput.value = "";
    nameInput.disabled = false;
    descInput.value = "";
    descInput.disabled = false;
    contextInput.value = "";
    contextInput.disabled = false;
    baixaInput.value = "";
    baixaInput.disabled = false;
    mediaInput.value = "";
    mediaInput.disabled = false;
    criticaInput.value = "";
    criticaInput.disabled = false;
    nameInput.focus();
    return;
  }

  // Existing profile mode
  const isBuiltin = Boolean(profile.is_builtin);
  if (titleEl) titleEl.textContent = isBuiltin ? `${profile.name} (Nativo)` : `Editar ${profile.name}`;
  if (badgeEl) {
    badgeEl.textContent = isBuiltin ? "Nativo (Gera Cópia ao Salvar)" : "Customizado";
    badgeEl.className = isBuiltin ? "badge badge-subtle" : "badge badge-high";
  }

  if (cloneBtn) cloneBtn.style.display = "inline-flex";
  if (deleteBtn) deleteBtn.style.display = isBuiltin ? "none" : "inline-flex";
  
  if (saveBtn) {
    saveBtn.style.display = "inline-flex";
    saveBtn.textContent = isBuiltin ? "💾 Salvar Como Novo Perfil" : "💾 Salvar Alterações";
  }
  if (saveTopBtn) {
    saveTopBtn.style.display = "inline-flex";
    saveTopBtn.innerHTML = `<span>${isBuiltin ? '💾 Salvar Como Novo Perfil' : '💾 Salvar Alterações'}</span>`;
  }

  idInput.value = profile.id;
  idInput.dataset.isBuiltin = isBuiltin ? "true" : "false";
  nameInput.value = profile.name;
  nameInput.disabled = false;
  descInput.value = profile.description || "";
  descInput.disabled = false;
  contextInput.value = profile.system_context || "";
  contextInput.disabled = false;
  baixaInput.value = profile.criteria_baixa;
  baixaInput.disabled = false;
  mediaInput.value = profile.criteria_media;
  mediaInput.disabled = false;
  criticaInput.value = profile.criteria_critica;
  criticaInput.disabled = false;
}

async function saveProfileFromModal() {
  const idInput = document.getElementById("v2FormProfileId");
  const nameInput = document.getElementById("v2FormProfileName");
  const descInput = document.getElementById("v2FormProfileDesc");
  const contextInput = document.getElementById("v2FormProfileContext");
  const baixaInput = document.getElementById("v2FormCriteriaBaixa");
  const mediaInput = document.getElementById("v2FormCriteriaMedia");
  const criticaInput = document.getElementById("v2FormCriteriaCritica");

  let name = nameInput.value.trim();
  const desc = descInput.value.trim();
  const ctx = contextInput.value.trim();
  const baixa = baixaInput.value.trim();
  const media = mediaInput.value.trim();
  const critica = criticaInput.value.trim();

  if (!name) {
    alert("O Nome do Perfil é obrigatório.");
    nameInput.focus();
    return;
  }
  if (!baixa) {
    alert("O Critério de Gravidade BAIXA é obrigatório.");
    baixaInput.focus();
    return;
  }
  if (!media) {
    alert("O Critério de Gravidade MÉDIA é obrigatório.");
    mediaInput.focus();
    return;
  }
  if (!critica) {
    alert("O Critério de Gravidade CRÍTICA é obrigatório.");
    criticaInput.focus();
    return;
  }

  const profileId = idInput.value.trim();
  const isBuiltin = idInput.dataset.isBuiltin === "true";
  const isNew = !profileId || isBuiltin;

  if (isBuiltin) {
    const orig = allProfiles.find(p => p.id === profileId);
    if (orig && name === orig.name) {
      name = `${name} (Personalizado)`;
    }
  }

  const payload = {
    name,
    description: desc,
    system_context: ctx,
    criteria_baixa: baixa,
    criteria_media: media,
    criteria_critica: critica
  };

  try {
    let res;
    if (isNew) {
      res = await fetch("/api/profiles", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch(`/api/profiles/${profileId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    }

    if (!res.ok) {
      const errPayload = await res.json().catch(() => ({ detail: "Falha ao salvar" }));
      throw new Error(formatErrorMessage(errPayload, "Erro ao salvar perfil."));
    }

    const savedProfile = await res.json();
    await loadProfiles(savedProfile.id);
    modalSelectedProfileId = savedProfile.id;
    renderProfileListInModal();
    renderProfileForm(savedProfile);
  } catch (err) {
    alert(err.message);
  }
}

async function cloneProfileFromModal(profileId) {
  const source = allProfiles.find(p => p.id === profileId);
  const newName = prompt("Nome para a cópia do perfil:", `${source ? source.name : 'Perfil'} (Cópia)`);
  if (!newName || !newName.trim()) return;

  try {
    const res = await fetch(`/api/profiles/${profileId}/clone`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName.trim() })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Falha ao clonar" }));
      throw new Error(formatErrorMessage(err, "Erro ao clonar perfil."));
    }

    const cloned = await res.json();
    await loadProfiles(cloned.id);
    selectProfileInModal(cloned.id);
  } catch (err) {
    alert(err.message);
  }
}

async function deleteProfileFromModal(profileId) {
  if (!confirm("Tem certeza que deseja excluir este perfil customizado?")) return;

  try {
    const res = await fetch(`/api/profiles/${profileId}`, { method: "DELETE" });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Falha ao excluir" }));
      throw new Error(formatErrorMessage(err, "Erro ao excluir perfil."));
    }

    await loadProfiles();
    const fallbackId = allProfiles.length > 0 ? allProfiles[0].id : null;
    selectProfileInModal(fallbackId);
  } catch (err) {
    alert(err.message);
  }
}

// ================= ANALYSES & UPLOAD =================

let cachedHistory = [];
let confirmDialogResolver = null;

function showConfirmDialog(title, message, confirmText = "Excluir Definitivamente") {
  return new Promise((resolve) => {
    const modal = document.getElementById("v2ConfirmModal");
    const titleEl = document.getElementById("v2ConfirmTitle");
    const msgEl = document.getElementById("v2ConfirmMessage");
    const acceptBtn = document.getElementById("v2ConfirmAcceptBtn");
    const cancelBtn = document.getElementById("v2ConfirmCancelBtn");

    if (titleEl) titleEl.textContent = title;
    if (msgEl) msgEl.textContent = message;
    if (acceptBtn) acceptBtn.textContent = confirmText;

    const cleanup = () => {
      if (modal) modal.classList.remove("active");
      if (acceptBtn) acceptBtn.onclick = null;
      if (cancelBtn) cancelBtn.onclick = null;
    };

    if (acceptBtn) {
      acceptBtn.onclick = () => {
        cleanup();
        resolve(true);
      };
    }

    if (cancelBtn) {
      cancelBtn.onclick = () => {
        cleanup();
        resolve(false);
      };
    }

    if (modal) modal.classList.add("active");
  });
}

function openHistoryModal() {
  const modal = document.getElementById("v2HistoryModal");
  if (modal) {
    modal.classList.add("active");
    renderHistoryModalList(cachedHistory);
  }
}

function closeHistoryModal() {
  const modal = document.getElementById("v2HistoryModal");
  if (modal) modal.classList.remove("active");
}

function renderHistoryModalList(items) {
  const container = document.getElementById("v2HistoryTableContainer");
  const badge = document.getElementById("v2HistoryCountBadge");
  if (!container) return;

  if (badge) badge.textContent = `${(items || []).length} análise(s)`;

  if (!items || items.length === 0) {
    container.innerHTML = `
      <div class="history-empty-state">
        <div class="history-empty-icon">📁</div>
        <div style="font-weight: 600; color: var(--text-primary); font-size: 14px;">Nenhuma análise salva no histórico</div>
        <div style="font-size: 12.5px; max-width: 360px;">Importe um arquivo de log para analisar incidentes com a inteligência Laya.</div>
      </div>
    `;
    return;
  }

  container.innerHTML = "";
  const fragment = document.createDocumentFragment();

  items.forEach(item => {
    const card = document.createElement("div");
    const isActive = currentAnalysis && currentAnalysis.id === item.id;
    card.className = `history-card-item ${isActive ? 'active-item' : ''}`;

    const profName = item.profile_name ? `<span class="badge badge-subtle">🎯 ${escapeHTML(item.profile_name)}</span>` : '';
    const critBadgeClass = (item.critical_errors || 0) > 0 ? 'badge-critical' : 'badge-low';
    const linesFmt = Number(item.total_lines).toLocaleString("pt-BR");
    const errorsFmt = Number(item.total_errors).toLocaleString("pt-BR");
    const critFmt = Number(item.critical_errors).toLocaleString("pt-BR");

    card.innerHTML = `
      <div class="history-card-info">
        <div class="history-card-title-row">
          <span class="history-card-filename">📄 ${escapeHTML(item.filename)}</span>
          ${profName}
          ${isActive ? '<span class="badge badge-brand">Ativo</span>' : ''}
        </div>
        <div class="history-card-date">🕒 ${escapeHTML(item.created_at)}</div>
        <div class="history-card-metrics">
          <span class="history-metric-badge">📏 ${linesFmt} linhas</span>
          <span class="history-metric-badge">⚠️ ${errorsFmt} erros</span>
          <span class="badge ${critBadgeClass}">🔴 ${critFmt} críticos</span>
          <span class="history-metric-badge">⚡ ${item.unavailability_rate || 0}% indisponibilidade</span>
        </div>
      </div>
      <div class="history-card-actions">
        <button class="btn btn-secondary btn-sm btn-load-history" data-id="${item.id}" title="Carregar esta análise">
          <span>Abrir</span>
        </button>
        <button class="btn btn-ghost btn-icon btn-delete-history" data-id="${item.id}" data-filename="${escapeHTML(item.filename)}" title="Excluir permanentemente" style="color: var(--critical-solid); padding: 5px 8px;">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </button>
      </div>
    `;

    // Bind action events
    const loadBtn = card.querySelector(".btn-load-history");
    if (loadBtn) {
      loadBtn.addEventListener("click", () => {
        closeHistoryModal();
        loadAnalysisById(item.id);
      });
    }

    const deleteBtn = card.querySelector(".btn-delete-history");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteAnalysisWithConfirmation(item.id, item.filename);
      });
    }

    fragment.appendChild(card);
  });

  container.appendChild(fragment);
}

async function deleteAnalysisWithConfirmation(analysisId, filename = "esta análise") {
  const confirmed = await showConfirmDialog(
    "Confirmar Exclusão de Análise",
    `Tem certeza de que deseja excluir permanentemente "${filename}"? Esta ação removerá definitivamente o registro do histórico e o arquivo físico de log do servidor.`,
    "Excluir Definitivamente"
  );

  if (!confirmed) return;

  try {
    const res = await fetch(`/api/analyses/${analysisId}`, {
      method: "DELETE"
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Falha ao excluir" }));
      throw new Error(err.detail || "Erro ao excluir análise.");
    }

    // If the active analysis was deleted, clear the UI
    if (currentAnalysis && currentAnalysis.id === analysisId) {
      clearV2Analysis();
    }

    await loadHistory();
  } catch (err) {
    alert(`Erro ao excluir análise: ${err.message}`);
  }
}

function clearV2Analysis() {
  currentAnalysis = null;
  selectedIncident = null;

  const contextFilename = document.getElementById("v2ContextFilename");
  if (contextFilename) contextFilename.textContent = "Nenhum log importado";

  const breadcrumbFile = document.getElementById("v2BreadcrumbFile");
  if (breadcrumbFile) breadcrumbFile.textContent = "Nenhum log selecionado";

  const kpiLines = document.getElementById("v2KpiLines");
  const kpiErrors = document.getElementById("v2KpiErrors");
  const kpiCritical = document.getElementById("v2KpiCritical");
  const kpiUnavail = document.getElementById("v2KpiUnavail");

  if (kpiLines) kpiLines.textContent = "-";
  if (kpiErrors) kpiErrors.textContent = "-";
  if (kpiCritical) kpiCritical.textContent = "-";
  if (kpiUnavail) kpiUnavail.textContent = "-";

  const countAll = document.getElementById("chipCountAll");
  const countCrit = document.getElementById("chipCountCrit");
  const countHigh = document.getElementById("chipCountHigh");
  const countMed = document.getElementById("chipCountMed");
  const countLow = document.getElementById("chipCountLow");

  if (countAll) countAll.textContent = "0";
  if (countCrit) countCrit.textContent = "0";
  if (countHigh) countHigh.textContent = "0";
  if (countMed) countMed.textContent = "0";
  if (countLow) countLow.textContent = "0";

  if (logViewerV2) {
    logViewerV2.setAnalysis(null, 0);
  }

  renderIncidentsList([]);
  renderEmptyDetail();

  const exportBtn = document.getElementById("v2ExportBtn");
  if (exportBtn) exportBtn.setAttribute("disabled", "true");

  const deleteCurrentBtn = document.getElementById("v2DeleteCurrentAnalysisBtn");
  if (deleteCurrentBtn) deleteCurrentBtn.style.display = "none";

  const historySelect = document.getElementById("v2HistorySelect");
  if (historySelect) historySelect.value = "";
}

async function loadHistory() {
  try {
    const res = await fetch("/api/analyses");
    if (!res.ok) return;
    const items = await res.json();
    cachedHistory = items;

    const select = document.getElementById("v2HistorySelect");
    if (select) {
      select.innerHTML = '<option value="">-- Histórico de Análises --</option>';
      items.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item.id;
        const profName = item.profile_name ? ` · 🎯 ${item.profile_name}` : '';
        opt.textContent = `${item.filename} (${item.created_at})${profName} - ${item.total_errors} erros`;
        select.appendChild(opt);
      });

      if (currentAnalysis) {
        select.value = currentAnalysis.id;
      }
    }

    const historyModal = document.getElementById("v2HistoryModal");
    if (historyModal && historyModal.classList.contains("active")) {
      renderHistoryModalList(items);
    }
  } catch (err) {
    console.error("Erro ao carregar histórico:", err);
  }
}

function showLoadingOverlay(filename = "Arquivo de log") {
  const overlay = document.getElementById("v2LoadingModal");
  const filenameEl = document.getElementById("v2ProgressFilename");
  const statusEl = document.getElementById("v2ProgressStatus");
  const percentEl = document.getElementById("v2ProgressPercent");
  const fillEl = document.getElementById("v2ProgressFill");

  if (filenameEl) filenameEl.textContent = filename;
  if (statusEl) statusEl.textContent = "Iniciando análise semântica...";
  if (percentEl) percentEl.textContent = "0%";
  if (fillEl) fillEl.style.width = "0%";

  if (overlay) overlay.classList.add("active");
}

function updateProgress(percent, message) {
  const statusEl = document.getElementById("v2ProgressStatus");
  const percentEl = document.getElementById("v2ProgressPercent");
  const fillEl = document.getElementById("v2ProgressFill");

  if (fillEl) fillEl.style.width = `${percent}%`;
  if (percentEl) percentEl.textContent = `${percent}%`;
  if (statusEl && message) statusEl.textContent = message;
}

function hideLoadingOverlay() {
  const overlay = document.getElementById("v2LoadingModal");
  if (overlay) overlay.classList.remove("active");
}

function renderOccurrencePillsHtml(lines, limit = 50) {
  if (!lines || lines.length === 0) return `<span style="font-size: 11.5px; color: var(--text-muted);">Nenhuma linha registrada</span>`;
  const visible = lines.slice(0, limit);
  const remaining = lines.length - limit;
  let html = visible.map(lineNum => `
    <button class="occurrence-pill" onclick="jumpToLogLine(${lineNum})" title="Ir para linha ${lineNum}">
      Linha ${lineNum}
    </button>
  `).join("");
  if (remaining > 0) {
    html += `
      <button class="occurrence-pill" id="btnShowMoreOccurrences" onclick="showAllOccurrencesForSelected()" style="background: var(--bg-hover); font-weight: 600; color: var(--accent-primary);" title="Carregar mais ${remaining} ocorrências">
        + ${remaining} mais...
      </button>
    `;
  }
  return html;
}

window.showAllOccurrencesForSelected = function() {
  if (!selectedIncident || !selectedIncident.lines) return;
  const grid = document.getElementById("v2OccurrencesGrid");
  if (!grid) return;
  const allPills = selectedIncident.lines.map(lineNum => `
    <button class="occurrence-pill" onclick="jumpToLogLine(${lineNum})" title="Ir para linha ${lineNum}">
      Linha ${lineNum}
    </button>
  `).join("");
  grid.innerHTML = allPills;
};

async function handleFileUpload(file) {
  showLoadingOverlay(file.name);
  const formData = new FormData();
  formData.append("file", file);
  if (selectedProfileId) {
    formData.append("profile_id", selectedProfileId);
  }

  uploadAbortController = new AbortController();

  try {
    const res = await fetch("/api/analyze-stream", {
      method: "POST",
      body: formData,
      signal: uploadAbortController.signal
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Falha na análise" }));
      throw new Error(err.detail || "Falha ao processar análise do log.");
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
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const event = JSON.parse(line);
          if (event.type === "progress") {
            updateProgress(event.percent, event.message);
          } else if (event.type === "complete") {
            completedData = event.data;
          } else if (event.type === "error") {
            throw new Error(event.message || "Erro no processamento");
          }
        } catch (parseErr) {
          if (parseErr.message && !parseErr.message.includes("JSON")) {
            throw parseErr;
          }
          console.error("Erro no stream event:", parseErr, line);
        }
      }
    }

    if (buffer && buffer.trim()) {
      try {
        const event = JSON.parse(buffer.trim());
        if (event.type === "complete") {
          completedData = event.data;
        } else if (event.type === "error") {
          throw new Error(event.message || "Erro no processamento");
        }
      } catch (parseErr) {
        if (parseErr.message && !parseErr.message.includes("JSON")) {
          throw parseErr;
        }
        console.error("Erro no residual do stream:", parseErr, buffer);
      }
    }

    hideLoadingOverlay();

    if (completedData) {
      requestAnimationFrame(() => {
        displayV2Analysis(completedData);
        loadHistory().then(() => {
          const sel = document.getElementById("v2HistorySelect");
          if (sel) sel.value = completedData.id;
        });
      });
    } else {
      throw new Error("O servidor encerrou o processamento sem retornar os dados completos.");
    }

  } catch (err) {
    hideLoadingOverlay();
    if (err.name === "AbortError") {
      console.log("Upload cancelado pelo usuário.");
      return;
    }
    alert(`Erro na análise: ${err.message}`);
    console.error(err);
  } finally {
    uploadAbortController = null;
    hideLoadingOverlay();
    const fileInput = document.getElementById("v2FileInput");
    if (fileInput) fileInput.value = "";
  }
}

async function loadAnalysisById(id) {
  showLoadingOverlay("Carregando análise...");
  updateProgress(50, "Buscando dados no banco de dados...");

  try {
    const res = await fetch(`/api/analyses/${id}`);
    if (!res.ok) throw new Error("Análise não encontrada.");
    const data = await res.json();
    hideLoadingOverlay();
    requestAnimationFrame(() => {
      displayV2Analysis(data);
    });
  } catch (err) {
    hideLoadingOverlay();
    alert(err.message);
    await loadHistory();
  } finally {
    hideLoadingOverlay();
  }
}

function displayV2Analysis(data) {
  currentAnalysis = data;

  // 1. Update Context in Sidebar & Topbar
  const contextFilename = document.getElementById("v2ContextFilename");
  if (contextFilename) contextFilename.textContent = data.filename || "log.txt";

  const breadcrumbFile = document.getElementById("v2BreadcrumbFile");
  if (breadcrumbFile) {
    const profileTag = data.profile_snapshot ? ` [🎯 ${data.profile_snapshot.profile_name}]` : '';
    breadcrumbFile.textContent = `${data.filename || "log.txt"}${profileTag}`;
  }

  // 2. Update KPIs
  const stats = data.stats;
  const kpiLines = document.getElementById("v2KpiLines");
  const kpiErrors = document.getElementById("v2KpiErrors");
  const kpiCritical = document.getElementById("v2KpiCritical");
  const kpiUnavail = document.getElementById("v2KpiUnavail");

  if (kpiLines) kpiLines.textContent = Number(stats.total_lines).toLocaleString("pt-BR");
  if (kpiErrors) kpiErrors.textContent = Number(stats.total_errors).toLocaleString("pt-BR");
  if (kpiCritical) kpiCritical.textContent = Number(stats.critical_errors).toLocaleString("pt-BR");
  if (kpiUnavail) kpiUnavail.textContent = `${stats.unavailability_rate}%`;

  // 3. Update Severity Counts on Chips
  const countAll = document.getElementById("chipCountAll");
  const countCrit = document.getElementById("chipCountCrit");
  const countHigh = document.getElementById("chipCountHigh");
  const countMed = document.getElementById("chipCountMed");
  const countLow = document.getElementById("chipCountLow");

  if (countAll) countAll.textContent = (data.incidents || []).length;
  if (countCrit) countCrit.textContent = stats.severity_counts["Crítica"] || 0;
  if (countHigh) countHigh.textContent = stats.severity_counts["Alta"] || 0;
  if (countMed) countMed.textContent = stats.severity_counts["Média"] || 0;
  if (countLow) countLow.textContent = stats.severity_counts["Baixa"] || 0;

  // 4. Populate Log Viewer
  if (logViewerV2 && data.id) {
    logViewerV2.setAnalysis(data.id, data.total_lines);
  }

  // 5. Render Incident List
  renderIncidentsList(data.incidents || []);

  // 6. Select first incident by default if available
  if (data.incidents && data.incidents.length > 0) {
    selectIncident(data.incidents[0]);
  } else {
    renderEmptyDetail();
  }

  // 7. Enable Export & Show Delete Current Analysis Button
  const exportBtn = document.getElementById("v2ExportBtn");
  if (exportBtn) exportBtn.removeAttribute("disabled");

  const deleteCurrentBtn = document.getElementById("v2DeleteCurrentAnalysisBtn");
  if (deleteCurrentBtn) deleteCurrentBtn.style.display = "inline-flex";
}

function renderIncidentsList(incidents) {
  const container = document.getElementById("v2IncidentsContainer");
  if (!container) return;
  container.innerHTML = "";

  if (!incidents || incidents.length === 0) {
    container.innerHTML = `
      <div class="empty-state-card">
        <svg class="empty-state-icon" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="empty-state-title">Nenhum erro encontrado</div>
        <div class="empty-state-desc">O arquivo de log analisado não apresenta erros ou falhas registradas.</div>
      </div>
    `;
    return;
  }

  const fragment = document.createDocumentFragment();

  incidents.forEach((inc) => {
    const row = document.createElement("div");
    const gravSlug = inc.gravidade === 3 ? "critical" : (inc.gravidade === 2 ? "medium" : "low");
    const badgeClass = inc.gravidade === 3 ? "badge-critical" : (inc.gravidade === 2 ? "badge-medium" : "badge-low");

    row.className = `incident-row-card ${selectedIncident && selectedIncident.id === inc.id ? 'selected' : ''}`;
    row.dataset.id = inc.id;
    row.dataset.severity = gravSlug;
    row.dataset.search = (inc.title + " " + inc.setor + " " + inc.tipo_falha + " " + (inc.technical_summary || "")).toLowerCase();

    row.innerHTML = `
      <div class="incident-top-line">
        <div class="incident-human-title">${escapeHTML(inc.title)}</div>
        <span class="badge ${badgeClass}">${escapeHTML(inc.gravidade_label.toUpperCase())}</span>
      </div>
      <div class="incident-tech-line">
        🏢 ${escapeHTML(inc.setor)} · 🏷️ ${escapeHTML(inc.tipo_falha)}
      </div>
      <div class="incident-badges-line">
        <span class="badge badge-subtle">🔁 ${inc.total_occurrences} ocorrência(s)</span>
        <span class="badge badge-subtle">Linha ${inc.first_seen_line}</span>
        ${inc.causa_indisponibilidade ? '<span class="badge badge-critical">Indisponibilidade</span>' : ''}
      </div>
    `;

    row.addEventListener("click", () => {
      document.querySelectorAll(".incident-row-card").forEach(r => r.classList.remove("selected"));
      row.classList.add("selected");
      selectIncident(inc);
    });

    fragment.appendChild(row);
  });

  container.appendChild(fragment);

  // Micro-animation with GSAP only if <= 25 items to keep UI buttery smooth
  if (window.gsap && incidents.length <= 25) {
    gsap.from(".incident-row-card", {
      opacity: 0,
      y: 6,
      duration: 0.15,
      stagger: 0.02,
      ease: "power2.out"
    });
  }
}

function filterIncidentsList(query = "") {
  const q = (query || "").toLowerCase();
  const rows = document.querySelectorAll(".incident-row-card");

  rows.forEach(row => {
    const rowSeverity = row.dataset.severity;
    const rowText = row.dataset.search || "";

    const matchesSeverity = (activeSeverityFilter === "all" || rowSeverity === activeSeverityFilter);
    const matchesSearch = (!q || rowText.includes(q));

    if (matchesSeverity && matchesSearch) {
      row.style.display = "flex";
    } else {
      row.style.display = "none";
    }
  });
}

function selectIncident(inc) {
  selectedIncident = inc;
  const container = document.getElementById("v2DetailContainer");
  if (!container) return;

  const gravBadgeClass = inc.gravidade === 3 ? "badge-critical" : (inc.gravidade === 2 ? "badge-medium" : "badge-low");
  const occurrencePills = renderOccurrencePillsHtml(inc.lines, 50);

  const stacktrace = inc.sample_stacktrace || inc.sample_raw || "Nenhum stacktrace registrado para esta ocorrência.";

  const profileSnap = currentAnalysis && currentAnalysis.profile_snapshot;
  const profileInfoHtml = profileSnap ? `
    <div style="font-size: 11.5px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; padding: 4px 8px; background: var(--bg-app); border-radius: var(--radius-sm); border: 1px solid var(--border-soft);">
      <span>🎯 <strong>Perfil de Calibração:</strong> ${escapeHTML(profileSnap.profile_name)}</span>
    </div>
  ` : '';

  container.innerHTML = `
    <!-- Top Metadata -->
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;">
        <h3 style="font-size: 16px; font-weight: 600; color: var(--text-primary); line-height: 22px;">
          ${escapeHTML(inc.title)}
        </h3>
        <span class="badge ${gravBadgeClass}">
          ${escapeHTML(inc.gravidade_label.toUpperCase())}
        </span>
      </div>

      <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
        <span class="badge badge-subtle">Setor: <strong>${escapeHTML(inc.setor)}</strong></span>
        <span class="badge badge-subtle">Falha: <strong>${escapeHTML(inc.tipo_falha)}</strong></span>
        <span class="badge badge-subtle">1ª vez: <strong>${inc.first_seen_time || 'N/D'}</strong></span>
        ${inc.causa_indisponibilidade ? '<span class="badge badge-critical">Afeta Disponibilidade do Sistema</span>' : '<span class="badge badge-subtle">Sem Indisponibilidade Geral</span>'}
      </div>
      ${profileInfoHtml}
    </div>

    <!-- Calm Laya AI Card -->
    <div class="laya-ai-card">
      <div class="laya-ai-header">
        <span class="sparkle">✦</span>
        <span>Laya AI Observability Engine</span>
      </div>

      <div class="ai-field-group">
        <span class="ai-field-label">Resumo do Diagnóstico</span>
        <div class="ai-field-text">${escapeHTML(inc.technical_summary || 'Diagnóstico preliminar gerado.')}</div>
      </div>

      <div class="ai-field-group">
        <span class="ai-field-label">Ação Sugerida / Recomendação</span>
        <div class="ai-recommendation-box">
          💡 ${escapeHTML(inc.recommendation || 'Verificar parâmetros de entrada e isolar o ponto de falha.')}
        </div>
      </div>
    </div>

    <!-- Occurrences Jump Grid -->
    <div style="display: flex; flex-direction: column; gap: 6px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
        <span class="ai-field-label">Ocorrências (${inc.lines.length}x) — Clique para inspecionar</span>
        <div style="display: flex; align-items: center; gap: 6px;">
          <input type="number" id="directLineJump" placeholder="Ir p/ linha..." min="1" class="input-field" style="width: 84px; height: 26px; font-size: 11px; padding: 2px 6px;" onkeydown="if(event.key==='Enter'){const v=parseInt(this.value);if(v)jumpToLogLine(v);}">
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; font-size: 11px; height: 26px;" onclick="const v=parseInt(document.getElementById('directLineJump').value);if(v)jumpToLogLine(v);">Ir</button>
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; font-size: 11px; height: 26px;" onclick="jumpToLogLine(${inc.first_seen_line})">
            📍 1ª (${inc.first_seen_line})
          </button>
        </div>
      </div>
      <div class="occurrences-grid" id="v2OccurrencesGrid">
        ${occurrencePills}
      </div>
    </div>

    <!-- Stacktrace Section -->
    <div style="display: flex; flex-direction: column; gap: 6px;">
      <div class="code-box-header">
        <span class="ai-field-label">Evidência / Stacktrace</span>
        <button class="btn btn-ghost btn-sm" onclick="copyStacktrace()" id="btnCopyCode" style="font-size: 11px;">
          Copiar
        </button>
      </div>
      <div class="code-box" id="stacktraceText">${escapeHTML(stacktrace)}</div>
    </div>
  `;

  // Animate detail panel in smoothly
  if (window.gsap) {
    gsap.from(container.children, {
      opacity: 0,
      y: 6,
      duration: 0.15,
      stagger: 0.02,
      ease: "power2.out"
    });
  }
}

function renderEmptyDetail() {
  const container = document.getElementById("v2DetailContainer");
  if (!container) return;
  container.innerHTML = `
    <div class="empty-state-card">
      <svg class="empty-state-icon" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
      </svg>
      <div class="empty-state-title">Nenhum incidente selecionado</div>
      <div class="empty-state-desc">Selecione um erro na lista ao lado para visualizar a análise completa da Laya AI.</div>
    </div>
  `;
}

function jumpToLogLine(lineNumber) {
  if (logViewerV2) {
    logViewerV2.scrollToLine(lineNumber, true);
  }
}

function copyStacktrace() {
  const codeBox = document.getElementById("stacktraceText");
  const copyBtn = document.getElementById("btnCopyCode");
  if (!codeBox) return;

  navigator.clipboard.writeText(codeBox.textContent || "").then(() => {
    if (copyBtn) {
      const origText = copyBtn.textContent;
      copyBtn.textContent = "Copiado!";
      setTimeout(() => { copyBtn.textContent = origText; }, 2000);
    }
  }).catch(err => {
    console.error("Falha ao copiar:", err);
  });
}

function escapeHTML(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
