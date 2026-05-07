# Founding Methodology

Rules governing decisions in this codebase are recorded in the changelog,
code comments, and scaffold stop-condition wiring. The following extends
**Rule 2** (research arithmetic, stop conditions, and explicit failure modes).

## Rule 2

Stop conditions, calibration brackets, and research arithmetic are enforced
at runtime as described in the most recent `changelog.md` scaffold entry and
via `Rule 2` raises and messages in implementation code.

**Rule 2a — Flags vs Notes**

The flag system tracks incomplete work. It is not a catalogue of
every constant, choice, or limitation in the codebase. To keep the
work queue legible, two distinct labels are used.

A **Flag** is opened when something requires follow-up. It identifies
a piece of work that has not yet been done. A flag is closed when the
work is completed and verified. Flags appear in the open-work queue
at the bottom of the most recent scaffold entry. Categories of flag:

- Blocked on an upstream cascade variable not yet built
- Placeholder, fit, or stub awaiting proper derivation
- Research outstanding (literature exists, not yet sourced)
- Verification pending (runtime confirmation not yet performed)
- Correction queued (identified as wrong, fix scheduled)

A **Note** is opened when a choice or limitation needs to be
documented for transparency but no follow-up is planned. A note is
not work — it is a record. Notes do not appear in the open-work
queue. Categories of note:

- Inherent model approximation (deliberately chosen, not on the
  upgrade roadmap)
- Earth-measured molecular constant (intrinsic to the molecule, not
  the planet — universal in physical content)
- Solar System or multi-body confirmed calibration
- Earth fallback accepted because no planet-general data exists
- Survey-scope or applicability limit documented
- Procedural or engineering choice recorded

The decision rule is single-question: *Does this entry track work
that is genuinely incomplete and has an identifiable next step on
the project roadmap?* YES → Flag. NO → Note.

A Note may later become a Flag if new research or new project scope
makes it actionable. The conversion is recorded in the changelog at
the time it occurs.
