---
name: junji
description: >-
  junji — long multi-session engineering projects (ports, migrations, large refactors, greenfield)
  driven from an on-disk working folder (.koi/run/) with durable project home at .koi/. Eleven verbs:
  begin, research, design, plan, grill, brief, refine, connect, next, iterate, consolidate. Use when the user
  wants a phased/junji project, says "do the next task", or invokes /junji (optionally with a verb).
license: MIT
user-invocable: true
metadata:
  author: matheusps
  version: "0.13.0"
---

# Junji execution

Drive long projects across disposable context windows. The filesystem is durable memory.
Junji is a standalone method: no Yokai executable, runtime settings or external service is required.
The standalone `junji-board` Rust binary provides validated edits; Python is not required.
Install it from the Koi checkout with `./install.sh --board-only` before stateful verbs.

## Durable state

Read [references/board.md](references/board.md) for every stateful verb.

- `.koi/board.json`: mandatory project board; efforts and executable cards, execution state,
  Next action and carry-forward. One active effort per repository; completed effort history persists.
- `.koi/run/BACKLOG.proposed.json`: durable candidate split, with temporary labels; never executable.
- `.koi/run/BACKLOG.md`: generated read-only summary. Never execution input.
- `.koi/run/CONTEXT.md`: stable facts, locked decisions, Skills, verification bar and overrides.
- `.koi/run/PLAN.md`: strategy and rationale. CONTEXT wins for execution; PLAN wins for rationale.
- `.koi/run/METHOD.md`: copied per-phase protocol, independent of installed skills.
- `.koi/run/phases/`: Markdown phase specifications and outcomes.
- `.koi/run/DESIGN.md`, researches/ and designs/: optional binding design and research notes.

Project home .koi/ and working folder .koi/run/ are git committed. Consolidation removes only run/.
Driver settings, sensors, board and optional adapter profiles/receipts survive. Never read or write
Yokai settings in ordinary method work; runnable verification commands are sufficient for Junji.

Cards are phases: independently verifiable execution units. Keep stable IDs P<digits>, dependencies,
gated flags and descriptions on the board. Execution stages are todo/planning/building/sealing/done;
adapter-facing todo/active/done/blocked is derived. A failed check never silently weakens the bar.
Runtime strategy/model tiers live in Yokai effort YAML; preserve imported legacy annotations.

## Verbs

Read that verb's reference before executing it:

| Verb | Reference |
| --- | --- |
| begin | [verbs/begin.md](verbs/begin.md) |
| research | [verbs/research.md](verbs/research.md) |
| design | [verbs/design.md](verbs/design.md) |
| plan | [verbs/plan.md](verbs/plan.md) |
| grill | [verbs/grill.md](verbs/grill.md) |
| brief | [verbs/brief.md](verbs/brief.md) |
| refine | [verbs/refine.md](verbs/refine.md) |
| connect | [verbs/connect.md](verbs/connect.md) |
| next | [verbs/next.md](verbs/next.md) |
| iterate | [verbs/iterate.md](verbs/iterate.md) |
| consolidate | [verbs/consolidate.md](verbs/consolidate.md) |

No argument: begin if there is no active effort; otherwise follow active effort next_action.
Explicit 'do the next task' means next. Legacy projects require explicit migration before execution.
The progression is begin → plan → refine → accept the split → next… → consolidate. Optional research/design/grill/brief/connect
do not advance position. Connect delegates optional Jira setup and publication to a dedicated host agent;
its authorization never permits executing a card or changing the accepted backlog. Iterate grills a
post-execution delta and points back to next.

## Rules

One card per next. Read CONTEXT including Must Skills; load only matching Must skills for the role.
Read DESIGN when present as a binding contract. Keep phase plans Markdown, with Explicitly out,
verification commands and self-contained outcomes. Follow standing branch/push directives and human
gates. Importing plans, creating remote issues or setting up a driver never authorizes gated actions.

Refine/iterate propose and wait for acceptance before changing executable cards. Revisions allocate no
new card identities until acceptance. Pending review pauses at the next phase boundary; drafts never
publish. Requests for fewer splits are revisions, not approval.

All execution changes use junji-board operations. Never write headings or pointer changes into the
summary. Begin copies METHOD without rewriting it; consolidate preserves durable project home.
For communication follow references/chat.md; for document responsibilities follow references/docs.md.
External visibility is optional; use /junji connect when requested. Read references/visibility.md
only when requested or enabled. Coding phase agents never publish to Jira; a dedicated host publisher
applies authorized progress, and the Yokai supervisor owns verified state during driven execution.
