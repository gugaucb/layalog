# Driver.js configuration reference

Source: https://driverjs.com/docs/configuration

Configure globally via `driver({...})` or `driverObj.setConfig({...})`, per step via `DriveStep`, or per popover. Written in TypeScript, so IDEs autocomplete every option.

## Contents
- Config (driver-level)
- Popover
- DriveStep
- HintsConfig
- DriverHint
- State

## Config (driver-level)

```ts
type Config = {
  steps?: DriveStep[];                 // tour steps

  animate?: boolean;                   // default true
  duration?: number;                   // ms, default 400; stage movement + overlay/popover fade-in; only when animate
  overlayColor?: string;               // default black
  overlayOpacity?: number;             // default 0.5
  smoothScroll?: boolean;              // default false
  allowClose?: boolean;                // click backdrop to close, default true
  allowScroll?: boolean;               // false locks body scroll, default true
  overlayClickBehavior?: "close" | "nextStep" | ((element, step, options) => void); // default "close"
  stagePadding?: number;               // gap between element and cutout, default 10
  stageRadius?: number;                // cutout radius, default 5
  allowKeyboardControl?: boolean;      // default true

  disableActiveInteraction?: boolean;  // block interaction with highlighted element; also per step; default false
  advanceOnClick?: boolean;            // clicking the highlighted element acts like "next"; onNextClick/onDoneClick still apply; no effect if disableActiveInteraction blocks clicks; also per step; default false
  skipMissingElement?: boolean;        // skip steps whose specified element is missing (steps with no element are never skipped); also per step; default false
  waitForElement?: number;             // wait up to N ms for the element to appear before treating as missing; current step stays highlighted; also per step; default 0 (off)

  popoverClass?: string;               // custom class on popover
  popoverOffset?: number;              // gap popover <-> element, default 10
  showButtons?: AllowedButtons[];      // default ["next","previous","close"] for tours, [] for single highlight
  disableButtons?: AllowedButtons[];   // show but disable

  showProgress?: boolean;              // default false
  progressText?: string;               // placeholders {{current}} {{total}}; default "{{current}} of {{total}}"

  nextBtnText?: string;
  prevBtnText?: string;
  doneBtnText?: string;                // used on last step

  onPopoverRender?: (popover: PopoverDOM, options: HookOptions) => void;

  // Step lifecycle hooks: (element?, step, options) => void
  onHighlightStarted?, onHighlighted?, onDeselected?

  // Destroy hooks
  onDestroyStarted?, onDestroyed?

  // Button hooks
  onNextClick?, onPrevClick?, onCloseClick?, onDoneClick?
};

// HookOptions = { config: Config; state: State; driver: Driver; index: number | undefined }
```

### Hook notes
- Overriding `onNextClick` / `onPrevClick` takes over navigation: the buttons no longer move the tour, you must call `driverObj.moveNext()` / `movePrevious()`. Useful for dynamic content or custom logic.
- Both can be set at driver level (affects all steps) or at step level (that step only).
- `onDoneClick` runs instead of `onNextClick` on the last step. When provided, Driver.js does **not** auto-destroy; call `driverObj.destroy()` yourself. Works at driver or step level.
- `options.index` is the zero-based *active* step index (same as `getActiveIndex()`), or `undefined` for a single `highlight()`. In `onDeselected` it points to the step being moved **to**.

## Popover

```ts
type Popover = {
  title?: string;                      // HTML allowed
  description?: string;                // HTML allowed; either may be omitted

  side?: "top" | "right" | "bottom" | "left";   // default "bottom"; auto-flips if it doesn't fit
  align?: "start" | "center" | "end";           // default "start"

  showButtons?: ("next" | "previous" | "close")[];
  disableButtons?: ("next" | "previous" | "close")[];

  nextBtnText?: string;
  prevBtnText?: string;
  doneBtnText?: string;

  showProgress?: boolean;
  progressText?: string;               // "{{current}} of {{total}}" by default when showProgress

  popoverClass?: string;

  onPopoverRender?: (popover: PopoverDOM, options: HookOptions) => void;
  onNextClick?, onPrevClick?, onCloseClick?, onDoneClick?   // same semantics as driver level
};
```

`PopoverDOM` exposes references to the popover DOM (container, title, description, body, buttons...), so `onPopoverRender` can inject custom markup or buttons.

## DriveStep

```ts
type DriveStep = {
  element?: Element | string | (() => Element);  // node, CSS selector (first match), or function
  popover?: Popover;

  disableActiveInteraction?: boolean;
  advanceOnClick?: boolean;            // overrides driver-level for this step
  skipMissingElement?: boolean;        // overrides driver-level for this step
  waitForElement?: number;             // overrides driver-level for this step

  data?: Record<string, any>;          // arbitrary data for hooks

  onDeselected?, onHighlightStarted?, onHighlighted?  // (element?, step, options) => void
};
```

Steps without `element` render a centered popover.

## HintsConfig

Used with `hints()` from `driver.js/hints`. Guide: https://driverjs.com/docs/hints

```ts
type HintsConfig = {
  hints?: DriverHint[];
  beacon?: HintBeacon;                 // defaults for every hint; a hint's own beacon values win

  buttonText?: string;                 // default "Got it"
  popoverClass?: string;
  popoverOffset?: number;

  overlay?: boolean;                   // dim page while a hint is open, cut out its element; popover anchors to element; clicking the dim closes the hint; default false
  overlayColor?: string;               // default "#000"
  overlayOpacity?: number;             // default 0.7

  onOpen?:    (element, hint, { config, hints }) => void;
  onDismiss?: (element, hint, { config, hints }) => void;
  onButtonClick?: (element, hint, { config, hints }) => void;  // replaces default dismiss; call options.hints.dismiss(hint.id) yourself to also remove; also per hint
};
```

## DriverHint

```ts
type DriverHint = {
  element: Element | string | (() => Element);  // missing element => hint skipped, picked up on next show()
  id?: string;                         // stable identity for open/dismiss/restore and hooks; default = index

  beacon?: {
    side?: "top" | "right" | "bottom" | "left";   // default "top"
    align?: "start" | "center" | "end";           // default "end"
    offsetX?: number;                  // px, + right / - left; default 0
    offsetY?: number;                  // px, + down / - up; default 0
    animate?: boolean;                 // pulse, default true; auto-pauses with prefers-reduced-motion
    className?: string;                // scope CSS vars --driver-hint-size / --driver-hint-color
  };

  popover?: {
    title?: string;
    description?: string;
    side?: "top" | "right" | "bottom" | "left";
    align?: "start" | "center" | "end";
    popoverClass?: string;
    showButton?: boolean;              // default true; hide for code-only dismissal
    buttonText?: string;               // overrides instance-level
    onButtonClick?: (element, hint, { config, hints }) => void;
    onPopoverRender?: (popover: PopoverDOM, { hint, hints }) => void;
  };

  onOpen?, onDismiss?                  // hint-level hooks, take precedence over instance-level
  data?: Record<string, any>;
};
```

## State

From `driverObj.getState()`; also passed to hooks.

```ts
type State = {
  isInitialized?: boolean;
  activeIndex?: number;                // tour only
  activeElement?: Element;
  activeStep?: DriveStep;
  previousElement?: Element;
  previousStep?: DriveStep;
  popover?: PopoverDOM;
};
```
