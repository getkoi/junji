# Mandatory local execution board

The method owns a mandatory .koi/board.json execution contract and validated standalone tooling.
Cards are phases, grouped by effort. BACKLOG.md is generated read-only; detailed phase plans remain
Markdown. This replaces the writable Markdown backlog and avoids competing execution models.
The repository-file contract works without Yokai or installed skills. External adapters are optional;
Jira is the first, translating efforts/cards to parent/child issue hierarchies.

Standalone operations use the `junji-board` Rust binary from Koi. Yokai links the same `koi-board`
library for storage, validation and adapters. The binary does not own method decisions or driver
setup; Python is not required and no runtime scripts are copied into project home.

Refine/iterate propose the backlog with temporary labels, save a separate durable draft, and wait
for user acceptance before allocating executable identities. Every reshape follows this boundary.
Pending review permits in-flight work to finish, then pauses before another phase; drafts never
publish. Accepted replacements retain complete retired history, while wording corrections retain
identity. Stale board/proposal content requires refreshed review and acceptance again.
