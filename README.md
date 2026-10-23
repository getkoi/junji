# junji

Junji is a method skill for long, multi-session engineering projects. Plans, decisions, and progress live in the repository under `.koi/run/`. The context window is disposable. The folder is the memory.

Junji needs no CLI. The optional Yokai driver lives in [getkoi/koi](https://github.com/getkoi/koi) and reads those repository files without this skill installed.

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

`begin` creates the working folder and surveys the repository. `plan` defines the work and runnable verification commands. `refine` decomposes it into phases. Repeat `next` to implement, verify, and commit one phase at a time. `goal` can ask the harness to repeat `next --subagent` until a halt or `--until`. It does not run `consolidate`. When every phase is done, `consolidate` writes the durable deliverable. Use `iterate` first when there is more work to add.

The guide is at <https://koi.deno.dev/junji/docs/guide>.

## Package

- [`skills/junji/SKILL.md`](skills/junji/SKILL.md): the skill.
- [`skills/junji/verbs/`](skills/junji/verbs/): the eleven verbs.
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
