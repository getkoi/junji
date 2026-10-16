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
   Jira board URL only when missing or when the user wants a different destination. Reuse secure
   host authentication. If it is missing or expired, guide the user through the local browser or
   hidden credential prompt; never request secrets in chat, files or command arguments. The user
   should not have to find account/status/type IDs or author JSON.
3. **Delegate discovery to the host connection agent.** Follow the internal preparation protocol in
   `references/visibility.md`. The runtime supplies MCP through ACP and a local host transport;
   the host agent inspects live tool schemas, the board/filter, project, Reporter, required fields,
   issue hierarchy and workflows. Preparation is read-only remotely and saves no approved profile.
   Resolve technical questions from metadata; ask the user only for unresolved business choices.
   Do not guess custom values, assume a fixed MCP tool inventory, or claim discovery without evidence.
4. **Review one exact summary.** Present destination, parent/child hierarchy, accepted card count,
   Reporter, required/default fields, board-filter inclusion, target/equivalent/source statuses,
   existing bindings, and the scope of automatic publication for later accepted cards. Explain that
   publication is not execution authorization. Ask for explicit approval of this exact configuration
   and scope; opting into Jira or accepting a backlog is not connection approval. If anything material
   changes, prepare again and obtain renewed approval. Declining leaves the existing connection intact.
5. **Save, then request publication.** Only after approval, save the unmodified prepared configuration
   through the runtime's review operation. Then request the dedicated host publisher to apply the
   accepted board within that authorization. Runtime authorization, proof and binding safeguards still
   apply; the agent does not bypass them by making its own Jira writes. Preserve uncertain operations
   for reconciliation rather than retrying creation blindly. Never publish a draft or infer verified
   Done from a local claim or a remote status.
6. **Report the observed result.** Separate **setup saved** from **publication verified**. Name confirmed
   issue links and pending/conflicting work only when supported by returned evidence and durable
   bindings/receipts. If no live publication was checked, say so. A failed or unavailable connection
   leaves local engineering results and Next action unchanged; stop rather than silently switching
   destination, authentication method or publication scope.
