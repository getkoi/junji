# Agent-owned Jira connection, runtime-owned safeguards

Status: amended — host-native official MCP and host-managed OAuth replace the Koi credential proxy.

## Decision

Keep the optional, pointer-neutral `connect` verb: the engineer supplies a board URL and approves one
readable exact summary, rather than driving a configuration CLI or resolving Jira IDs. Dedicated
host agents discover and publish through their host's official Atlassian Jira MCP with host-managed
OAuth. Live tool schemas and Jira workflows need contextual reasoning, not a fixed Rust recipe.
Interactive sign-in belongs in the host's existing MCP/OAuth UI; no new setup service or wizard.

Save the publishing agent host and named MCP server identity with the reviewed Profile. Keep that
identity pinned independently of coding candidates and model tiers. Optional `--agent`, `--mcp-server`
and `--model` are preparation overrides, not prerequisites for `/junji connect BOARD_URL`. Prefer the
known requesting host; only new preparation without that context uses `claude` / `atlassian` defaults.
Save the optional model too. Sync cannot override agent, server or model; changes require renewed
prepare/review. Legacy publishers missing `mcp_server` must reconnect explicitly. ACP is the
agent session connector, not a promise of OAuth reuse or host-config inheritance. If the named server
is unavailable, fail explicitly; no credential copying or automatic provider switch.

Koi owns no Jira login, token storage, refresh or credential proxy in this OAuth-only path; there is
no API-token fallback. Headless authentication failure stays pending without opening a browser, while
local execution continues. Do not delete existing OS credentials. Preserve existing profiles, remote
issues, stable bindings, partial hierarchies and receipts; reconnecting is not a reset.

Keep Profile and prepare/review/sync as internal tooling. The runtime retains local-board authority,
exact reviewed authorization, verification proofs, publication requests, stable bindings and
uncertain-operation reconciliation. Coding phase agents never publish; the Yokai supervisor owns
verified state during execution. The publisher cannot manufacture local completion proof.

## Trade-off and evidence

Direct MCP is an accepted trusted host/agent boundary: the runtime validates local authorization,
proofs, requests and bindings but cannot intercept every remote write or claim an independent
transport audit. Read-only discovery and publication scope are trusted-agent obligations. This
replaces the earlier local-transport evidence claim; do not describe agent-reported observations as
independently captured MCP traffic.

Require agent-reported actual remote readbacks, matched to local requests and bindings, before
reporting publication verified. Narrative success is insufficient; missing evidence stays pending/
review. Uncertain creates require reconciliation before any retry, not a blind second create. Saving
a connection is distinct from verifying publication, and remote delivery never changes engineering
verification results.

## Consequences

The host owns its OAuth lifecycle and server configuration. No credentials enter the repository or
coding sandbox. Authentication unavailable to a delegated session must be diagnosed explicitly,
even if the interactive host is already signed in. Legacy identity-free profiles need reviewed host/
server selection without discarding their bindings or issues. The method stays usable offline.
