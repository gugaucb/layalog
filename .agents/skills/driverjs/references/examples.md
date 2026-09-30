# Driver.js recipes

Sources: basic-usage, animated-tour, simple-highlight pages on https://driverjs.com/docs/

## Contents
1. Basic tour with progress
2. Animated tour: fast / slow `duration`
3. Simple highlight
4. Modal popover without an element
5. Contextual help on form-field focus
6. Hints
7. Async content and custom navigation
8. Framework integration (React)

## 1. Basic tour with progress

```js
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver({
  showProgress: true,
  steps: [
    { element: ".page-header", popover: { title: "Title", description: "Description" } },
    { element: ".top-nav",     popover: { title: "Title", description: "Description" } },
    { element: ".sidebar",     popover: { title: "Title", description: "Description" } },
    { element: ".footer",      popover: { title: "Title", description: "Description" } },
  ],
});
driverObj.drive();
```

## 2. Animated tour: `duration`

`duration` (ms, default 400) controls both the highlight's movement between steps and the overlay/popover fade-in. It only applies when `animate` is true.

```js
// Snappy
driver({ duration: 150, showProgress: true, steps: [/* ... */] }).drive();

// Relaxed
driver({ duration: 1200, showProgress: true, steps: [/* ... */] }).drive();

// No animation at all
driver({ animate: false, steps: [/* ... */] }).drive();
```

## 3. Simple highlight

```js
const driverObj = driver({ popoverClass: "driverjs-theme", stagePadding: 4 });

driverObj.highlight({
  element: "#highlight-me",
  popover: { side: "bottom", title: "This is a title", description: "This is a description" },
});
```

`driverjs-theme` is the class the docs site uses for its own theme; define your own CSS for it or pick another `popoverClass` (see https://driverjs.com/docs/theming).

## 4. Modal popover without an element

Omit `element` to show a centered popover, useful as a simple modal. Descriptions accept HTML:

```js
const driverObj = driver();
driverObj.highlight({
  popover: {
    description: "<img src='/animated-example.webp' style='height: 202.5px; width: 270px;' /><span style='font-size: 15px; display: block; margin-top: 10px; text-align: center;'>Yet another highlight example.</span>",
  },
});
```

## 5. Contextual help on form-field focus

```js
const driverObj = driver({
  popoverClass: "driverjs-theme",
  stagePadding: 0,
  onDestroyed: () => { document?.activeElement?.blur(); },
});

const fields = {
  name:      { title: "Name",      description: "Enter your name here" },
  education: { title: "Education", description: "Enter your education here" },
  age:       { title: "Age",       description: "Enter your age here" },
  address:   { title: "Address",   description: "Enter your address here" },
};

for (const [id, popover] of Object.entries(fields)) {
  const el = document.getElementById(id);
  el.addEventListener("focus", () => driverObj.highlight({ element: el, popover }));
}

document.querySelector("form").addEventListener("blur", () => driverObj.destroy());
```

## 6. Hints

```js
import { hints } from "driver.js/hints";
import "driver.js/dist/hints.css";

const productHints = hints({
  overlay: false,               // true dims the page while a hint is open
  buttonText: "Got it",
  hints: [
    { id: "export",  element: "#export-btn", popover: { title: "Export your data", description: "Download this report as CSV or PDF." } },
    { id: "summary", element: "#summary",    beacon: { side: "top", align: "end" }, popover: { title: "Auto-generated summary", description: "Written for you from the numbers." } },
  ],
  onDismiss: (el, hint) => localStorage.setItem(`hint:${hint.id}`, "1"),  // persist dismissals yourself
});

productHints.show();
```

## 7. Async content and custom navigation

```js
const driverObj = driver({
  showProgress: true,
  steps: [
    {
      element: "#open-modal",
      popover: {
        title: "Open the modal",
        description: "Click it to continue.",
        // take over navigation: open the modal, then move on
        onNextClick: () => { document.querySelector("#open-modal").click(); driverObj.moveNext(); },
      },
    },
    {
      element: "#modal-field",
      waitForElement: 1500,      // wait up to 1.5s for the modal to render
      popover: { title: "Inside the modal", description: "This element appears on demand." },
    },
  ],
  onDoneClick: () => { /* custom finish logic */ driverObj.destroy(); },
});
```

Other useful step options: `skipMissingElement: true`, `advanceOnClick: true`, `disableActiveInteraction: true`.

## 8. Framework integration (React)

```jsx
import { useEffect } from "react";
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

export function useTour(steps) {
  useEffect(() => {
    const d = driver({ showProgress: true, steps });
    d.drive();
    return () => d.destroy();   // avoid leaving an overlay behind on unmount
  }, []);
}
```

Create the driver after the target elements are mounted. If targets are conditionally rendered, use function elements (`element: () => ref.current`) or `waitForElement`.
