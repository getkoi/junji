# Verb: `iterate` — grill a post-execution delta onto the backlog

Read `references/board.md` first. Execution-state changes use validated board operations.
Heading/tag examples describe the generated summary; never edit it.

After every phase is `[done]`, add more work without consolidating. **Method artifacts only: write no product code.**
Grill a candidate delta, save its proposed split, and wait for acceptance before adding executable
phases or their how-to contracts. Execution is `/junji next` or yokai.

Chat like `references/chat.md`. Write phase plans as **how-to contracts** and BACKLOG as **reference**
per `references/docs.md`. Crystallize locks like `verbs/grill.md`.

**Guard.** Stop unless all of these hold: name the miss and the verb to run instead:

- `.koi/run/PLAN.md` exists (else `/junji plan`).
- `.koi/board.json` has **at least one** accepted card (else `/junji refine`).
- **Every** phase is `[done]`: no `[todo]`, no in-flight tag (`[planning]` / `[building]` / `[sealing]`)
  (else `/junji next` / yokai). Serial: illegal while any phase is not done.
- The user named a request. Missing → ask what to iterate, one line, stop.

Pending proposal review points Next action to /junji refine; iterate itself never occupies it.

1. **Gather.** Read `.koi/run/CONTEXT.md` (including **Skills**), `.koi/run/PLAN.md`, `.koi/board.json` (Carry-forward +
   compacted phases). If `.koi/run/researches/` exists, **read every research note**. If
   `.koi/run/DESIGN.md` exists (or `CONTEXT.md › Design contract` names it), **read it**. Skim the
   implemented code enough to name what the request would change.
1b. **Activate design when needed.** Same as **`verbs/plan.md` step 1b**: human-facing surface and no
   `DESIGN.md` → follow **`verbs/design.md`** (or instruct `/junji design …`) before locking surface
   decisions. Pure backend / library / non-UI work: skip entirely.
2. **Reason.** Form a position on the request *before* grilling: what changes, what stays out, a candidate
   slice list (count, boundaries, `depends_on`, `[gated]`).
3. **Grill.** Follow **`verbs/grill.md`**. The frontier includes the slice list (how many phases, each
   phase's in/out, `depends_on`, and `[gated]`). Do **not** write phase
   files or board cards until the frontier is empty and the user confirms shared understanding.
4. **Crystallize.** Already happening during the grill. New terms → `.koi/run/CONTEXT.md › Language`.
   New locks → CONTEXT (fact) + `PLAN.md › Key decisions` (rationale). Read `.koi/run/CONTEXT.md`
   before each of those edits and replace a span copied from that read. Do not rewrite PLAN's
   problem/approach unless the goal is reframed (standing override). Record bar changes in CONTEXT;
   Yokai must review its gate again before running. Visual locks → `.koi/run/DESIGN.md`.
5. **Propose the delta.** Follow refine's proposal/acceptance workflow in references/board.md. The
   complete order keeps all completed cards unchanged, followed by new work with temporary labels.
   Save with propose, render it and wait for acceptance of the exact candidate. Grilling a delta
   or agreeing on strategy does not implicitly accept a newly written slice list. Revisions update
   the proposal without creating executable cards, phase-plan files or retirement records.
6. **Materialize accepted work.** After explicit acceptance, accept-proposal checks the reviewed
   revision and identity, allocates fresh phase IDs and points to /junji next. If the board changed,
   refresh/review and obtain acceptance again. Only then write new phase-plan Markdown using the
   assigned IDs, with Explicitly out and a numbered Approach; link plans with validated operations.
   Runtime choices stay with their owner. No product code. Discard cancels the pending review.
7. **Commit and stop.** Conventional commit of accepted board and method artifacts, honoring Standing
   overrides. First line: `Next action: /junji next`. Then the new goals (chat cap 5; full accepted
   list in BACKLOG.md). Draft work never publishes; the dedicated host publisher handles accepted
   additions within existing authorization without authorizing execution or bypassing human gates.
   For a new or changed connection, offer `/junji connect`; iterate does not write to Jira.
