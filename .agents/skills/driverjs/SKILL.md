---
name: driverjs
description: Build product tours, onboarding flows, element highlights, contextual help popovers and feature hints with Driver.js (driver.js), the lightweight zero-dependency JavaScript library. Use this skill whenever the user mentions Driver.js, driverjs, driver.js, product tour, onboarding tour, guided tour, step-by-step walkthrough, spotlight/highlight an element with a popover, feature hints/beacons, or asks to guide users through a UI in vanilla JS, React, Vue, Angular or any framework - even if they don't name the library. Also use for installing Driver.js (npm/pnpm/yarn/CDN), configuring steps, popovers, overlay, animation duration, button hooks (onNextClick, onDoneClick), or debugging a tour. Triggers em português - tour de produto, onboarding, guia passo a passo, destacar elemento, tutorial interativo, dicas de funcionalidade.
---

# Driver.js

Driver.js is a small, dependency-free library that dims the page, cuts a "stage" around a target element and shows a popover next to it. It has three modes:

| Mode | Use it for | Entry point |
|---|---|---|
| **Tour** | Multi-step walkthrough with next/previous buttons | `driver({ steps }).drive()` |
| **Highlight** | One element (or none) + popover: contextual help, form field help, simple modal | `driver().highlight({...})` |
| **Hints** | Pulsing beacons that open a popover on click; no overlay, page stays interactive | `hints({ hints }).show()` from `driver.js/hints` |

Pick the mode from the user's goal first. If they say "onboarding" or "walk the user through", use a tour. If they say "explain this field/feature", use highlight. If they want passive, non-blocking pointers, use hints.

## Install

```bash
npm install driver.js   # or: pnpm install driver.js / yarn add driver.js
```

CDN (no bundler):

```html
<script src="https://cdn.jsdelivr.net/npm/driver.js@latest/dist/driver.js.iife.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/driver.js@latest/dist/driver.css" />
<!-- Only if you use hints -->
<script src="https://cdn.jsdelivr.net/npm/driver.js@latest/dist/hints.iife.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/driver.js@latest/dist/hints.css" />
```

With the CDN the library lives on `window`, so destructure it first:

```js
const driver = window.driver.js.driver;   // tours and highlights
const hints  = window.driverHints.hints;  // hints
```

Always import the stylesheet (`driver.js/dist/driver.css`, or `driver.js/dist/hints.css` for hints). Without it the popover and overlay render unstyled, which is the most common "it doesn't work" cause.

## Quick start

**Tour**

```js
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver({
  showProgress: true,
  steps: [
    { element: ".page-header", popover: { title: "Header", description: "Start here.", side: "bottom", align: "start" } },
    { element: ".sidebar",     popover: { title: "Sidebar", description: "Navigate from here." } },
    { popover: { title: "All set", description: "No element = centered popover." } },
  ],
});
driverObj.drive();        // drive(n) starts at step n
```

**Single highlight** (no buttons by default)

```js
const driverObj = driver({ popoverClass: "driverjs-theme", stagePadding: 4 });
driverObj.highlight({
  element: "#some-element",
  popover: { side: "bottom", title: "Title", description: "Description" },
});
```

Omit `element` to show a standalone modal-like popover. `title` and `description` accept HTML.

**Hints**

```js
import { hints } from "driver.js/hints";
import "driver.js/dist/hints.css";

const productHints = hints({
  hints: [
    { id: "export", element: "#export-btn", popover: { title: "Export", description: "Download as CSV or PDF." } },
  ],
});
productHints.show();
```

## Where to find details

Read only what the task needs:

- `references/configuration.md` - every option of `Config`, `Popover`, `DriveStep`, `HintsConfig`, `DriverHint` and `State`. Read when choosing or debugging options, hooks or button behavior.
- `references/api.md` - every method on the `driver()` and `hints()` instances. Read when controlling a tour programmatically (moveNext, moveTo, refresh, destroy, open/dismiss/restore).
- `references/examples.md` - animated tour (`duration`), simple highlight, form-field help, modal popover, and framework integration patterns. Read when the user wants a concrete recipe.

## Behaviors worth knowing (they explain most bugs)

- **Instances are independent.** Each `driver()` / `hints()` call has its own config, steps and state, so several can coexist on one page.
- **Taking over navigation.** Setting `onNextClick` / `onPrevClick` (driver or step level) disables the default navigation. You must call `driverObj.moveNext()` / `movePrevious()` yourself. The same applies to `onDoneClick` on the last step: the tour is no longer auto-destroyed, so call `driverObj.destroy()`.
- **Dynamic DOM.** If a step's element renders late (modal opened by the previous step, async content), use `waitForElement: <ms>`. Use `skipMissingElement: true` to skip steps whose element is absent instead of showing the centered fallback. A step with no `element` is an intentional centered step and is never skipped.
- **Element can be a selector, a DOM node, or a function** returning a node. With a selector, the first match is used. Prefer a function when the node may be re-created between renders (React/Vue).
- **Layout changes.** Call `driverObj.refresh()` (or `productHints.refresh()`) after resizes or DOM shifts so the stage and popover reposition.
- **`options.index`** in hooks is the *active* step index. Inside `onDeselected` it already points to the step being moved to, not the one being left.
- **Interactive steps.** `disableActiveInteraction: true` blocks clicks on the highlighted element; `advanceOnClick: true` advances when it is clicked (no effect if interaction is disabled).
- **Closing behavior.** `allowClose` (click backdrop to close, default true) and `overlayClickBehavior` (`'close' | 'nextStep' | fn`) control backdrop clicks. `onDestroyStarted` lets you intercept closing (e.g. confirm dialogs); call `driverObj.destroy()` to actually close.
- **Animation.** `animate` (default true) and `duration` (ms, default 400) control both the stage movement and the overlay/popover fade-in.
- **Scroll.** `smoothScroll` defaults to false; `allowScroll: false` locks body scroll during the tour.
- **Hints dismissals** reset on `setHints()`. Use stable `id`s and persist dismissals yourself (e.g. in `localStorage`) via `onDismiss`.

## Output guidelines

- Match the user's stack (vanilla, React, Vue, etc.) and module style (ESM import vs. CDN `window`). When unsure, ask in one line or default to ESM.
- Show complete, runnable snippets including the CSS import.
- In React/Vue, create the driver inside an effect/mounted hook after the target elements exist and call `destroy()` on cleanup.
- Don't invent options. If something is not in the references, say so and point to https://driverjs.com/docs/configuration. Related docs pages not covered here: theming, static-tour, styling-popover, tour-progress, async-tour, confirm-on-exit, interactive-tour, prevent-destroy, multi-page-tour, styling-overlay, hints, styling-hints, popover-position, buttons, changelog (all under https://driverjs.com/docs/).
