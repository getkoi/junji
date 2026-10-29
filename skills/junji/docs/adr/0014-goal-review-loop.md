# `goal --review` drain-and-review loop

## Status

Accepted. Amends [0012](0012-goal-verb.md): `goal` gains a third option and may run one verb other
than `next` under it. Depends on [0013](0013-review-verb.md) for the `review` round it repeats.

## Context

ADR-0012 made `goal` a harness goal that repeats `/junji next --subagent` and stops when no runnable
phase remains, never running `consolidate` or `iterate`. ADR-0013 made `review` write fix phases to
the backlog. Run by hand, the human alternates: `goal`, `review`, `goal`, `review`. Nothing in that
alternation needs a human decision until the verdict is Approve or the loop stops converging. A
goal that drains, reviews, and drains again closes the loop without a driver flag or a new verb.

## Decision

1. **`--review` on `goal`** is valueless. It is the only way the goal runs `review`; without it the
   ADR-0012 objective is unchanged. All three options may be set, in any order; a second `--review`
   stops the verb.
2. **The objective alternates drain and review.** Drain: `/junji next --subagent` per phase until no
   runnable phase remains. Review: `/junji review --subagent` once. Then read the backlog again and
   drain the fix phases it appended. Repeat.
3. **Stop conditions, first that applies**: a halt from any child (red gate, gated stop, dirty tree,
   unresolved base, missing subagent, child failure); a review verdict of **Approve** (surface
   `/junji consolidate`, do not run it); or the end of the **third review round**. After the third
   round the verdict is reported whatever it is; its fix phases stay `[todo]` and are not drained.
   Do not retry a round.
4. **With `--until`**, the cap bounds the first drain. Fix phases a review in this goal run appended
   are drained even though their ids exceed the cap; every other heading above the cap is still not
   started. `--allow-gated` passes through every `next` child as before; the review child never
   needs it.
5. **Each review child is fresh** (ADR-0010 pattern): it re-reads `.koi/run/` and runs
   `/junji review`. The verb's own preconditions hold between drains because every `next` child
   commits and every review child commits.
6. **This window still writes nothing.** The review child may set Next action to `/junji next`; the
   goal window does not touch CONTEXT, METHOD, or the backlog. Yokai does not grow a `goal` or
   `review` flag.

## Consequences

- `verbs/goal.md` names `--review` under Options and Objective, and its "do not run `consolidate` or
  `iterate`" sentence permits `review` only under `--review`.
- The glossary's **goal** and **Review round** entries name the three-round cap.
- The round cap is the loop's only budget; a run that reaches it with Request changes leaves the
  pointer at `/junji next` so a human can continue with `goal` again or read the third note.

## Rejected

- **Unbounded rounds** — a reviewer and a coder can disagree forever; three rounds is enough to show
  convergence or its absence.
- **Review after every phase** — the unit of review is the PR, not a phase; yokai's judge already
  covers the phase.
- **Draining the third round's fix phases** — the stop is the cap, not "one more". A human decides.
- **Reviewing when `--until` stopped the drain with `[todo]` left and no `--review`** — the goal
  does not run `review` unless asked.
- **A `--rounds <n>` option** — a second valued option on `goal` for one number nobody has asked to
  change. Reopen when a run needs it.
- **Auto-run `consolidate` on Approve** — surface it, as ADR-0012 does.
