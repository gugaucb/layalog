/**
 * V2 Virtual Log Viewer Component
 * High-performance chunk-based stream rendering with JetBrains Mono precision typography
 * Includes infinite loop protection, attempted range tracking, and RAF-batched rendering.
 */
class V2LogViewer {
  constructor(containerElement, options = {}) {
    this.container = containerElement;
    this.rowHeight = options.rowHeight || 20;
    this.buffer = options.buffer || 25;
    this.chunkSize = options.chunkSize || 200;

    this.analysisId = null;
    this.totalLines = 0;
    this.lineCache = new Map(); // lineNum (1-indexed) -> text string
    this.loadingRanges = new Set();
    this.attemptedRanges = new Set();
    this.highlightedLine = null;
    this.searchQuery = "";
    this.rafPending = false;

    this.initDOM();
    this.attachEvents();
  }

  initDOM() {
    this.container.innerHTML = "";
    this.container.className = "log-viewer-v2-container";

    this.phantom = document.createElement("div");
    this.phantom.className = "virtual-scroll-phantom";

    this.content = document.createElement("div");
    this.content.className = "virtual-scroll-content";

    this.phantom.appendChild(this.content);
    this.container.appendChild(this.phantom);
  }

  attachEvents() {
    this.container.addEventListener("scroll", () => this.scheduleRender());
    window.addEventListener("resize", () => this.scheduleRender());
  }

  setAnalysis(analysisId, totalLines, initialLines = null) {
    this.analysisId = analysisId;
    this.totalLines = totalLines || 0;
    this.lineCache.clear();
    this.loadingRanges.clear();
    this.attemptedRanges.clear();
    this.highlightedLine = null;

    if (initialLines && Array.isArray(initialLines)) {
      initialLines.forEach((text, idx) => {
        this.lineCache.set(idx + 1, text);
      });
    }

    this.phantom.style.height = `${this.totalLines * this.rowHeight}px`;
    this.container.scrollTop = 0;
    this.container.scrollLeft = 0;
    this.scheduleRender(true);

    if (!initialLines || initialLines.length === 0) {
      this.ensureRangeLoaded(1, Math.min(this.totalLines, this.chunkSize));
    }
  }

  setSearchQuery(query) {
    this.searchQuery = (query || "").toLowerCase();
    this.scheduleRender();
  }

  scheduleRender() {
    if (this.rafPending) return;
    this.rafPending = true;
    requestAnimationFrame(() => {
      this.rafPending = false;
      this.render();
    });
  }

  async ensureRangeLoaded(startLine, count) {
    if (!this.analysisId || count <= 0) return;

    let allCached = true;
    for (let l = startLine; l < startLine + count; l++) {
      if (l <= this.totalLines && !this.lineCache.has(l)) {
        allCached = false;
        break;
      }
    }
    if (allCached) return;

    const chunkStart = Math.max(1, Math.floor((startLine - 1) / this.chunkSize) * this.chunkSize + 1);
    const chunkLimit = Math.max(this.chunkSize, Math.ceil(count / this.chunkSize) * this.chunkSize);
    const chunkKey = `${chunkStart}_${chunkLimit}`;

    // Loop protection: Never re-request a chunk that is already in-flight or already attempted
    if (this.loadingRanges.has(chunkKey) || this.attemptedRanges.has(chunkKey)) return;
    this.loadingRanges.add(chunkKey);
    this.attemptedRanges.add(chunkKey);

    try {
      const res = await fetch(`/api/analyses/${this.analysisId}/lines?start_line=${chunkStart}&limit=${chunkLimit}`);
      if (!res.ok) throw new Error("Falha ao carregar linhas");
      const data = await res.json();

      const receivedCount = (data.lines && Array.isArray(data.lines)) ? data.lines.length : 0;
      if (receivedCount > 0) {
        data.lines.forEach((text, idx) => {
          this.lineCache.set(data.start_line + idx, text);
        });
      }

      // Guarantee every line in the requested window is populated in lineCache to prevent re-query loops
      const maxRangeLine = Math.min(this.totalLines, chunkStart + chunkLimit - 1);
      for (let l = chunkStart; l <= maxRangeLine; l++) {
        if (!this.lineCache.has(l)) {
          this.lineCache.set(l, "");
        }
      }
    } catch (err) {
      console.warn(`Aviso ao carregar linhas do log (${chunkStart}..${chunkStart + chunkLimit}):`, err);
      // Mark lines as blank on error to prevent infinite retries
      const maxRangeLine = Math.min(this.totalLines, chunkStart + chunkLimit - 1);
      for (let l = chunkStart; l <= maxRangeLine; l++) {
        if (!this.lineCache.has(l)) {
          this.lineCache.set(l, "");
        }
      }
    } finally {
      this.loadingRanges.delete(chunkKey);
      this.scheduleRender();
    }
  }

  async scrollToLine(lineNumber, doHighlight = true) {
    if (!this.totalLines || lineNumber < 1 || lineNumber > this.totalLines) return;

    const targetIndex = lineNumber - 1;
    const viewportHeight = this.container.clientHeight || 500;
    const targetScrollTop = Math.max(0, targetIndex * this.rowHeight - (viewportHeight / 3));

    const windowStart = Math.max(1, lineNumber - 50);
    const windowCount = 150;
    await this.ensureRangeLoaded(windowStart, windowCount);

    this.container.scrollTo({
      top: targetScrollTop,
      behavior: "smooth"
    });

    if (doHighlight) {
      this.highlightedLine = lineNumber;
      this.scheduleRender();

      if (this.highlightTimeout) clearTimeout(this.highlightTimeout);
      this.highlightTimeout = setTimeout(() => {
        this.highlightedLine = null;
        this.scheduleRender();
      }, 5000);
    }
  }

  escapeHTML(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  formatLine(text, lineNum) {
    if (text === undefined || text === null) {
      return `<span style="color:#484F58;font-style:italic;">Carregando linha ${lineNum}...</span>`;
    }

    let escaped = this.escapeHTML(text);

    if (this.searchQuery && escaped.toLowerCase().includes(this.searchQuery)) {
      const regex = new RegExp(`(${this.escapeRegExp(this.searchQuery)})`, "gi");
      escaped = escaped.replace(regex, `<mark style="background:#FEF08A;color:#111827;border-radius:2px;padding:0 2px;">$1</mark>`);
    }

    if (text.includes(".ERROR:") || text.includes("[ERROR]") || text.includes("Exception") || text.includes("Fatal")) {
      escaped = `<span class="v2-err-text">${escaped}</span>`;
    } else if (text.includes(".WARNING:") || text.includes("[WARN]")) {
      escaped = `<span class="v2-warn-text">${escaped}</span>`;
    }

    return escaped;
  }

  render() {
    if (!this.totalLines) {
      this.content.innerHTML = `
        <div class="empty-state-card" style="padding: 4rem 1rem;">
          <svg class="empty-state-icon" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
          </svg>
          <div class="empty-state-title">Nenhum log carregado</div>
          <div class="empty-state-desc">Selecione uma análise no histórico ou importe um arquivo de log.</div>
        </div>
      `;
      return;
    }

    const scrollTop = this.container.scrollTop;
    const viewportHeight = this.container.clientHeight || 500;

    const startIndex = Math.max(0, Math.floor(scrollTop / this.rowHeight) - this.buffer);
    const endIndex = Math.min(this.totalLines - 1, Math.ceil((scrollTop + viewportHeight) / this.rowHeight) + this.buffer);

    const visibleStartLine = startIndex + 1;
    const visibleCount = endIndex - startIndex + 1;

    this.ensureRangeLoaded(visibleStartLine, visibleCount);

    let html = "";
    for (let i = startIndex; i <= endIndex; i++) {
      const lineNum = i + 1;
      const topPos = i * this.rowHeight;
      const lineText = this.lineCache.get(lineNum);
      const isHighlighted = (this.highlightedLine === lineNum);

      let extraClass = "";
      if (isHighlighted) {
        extraClass = "highlight-line";
      } else if (lineText) {
        if (lineText.includes(".ERROR:") || lineText.includes("[ERROR]") || lineText.includes("Exception") || lineText.includes("Fatal")) {
          extraClass = "critical-line";
        } else if (lineText.includes(".WARNING:") || lineText.includes("[WARN]")) {
          extraClass = "warn-line";
        }
      }

      html += `
        <div class="v2-log-line ${extraClass}" style="top: ${topPos}px;" data-line="${lineNum}">
          <span class="v2-line-num">${lineNum}</span>
          <span class="v2-line-text">${this.formatLine(lineText, lineNum)}</span>
        </div>
      `;
    }

    this.content.innerHTML = html;
  }
}
