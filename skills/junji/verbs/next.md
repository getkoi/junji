# Verb: next — execute one card

Read references/board.md and the copied METHOD. Load CONTEXT including Skills, the active board effort
and existing phase plan. Resume the in-flight card, otherwise select the first todo card. Dependencies
must be done; explicit blocking reasons halt. Honor gated actions and standing overrides.

If no phase plan exists, set planning with the current revision, research this card only and write
.koi/run/phases/phase-NN-slug.md from the phase-plan template (P0 uses phase-00). Preserve Explicitly
out. An existing unique nonempty plan is reused. Ambiguous plans halt; never write another phase.

Set building and implement only the card's scope. Match Must Skills and the binding DESIGN contract.
Run every verification-bar command from its documented directory. Fix failures or halt with the card
still building; never weaken checks. Sealing resumes at completion without reimplementing.

Set sealing, write the plan Outcome, and use junji-board apply to record the card's done claim, concise
outcome, phase-plan link and carry-forward. Set next_action to /junji next while cards remain, else
/junji consolidate. Commit all authorized deliverables and method artifacts, excluding runtime sync
receipts and regenerable noise; follow branch/push directives. Verify commit and clean product state.
The board remains authoritative; BACKLOG.md is only the generated view.

Standalone publication: after the green bar and required commit/clean-tree checks, record verified
completion and sync per references/visibility.md. During a Yokai run, the supervisor owns publication.
Report Phase N of M, Next action and the concrete outcome. When complete, also name iterate as the
way to add work. Stop after one card.
