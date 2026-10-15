# Optional external visibility — Jira first

The local board always works offline. Ask during plan whether this effort should publish to Jira.
Existing issues are optional: a run normally creates its remote hierarchy. The effort becomes either
one issue with subtasks or an epic with tasks; executable cards become the children. Select the
existing Jira board/project, discover its actual issue types, required fields, columns and workflows,
and review one target per local state with equivalent remote statuses and allowed source statuses.
Keep all provider data outside canonical cards, in .koi/adapters/jira.json and .koi/visibility/.

Use `junji-board visibility` for setup, login, discover, review, import, sync, status and verified
operations. It uses the same Rust library as the driver and the host OS credential store; it
requires no Yokai executable. Browser OAuth is the default interactive login. If the user chooses
a personal API token, an organization admin must allow API-token authentication in the Rovo MCP
server. Use `junji-board visibility login --auth-method api-token --site https://example.atlassian.net
--cloud-id CLOUD_UUID`, then setup. The user enters their account email and token in the hidden CLI
prompt, never in chat or command arguments. Choose **Create API token with scopes** for **MCP v2**,
with only read, write and search Jira agent-interface scopes. Login checks read access before replacing credentials in the host OS store. API-token setup
uses the explicit site/cloud ID rather than OAuth grant discovery. `visibility login --auth-method
oauth` switches back. Each process reuses its approved credential read across syncs. A newly rebuilt
macOS binary may require Keychain approval again. Never store tokens in repository files or transfer them into a sandbox.

After the user accepts the refined backlog, review the accepted board and profile and publish parent then all children. Opt-in authorizes
automatic publication of accepted later discovered cards using the same configuration. Publishing a new card
does not authorize implementing it or bypassing its human gate. External edits never change local
scope or verification automatically. Import only explicitly selected external work.

After each standalone next passes the documented bar, required commit and clean-tree checks, record
`verified --phase PN --commit HEAD_SHA`, then sync. During Yokai execution, its supervisor alone
records verified completion and its host worker publishes; coding turns must not duplicate that work.
Failed publication stays pending and never changes engineering results. Ambiguous issue creation
requires reconciliation before retrying; preserve human workflow edits and show conflicts for review.

Use `junji-board visibility setup` for interactive connection, hierarchy and workflow selection, then sync after the initial refined board is reviewed.

Uncertain creation can be reconciled with resolve --input FILE: select an existing issue_key or
confirm_absent after checking Jira, naming phase_id (null for the effort parent). Review is interactive;
only then may a subsequent sync retry creation. Pre-registered clients may specify --redirect-port.
Connection setup also accepts additional field defaults required by the selected board's filter.

BACKLOG.proposed.json is never a publication input. Empty, unaccepted efforts create no remote
hierarchy. Pending review still allows progress publication for previously accepted cards.
