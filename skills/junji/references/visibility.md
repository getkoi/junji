# Optional external visibility — Jira first

The engineer-facing flow is `/junji connect BOARD_URL`: give the agent the existing Jira board link,
review one readable summary, and approve it. Jira is optional; `.koi/board.json` remains authoritative
and works offline. Connection and publication never authorize execution or bypass human gates.

## Ownership and trust boundary

A dedicated host connection agent discovers Jira through the agent host's official Atlassian Jira
MCP, using host-managed OAuth. A dedicated host publisher applies the reviewed configuration to
accepted work. Both read actual tool schemas and metadata rather than relying on a fixed Rust
recipe. The local runtime retains the Profile, exact-review authorization checks, verification
proofs, publication requests, stable bindings, pending operations and durable receipts.

Direct MCP is a trusted host/agent boundary. The runtime checks local authorization, proofs, requests
and bindings; it cannot intercept every remote write through the host's MCP connection or claim an
independent transport audit. Read-only preparation and approved publication scope are instructions
the trusted host agent must obey, not runtime interception guarantees. Require agent-reported actual
remote readbacks, not narrative success. Receipts record that reported evidence; they are not an
independent audit of the host's remote traffic.

Coding phase agents never publish to Jira or receive its MCP server from the runtime. During Yokai
execution, the supervisor owns verified state and the pinned host publisher applies it. A publisher
cannot turn a provisional done claim into verified completion. Standalone `next` may record local
proof only after the documented bar, required commit and clean-tree checks pass, then request sync;
publication is delegated host work. Local engineering verification remains separate from remote
observations reported by the publishing agent.

## Host-managed OAuth, not Koi authentication

Connect through the host's own MCP connection/OAuth UI when interactive sign-in is needed. Reuse
host authentication only when the selected host actually makes it available to the delegated session.
Koi does not implement Jira login, token storage, refresh or a credential proxy for this path. It is
OAuth-only, with no API-token fallback. Never request secrets in chat or command arguments, store
them in repository files, read or copy host credentials, or transfer them to a sandbox.

ACP does not guarantee OAuth reuse or host-config inheritance. An unavailable named server must
fail explicitly; do not copy credentials, silently choose another server/provider, or fall back to
Koi-owned authentication. In headless execution, unavailable or expired authentication stays pending:
never open a surprise browser or onboard. Local execution continues. Preserve existing OS credentials;
this change does not authorize deleting them. Existing profiles, remote issues and bindings survive
reconnection; a legacy profile needs reviewed publisher identity before using the new path.

## Connection protocol — internal agent tooling

Read `verbs/connect.md` for the conversation. These are implementation tools for the agent, not an
engineer checklist. Standalone Junji uses `junji-board visibility`; the driver exposes compatible
`yokai visibility` operations. No Yokai executable, setup service or new wizard is required.

1. Read the accepted board, existing profile, bindings and pending state. Ask for the board URL only
   if unknown. Empty, unaccepted efforts create no remote hierarchy. `BACKLOG.proposed.json` is never
   a preparation or publication input.
2. Run `junji-board visibility prepare --board-url BOARD_URL` on the host and retain its JSON output
   in a temporary file. Optional `--agent`, `--mcp-server` and `--model` select the publishing host,
   named server and model on preparation; they are not engineer setup requirements. Prefer the known
   requesting host agent. For a new connection with no known requesting host, runtime defaults are
   `claude` and named server `atlassian`; this is not a fallback for legacy or unavailable settings.
   Save the resolved publishing host, named MCP server and optional model with the reviewed Profile.
   Reuse saved settings on later review/sync independently of coding candidate fallback and model
   tiers. Sync cannot override agent, server or model; changes require prepare/review. A legacy
   publisher missing `mcp_server` requires explicit reconnect. Missing or unavailable identity needs
   explicit resolution, never an automatic provider switch. The host connection agent discovers
   project, current account, issue
   types, required fields, board filter and workflows through the named official MCP server.
   Preparation requests remote reads only; it creates no issues and saves no approved profile.
3. Resolve technical questions through metadata discovery. For unresolved business choices, ask in
   plain language with named options. The internal `prepare --input REQUEST_FILE` protocol carries
   `board_url` and `answers`; use returned question keys and choice values, not invented identifiers.
   Check filter inclusion and required defaults before marking a filter reviewed. Preserve existing
   hierarchy and bindings unless the user explicitly reviews a change. Recommend a supported
   hierarchy appropriate to the effort; do not assume a fixed card-count rule.
4. Present one exact summary: publishing host and named MCP server, board/project, parent and child
   types, accepted cards, Reporter, fields/defaults, board-filter inclusion, status targets/equivalents/
   allowed sources, existing bindings and automatic publication scope for later accepted cards.
   Wait for explicit approval. Backlog acceptance and a general opt-in are not connection approval.
5. Only after approval, run `junji-board visibility review --input PREPARED_FILE --approve APPROVAL_HASH`
   with the unmodified preparation and exact `approval_hash`. The runtime checks exact board/profile
   hashes and scope against a fresh host-agent read-only discovery report. Compare actual remote
   readbacks of reviewed metadata, not nondeterministic recommendations. These are agent-reported
   observations, not runtime-intercepted MCP evidence. Missing evidence stays pending/review; stale
   board, configuration, host/server identity or metadata requires renewed preparation and approval.
   Never edit a hash or substitute a revision to bypass approval. Saving creates no issues:
   **setup saved** is not **publication verified**.
6. Request `junji-board visibility sync` on the host. This invokes the pinned host publisher; it is
   not permission for the orchestrating or coding agent to make independent remote writes. Require
   actual remote readbacks after operations, including issue identity, parent/child relationships,
   board-filter inclusion and requested status, matched to local requests and durable bindings.
   Read `junji-board visibility status` and returned receipts before reporting confirmed links or
   delivery. Narrative success or a locally saved binding alone is insufficient. Missing evidence
   stays pending/review. If no live publication was checked, say it has not been verified.

Status, import and reconciliation remain internal support operations. No Koi login, OAuth callback,
API-token or Keychain procedure is part of this workflow. Reconnecting must not reset a profile or
remove existing credentials, remote issues, partial hierarchies or delivery history.

## Publication and reconciliation safeguards

Publish the effort parent and accepted cards only within the approved destination and scope. Later
accepted additions may publish under that authorization; a different publishing host, named server,
destination, hierarchy or scope requires renewed review. Existing remote issues and bindings must
be reused, not recreated. Imported work requires explicit selection and still does not authorize
execution. Remote edits never silently replace local scope, dependencies, verification requirements
or human gates.

Done requires a matching local verification proof, not merely a card marked done, an agent's claim,
or a Jira status. Standalone local proof uses `verified --phase PN --commit HEAD_SHA` only after the
bar, required commit and clean-tree checks pass, then requests `junji-board visibility sync` to
delegate publication to the pinned host agent. During Yokai runs, only the supervisor records proof
and requests sync; phase agents do neither. Coding phase agents never perform Jira writes. Pending
delivery never changes engineering results; publication can resume independently after consolidation.

Keep stable creation/comment markers, partial hierarchies, bindings and receipts. Reconcile uncertain
creation before retrying; a timeout, auth failure or missing readback does not prove absence. The
internal `resolve --input FILE` flow can bind an existing `issue_key` or authorize retry with
`confirm_absent` after checking Jira, naming `phase_id` (null for the parent). Do not confirm absence
without actual remote readback evidence or silently rebind a card. Preserve unexpected human workflow
edits and present conflicts; transitions must respect reviewed targets, equivalents and source states.

Profiles remain in `.koi/adapters/jira.json`; bindings, proofs and receipts remain under
`.koi/visibility/`, outside canonical cards. Preserve these when reconnecting or consolidating.
Pending review allows progress publication for previously accepted cards, never the draft proposal.
