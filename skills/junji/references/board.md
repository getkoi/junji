# Board contract

`.koi/board.json` is mandatory execution state. BACKLOG.md is a generated read-only view.
A card is one executable phase; an effort owns ordered cards, Next action and carry-forward.
Use the standalone `junji-board` Rust binary. Install it from a Koi checkout with
`./install.sh --board-only`; `./install.sh` installs it alongside Yokai. Never require Yokai or its
settings for method operations. Local edits need no Python runtime, credentials or network.
Yokai links the same library and supplies equivalent `yokai board` operations.

Read accepted work with `junji-board show`. Read a pending draft with `show-proposal`.
Refine and iterate always propose first, wait for the user's acceptance, then materialize cards:

```sh
junji-board propose --revision N --input candidate.json
junji-board show-proposal
junji-board accept-proposal --revision REVIEWED_N --proposal REVIEWED_ID
junji-board discard-proposal --revision CURRENT_N --proposal REVIEWED_ID
```

Candidate input has a complete `cards` order and optional `retire` entries. New cards use
`{"label":"foundation","title":"Foundation","description":"Shared tokens","depends_on":[],"gated":false}`.
Labels are temporary and cannot be P<digits>. Keep accepted cards with `{"existing":"P0"}`.
Dependencies reference existing IDs or new labels. Retire a replaced unstarted card with
`{"phase_id":"P1","reason":"Scope merged into foundation"}`; every accepted card must be kept
or explicitly retired. Wording-only corrections use an existing entry's `correction` object with
`reason` and optional title/description. Retain started/completed cards unchanged. Existing todo
entries may explicitly update depends_on/gated. Runtime choices stay in Yokai YAML.

The tool owns .koi/run/BACKLOG.proposed.json and binds it to a pending marker on the effort.
Repeated proposal revisions create neither card identities nor retirement records. Only acceptance
assigns permanent IDs, including all historical retired IDs when selecting the next number.
It applies exactly the reviewed content atomically and regenerates BACKLOG.md. Intervening board
changes require refresh/review and acceptance again: `propose --revision CURRENT --input
.koi/run/BACKLOG.proposed.json` can refresh the saved candidate. Never silently retry stale approval.
Discard restores the prior next action and preserves accepted work, even if the draft file is lost.
Both resolution operations remove the proposal artifact. An empty effort is unaccepted, not complete.

Pending review lets an in-flight card finish, then pauses execution. Do not start another card,
accept during an in-flight phase or publish draft work. The next action stays /junji refine until
review resolves. Existing boards without a pending marker remain accepted. Ordinary apply/status
operations update stages, outcomes, plan links, blocking facts and carry-forward. Apply rejects
new cards, title/description edits, removals, order and dependency/gate edits; send minimal progress
patches, not full card snapshots. Those changes require a proposal/acceptance workflow.

Use `status P0 planning|building|sealing|done --revision N` at method boundaries. A stale update
requires rereading and reconsideration; never blindly retry. A summary rendering error does not
roll back the saved board; `render` repairs the view. Preserve unrelated board fields.

Dependencies must be done before a card executes. Resume an in-flight card before picking the
first todo card; two in-flight cards or an explicit blocking reason halt. Human gates and standing
instructions remain binding. A failing verification command does not mean blocked or done.
The done claim still requires the green bar, required commit and clean-tree checks.
Detailed phase plans remain Markdown specifications with Outcome; status points to the board card.

Begin uses `init --title TITLE` only when no active effort exists. Existing legacy BACKLOG state
requires explicit `migrate`, retaining BACKLOG.md.legacy and custom prose; conflicting sources halt.
Missing or malformed execution state is never repaired by resetting progress or reading the summary.

Consolidate first records outcome summaries and archived phase-plan commit identities in cards.
Then use `consolidate --deliverable REPO_PATH --revision N` after every card is done. Remove only
run/ after the deliverable exists. The board, adapters and receipts survive consolidation.

External publication is optional; read references/visibility.md only when requested or enabled.

Machine-readable shape: references/board.schema.json. Runtime validation additionally checks identity, dependencies, stages and revision conflicts.

Reshaping may remove an unstarted card with a remove entry containing phase_id and reason. Its original content and identity are retained in retired_cards; never reuse retired identities or delete completed history. Remote items receive a withdrawal comment, never automatic deletion.
