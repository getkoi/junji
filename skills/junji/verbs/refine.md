# Verb: refine — propose a split, then materialize accepted work

Read references/board.md, PLAN and CONTEXT. Decompose work into coherent, independently verifiable
candidate slices. PLAN holds strategy/rationale; the split belongs in the backlog proposal.
Never edit BACKLOG.md or write product code. Runtime tier/strategy choices remain in Yokai YAML.

Read `junji-board show`. Build a complete proposed order: existing entries reference accepted phase
IDs; new entries use temporary labels with full descriptions, dependencies and gates. Substantial
merges/splits explicitly retire replaced unstarted cards with accurate reasons. Never overwrite an
accepted card's description with different work to keep its phase number. Wording-only corrections
retain identity and state their reason; started/completed cards and outcomes remain intact.

Use `junji-board propose --revision N --input FILE`, then `show-proposal`. This saves the durable
BACKLOG.proposed.json and marks review pending, without creating cards or retirement history.
Present the candidate count, boundaries, dependencies, gates and replacements. Wait for the user's
acceptance of this exact proposal. Requests to refine, reduce splits or revise wording are revisions,
not acceptance. Revise freely with another propose; no permanent phase IDs exist for new work yet.

After explicit acceptance, use `accept-proposal --revision REVIEWED_N --proposal REVIEWED_ID`.
Changed board/proposal content requires rereading, refreshing the proposal and obtaining acceptance
again. Do not silently retry acceptance against a new revision. To cancel review, use discard-proposal
with the current revision and proposal ID; it retains accepted work and restores its next action.
Pending review lets an in-flight phase finish, then pauses before another card. Do not accept while
a phase is in flight. The accepted board and generated summary stay the execution source of truth.

Acceptance allocates IDs, resolves dependencies, retains retired content and advances to /junji next.
Read `junji-board show` for the assigned IDs. Only then create/link needed phase-plan Markdown and reconcile affected runtime YAML references
through their owner. Changed locks go in CONTEXT as facts and PLAN as rationale. When publication is
requested, hand off initial connection review to `/junji connect`; backlog acceptance is not
connection approval. The dedicated host publisher handles accepted additions within existing
authorization. Drafts never publish or authorize gated execution; refine does not write to Jira.
