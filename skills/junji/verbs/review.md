# Verb: `review` — review the PR diff and schedule the fixes

Review the branch's PR diff against its base and against the spec on disk, write one **review
note** under `.koi/run/reviews/`, and turn every Critical / Required finding into an ordinary
phase that `next` can run. **Markdown only: write no product code.** The reviewer reads, probes,
and schedules; the fix is a later `next`.

**On demand.** Human-triggered, or by `goal --review`. Legal any time after `refine` while the tree is
clean and no phase is in flight. `review` never occupies `.koi/run/BACKLOG.md › Next action`: on
**Approve** it leaves the pointer untouched; on **Request changes** it sets the pointer to
`/junji next` (same as `iterate`). The autonomous driver never calls this verb.

Not **grill** (that sharpens a plan before code exists) and not yokai's **judge** (that reviews one
Build iteration inside a phase and writes `FEEDBACK.md`). `review` reads a whole PR and writes
phases. It never writes `FEEDBACK.md`: yokai is that file's sole writer.

Chat like `references/chat.md`. Write the note as **reference** (claims with `file:line`) and the fix
phases as **how-to contracts** per `references/docs.md`.

## Options

Valueless flags stay valueless (`--name`, no value). `--base` takes the next token. `--base=main` is
an unknown option and stops the verb. An unknown token, a second `--base`, a second `--subagent`, or
`--base` with no ref stops the verb and names the token. Leave `.koi/run/` and the tree untouched.

Both may be set, in either order.

- **`--base <ref>`**: The next token is a git ref (`main`, `origin/main`, a sha). It is the base the
  diff is computed against. Without it, resolve the base in step 2.
- **`--subagent`**: Ask the harness for one isolated **subagent**. Do not name a vendor tool. The
  child does not inherit this window's transcript. Tell it to re-read `.koi/run/` and run
  `/junji review` (pass `--base <ref>` through when it was given; never pass `--subagent`): one review
  round, the protocol below. This window does not diff, probe, write, or commit. When the child
  finishes, post its Report here (base, verdict, scheduled phase ids or the halt) and stop. Do not
  retry. Do not start a second round. If this harness cannot start a subagent, stop and say so; leave
  the backlog, the tree, and `reviews/` untouched.

## Preconditions

Stop unless all of these hold; name the miss and the verb to run instead:

- `.koi/run/BACKLOG.md` and `.koi/run/CONTEXT.md` exist (else `/junji begin`). `.koi/run/PLAN.md`
  exists (else `/junji plan`). The backlog has at least one phase heading (else `/junji refine`).
- **Clean tree.** `git status --porcelain` prints nothing. A dirty tree stops the verb: name the paths.
  Do not stash or commit them.
- **No phase in flight.** No `[planning]` / `[building]` / `[sealing]` heading (else `/junji next`
  finishes it first). Two in-flight tags → stop and tell the human to leave only one.
- Remaining `[todo]` phases only **warn**: say how many, then review what is on the branch. Do not
  wait for them.

## Protocol

1. **Load state.** Read `.koi/run/CONTEXT.md` (Locked decisions, Design contract, Verification bar,
   Toolchain, Standing overrides), `.koi/run/PLAN.md` (approach and Key decisions), and
   `.koi/run/BACKLOG.md` (headings, tier tags, Carry-forward). If `.koi/run/DESIGN.md` exists (or
   `CONTEXT.md › Design contract` names it), **read it**. Read every `[done]` phase plan's **Goal &
   scope** (In scope, Explicitly out) and **Outcome**. Read earlier `.koi/run/reviews/review-*.md`
   to see what a previous round already scheduled. Do not read `researches/` or `designs/`.
2. **Resolve the base.** In this order, first hit wins: `--base <ref>`; then
   `gh pr view --json baseRefName` for the current branch (use `origin/<baseRefName>`); then
   `origin/HEAD` (`git symbolic-ref refs/remotes/origin/HEAD`). None resolvable → stop and ask for
   `--base <ref>` in one line. Record which rule produced the base: the first chat line names it.
3. **Compute the diff.** `git diff <base>...HEAD` (merge-base form) and `git diff --stat <base>...HEAD`.
   Review only this range: not the working tree, not unrelated history. An empty diff → stop: nothing
   to review; leave the tree untouched. Note the file list and size; a range that cannot be read in
   one window is a Required finding against the PR shape (split it), not a reason to sample.
4. **Spec conformance first.** Before the five axes, check the diff against what is on disk: PLAN's
   approach and Key decisions; every CONTEXT **Locked decision**; the **Verification bar** (commands
   present and unweakened: a deleted or loosened check is Critical); `DESIGN.md` for human-facing
   surfaces; each `[done]` phase's **In scope** (landed?), **Explicitly out** (respected?), and
   **Outcome** (matches the diff?). Standing overrides (branch, scope boundaries) are part of the spec.
   A diff that does more than its phases say is a finding, not a bonus.
5. **Tests first, one probe.** Read the tests the diff adds or changes before the implementation: do
   they test behavior, name the case, cover the edges the phase plan named? Then run **one mutation
   probe**: invert one condition the diff adds (drop a negation, swap `&&` for `||`, off-by-one a
   bound) in one source file, run the project's test command from `CONTEXT.md › Toolchain` (not the
   whole verification bar), then restore the file so `git status --porcelain` is empty again. A probe
   that stays green is a Required finding: name the missing test case. One probe per round. The
   reviewer never runs the verification bar: its verdict belongs to `next` and the driver.
6. **Five axes.** For each changed file, in this order: **correctness** (does it do what the phase and
   tests say; edges, error paths, state), **readability and simplicity** (names, control flow, dead
   code, abstractions that earn their weight, a conditional bolted onto an unrelated flow), **architecture**
   (existing patterns, module boundaries, duplication, dependency direction, complexity reduced rather
   than relocated), **security** (untrusted input at boundaries, secrets, authz, injection, encoding),
   **performance** (N+1, unbounded loops or fetches, hot-path allocation, sync where async is the
   pattern). When you flag a structural problem, name the move, not only the problem. Lead with what
   matters: a few high-conviction findings beat a long list.
7. **Grade every finding.** One severity each: **Critical** (blocks merge: security, data loss,
   broken function, a weakened bar, a violated lock), **Required** (must change before merge),
   **Nit** (style; author may ignore), **Optional** (worth considering), **FYI** (no action). Every
   finding carries `file:line` and its axis (or "spec" / "tests"). Do not soften a Critical into a Nit;
   do not inflate taste into Required.
8. **Write the review note.** Ensure `.koi/run/reviews/` (create on first use; not in `begin`). Copy
   `templates/review-note.template.md` to `.koi/run/reviews/review-NN.md` (`NN` = next zero-padded
   sequence in that folder; it is the **review round**). Fill base and how it was resolved, the diff
   range and stat, the verdict, spec conformance, the probe, and the findings grouped by severity.
9. **Cluster and append fix phases.** Only Critical and Required are scheduled. Cluster them by
   subsystem or root cause so one phase fixes one thing; Critical clusters come first. Continue
   `P{max+1}`. For each cluster:
   - Append an ordinary heading: `### [todo] PN - Fix: <cluster title>`. If the fix is destructive or
     needs a human decision, prefix `[gated]` as `refine` would. Copy the **tier tag** of the `[done]`
     phase the cluster mostly touches, when that heading has one; otherwise none. Then one line: the
     finding ids from the note, the files, `depends_on` when a cluster builds on another.
   - Write `.koi/run/phases/phase-NN-<slug>.md` from `templates/phase-plan.template.md`: **In scope**
     is the findings, **Explicitly out** is every other finding and any adjacent improvement, a numbered
     **Approach** naming each move, and the test the probe or the finding showed missing. Pad `NN` to
     match siblings. Never write under repo-root `phases/`.
   Record each phase id under the note's **Scheduled as**. Nit / Optional / FYI go under **Not
   scheduled**: promote one with `/junji refine`. Write **no product code**.
10. **Set the verdict and the pointer.** Zero Critical and zero Required → **Approve**: no heading, no
    phase file, Next action untouched. Otherwise → **Request changes**: set `.koi/run/BACKLOG.md ›
    Next action` to `/junji next`.
11. **Commit.** One conventional commit of the working-folder artifacts for this round (the note,
    `BACKLOG.md`, new phase files), honoring Standing overrides (e.g. commit locally, never push).
    Nothing is posted to GitHub: no PR comment, no review, no label. The tree is clean again.
12. **Report and stop.** First line: `Next action: /junji <pointer>` plus the base used and how it was
    resolved, e.g. `Next action: /junji next · base origin/main (gh pr view) · Request changes`. Then
    the note path, counts per severity, and the scheduled phases (chat cap 5; full list in the note).
    On Approve: `Approve: 0 Critical, 0 Required` and the not-scheduled counts. Do not start `next`.

## Rules

- Finding *defects* is this verb's job; *decisions* belong to grilling. A finding that needs a new
  decision names it as a question for `/junji grill`, not as a phase.
- The diff is reviewed as it is. The reviewer does not fix, rebase, or amend product code.
- A fix phase is an ordinary phase: `next`, `goal`, and yokai run it with no special casing.
- `consolidate` removes `reviews/` with the rest of `.koi/run/`; git history is the archive.
