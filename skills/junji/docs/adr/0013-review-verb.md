# On-demand `review` verb

## Status

Accepted. Extends the option grammar in [0010](0010-next-subagent-option.md) and
[0012](0012-goal-verb.md): `--base` is the second valued option; `--subagent` on `review` reuses the
`next` child pattern. The loop that repeats this verb is [0014](0014-goal-review-loop.md).

## Context

After `next` has landed phases on a branch, the method had no verb that reads the resulting PR as a
whole. `grill` interviews a plan before code exists. Yokai's **judge** reviews one Build iteration
inside one phase and writes `FEEDBACK.md`, which yokai alone owns. A human reviewer, or a review bot,
finds cross-phase defects, spec drift, and missing tests, but their comments land on GitHub, not on
disk, so the next window cannot act on them. `iterate` already shows the mechanism for turning a
decision into runnable work: ordinary headings plus `phases/phase-NN-*.md` that `next` and yokai
consume unchanged. The review method is adapted from Addy Osmani's `code-review-and-quality` skill:
five axes, severity prefixes, tests first with a mutation probe, structural remedies named.

## Decision

1. **Add an on-demand `review` verb** — twelfth verb, same progressive-disclosure skill. Human
   triggered, or by `goal --review`. The autonomous driver never calls it.
2. **The unit is the PR diff against its base, computed with git.** Base resolution, first hit wins:
   `--base <ref>` → `gh pr view --json baseRefName` → `origin/HEAD` → stop and ask. The range is
   `git diff <base>...HEAD`. The first chat line names the base and the rule that produced it. An
   empty diff stops the verb.
3. **Preconditions.** A dirty tree stops the verb (name the paths; no stash, no commit). An in-flight
   phase (`[planning]` / `[building]` / `[sealing]`) stops the verb. Remaining `[todo]` phases only
   warn. `BACKLOG.md`, `CONTEXT.md`, `PLAN.md`, and at least one phase heading are required.
4. **Method order.** Spec conformance first: `PLAN.md`, every CONTEXT Locked decision and the
   Verification bar (a weakened check is Critical), `DESIGN.md` when present, each `[done]` phase's
   In scope / Explicitly out / Outcome. Then tests first with **one** mutation probe (invert one
   added condition, run the project's test command, restore the file; a green probe is a Required
   finding naming the missing test). Then five axes in order: correctness, readability and simplicity,
   architecture, security, performance. The reviewer never runs the verification bar.
5. **Severity is one of five**: Critical, Required, Nit, Optional, FYI. Every finding carries
   `file:line` and an axis. Only Critical and Required are scheduled.
6. **Feedback lives on disk as ordinary phases.** Critical / Required findings are clustered by
   subsystem or root cause, Critical first, and appended as `### [todo] PN - Fix: <cluster>` headings
   continuing `P{max+1}` with a full `phases/phase-NN-<slug>.md` each (same mechanism as `iterate`).
   A fix phase copies the tier tag of the `[done]` phase it mostly touches; `[gated]` under the
   `refine` rule. The full record is `.koi/run/reviews/review-NN.md` from
   `templates/review-note.template.md`; `NN` is the review round. Nit / Optional / FYI are listed
   under "Not scheduled" and promoted only through `refine`. Never `FEEDBACK.md`.
7. **Verdict.** **Approve**: zero Critical and zero Required, nothing appended, Next action
   untouched. **Request changes**: phases appended, Next action set to `/junji next`. `review` never
   occupies the pointer.
8. **One commit per round** of the working-folder artifacts (note, backlog, phase files), honoring
   standing overrides. No product code. Nothing is posted to GitHub.
9. **Options.** `--base <ref>` takes the next token; `--base=main` is unknown. `--subagent` is
   valueless and delegates one round to a fresh child that re-reads `.koi/run/` and runs
   `/junji review` (with `--base` passed through, never `--subagent`), as ADR-0010 does for `next`.
   A repeated option or `--base` with no ref stops the verb.
10. **Not the driver's judge.** No Rust changes: fix phases are ordinary phases to yokai. Yokai does
    not grow a `review` flag. The glossary says **Review** is neither **Grill** nor **Judge**.

## Consequences

- Verb count is twelve. `review` is on demand like `research`, `design`, `grill`, `brief`, and
  `goal`, but unlike those five it may set the pointer (to `next`, on Request changes only).
- `SKILL.md` dispatch names two valued options: `goal`'s `--until` and `review`'s `--base`. The
  layout gains `reviews/`. The Documents table lists review notes as reference.
- The glossary gains **review**, **Review note**, **Finding**, **Severity**, **Verdict**, **Review
  round**, and **Fix phase**, and a flagged ambiguity for "review" (verb vs judge vs grilling).
- `verbs/next.md` says a fix phase is an ordinary phase. In-flight `METHOD.md` copies are not patched.
- Skill metadata and the three plugin manifests move from 0.14.0 to 0.15.0.
- Public guide and the koi / site counts move to twelve in their own repositories.

## Rejected

- **Posting findings to GitHub** — comments are not durable memory. The next window reads
  `.koi/run/`, not a PR thread.
- **Writing `FEEDBACK.md`** — yokai is its sole writer; a second writer breaks the Build loop's
  contract.
- **Scheduling every finding** — Nits and Optionals as phases bury the backlog. `refine` promotes one
  when a human wants it.
- **Running the verification bar** — the bar's verdict is `next`'s and the driver's. The reviewer
  reads and probes; it does not grant green.
- **More than one mutation probe** — one probe proves the suite can fail; a mutation score is not a
  review.
- **Reviewing the working tree or a phase at a time** — the PR is what merges. A dirty tree means a
  phase is unfinished: `next` first.
- **Blocking on remaining `[todo]`** — a mid-branch review is useful; the warning is enough.
- **A yokai judge extension** — the judge sees one iteration of one phase and cannot write phases.
- **`--base=main`** — the value is the next token, as with `--until`.
