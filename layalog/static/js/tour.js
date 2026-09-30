/**
 * LayaLog - Interactive Product Tour powered by Driver.js
 * Multi-language support (EN, PT-BR, CN) using LayaI18n
 */

let activeDriverInstance = null;

function startLayaTour() {
  if (typeof window.driver === "undefined" || !window.driver.js || !window.driver.js.driver) {
    console.warn("Driver.js library not loaded on page.");
    return;
  }

  if (activeDriverInstance) {
    try {
      activeDriverInstance.destroy();
    } catch (e) {
      console.warn("Error destroying previous driver instance:", e);
    }
    activeDriverInstance = null;
  }

  const driver = window.driver.js.driver;
  const t = window.LayaI18n ? window.LayaI18n.t : (k) => k;

  const steps = [
    {
      element: "#v2ProfileControlGroup",
      popover: {
        title: t("tour.step1Title"),
        description: t("tour.step1Desc"),
        side: "bottom",
        align: "start"
      }
    },
    {
      element: "#v2UploadBtn",
      popover: {
        title: t("tour.step2Title"),
        description: t("tour.step2Desc"),
        side: "bottom",
        align: "center"
      }
    },
    {
      element: ".kpi-grid",
      popover: {
        title: t("tour.step3Title"),
        description: t("tour.step3Desc"),
        side: "bottom",
        align: "center"
      }
    },
    {
      element: ".master-detail-container",
      popover: {
        title: t("tour.step4Title"),
        description: t("tour.step4Desc"),
        side: "top",
        align: "center"
      }
    },
    {
      element: "#v2LogViewerSection",
      popover: {
        title: t("tour.step5Title"),
        description: t("tour.step5Desc"),
        side: "top",
        align: "center"
      }
    },
    {
      element: "#v2HistoryControlGroup",
      popover: {
        title: t("tour.step6Title"),
        description: t("tour.step6Desc"),
        side: "bottom",
        align: "end"
      }
    }
  ];

  activeDriverInstance = driver({
    showProgress: true,
    animate: true,
    duration: 350,
    stagePadding: 8,
    stageRadius: 8,
    smoothScroll: true,
    allowClose: true,
    popoverClass: "layalog-tour-theme",
    nextBtnText: t("tour.btnNext"),
    prevBtnText: t("tour.btnPrev"),
    doneBtnText: t("tour.btnDone"),
    steps: steps,
    onDestroyed: () => {
      localStorage.setItem("layalog_tour_seen", "true");
      activeDriverInstance = null;
    }
  });

  activeDriverInstance.drive();
}

function checkAutoTour() {
  const tourSeen = localStorage.getItem("layalog_tour_seen");
  if (!tourSeen) {
    setTimeout(() => {
      startLayaTour();
    }, 1200);
  }
}

// Global expose
window.startLayaTour = startLayaTour;
window.checkAutoTour = checkAutoTour;
