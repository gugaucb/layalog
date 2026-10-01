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
const i18nT = (key, fallback) => (window.LayaI18n ? window.LayaI18n.t(key, fallback) : (fallback || key));

document.addEventListener("DOMContentLoaded", () => {
  if (window.LayaI18n) {
    window.LayaI18n.applyTranslations();
  }
  initV2App();
  loadProfiles();
  loadHistory();
  setupKeyboardShortcuts();
  setupProfileModalHandlers();
  if (window.checkAutoTour) {
    window.checkAutoTour();
  }
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

  // Close modals on backdrop click
  const historyModal = document.getElementById("v2HistoryModal");
  if (historyModal) {
    historyModal.addEventListener("click", (e) => {
      if (e.target === historyModal) closeHistoryModal();
    });
  }

  // Driver.js Tour Button
  const tourBtn = document.getElementById("v2TourBtn");
  if (tourBtn) {
    tourBtn.addEventListener("click", () => {
      if (window.startLayaTour) {
        window.startLayaTour();
      }
    });
  }

  // Language Selector
  const langSelect = document.getElementById("v2LangSelect");
  if (langSelect) {
    if (window.LayaI18n) {
      langSelect.value = window.LayaI18n.getCurrentLang();
    }
    langSelect.addEventListener("change", (e) => {
      if (window.LayaI18n) {
        window.LayaI18n.setLanguage(e.target.value);
      }
    });
  }

  // Language Change Event Dispatcher Callback
  window.addEventListener("layalog-language-changed", () => {
    if (currentAnalysis) {
      if (selectedIncident) {
        selectIncident(selectedIncident);
      } else {
        renderEmptyDetail();
      }
    } else {
      clearV2Analysis();
    }
    if (allProfiles && allProfiles.length > 0) {
      populateProfileDropdown();
    }
  });

  const confirmModal = document.getElementById("v2ConfirmModal");
  if (confirmModal) {
    confirmModal.addEventListener("click", (e) => {
      if (e.target === confirmModal) {
        confirmModal.classList.remove("active");
        if (confirmDialogResolver) confirmDialogResolver(false);
      }
    });
  }
}

function setupKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    // ⌘K or Ctrl+K -> Focus Search
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      const searchInput = document.getElementById("v2SearchInput");
      if (searchInput) searchInput.focus();
    }
    // Esc -> Close detail / blur search / close modals
    if (e.key === "Escape") {
      const searchInput = document.getElementById("v2SearchInput");
      if (document.activeElement === searchInput) {
        searchInput.blur();
      }
      closeProfileModal();
      closeHistoryModal();
      const confirmModal = document.getElementById("v2ConfirmModal");
      if (confirmModal && confirmModal.classList.contains("active")) {
        confirmModal.classList.remove("active");
        if (confirmDialogResolver) confirmDialogResolver(false);
      }
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
    loadHistory();
  }
}

function closeHistoryModal() {
  const modal = document.getElementById("v2HistoryModal");
  if (modal) modal.classList.remove("active");
}

window.openHistoryModal = openHistoryModal;
window.closeHistoryModal = closeHistoryModal;
window.showConfirmDialog = showConfirmDialog;
window.deleteAnalysisWithConfirmation = deleteAnalysisWithConfirmation;

function renderHistoryModalList(items) {
  const container = document.getElementById("v2HistoryTableContainer");
  const badge = document.getElementById("v2HistoryCountBadge");
  if (!container) return;

  if (badge) badge.textContent = `${(items || []).length}`;

  if (!items || items.length === 0) {
    container.innerHTML = `
      <div class="history-empty-state">
        <div class="history-empty-icon">📁</div>
        <div style="font-weight: 600; color: var(--text-primary); font-size: 14px;">${i18nT("history.emptyTitle", "No analyses saved in history")}</div>
        <div style="font-size: 12.5px; max-width: 360px;">${i18nT("history.emptyDesc", "Import a log file to analyze incidents with Laya AI intelligence.")}</div>
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
    const linesFmt = Number(item.total_lines).toLocaleString();
    const errorsFmt = Number(item.total_errors).toLocaleString();
    const critFmt = Number(item.critical_errors).toLocaleString();

    card.innerHTML = `
      <div class="history-card-info">
        <div class="history-card-title-row">
          <span class="history-card-filename">📄 ${escapeHTML(item.filename)}</span>
          ${profName}
          ${isActive ? `<span class="badge badge-brand">${i18nT("history.activeBadge", "Active")}</span>` : ''}
        </div>
        <div class="history-card-date">🕒 ${escapeHTML(item.created_at)}</div>
        <div class="history-card-metrics">
          <span class="history-metric-badge">📏 ${linesFmt} ${i18nT("history.lines", "lines")}</span>
          <span class="history-metric-badge">⚠️ ${errorsFmt} ${i18nT("history.errors", "errors")}</span>
          <span class="badge ${critBadgeClass}">🔴 ${critFmt} ${i18nT("history.critical", "critical")}</span>
          <span class="history-metric-badge">⚡ ${item.unavailability_rate || 0}% ${i18nT("history.unavail", "unavailability")}</span>
        </div>
      </div>
      <div class="history-card-actions">
        <button class="btn btn-secondary btn-sm btn-load-history" data-id="${item.id}" title="${i18nT("history.open", "Open")}">
          <span>${i18nT("history.open", "Open")}</span>
        </button>
        <button class="btn btn-ghost btn-icon btn-delete-history" data-id="${item.id}" data-filename="${escapeHTML(item.filename)}" title="${i18nT("history.delete", "Delete")}" style="color: var(--critical-solid); padding: 5px 8px;">
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

async function deleteAnalysisWithConfirmation(analysisId, filename = "this analysis") {
  const msgTemplate = i18nT("confirm.deleteMsg", 'Are you sure you want to permanently delete "{filename}"? This action will completely remove the history record and physical log file from the server.');
  const confirmed = await showConfirmDialog(
    i18nT("confirm.deleteTitle", "Confirm Analysis Deletion"),
    msgTemplate.replace("{filename}", filename),
    i18nT("btn.confirmDelete", "Delete Permanently")
  );

  if (!confirmed) return;

  try {
    const res = await fetch(`/api/analyses/${analysisId}`, {
      method: "DELETE"
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to delete" }));
      throw new Error(err.detail || "Error deleting analysis.");
    }

    // If the active analysis was deleted, clear the UI
    if (currentAnalysis && currentAnalysis.id === analysisId) {
      clearV2Analysis();
    }

    await loadHistory();
  } catch (err) {
    alert(`Error deleting analysis: ${err.message}`);
  }
}

function clearV2Analysis() {
  currentAnalysis = null;
  selectedIncident = null;

  const contextFilename = document.getElementById("v2ContextFilename");
  if (contextFilename) contextFilename.textContent = i18nT("nav.noActiveLog", "No active log");

  const breadcrumbFile = document.getElementById("v2BreadcrumbFile");
  if (breadcrumbFile) breadcrumbFile.textContent = i18nT("breadcrumb.selectFile", "Select a file");

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
      select.innerHTML = `<option value="">${i18nT("history.defaultOption", "-- Analysis History --")}</option>`;
      items.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item.id;
        const profName = item.profile_name ? ` · 🎯 ${item.profile_name}` : '';
        opt.textContent = `${item.filename} (${item.created_at})${profName} - ${item.total_errors} ${i18nT("history.errors", "errors")}`;
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
    console.error("Error loading history:", err);
  }
}

/* ==========================================================================
   LayaLog V2 — Processing Modal Canvas Animation Engine
   ========================================================================== */

let animRafId = null;
let animParticles = [];
let animCounts = { low: 0, medium: 0, high: 0 };
let animLastTime = 0;
let animSpawnTimer = 0;

const ANIM_PRIORITIES = [
  { name: "low", color: "#10B981", weight: 0.50 },
  { name: "medium", color: "#F59E0B", weight: 0.35 },
  { name: "critical", color: "#EF4444", weight: 0.15 }
];

class ProcessingDocParticle {
  constructor(canvasWidth, canvasHeight, explicitSeverity = null) {
    this.w = canvasWidth;
    this.h = canvasHeight;
    this.cx = canvasWidth / 2;
    this.cy = canvasHeight / 2 - 25;

    if (explicitSeverity && ["low", "medium", "critical"].includes(explicitSeverity)) {
      this.priority = explicitSeverity;
      const match = ANIM_PRIORITIES.find(p => p.name === explicitSeverity);
      this.color = match ? match.color : "#10B981";
    } else {
      // Pick priority weighted for ambient particles
      const r = Math.random();
      let acc = 0;
      this.priority = "low";
      this.color = "#10B981";
      for (const p of ANIM_PRIORITIES) {
        acc += p.weight;
        if (r <= acc) {
          this.priority = p.name;
          this.color = p.color;
          break;
        }
      }
    }

    // Target positions aligned to the 3 folder zones in the canvas base
    const folderSpacing = Math.min(canvasWidth * 0.32, 160);
    if (this.priority === "low") {
      this.targetX = this.cx - folderSpacing;
      this.targetY = canvasHeight - 12;
    } else if (this.priority === "medium") {
      this.targetX = this.cx;
      this.targetY = canvasHeight - 12;
    } else {
      this.targetX = this.cx + folderSpacing;
      this.targetY = canvasHeight - 12;
    }

    // Arc control point
    this.controlX = this.cx + (Math.random() - 0.5) * (canvasWidth * 0.5);
    this.controlY = this.cy - 50 - Math.random() * 40;

    this.progress = 0;
    this.speed = 0.012 + Math.random() * 0.008;
    this.size = 9 + Math.random() * 4;
    this.rotation = (Math.random() - 0.5) * 0.4;
    this.alpha = 1;
    this.trail = [];
    this.x = this.cx;
    this.y = this.cy;
    this.counted = false;
  }

  update() {
    this.progress += this.speed;

    if (this.progress < 1) {
      // Cubic ease out
      const t = 1 - Math.pow(1 - this.progress, 3);
      const mt = 1 - t;

      this.x = mt * mt * this.cx + 2 * mt * t * this.controlX + t * t * this.targetX;
      this.y = mt * mt * this.cy + 2 * mt * t * this.controlY + t * t * this.targetY;

      this.trail.push({ x: this.x, y: this.y, alpha: 0.35 });
      if (this.trail.length > 6) this.trail.shift();
    } else {
      this.alpha -= 0.1;
    }
  }

  draw(ctx) {
    // Particle trail
    for (let i = 0; i < this.trail.length; i++) {
      const p = this.trail[i];
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.4, 0, Math.PI * 2);
      ctx.fillStyle = this.color + "44";
      ctx.fill();
    }

    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation * this.progress);
    ctx.globalAlpha = Math.max(0, this.alpha);

    // Document miniature
    ctx.fillStyle = "#FFFFFF";
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(-this.size / 2, -this.size / 1.4, this.size, this.size * 1.3, 2);
    } else {
      ctx.rect(-this.size / 2, -this.size / 1.4, this.size, this.size * 1.3);
    }
    ctx.fill();
    ctx.stroke();

    // Document inner lines
    ctx.strokeStyle = "#CBD5E1";
    ctx.lineWidth = 1;
    for (let i = 0; i < 2; i++) {
      ctx.beginPath();
      ctx.moveTo(-this.size / 3, -this.size / 3 + i * 4);
      ctx.lineTo(this.size / 3, -this.size / 3 + i * 4);
      ctx.stroke();
    }

    // Badge dot
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.size / 2 - 2, -this.size / 1.4 + 3.5, 2.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  isDead() {
    return this.alpha <= 0;
  }
}

function spawnStreamIncidentParticles(severity, count = 1) {
  const canvas = document.getElementById("v2ProcessingCanvas");
  if (!canvas) return;
  const width = canvas.width || 530;
  const height = canvas.height || 210;
  const numParticles = Math.min(Math.max(1, count), 3);
  for (let i = 0; i < numParticles; i++) {
    const p = new ProcessingDocParticle(width, height, severity);
    p.speed += (Math.random() - 0.5) * 0.003;
    animParticles.push(p);
  }
}

function drawOrb(ctx, width, height, time) {
  const cx = width / 2;
  const cy = height / 2 - 25;

  // Outer ambient glow
  const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, 65);
  gradient.addColorStop(0, "rgba(37, 99, 235, 0.22)");
  gradient.addColorStop(0.5, "rgba(37, 99, 235, 0.06)");
  gradient.addColorStop(1, "rgba(37, 99, 235, 0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(cx, cy, 65, 0, Math.PI * 2);
  ctx.fill();

  // Core Orb (Laya Brand Gradient)
  const pulseRadius = 22 + Math.sin(time * 0.0035) * 1.5;
  const orbGrad = ctx.createRadialGradient(cx - 6, cy - 6, 3, cx, cy, 24);
  orbGrad.addColorStop(0, "#60A5FA");
  orbGrad.addColorStop(0.5, "#2563EB");
  orbGrad.addColorStop(1, "#1D4ED8");

  ctx.beginPath();
  ctx.arc(cx, cy, pulseRadius, 0, Math.PI * 2);
  ctx.fillStyle = orbGrad;
  ctx.fill();

  // Inner highlight reflection
  ctx.beginPath();
  ctx.arc(cx - 6, cy - 6, 6, 0, Math.PI * 2);
  ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
  ctx.fill();

  // LAYA text
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "bold 9.5px 'Inter', system-ui, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("LAYA", cx, cy);
}

function animateProcessing(time) {
  const canvas = document.getElementById("v2ProcessingCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  // Background subtle canvas fill
  ctx.fillStyle = "#FAFBFD";
  ctx.fillRect(0, 0, width, height);

  drawOrb(ctx, width, height, time);

  // Subtle ambient particles if no stream events are currently in flight
  animSpawnTimer += time - animLastTime;
  if (animSpawnTimer > 350 && animParticles.length < 2) {
    animParticles.push(new ProcessingDocParticle(width, height));
    animSpawnTimer = 0;
  }

  // Update and draw particles
  for (let i = animParticles.length - 1; i >= 0; i--) {
    const p = animParticles[i];
    p.update();
    p.draw(ctx);

    if (p.isDead()) {
      animParticles.splice(i, 1);
    }
  }

  animLastTime = time;
  animRafId = requestAnimationFrame(animateProcessing);
}

function startProcessingAnimation() {
  stopProcessingAnimation();
  animParticles = [];
  animCounts = { low: 0, medium: 0, critical: 0 };
  animLastTime = performance.now();
  animSpawnTimer = 0;

  const elLow = document.getElementById("v2AnimCountLow");
  const elMed = document.getElementById("v2AnimCountMedium");
  const elCrit = document.getElementById("v2AnimCountCritical");
  if (elLow) elLow.textContent = "0";
  if (elMed) elMed.textContent = "0";
  if (elCrit) elCrit.textContent = "0";

  const canvas = document.getElementById("v2ProcessingCanvas");
  if (canvas) {
    const rect = canvas.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      canvas.width = rect.width;
      canvas.height = rect.height;
    } else {
      canvas.width = 530;
      canvas.height = 210;
    }
  }

  animRafId = requestAnimationFrame(animateProcessing);
}

function stopProcessingAnimation() {
  if (animRafId) {
    cancelAnimationFrame(animRafId);
    animRafId = null;
  }
  animParticles = [];
  const canvas = document.getElementById("v2ProcessingCanvas");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
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
  startProcessingAnimation();
}

function updateProgress(percent, message, counts = null, lastSeverity = null, lastOccurrences = 1) {
  const statusEl = document.getElementById("v2ProgressStatus");
  const percentEl = document.getElementById("v2ProgressPercent");
  const fillEl = document.getElementById("v2ProgressFill");

  if (fillEl) fillEl.style.width = `${percent}%`;
  if (percentEl) percentEl.textContent = `${percent}%`;
  if (statusEl && message) statusEl.textContent = message;

  // Atualização em tempo real dos quantitativos reais da análise
  if (counts) {
    if (typeof counts.low === "number") animCounts.low = counts.low;
    if (typeof counts.medium === "number") animCounts.medium = counts.medium;
    if (typeof counts.critical === "number") animCounts.critical = counts.critical;

    const elLow = document.getElementById("v2AnimCountLow");
    const elMed = document.getElementById("v2AnimCountMedium");
    const elCrit = document.getElementById("v2AnimCountCritical");
    if (elLow) elLow.textContent = animCounts.low.toLocaleString();
    if (elMed) elMed.textContent = animCounts.medium.toLocaleString();
    if (elCrit) elCrit.textContent = animCounts.critical.toLocaleString();
  }

  if (lastSeverity) {
    spawnStreamIncidentParticles(lastSeverity, lastOccurrences);
  }
}

function hideLoadingOverlay() {
  const overlay = document.getElementById("v2LoadingModal");
  if (overlay) overlay.classList.remove("active");
  stopProcessingAnimation();
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
            updateProgress(event.percent, event.message, event.counts, event.last_severity, event.last_occurrences);
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
        <span class="badge badge-subtle">🔁 ${inc.total_occurrences} ${i18nT("incident.occurrencesCount", "occurrence(s)")}</span>
        <span class="badge badge-subtle">${i18nT("incident.line", "Line")} ${inc.first_seen_line}</span>
        ${inc.causa_indisponibilidade ? `<span class="badge badge-critical">${i18nT("incident.affectsUnavail", "Unavailability")}</span>` : ''}
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

  const stacktrace = inc.sample_stacktrace || inc.sample_raw || "No stacktrace recorded for this occurrence.";

  const profileSnap = currentAnalysis && currentAnalysis.profile_snapshot;
  const profileInfoHtml = profileSnap ? `
    <div style="font-size: 11.5px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; padding: 4px 8px; background: var(--bg-app); border-radius: var(--radius-sm); border: 1px solid var(--border-soft);">
      <span>🎯 <strong>${i18nT("incident.profileCalibration", "Calibration Profile")}:</strong> ${escapeHTML(profileSnap.profile_name)}</span>
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
        <span class="badge badge-subtle">${i18nT("incident.sector", "Sector")}: <strong>${escapeHTML(inc.setor)}</strong></span>
        <span class="badge badge-subtle">${i18nT("incident.failure", "Failure")}: <strong>${escapeHTML(inc.tipo_falha)}</strong></span>
        <span class="badge badge-subtle">${i18nT("incident.firstSeen", "First seen")}: <strong>${inc.first_seen_time || 'N/A'}</strong></span>
        ${inc.causa_indisponibilidade ? `<span class="badge badge-critical">${i18nT("incident.affectsUnavail", "Affects System Availability")}</span>` : `<span class="badge badge-subtle">${i18nT("incident.noUnavail", "No General Outage")}</span>`}
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
        <span class="ai-field-label">${i18nT("incident.diagSummary", "Diagnostic Summary")}</span>
        <div class="ai-field-text">${escapeHTML(inc.technical_summary || 'Preliminary diagnosis generated.')}</div>
      </div>

      <div class="ai-field-group">
        <span class="ai-field-label">${i18nT("incident.recommendation", "Suggested Action / Recommendation")}</span>
        <div class="ai-recommendation-box">
          💡 ${escapeHTML(inc.recommendation || 'Verify input parameters and isolate failure origin.')}
        </div>
      </div>
    </div>

    <!-- Occurrences Jump Grid -->
    <div style="display: flex; flex-direction: column; gap: 6px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
        <span class="ai-field-label">${i18nT("incident.occurrences", "Occurrences")} (${inc.lines.length}x) — ${i18nT("incident.occurrencesHint", "Click to inspect")}</span>
        <div style="display: flex; align-items: center; gap: 6px;">
          <input type="number" id="directLineJump" placeholder="${i18nT("incident.jumpPlaceholder", "Go to line...")}" min="1" class="input-field" style="width: 84px; height: 26px; font-size: 11px; padding: 2px 6px;" onkeydown="if(event.key==='Enter'){const v=parseInt(this.value);if(v)jumpToLogLine(v);}">
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; font-size: 11px; height: 26px;" onclick="const v=parseInt(document.getElementById('directLineJump').value);if(v)jumpToLogLine(v);">${i18nT("incident.jumpGo", "Go")}</button>
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; font-size: 11px; height: 26px;" onclick="jumpToLogLine(${inc.first_seen_line})">
            📍 ${i18nT("incident.jumpFirst", "1st")} (${inc.first_seen_line})
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
        <span class="ai-field-label">${i18nT("incident.evidenceTitle", "Evidence / Stacktrace")}</span>
        <button class="btn btn-ghost btn-sm" onclick="copyStacktrace()" id="btnCopyCode" style="font-size: 11px;">
          ${i18nT("incident.copy", "Copy")}
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
      <div class="empty-state-title">${i18nT("incident.waitingTitle", "Waiting for selection")}</div>
      <div class="empty-state-desc">${i18nT("incident.waitingDesc", "Details and AI semantic analysis will appear here when you select an incident.")}</div>
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
      copyBtn.textContent = i18nT("incident.copied", "Copied!");
      setTimeout(() => { copyBtn.textContent = origText; }, 2000);
    }
  }).catch(err => {
    console.error("Failed to copy:", err);
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
