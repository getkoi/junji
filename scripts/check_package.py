#!/usr/bin/env python3
"""Package checks for the junji skill.

The context-file checks used to live in the yokai crate, which read this tree
from the koi checkout. They prove that verb quotes match the CONTEXT template
`begin` copies. The backlog check proves that template has no phase heading
yokai would parse.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "junji"

STATUSES = {"[todo]", "[planning]", "[building]", "[sealing]", "[done]"}
STRATEGIES = {"[plain]", "[swarm]"}
TIERS = {"[low]", "[medium]", "[high]", "[ultra]"}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def take_bracket(text: str, accepted: set[str]) -> tuple[str | None, str]:
    if not text.startswith("["):
        return None, text
    close = text.find("]")
    if close < 0:
        return None, text
    tag = text[: close + 1]
    if tag in accepted:
        return tag, text[close + 1 :]
    return None, text


def is_phase_heading(line: str) -> bool:
    """Match yokai's backlog heading parser. A phase needs a status tag and a P<digits> id."""
    rest = line.lstrip()
    if not rest.startswith("###"):
        return False
    rest = rest[3:].lstrip()
    if rest.startswith("[gated]"):
        rest = rest[len("[gated]") :].lstrip()
    strategy, after = take_bracket(rest, STRATEGIES)
    if strategy is not None:
        rest = after
    rest = rest.lstrip()
    tier, after = take_bracket(rest, TIERS)
    if tier is not None:
        rest = after
    rest = rest.lstrip()
    status, after = take_bracket(rest, STATUSES)
    if status is None:
        return False
    rest = after.lstrip()
    if not rest.startswith("P") or len(rest) < 2 or not rest[1].isdigit():
        return False
    return True


def assert_parser_samples() -> None:
    samples = [
        ("### [todo] P0 - Port the CLI entrypoint", True),
        ("### [gated] [swarm] [high] [todo] P2 - Rewrite adapters", True),
        ("### [swarm] [todo] P1 - migrate handlers", True),
        ("### [weird] [todo] P0 - nope", False),
        ("## Verification bar", False),
        ("### Notes", False),
    ]
    for line, expected in samples:
        got = is_phase_heading(line)
        if got != expected:
            fail(f"phase parser mismatch for {line!r}: got {got}, expected {expected}")


def context_file_spans(text: str, origin: str) -> list[tuple[str, str, int]]:
    lines = text.splitlines()
    spans: list[tuple[str, str, int]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        marker = line.lstrip()
        if marker == "```context-file":
            indent = len(line) - len(marker)
            index += 1
            dedented: list[str] = []
            raw: list[str] = []
            while index < len(lines) and lines[index].lstrip() != "```":
                content = lines[index]
                raw.append(content)
                if content == "":
                    dedented.append("")
                else:
                    prefix = " " * indent
                    if not content.startswith(prefix):
                        fail(
                            f"{origin}: context-file line is indented less than its fence: {content!r}"
                        )
                    dedented.append(content[indent:])
                index += 1
            if index >= len(lines):
                fail(f"{origin}: unclosed context-file fence")
            spans.append(("\n".join(dedented), "\n".join(raw), indent))
        index += 1
    return spans


def markdown_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*.md") if path.is_file())


def read_skill(relative: str) -> str:
    path = SKILL / relative
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        fail(f"reading {path}: {error}")
        return ""


def slice_between(text: str, start: str, end: str) -> str:
    try:
        start_at = text.index(start)
    except ValueError:
        fail(f"missing {start!r}")
        return ""
    rest = text[start_at:]
    try:
        end_at = rest.index(end)
    except ValueError:
        fail(f"missing end after {start!r}")
        return ""
    return rest[:end_at].rstrip()


def quoted_in(relative: str) -> list[str]:
    return [span[0] for span in context_file_spans(read_skill(relative), relative)]


def check_backlog_template() -> None:
    text = read_skill("templates/BACKLOG.template.md")
    hits = [line for line in text.splitlines() if is_phase_heading(line)]
    if hits:
        fail(
            "BACKLOG.template.md must not contain ### headings yokai would parse as phases:\n"
            + "\n".join(hits)
        )


def check_context_file_spans(template: str) -> None:
    spans: list[tuple[str, str, int]] = []
    for path in markdown_files(SKILL):
        text = path.read_text(encoding="utf-8")
        for dedented, raw, indent in context_file_spans(text, str(path)):
            if not dedented.strip():
                fail(f"{path} has an empty context-file block")
            if dedented not in template:
                fail(
                    f"{path} quotes a CONTEXT span that begin does not copy:\n{dedented}"
                )
            if indent > 0 and raw in template:
                fail(
                    f"{path} list indent is not an oldString; the raw fence body must miss:\n{raw}"
                )
            spans.append((dedented, raw, indent))
    if not any(indent > 0 for _, _, indent in spans):
        fail("expected a list-indented context-file fence")
    if len(spans) < 11:
        fail(f"expected the verb placeholders that begin copies, found {len(spans)}")


def check_verb_spans(template: str) -> None:
    file_map = slice_between(
        template,
        "- **Port / change from:**",
        "\n\n## Deliverable spec model",
    )
    short_language = slice_between(
        template,
        "**<Canonical term>**:\n<Definition.>",
        "\n\n## Locked decisions",
    )
    deliverable = slice_between(template, "- **Format:**", "\n\n## Standing overrides")
    code_style = slice_between(template, "<Point to the repo's style guide", "\n")
    locked = slice_between(
        template,
        "- **<Area, e.g. Architecture>:**",
        "\n\n## Design contract",
    )
    skills_must = slice_between(
        template,
        "- `<path>` (`<name>`) — <when as the docs state",
        "\n",
    )
    skills_by_role = slice_between(template, "- **design:**", "\n\n## Toolchain")
    bar = slice_between(template, "- **Language gates:**", "\n\nWire the project's")
    overrides = slice_between(template, "- **Branch:**", "\n\n## Code style")
    groups = [
        ("begin", quoted_in("verbs/begin.md"), [file_map, short_language, deliverable]),
        ("plan", quoted_in("verbs/plan.md"), [file_map, deliverable, code_style]),
        (
            "grill",
            quoted_in("verbs/grill.md"),
            [short_language, locked, skills_must, skills_by_role, bar, overrides],
        ),
    ]
    for verb, spans, required in groups:
        for span in required:
            if span not in spans:
                fail(f"{verb} does not quote this template span:\n{span}")


def check_grill_and_sections(template: str) -> None:
    grill = read_skill("verbs/grill.md")
    if "**Term**:" in template or "**Term**:" in grill:
        fail("grill names a term marker missing from the template contract")
    for heading in [
        "## What this is",
        "## Language",
        "## Locked decisions",
        "## Design contract",
        "## Skills",
        "## Toolchain",
        "## Verification bar",
        "## File map",
        "## Deliverable spec model",
        "## Standing overrides",
        "## Code style & commits",
    ]:
        if heading not in template:
            fail(f"CONTEXT.template.md is missing {heading}")
    if "It is not text already in `.koi/run/CONTEXT.md`" not in grill:
        fail("grill illustration note is missing")
    illustration = "**Turn**:\nOne prompt→stop exchange with an agent"
    if illustration not in grill:
        fail("grill illustration is missing")
    if illustration in template:
        fail("the grill illustration must not be copied into a project's CONTEXT.md")


def check_connect_contract() -> None:
    """Keep the exported router and agent/runtime ownership boundary in the package."""
    router = read_skill("SKILL.md")
    expected = {
        "begin", "research", "design", "plan", "grill", "brief", "refine",
        "connect", "next", "iterate", "consolidate",
    }
    routes = re.findall(r"^\| (\w+) \| \[verbs/([^]]+)\]\(([^)]+)\) \|$", router, re.M)
    if len(routes) != len(expected) or {verb for verb, _, _ in routes} != expected:
        fail("SKILL.md must route all eleven verbs exactly once, including connect")
    for verb, label, target in routes:
        if label != f"{verb}.md" or target != f"verbs/{verb}.md" or not (SKILL / target).is_file():
            fail(f"invalid verb route: {verb} -> {target}")
    if {path.stem for path in (SKILL / "verbs").glob("*.md")} != expected:
        fail("verb files and exported routes must match")
    for origin, terms in {
        "SKILL.md": ["Eleven verbs:", "verbs/connect.md"],
        "verbs/connect.md": [
            "pointer-neutral", "BACKLOG.proposed.json", "explicit approval",
            "existing profiles", "bindings", "setup saved", "publication verified",
            "references/visibility.md", "host connection agent",
        ],
        "references/visibility.md": [
            "local runtime retains the Profile", "prepare --board-url", "review --input",
            "--approve APPROVAL_HASH", "visibility sync", "read-only MCP discovery evidence",
            "exact board/profile hashes", "host OS credential store", "confirm_absent",
            "matching local verification proof", "Existing remote issues and bindings",
        ],
        "templates/METHOD.template.md": [
            "Coding phase agents never call Jira tools", "visibility verified",
            "visibility sync", "supervisor alone", "coding turns do neither",
        ],
        "verbs/next.md": [
            "Coding phase agents never call Jira tools", "visibility sync",
            "phase agents do neither",
        ],
    }.items():
        text = " ".join(read_skill(origin).split())
        for term in terms:
            if term not in text:
                fail(f"{origin} is missing the connect contract: {term}")


def main() -> None:
    if not (SKILL / "SKILL.md").is_file():
        fail(f"missing {SKILL / 'SKILL.md'}")
    check_connect_contract()
    assert_parser_samples()
    check_backlog_template()
    template = read_skill("templates/CONTEXT.template.md")
    check_context_file_spans(template)
    check_verb_spans(template)
    check_grill_and_sections(template)
    print("junji package check passed")


if __name__ == "__main__":
    main()
