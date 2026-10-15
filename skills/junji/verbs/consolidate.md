# Verb: consolidate — archive the effort into its native deliverable

Read references/board.md. Require an active effort whose cards are all done. Read CONTEXT's
Deliverable spec model, PLAN rationale, card outcomes/carry-forward and linked phase-plan Outcomes.
Follow standing branch, push and human-gate instructions; do not execute new product work.

1. Harvest the implemented system and settled decisions, not scaffolding or acceptance-checklist
   dumps. Use the recorded section outline verbatim. Include useful outcomes and carry-forward.
2. Write the deliverable at the repo-native location and filename recorded in CONTEXT. If no model
   exists, use narrative explanation plus locked facts. Keep truthful verification results.
3. Record each card's outcome and plan reference with junji-board apply using the current revision.
   Run junji-board consolidate --revision N --deliverable REPO_PATH. The helper requires the deliverable
   to exist and archives plan paths with their commit identities before clearing the active effort.
4. Only after that succeeds, remove `.koi/run/` using git rm. Never remove the durable board,
   adapters, sensors, driver settings or visibility receipts. Pending publication survives.
5. Commit the deliverable, archived board and run-folder removal, respecting standing directives.
   Report the deliverable path and verification results. Further work starts with begin.
