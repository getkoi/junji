# Verb: connect — review an optional Jira connection

Read `references/board.md` and `references/visibility.md`. This is an optional, pointer-neutral verb:
leave the effort's `next_action`, accepted cards, dependencies and human gates unchanged. Write no
product code. The local board works offline whether connection or publication succeeds or fails.

1. **Read accepted work and existing connection state.** Use validated board operations. Require an
   active effort with accepted cards; an empty effort needs `/junji refine` and acceptance first.
   `BACKLOG.proposed.json` is never input. Pending review does not authorize publishing the proposal.
   Preserve existing profiles, remote issues, bindings and durable receipts; never start over to
   hide a conflict. Do not move this work into a coding phase or its sandbox.
2. **Get the board URL, not a configuration form.** Reuse a known destination. Ask for the existing
   Jira board URL only when missing or when the user wants a different destination. Use the agent
   host's official Atlassian Jira MCP with host-managed OAuth. If sign-in is needed interactively,
   guide the user to that host's MCP connection/OAuth UI, then resume after the host confirms access.
   Never request tokens or technical account/status/type IDs, copy credentials, or use a Koi login
   or API-token fallback. Headless auth failures stay pending without opening a browser; local work
   continues. Do not delete existing OS credentials.
3. **Delegate discovery to the host connection agent.** Follow the internal preparation protocol in
   `references/visibility.md`. Resolve and retain the publishing agent host and named MCP server;
   reuse that identity independently of coding candidates and model tiers. ACP does not guarantee
   OAuth reuse or host-config inheritance. If the named server is unavailable to the delegated
   session, fail explicitly: no credential copying or automatic provider switch. The host agent
   inspects actual tool schemas, board/filter, project, Reporter, required fields, issue hierarchy
   and workflows. Instruct read-only remote preparation; save no approved profile yet. Resolve
   technical questions from metadata; ask only for unresolved business choices. Do not guess custom
   values, assume a fixed tool inventory, or claim discovery without agent-reported actual remote
   readbacks. This direct MCP path trusts the host/agent, not a runtime transport audit.
4. **Review one exact summary.** Present publishing host and named MCP server, destination,
   parent/child hierarchy, accepted card count, Reporter, required/default fields, board-filter
   inclusion, target/equivalent/source statuses, existing bindings, and the scope of automatic
   publication for later accepted cards. Explain that publication is not execution authorization.
   Ask for explicit approval of this exact configuration and scope; opting into Jira or accepting
   a backlog is not connection approval. If anything material changes, prepare again and obtain
   renewed approval. Declining leaves the existing connection intact.
5. **Save, then request publication.** Only after approval, save the unmodified prepared configuration
   through the runtime's review operation. Then request the pinned host publisher to apply accepted
   work within that authorization. The runtime controls local authorization, proofs, requests and
   bindings, but cannot intercept every remote write made through host-native MCP. Keep that trust
   boundary explicit. Preserve uncertain operations for reconciliation rather than retrying creation
   blindly. Never publish a draft or infer verified Done from a local claim or remote status.
6. **Report the observed result.** Separate **setup saved** from **publication verified**. Require
   agent-reported actual remote readbacks of the resulting issues, relationships, filter inclusion
   and requested statuses, matched to durable bindings/receipts. Narrative success is not evidence;
   missing or conflicting evidence stays pending/review. Attribute the readbacks to the host agent,
   not an independent runtime transport audit. If no live publication was checked, say so. A failed
   or unavailable connection leaves local engineering results and Next action unchanged; stop rather
   than silently switching host, server, destination, authentication method or publication scope.
