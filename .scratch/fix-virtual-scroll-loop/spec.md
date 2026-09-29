# Spec: Fix Virtual Scroll Infinite Fetch Loop

## Problem
When loading an analysis whose log lines cannot be retrieved for a specific range (e.g. empty lines array from backend), the virtual log viewer's `ensureRangeLoaded` method did not mark those lines in `lineCache`. When `finally` called `render()`, `render()` detected the same missing lines and immediately triggered another `fetch`, creating an infinite asynchronous recursive loop that consumed 100% CPU and caused the screen to turn white.

## Solution
1. Add strict chunk tracking (`attemptedRanges` Set) so the same chunk is never re-requested.
2. Ensure every requested line index in the chunk range is populated in `lineCache` (with fallback text if missing).
3. Throttle/schedule `render()` using `requestAnimationFrame`.
4. Update both `v2-log-viewer.js` and `virtual-scroll.js`.
