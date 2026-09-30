# Driver.js API reference

Source: https://driverjs.com/docs/api

Each `driver()` / `hints()` call returns an independent instance; configuration, steps and state never overlap between instances.

## driver() instance

```js
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver({ /* Config, see configuration.md */ });

driverObj.drive();          // start tour from step 0
driverObj.drive(4);         // start at step 4

driverObj.moveNext();
driverObj.movePrevious();
driverObj.moveTo(4);
driverObj.hasNextStep();
driverObj.hasPreviousStep();

driverObj.isFirstStep();
driverObj.isLastStep();

driverObj.getActiveIndex();
driverObj.getActiveStep();      // step config
driverObj.getPreviousStep();
driverObj.getNextStep();
driverObj.getActiveElement();   // HTMLElement
driverObj.getPreviousElement();

driverObj.isActive();           // tour or highlight currently active
driverObj.refresh();            // recalculate and redraw the highlight

driverObj.getConfig();
driverObj.setConfig({ /* ... */ });
driverObj.setSteps([ /* ... */ ]);
driverObj.getState();

driverObj.highlight({ /* DriveStep */ });  // highlight one element
driverObj.destroy();                        // end the tour / remove highlight
```

## hints() instance

```js
import { hints } from "driver.js/hints";
import "driver.js/dist/hints.css";

const productHints = hints({ /* HintsConfig */ });

productHints.show();        // mount beacons; calling again picks up hints whose elements appeared since
productHints.hide();        // remove beacons and listeners; show() brings them back

// Address hints by `id`, or by array index if no id
productHints.open("export");      // open popover
productHints.close();             // close open popover, keep beacon
productHints.dismiss("export");   // remove beacon and fire onDismiss
productHints.restore("export");   // bring back a dismissed hint
productHints.restoreAll();

productHints.setHints([ /* ... */ ]);  // replace hints; resets dismissals
productHints.getHints();
productHints.getActive();         // hint whose popover is open, if any
productHints.isVisible();

productHints.refresh();           // reposition beacons, open popover and overlay after layout changes
```

CDN globals: `window.driver.js.driver` and `window.driverHints.hints`.
