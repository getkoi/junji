# Verb: next — execute one card

Read references/board.md and the copied METHOD. Load CONTEXT including Skills, the active board effort
and existing phase plan. Resume the in-flight card, otherwise select the first todo card. Dependencies
must be done; explicit blocking reasons halt. Pending proposal review permits only finishing an
already in-flight card, then halts before another starts. An empty effort awaits acceptance; it is
not complete. Do not accept or discard review implicitly. Honor gated actions and standing overrides.

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
The board remains authoritative; BACKLOG.md is only the generated view. Pending review keeps
next_action at /junji refine even after the current card finishes.

Coding phase agents never call Jira tools. When publication is enabled, standalone next records local
verified proof after the green bar and required commit/clean-tree checks, then requests
`junji-board visibility sync` per references/visibility.md.
Sync delegates to the dedicated host publisher; it is not coding-agent Jira access. During a Yokai run,
the supervisor alone records verified state and requests sync; phase agents do neither. The host
publisher uses the saved host and named official MCP server with host-managed OAuth, independently
of coding candidates and model tiers. Require agent-reported actual remote readbacks before reporting
delivery, not narrative success or an independent transport audit. Missing evidence or headless auth
stays pending; reconcile uncertain creates before retrying. Failed delivery does not change engineering
results. Use `/junji connect` outside the phase for connection review or publication follow-up.

Report Phase N of M, Next action and the concrete outcome. When complete, also name iterate as the
way to add work. Stop after one card.
