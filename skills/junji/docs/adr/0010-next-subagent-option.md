# Verb option `--subagent` on `next`

## Status

Accepted

## Context

Claude Code's `/code-review [--comment]` keeps the command and changes where the result is delivered.
Bare `/junji next` fills the parent window with one phase's research, edits, and gate output. A human
who wants that phase isolated still needs the Report in the window they invoked. Yokai already spawns
a fresh window per phase. Swarm is a driver Build fan-out. Neither is this request.

## Decision

1. **Verb options.** Tokens after a verb are `--name` with no value. The verb reference defines which
   options exist. An unknown option stops the verb and names the token. "Do the next task" is bare
   `next`. Today only `next` defines an option.
2. **`--subagent`.** This window asks the harness for one child and does not name a vendor tool. The
   child does not inherit this window's transcript. It re-reads `.koi/run/` and runs `/junji next`
   with no options, so it cannot delegate again. This window does not load, implement, verify, or
   commit. When the child finishes, this window posts that Report and stops. One phase. No retry.
3. **No subagent, no work.** If the harness cannot start a subagent, stop and say so. Leave the
   backlog, phase plan, and tree untouched. A `[gated]` phase still halts inside the child. The parent
   does not pre-authorize it.
4. **Skill dispatch only.** The option is not a backlog tag, a standing override, or a yokai launch
   flag. Do not patch in-flight `METHOD.md`. The copied method stays the seven steps. Yokai does not
   grow this flag. A **subagent** is one host child for a single interactive `next`. **Swarm** stays
   yokai's partition-and-merge Build act.

## Consequences

- `SKILL.md` dispatch parses verb options before the verb body runs. `verbs/next.md` holds the
  `--subagent` protocol. The glossary defines **Verb option** and **Subagent**.
- ADR-0001 still holds: one skill, verb bodies under `verbs/`. This is an option, not an eleventh verb.
- Public guide and cheatsheet name the flag. Existing working-folder `METHOD.md` copies stay authoritative.

## Rejected

- **Inline fallback** — the human asked for a child. Running the phase here hides the miss.
- **Shared transcript** — the working folder is the memory. The child re-reads it.
- **A yokai `--subagent` flag** — the driver already uses a fresh window per phase.
- **A backlog tag or standing override** — the choice is this invocation only.
- **Patching in-flight `METHOD.md`** — that file is stable after `begin`.
- **Swarm, or more than one child** — fan-out stays a driver Build act. One phase, one child.
