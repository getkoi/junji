# Board contract

`.koi/board.json` is mandatory execution state. BACKLOG.md is a generated read-only view.
A card is one executable phase; an effort owns ordered cards, Next action and carry-forward.
Use the standalone `junji-board` Rust binary. Install it from a Koi checkout with
`./install.sh --board-only`; `./install.sh` installs it alongside Yokai. Never require Yokai or its
settings for method operations. Local edits need no Python runtime, credentials or network.
Yokai links the same library and supplies equivalent `yokai board` operations.

Read with `junji-board show`. Apply mutations using that exact revision:
`junji-board apply --revision N --input patch.json`.
The JSON patch may contain:
- effort: title, next_action, carry_forward.
- cards: phase_id, title, description, gated, depends_on, plan, outcome, status and blocked reason.
  Existing card patches preserve omitted fields and identity; new cards receive stable IDs and todo
  status. Card phase IDs use P<digits>. Runtime choices stay in Yokai YAML.
- order: the complete ordered list of phase IDs, with no omissions or duplicates.

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
