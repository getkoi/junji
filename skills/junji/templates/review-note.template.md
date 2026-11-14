# Review NN — <branch or PR title>

**Reference: review findings.** Claims with `file:line` and an axis; no "so we should…" beyond the
named fix. The fix itself is a phase, never product code written here.

**Base:** `<ref>` — resolved via <`--base` | `gh pr view` | `origin/HEAD`>
**Diff:** `<base>...<head sha>` — <N> files, +<added> −<deleted>
**Round:** <NN>
**Verdict:** <Approve | Request changes>

## Spec conformance

<The diff against `PLAN.md` approach and Key decisions, every `CONTEXT.md` Locked decision, the
Verification bar (present, unweakened), `DESIGN.md` when present, and each `[done]` phase's In scope /
Explicitly out / Outcome. Claims only. A gap here is also a finding below.>

## Tests

<Coverage of the diff: which cases the new or changed tests prove, which named edges they skip.>

**Probe:** `<file:line>` — <the inverted condition> — `<test command>` → <red (covered) | green (gap:
the missing case)>

## Findings

<Group by severity. Each line: `path:line` — axis (correctness · readability · architecture · security ·
performance · spec · tests) — finding. Fix: the move. Number them F1, F2, … across all groups.>

### Critical

- F1 `path:line` — <axis> — <finding>. Fix: <the move>.

### Required

- F2 `path:line` — <axis> — <finding>. Fix: <the move>.

### Nit

- F3 `path:line` — <axis> — <finding>.

### Optional

- F4 `path:line` — <axis> — <finding>.

### FYI

- F5 `path:line` — <axis> — <note>.

## Scheduled as

<One line per fix phase: heading id, title, the finding ids it closes. Critical clusters first.
`_none — Approve_` when nothing was scheduled.>

- P<N> `Fix: <cluster title>` — F1, F2

## Not scheduled

<Nit / Optional / FYI by id. Promote one with `/junji refine`; it is not a phase until then.>

- F3, F4, F5
