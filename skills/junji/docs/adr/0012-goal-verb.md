# On-demand `goal` verb

## Status

Accepted. Amends the `--subagent` handoff in [0010](0010-next-subagent-option.md): a pre-authorization
sentence already in the invoking prompt is copied into the child task. Bare `--subagent` still does not
invent one. Numbered 0012 because [0011](0011-no-phase-strategy.md) records that headings carry no
strategy tag.

## Context

A human can type `/junji next` once per phase, or `/junji next --subagent` to isolate that phase, or
hand the loop to an autonomous driver. None of those asks this harness to keep going. ADR-0010 kept
verb options valueless and recorded `--subagent` as an option, not an eleventh verb. A long run still
needs a stop phase, and a way to pre-authorize gates for that run, without a driver flag. The driver
already halts on a red gate, surfaces consolidate, and never auto-runs it.

## Decision

1. **Add an on-demand `goal` verb** — eleventh verb, same progressive-disclosure skill. This window
   does not run phases. It asks the harness for its long-running goal tool and passes one objective.
   Do not name a vendor tool. If that tool is missing, stop and leave `.koi/run/` and the tree
   untouched. The objective: complete runnable phases one by one; for each, run
   `/junji next --subagent` and wait for that child's Report; then read the backlog again. One phase
   per `next`. On a halt (red gate, gated stop, missing subagent, child failure), stop the goal. Do
   not retry. Do not run `consolidate` or `iterate`. Surface consolidate; never auto-run it.
2. **`goal` never occupies Next action.** Same class as `brief`. The pointer stays
   `begin → plan → refine → next … → consolidate`.
3. **`--until <phase>` is the first valued option.** Valueless flags stay as ADR-0010 left them.
   `--until` takes the next token. `--until=p4` is an unknown option and stops the verb. Accept `4`,
   `p4`, or `P4` (case-insensitive `P` plus the backlog id). Match the heading id from refine
   (`### [todo] P4 - Title`), not the 4th heading and not `phase-04`. Inclusive: run that phase, then
   stop. Do not start a later heading whose numeric id is greater. If that id is not on the backlog,
   or the first runnable id is already greater, stop before creating the goal. An unknown token, a
   second `--until`, a second `--allow-gated`, or `--until` with no phase stops the verb and names
   the token.
4. **`--allow-gated`** pre-authorizes every gated phase in this goal run, subject to standing
   directives, same scope as `yokai --allow-gated`. Without it, a `[gated]` phase still halts inside
   the child. Both options may be set, in either order. Nothing is written to CONTEXT, METHOD, or the
   backlog. In-flight `METHOD.md` copies stay as they are. The template already allows an explicit
   pre-authorization.
5. **Handoff only.** `verbs/next.md` already proceeds when this run pre-authorized gated phases. If
   the invoking prompt already says that, the `--subagent` parent includes that one sentence in the
   child task. Bare `/junji next --subagent` does not invent authorization. No new `next` option.
   When `--allow-gated` is set, the goal objective contains that sentence and tells the goal window
   to pass it through every `/junji next --subagent`.
6. **Not the driver.** Yokai does not grow a `goal` flag. No fresh process per phase, no recovery,
   no cost ceiling.

## Consequences

- Verb count is eleven. `goal` joins `research`, `design`, `grill`, and `brief` as on-demand (none of
  those five advances Next action).
- ADR-0010 still holds for valueless flags and for `--subagent`. `--until` is the valued exception.
  It is hard to reverse and surprising next to that rule, so it is recorded here.
- Glossary **goal** is not a phase plan's **Goal & scope**.
- Skill metadata and the three plugin manifests move from 0.13.0 to 0.14.0.

## Rejected

- **Run the phases in this window when the goal tool is missing** — the human asked for that tool.
  Running the loop here hides the miss. Leave the tree untouched.
- **A yokai `goal` flag** — the driver already loops phases in fresh processes, with recovery and a
  cost ceiling. This verb is the harness goal.
- **Auto-run `consolidate` or `iterate`** — surface consolidate. The human may iterate later.
- **Retry on halt** — a red gate, gated stop, missing subagent, or child failure stops the goal.
- **Writing the pre-authorization into CONTEXT, METHOD, or the backlog** — the copied method already
  honors an explicit sentence in the invoking prompt. In-flight METHOD stays untouched.
- **A new `next` option for gated phases** — amend only the `--subagent` handoff.
- **`--until=p4`** — the value is the next token. An equals form is an unknown option.
- **The 4th heading, or `phase-04`** — the id is the backlog heading id.
- **`goal` on the Next-action pointer** — same class as `brief`. The pointer stays on the pipeline.
