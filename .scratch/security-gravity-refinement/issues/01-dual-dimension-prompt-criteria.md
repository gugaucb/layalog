# 01: Dual-Dimension Gravity Prompt & Profile Criteria Refinement

**What to build:** Refine the gravity classification question instructions and the built-in profile criteria (especially `keycloak-iam`) to incorporate both service availability and active security threats (e.g. Brute Force attacks, lockout triggers) as high-priority severity factors, removing semantic ambiguity between Medium and Critical.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] Update `build_questions` instructions in `layalog/classifier.py` to evaluate both service availability and active security threats.
- [x] Update `keycloak-iam` criteria in `layalog/profiles.py` removing ambiguous "Security protections" from Medium and placing brute force/lockout in Critical.
- [x] Update SQLite profile seeding/updating logic so built-in and default profiles reflect the dual-dimension criteria.
