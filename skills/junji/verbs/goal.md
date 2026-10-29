# Verb: `goal` — run runnable phases through one harness goal

On demand. This window does not run phases. It asks the harness for its long-running goal tool and
passes a single objective. If that tool is missing, stop and say so. Leave `.koi/run/` and the tree
untouched.

The objective is to complete runnable phases one by one. For each phase, run `/junji next --subagent`
and wait for that child's Report. Then read the backlog again. One phase per `next`. On a halt (red
gate, gated stop, missing subagent, child failure), stop the goal. Do not retry. Do not run
`consolidate` or `iterate`; run `review` only under `--review`. When no runnable phase remains,
surface `/junji consolidate` and stop. Do not auto-run it. The autonomous driver has the same rule
(`references/autonomous-driver.md`).

It does **not** advance `.koi/run/BACKLOG.md › Next action` (same class as `brief`); under
`--review`, the review child may set it to `/junji next`, and this window still writes nothing.
Distinct from the autonomous driver: no fresh process per phase, no recovery, no cost ceiling. Yokai
does not grow a `goal` or `review` flag.

Chat like `references/chat.md`. First line: `Next action:` as the backlog already states it.

## Options

Valueless flags stay valueless (`--name`, no value). `--until` is the first option that takes the
next token. `--until=p4` is an unknown option and stops the verb. An unknown token, a second
`--until`, a second `--allow-gated`, a second `--review`, or `--until` with no phase stops the verb
and names the token. Do not create the goal. Leave `.koi/run/` and the tree untouched.

All three may be set, in any order.

- **`--until <phase>`**: The next token is `4`, `p4`, or `P4` (case-insensitive `P` plus the backlog
  id, or the digits alone). It matches the heading id from refine (`### [todo] P4 - Title`), not the
  4th heading and not `phase-04`. Compare the integer (`P10` is greater than `P4`). Inclusive: run
  that phase, then stop. Do not start a later heading whose numeric id is greater. If that id is not
  on the backlog, or the first runnable id is already greater, stop before creating the goal.
- **`--allow-gated`**: Pre-authorizes every gated phase in this goal run, subject to standing
  directives, same scope as `yokai --allow-gated`. Without it, a `[gated]` phase still halts inside
  the child. When set, the objective contains "This run pre-authorized gated phases." and tells the
  goal window to pass that sentence through every `/junji next --subagent`.
- **`--review`**: Valueless. The objective alternates **drain** and **review**: drain runnable phases
  with `/junji next --subagent` until none remain, run `/junji review --subagent` once, read the
  backlog again, drain the fix phases it appended, review again. Stop on **Approve**, on any halt,
  or after **3 review rounds**: the third round's verdict is reported and its fix phases stay
  `[todo]` on the backlog; do not drain them. Each review child is fresh and re-reads `.koi/run/`;
  the review verb's own preconditions (clean tree, no phase in flight) hold between drains because
  every child commits. With `--until`, the cap bounds the first drain; fix phases a review in this
  goal run appended are drained even though their ids exceed the cap, and every other heading above
  the cap is still not started. `--allow-gated` passes through every `next` child as above; the
  review child never needs it. Without `--review`, the goal never runs `review`.

## Protocol

1. **Read the backlog.** Read `.koi/run/BACKLOG.md` only. If it is missing, say so and stop: point at
   `/junji begin`. Do not scaffold. Do not create the goal. Pick **first_runnable** the same way
   `next` does: the first `[planning]` / `[building]` / `[sealing]`, else the first `[todo]`. The
   phase id is the `P` plus digits on that heading, ignoring other bracket tags. Two in-flight tags →
   stop and tell the human to leave only one. Do not create the goal.
2. **Resolve options before the goal exists.** Apply **Options**. A failed `--until` check stops
   here: the id is not on a heading, or the first runnable id is already greater. Name the phase
   token. Do not create the goal.
3. **Ask for the goal tool.** Do not name a vendor tool. Pass one objective, below. If this harness
   cannot start that tool, stop and say so. Leave `.koi/run/` and the tree untouched.
4. **Stop.** This window does not load, implement, verify, or commit, and does not run `next`.
   Nothing in this verb is written to CONTEXT, METHOD, or the backlog.

## Objective

One objective. Include only the parts that apply.

- Always: complete runnable phases one by one. For each phase, run `/junji next --subagent` and wait
  for that child's Report. Then read `.koi/run/BACKLOG.md` again. One phase per `next`. On a halt
  (red gate, gated stop, missing subagent, child failure), stop the goal. Do not retry. Do not run
  `consolidate` or `iterate`. When no runnable phase remains, surface `/junji consolidate` and stop
  (under `--review`, review first).
- With `--until`: name the heading id as `P` plus the integer (`P4` when the token was `4`, `p4`, or
  `P4`). Stop after that phase, inclusive. Do not start a later heading whose numeric id is greater.
- With `--allow-gated`: include the sentence "This run pre-authorized gated phases." Tell the goal
  window to pass that sentence through every `/junji next --subagent`. Standing directives still apply.
- With `--review`: when no runnable phase remains (or the `--until` cap is reached), run
  `/junji review --subagent` and wait for its Report. Count it as one review round. On
  **Approve**, stop: surface `/junji consolidate` when no runnable phase remains, else the pointer
  as the backlog states it. On **Request changes**, read `.koi/run/BACKLOG.md` again and drain the
  fix phases that review appended (they are runnable even when their ids exceed the `--until` cap),
  then review again. After the third review round, stop whatever the verdict: report it and the ids
  left `[todo]`. A review halt (dirty tree, unresolved base, missing subagent, child failure) stops
  the goal like any other halt. Do not retry a round. Do not run `review` in this window.
