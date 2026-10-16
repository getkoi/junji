# Optional external visibility — Jira first

The engineer-facing flow is `/junji connect BOARD_URL`: give the agent the existing Jira board link,
review one readable summary, and approve it. Jira is optional; `.koi/board.json` remains authoritative
and works offline. Connection and publication never authorize execution or bypass human gates.

## Ownership and trust boundary

A dedicated host connection agent discovers Jira through MCP supplied over ACP. It reads current
tool schemas and metadata instead of relying on a fixed Rust discovery recipe or hard-coded Jira
operation selection. A dedicated host publisher applies the reviewed configuration to accepted work.
The local runtime retains the Profile, exact-review authorization checks, verification proofs,
stable bindings, pending operations and durable receipts. Agent reasoning does not replace those guards.

Coding phase agents never publish to Jira. During Yokai execution, the supervisor owns verified
state and the dedicated host publisher applies it. A publisher cannot turn a provisional done claim
into verified completion. Standalone `next` may record local proof only after the documented bar,
required commit and clean-tree checks pass, then request sync; publication is delegated host work.

Credentials stay in the host OS credential store. The runtime's local MCP transport supplies the
host agent's tool access; it does not hand tokens to the model or coding sandbox. Reuse existing
credentials and connection state. Only missing/expired authentication requires the user's secure
host login (browser OAuth or hidden API-token entry). Never request tokens in chat or command
arguments, store them in repository files, or transfer them into a sandbox. Headless execution
never opens sign-in. Do not silently change the authentication method to work around a failure.

## Connection protocol — internal agent tooling

Read `verbs/connect.md` for the conversation. The commands below are implementation tools for the
agent, not an engineer checklist. Standalone Junji uses `junji-board visibility`; the driver exposes
the compatible `yokai visibility` operations. No Yokai executable is required by standalone Junji.

1. Read the accepted board, existing profile, bindings and pending state. Ask for the board URL only
   if unknown. Empty, unaccepted efforts create no remote hierarchy. `BACKLOG.proposed.json` is never
   a preparation or publication input.
2. Run `junji-board visibility prepare --board-url BOARD_URL` on the host and retain its JSON output
   in a temporary file. The host connection agent discovers the actual project, current account,
   issue types, required fields, board filter and workflows through MCP. Preparation reads remote
   data; it does not create issues or save an approved profile.
3. Resolve technical questions through the host agent's metadata discovery. For unresolved business
   choices, ask in plain language with named options. The internal `prepare --input REQUEST_FILE`
   protocol carries `board_url` and `answers`; use the returned question keys and choice values,
   not invented identifiers. Check filter inclusion and required defaults before marking a filter
   reviewed. Preserve existing hierarchy and bindings unless the user explicitly reviews a change.
   Recommend a supported hierarchy appropriate to the effort; do not assume a fixed card-count rule.
4. Present one exact summary: board/project, parent and child types, accepted cards, Reporter,
   fields/defaults, board-filter inclusion, status targets/equivalents/allowed sources, existing
   bindings and automatic publication scope for later accepted cards. Wait for explicit approval.
   Backlog acceptance and a general opt-in are not approval of an unseen configuration.
5. Only after approval, run `junji-board visibility review --input PREPARED_FILE --approve APPROVAL_HASH`
   with the unmodified preparation and its exact `approval_hash`. Let the runtime check freshness and
   scope. Freshness replays the actual read-only MCP discovery evidence, not nondeterministic
   recommendations, and checks exact board/profile hashes. If that evidence or the reviewed board or
   configuration is stale, prepare and review again; never edit a hash or substitute a new revision
   to bypass approval. Saving creates no issues: **setup saved** is not
   **publication verified**.
6. Request `junji-board visibility sync` on the host. This invokes the dedicated host publisher;
   it is not permission for the orchestrating or coding agent to make independent remote writes.
   Read `junji-board visibility status` and the returned evidence before reporting confirmed issue
   links or delivery. Report pending/conflicting work honestly. Without live evidence, state that
   publication has not been verified.

Secure login, discovery, review, import and reconciliation operations remain available internally
for compatibility and support. Optional `--agent` / `--model` select an existing host ACP agent;
do not require them, technical IDs or profile JSON as engineer setup steps.

### Advanced authentication support

Only when secure login is needed, use the retained host auth flow. Browser OAuth remains the default;
`junji-board visibility login --auth-method oauth` explicitly selects it. API-token login uses
`junji-board visibility login --auth-method api-token --site SITE_URL --cloud-id CLOUD_UUID`;
the connection agent resolves technical site identifiers rather than asking the user to hunt for them.
The user enters the account email locally; token input is hidden. Rovo MCP API-token auth must
be allowed by the organization; choose a scoped MCP v2 token with `read:jira:agent-interface`,
`write:jira:agent-interface` and `search:jira:agent-interface`. Login checks read access before
replacing credentials. Pre-registered OAuth clients may need `--client-id` / `--redirect-port`.
These are authentication support tools, not the connection workflow. Never echo credentials.

## Publication and reconciliation safeguards

Publish the effort parent and accepted cards only within the approved destination and scope. Later
accepted additions may publish under that authorization; a different destination, hierarchy or scope
requires renewed review. Existing remote issues and bindings must be reused, not recreated. Imported
work requires explicit selection and still does not authorize execution. Remote edits never silently
replace local scope, dependencies, verification requirements or human gates.

Done requires a matching local verification proof, not merely a card marked done, an agent's claim,
or a Jira status. Standalone local proof uses `verified --phase PN --commit HEAD_SHA` only after the
bar, required commit and clean-tree checks pass, then requests `junji-board visibility sync` to
delegate publication to the host agent. During Yokai runs, only the supervisor records proof and
requests sync; phase agents do neither. Coding phase agents never perform Jira writes. Pending delivery
never changes engineering results; publication can resume independently, including after consolidation.

Keep stable creation/comment markers, partial hierarchies, bindings and receipts. Reconcile uncertain
creation before retrying. The internal `resolve --input FILE` flow can bind an existing `issue_key`
or authorize retry with `confirm_absent` after checking Jira, naming `phase_id` (null for the parent).
Do not confirm absence without evidence or silently rebind a card. Preserve unexpected human workflow
edits and present conflicts; transitions must respect reviewed targets, equivalents and source states.

Profiles remain in `.koi/adapters/jira.json`; bindings, proofs and receipts remain under
`.koi/visibility/`, outside canonical cards. Preserve these when reconnecting or consolidating.
Pending review allows progress publication for previously accepted cards, never the draft proposal.
