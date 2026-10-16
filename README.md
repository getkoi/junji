# junji

Junji is a method skill for long, multi-session engineering projects. Plans, decisions, and progress live in the repository under `.koi/run/`. The context window is disposable. The folder is the memory.

Junji needs the standalone `junji-board` binary for validated local board operations, but no Yokai executable. The optional Yokai driver lives in [getkoi/koi](https://github.com/getkoi/koi) and reads those repository files without this skill installed.

## Install

```bash
npx skills add getkoi/junji
```

In the project you want to work on:

```text
/junji begin
/junji plan
/junji refine
/junji next
```

`begin` creates the working folder and surveys the repository. `plan` defines the work and runnable verification commands. `refine` decomposes it into phases. Repeat `next` to implement, verify, and commit one phase at a time. When every phase is done, `consolidate` writes the durable deliverable. Use `iterate` first when there is more work to add.

The guide is at <https://koi.deno.dev/junji/docs/guide>.

## Package

- [`skills/junji/SKILL.md`](skills/junji/SKILL.md): the skill.
- [`skills/junji/verbs/`](skills/junji/verbs/): the eleven verbs, including optional `connect`.
- [`skills/junji/templates/`](skills/junji/templates/): files `begin` copies.
- [`skills/junji/CONTEXT.md`](skills/junji/CONTEXT.md): method glossary.
- [`skills/junji/docs/adr/`](skills/junji/docs/adr/): method packaging decisions.
- [`plugin.json`](plugin.json): portable plugin manifest.
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json): Claude Code plugin.
- [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json): Codex compatibility manifest.

Check the package:

```bash
python3 scripts/check_package.py
```

## License

[MIT](LICENSE)

## Execution board

The mandatory .koi/board.json is execution state; BACKLOG.md is a generated read-only summary.
The standalone `junji-board` Rust binary provides atomic revision-checked updates without
Yokai. Install it from a Koi checkout with `./install.sh --board-only`; both tools link the same
`koi-board` library. Local execution requires no Python runtime. Existing efforts require explicit migration. Detailed phase plans remain Markdown. External
publication is optional. After accepting the backlog, use `/junji connect BOARD_URL`: a dedicated
host agent discovers Jira through MCP, you approve one exact readable summary, then the host
publisher applies accepted work within that authorization. Saved setup is not verified publication.
The runtime preserves authorization, local verification proofs and existing bindings. Coding phase
agents never publish; credentials stay on the host, outside the coding sandbox.
