# Optional external visibility — Jira first

The local board always works offline. Ask during plan whether this effort should publish to Jira.
Existing issues are optional: a run normally creates its remote hierarchy. The effort becomes either
one issue with subtasks or an epic with tasks; executable cards become the children. Select the
existing Jira board/project, discover its actual issue types, required fields, columns and workflows,
and review one target per local state with equivalent remote statuses and allowed source statuses.
Keep all provider data outside canonical cards, in .koi/adapters/jira.json and .koi/visibility/.

Use `junji-board visibility` for setup, login, discover, prepare, review, import, sync, status and verified
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

## Agent-led connection

Own configuration on the user's behalf. After the backlog is accepted, ask for the Jira board URL
only if it is not already known. Reuse the saved login and connection. If login is needed, guide
the user through the host credential flow; never ask them to paste secrets into chat. Do not ask the
user to find project keys, account IDs, status IDs or write JSON that Jira metadata can resolve.

1. Run `junji-board visibility prepare --board-url BOARD_URL` and save stdout to a temporary JSON
   file. Preparation only reads Jira and the local board; it does not save settings or create issues.
2. Read `summary`, `questions` and the accepted backlog. The adapter recommends an epic with tasks
   for multiple accepted cards, or an issue with subtasks for one card when supported. Existing
   reviewed hierarchy takes precedence. Explain the recommendation and adjust it if the effort's
   scope calls for a different supported hierarchy.
3. Resolve technical questions through Jira metadata. Write a request containing `board_url` and
   `answers`, using each question's `key` and a choice's `value`, then rerun
   `junji-board visibility prepare --input REQUEST_FILE`. Supported answers include `hierarchy`,
   `project_key`, `parent_type`/`child_type`, required fields such as `parent.components`, and status
   targets such as `child.active`. Additional filter defaults go in `parent.defaults`/`child.defaults`.
   Set `filter_reviewed: true` only after checking the actual board filter and supplying the defaults
   needed for created issues to appear there. Ask the user only for business choices that the
   available context cannot settle, in plain language with named options. Never forward raw JSON
   prompts or guess a required custom value. Repeat until `questions` is empty.
4. Present one readable summary: Jira board/project, parent and child hierarchy and card count,
   Reporter, field defaults, status targets/equivalents and allowed source statuses, plus automatic
   publication of later accepted cards. Use names, not IDs. Ask the user to approve that exact
   configuration and publication scope. Merely opting into Jira or accepting the backlog does not
   approve a connection the user has not reviewed.
5. Only after that explicit approval, run `junji-board visibility review --input PREPARED_FILE
   --approve APPROVAL_HASH`, using the unmodified preparation's `approval_hash`. This records the
   chat approval without another terminal confirmation. Never edit the generated profile or use
   the hash before approval. If local state, configuration or Jira recommendations changed,
   prepare again and obtain renewed approval for the new summary.
6. Sync the approved connection. Saving itself creates no issues. Later accepted cards publish
   under that authorization without another publication question.

`junji-board visibility setup --board-url BOARD_URL` is the interactive alternative. It uses the
same preparation and one summary approval; unresolved custom questions return to the agent.

Uncertain creation can be reconciled with resolve --input FILE: select an existing issue_key or
confirm_absent after checking Jira, naming phase_id (null for the effort parent). Review is interactive;
only then may a subsequent sync retry creation. Pre-registered clients may specify --redirect-port.
Connection setup also accepts additional field defaults required by the selected board's filter.

BACKLOG.proposed.json is never a publication input. Empty, unaccepted efforts create no remote
hierarchy. Pending review still allows progress publication for previously accepted cards.
