# No phase strategy tag

## Status

Accepted — amends [0005](0005-iterate-verb.md) and [0009](0009-per-phase-model-tier.md).
[0010](0010-next-subagent-option.md) still holds: `--subagent` runs `/junji next` in one host child
and does not delegate that phase to a driver verb.

## Context

ADR-0005 told `iterate` to select `[plain]` or `[swarm]` and write that tag on new headings.
The method does not fan a phase out. Every phase is one coder. Those tags are not a planning decision.

## Decision

1. **Do not select a strategy.** `iterate` and `refine` write ordinary headings. Grill does not
   decide `[plain]` or `[swarm]`.
2. **Status rewrites drop those tags.** `next` keeps `[gated]` and any tier tag, and removes a
   leftover `[plain]` or `[swarm]`.
3. **No fan-out in the method.** The glossary and the autonomous-driver reference do not describe a swarm.

## Consequences

- A new heading is optional `[gated]`, optional tier, status, then `P<digits>`.
- A leftover tag on an old heading stays until a status rewrite strips it.

## Rejected

- **Keep the tags as annotations to preserve** — the method would still be talking about a fan-out it does not run.
