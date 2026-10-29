# junji method — context

Domain glossary for the **junji method**: the project-agnostic skill that teaches a coding agent to
drive a long, decomposable project across disposable context windows from an on-disk working folder. The
method is markdown and discipline only; everything project-specific lives under `.koi/` (project home +
working folder), never in the skill. The method rests on one idea: *the filesystem is the durable memory,
the context window is a disposable cache.*

> This is the **method** context. The runtime **driver**'s vocabulary lives in
> [`crates/yokai/CONTEXT.md`](https://github.com/getkoi/koi/blob/main/crates/yokai/CONTEXT.md).
> The map is [`CONTEXT-MAP.md`](https://github.com/getkoi/koi/blob/main/CONTEXT-MAP.md).

## Language

### The folder and the windows

**Project home**:
The durable repository home shared by method and optional driver. Junji creates it as needed;
reusable infrastructure survives the end of an effort.
_Avoid_: working folder (that is `.koi/run/`), workspace, project dir

**Working folder**:
The `.koi/run/` subtree the method maintains for one effort: git-committed volatile scaffolding
(plans, decisions, position, driver run prefs). `consolidate` removes only this subtree
(`git rm -r .koi/run/`). The deliverable does not live here.
_Avoid_: project home, workspace, scratch dir

**Window**:
One agent session working on the project: deliberately disposable: it can be thrown away and rebuilt by
re-reading the working folder. An autonomous driver spawns a fresh window per phase.
_Avoid_: session (an ACP concept in the driver), run, context, subagent

**Subagent**:
One host child that runs a single `next` phase for `/junji next --subagent`, or a single **review
round** for `/junji review --subagent`. It re-reads the working folder and runs `/junji next` (or
`/junji review`), not a driver verb. The parent window posts the Report when the child finishes.
If the invoking prompt already says this run pre-authorized gated phases, the parent includes that one
sentence in the child task. Bare `--subagent` does not invent it.
_Avoid_: window (the parent session), autonomous driver

### The twelve verbs

**Verb**:
One of the method's twelve dispatchable commands, parsed as the first argument to `/junji`. The pipeline is
`begin → (research*|design*) → plan → refine → next … → (iterate → next …)* → consolidate`, with
`research`, `design`, `grill`, `brief`, and `goal` available on demand at any point (none of those five advances
the Next-action pointer). `iterate` is on demand after every phase is `[done]`; it moves the pointer only
`consolidate → next`. `review` is on demand once the tree is clean and no phase is in flight; it never
occupies the pointer and sets it to `next` only on Request changes. `goal` never occupies the pointer
(same class as `brief`).
_Avoid_: command, subcommand, action

**Verb option**:
A `--name` token after a verb on `/junji`, for that invocation only. The verb reference defines which
options exist. Flags have no value, except `goal`'s `--until`, which takes the next token (`4`, `p4`,
or `P4`), and `review`'s `--base`, which takes a git ref. `--until=p4` and `--base=main` are unknown
options. An unknown option stops the verb.
_Avoid_: standing override, status tag, strategy, tier, yokai launch flag

**begin**:
The verb that copies `METHOD.md` and `BACKLOG.md` from the skill templates (byte-identical, no rewrite)
and surveys the repo for *observable* facts into `CONTEXT.md` (candidate terms, file map, toolchain,
**Skill scout**). Makes no load-bearing decisions and is idempotent. CONTEXT is the only file it authors.
_Avoid_: init (the driver's CLI wizard, a different thing), setup (the CLI's project-home
scaffold, also a different thing), scout (the step, not a verb)

**research**:
An optional on-demand verb that investigates factual questions against primary sources and writes one
cited **research note** per question under `.koi/run/researches/`. Context for `plan` and `grill`; does
not advance the Next-action pointer and does not lock decisions. Distinct from **phase research** inside
`next`.
_Avoid_: investigate, study, phase research

**design**:
An optional on-demand verb that synthesizes a binding **visual / experiential contract** for human-facing
surfaces into `.koi/run/DESIGN.md` (working notes under `.koi/run/designs/`). Research → analyse →
consolidate; follows **Skills** rows for this verb; may grill unsettled visual direction or which of
several design skills via `verbs/grill.md`. Does not advance the Next-action pointer. `plan` and
`iterate` may activate it when the work is human-facing and `DESIGN.md` is missing. Distinct from
grilling's **design tree** (decision topology).
_Avoid_: design tree, mockup, wireframe, Skill scout (begin's step)

**plan**:
The thinking verb: reasons and grills the source into a plan, runnable verification commands and
binding project facts. It may reuse existing sensors but does not require or create driver setup.
_Avoid_: spec, blueprint

**grill**:
An extra standalone grilling pass, on demand, to sharpen a soft plan or fuzzy terminology. Requires
`PLAN.md`, and does not advance the Next-action pointer. Uses frontier rounds (see **Grilling**). Also
used inside `plan`, `design`, and `iterate`. Reads `DESIGN.md` when present. Not the **review** verb:
grill sharpens a plan before code exists; review reads a PR diff after it.
_Avoid_: review (the verb, a different thing), interrogate, critique

**brief**:
An on-demand verb that returns a chat-only product briefing synthesized from `[done]` Outcomes and
CONTEXT: a regenerable projection, never stored, never moving Next action. Distinct from **Chat
contract** and from **Outcome**.
_Avoid_: recap, status, handoff, summary, chat contract

**refine**:
The verb that decomposes the plan into ordered, independently-verifiable phases or reshapes an
unfinished phase list. Human gates and dependencies remain method concerns; runtime choices do not.
_Avoid_: decompose (only its first mode), breakdown, iterate

**next**:
The verb that runs ONE full phase end to end: load → phase research → write or reuse the phase plan →
implement → verify → compact → commit. It then stops. The per-phase loop a human or an autonomous driver
calls repeatedly. Skips writing the phase file when a matching `phases/phase-NN-*.md` already exists
(`iterate` writes these). Obeys `.koi/run/DESIGN.md` when present for human-facing output. Implement
follows **Skills** Must rows for `next` whose *when* matches the phase. The `--subagent` **verb option**
delegates that phase to one **subagent**; bare `next` runs it in this window. If the invoking prompt
already says this run pre-authorized gated phases, that one sentence is part of the child task.
_Avoid_: run (the driver's CLI subcommand), execute-all, step

**goal**:
An on-demand verb that asks the harness for its long-running goal tool and passes one objective:
complete runnable phases one by one by running `/junji next --subagent` and waiting for each child's
Report. This window does not run phases. If the tool is missing, it stops and leaves `.koi/run/` and
the tree untouched. `--until <phase>` stops after that backlog heading id, inclusive. `--allow-gated`
pre-authorizes gated phases for this goal run, subject to standing directives, and the objective tells
the goal window to pass that sentence into every child task. On a halt, it stops and does not retry.
It does not run `consolidate` or `iterate`; `--review` makes it alternate draining runnable phases
with `/junji review --subagent`, stopping on Approve, on a halt, or after three **review rounds**.
It does not advance the Next-action pointer. Distinct from the **autonomous driver**: no fresh process
per phase, no recovery, no cost ceiling. Yokai does not grow a `goal` flag.
_Avoid_: Goal & scope (a phase-plan section), autonomous driver, yokai launch flag

**review**:
An on-demand verb that reviews the branch's PR diff against its base (`--base <ref>`, else
`gh pr view`, else `origin/HEAD`) and against the spec on disk (PLAN, CONTEXT locks and bar, DESIGN,
each `[done]` phase's In scope / Explicitly out / Outcome), tests first with one mutation probe, then
five axes: correctness, readability and simplicity, architecture, security, performance. Writes one
**review note** under `.koi/run/reviews/` and appends every Critical / Required **finding** as an
ordinary **fix phase** (heading + `phases/phase-NN-*.md`), then commits those working-folder files.
Stops on a dirty tree or an in-flight phase; remaining `[todo]` only warn. Writes no product code and
never `FEEDBACK.md`; posts nothing to GitHub; never runs the verification bar. `--subagent` delegates
one round to a fresh child. Neither **grill** (plan-time) nor yokai's **judge** (one Build iteration
inside a phase).
_Avoid_: judge (yokai's advisory Build reviewer), grill, code review bot, audit

**iterate**:
The verb that, after every phase is `[done]`, grills a request (including how to slice it) and appends N
already-specced phases to the backlog. Each includes a heading and a full `phases/phase-NN-*.md` contract. The verb then commits those working-folder artifacts. Write no product code. Never occupies Next action; sets the
pointer to `/junji next`. Repeatable, serial (illegal while any phase is not `[done]`). Distinct from yokai
Build **iteration**.
_Avoid_: iteration (Build loop pass), refine (live-list reshape), plan (rewrites strategy), task

**consolidate**:
The final verb: collapses the working folder into one repo-native deliverable named for what was
delivered, then removes `.koi/run/` in a single commit. Project-home infrastructure (`sensors/`,
sandbox) survives. Destructive for the run; git history is the archive.
_Avoid_: finalize, archive, cleanup

### The documents in the working folder

**Source doc**:
The input to `plan`: the RFC / ADR / PRD / rough idea the user points at, which `plan` turns into
`PLAN.md`.
_Avoid_: requirements, ticket

**PLAN.md**:
The **explanation** document: problem, chosen approach, reasoning, key decisions *with rationale*, success
criteria. Written for a human. `CONTEXT.md` wins for execution, PLAN wins for rationale. Not a how-to.
Visual / experiential system for human-facing surfaces lives in **DESIGN.md**, not here.
_Avoid_: spec, visual system, roadmap, how-to

**DESIGN.md** (of a managed project run):
The binding visual / experiential **reference** for this run's human-facing surfaces, written by the
`design` verb. Tokens and checkable rules, not an essay. Cites and inherits a project/root design doc
when one exists; records this-run deltas only. Never overwrites the project design doc.
`CONTEXT.md › Design contract` points here. Optional until first `design` use; removed with `.koi/run/`
on `consolidate`.
_Avoid_: project DESIGN.md (durable product doc), design note, mockup

**Design note** (`.koi/run/designs/NN-<slug>.md`):
A **reference** capture written during the `design` verb's research stage: one note per reference (or
project design doc). Cited findings only; not the binding contract.
_Avoid_: DESIGN.md, research note

**CONTEXT.md** (of a managed project):
The stable **reference** inside a managed project's working folder: orientation, locked decisions
(**fact-only**), optional Design contract, **Skills**, verification bar, file map, deliverable spec model, standing
overrides, and the toolchain commands `begin` detected. A `next` window reads this and never needs
`PLAN.md`. Not this repo's own root `CONTEXT.md`. The verification bar is the runnable commands in
that file. Existing `.koi/sensors/*.sh` scripts may implement those commands.
_Avoid_: spec, plan, config, explanation

**Design contract** (CONTEXT section):
The CONTEXT pointer filled by `design`: path to `.koi/run/DESIGN.md` plus the rule that human-facing
surfaces in this run must obey it. Absent or "none" when design never ran.
_Avoid_: DESIGN.md (the file), verification bar, Skills (the skill map)

**Skill scout**:
The `begin` step that records which in-repo skills this run must follow. Reads project docs for
**Must** names, resolves them against on-disk `SKILL.md` trees (**catalog**), writes
`CONTEXT.md › Skills`. Facts only; not a verb. Distinct from begin's whole **reconnaissance**
(orientation, file map, toolchain, this step).
_Avoid_: reconnaissance (the whole begin survey), scout verb, yokai Guide, research (the verb)

**Skills** (CONTEXT section):
The run's skill map: **Must** (named in project docs, with *when* and roles), **Available** (catalog
not named), and a **by-role** index (`design`, `next`, yokai `plan` / `coder` / `judge` / `seal`).
Filled by Skill scout; later windows follow their Must rows. Not File map, not Design contract.
_Avoid_: Guide (yokai feedforward), plugin, harness skill (user-global, not in-repo)

**Design skill**:
An in-repo visual / frontend / UI `SKILL.md` that `design` follows when Must-for-`design` or, if none,
when it is design-flavored Available (Impeccable, frontend-design, or a matching description).
_Avoid_: design (the verb), DESIGN.md, Skill scout

**METHOD.md**:
The stable **how-to** a fresh window follows for "do the next task": byte-copied from the skill
template by `begin` and never edited afterward. Includes a **Report** subsection so `next` windows chat
without reloading the skill.
_Avoid_: HOW-WE-WORK (old name), readme, guide, process doc

**Backlog** (`BACKLOG.md`):
The living **reference**: the Next-action pointer, the ordered phase list with status markers, and
carry-forward decisions. Compacted by `next` every phase.
_Avoid_: worklog (old name), todo-list, log

**Next action** (pointer):
The line at the top of `BACKLOG.md` naming the verb a fresh or headless window runs next: the on-disk
source of truth for "what's next". Advances `begin → plan → refine → next … → consolidate` (`research`,
`design`, `grill`, `brief`, and `goal` never move it; `iterate` never occupies it and moves it only
`consolidate → next`; `review` never occupies it and sets it to `next` only on Request changes).
_Avoid_: cursor, current step, status

**Research note** (`.koi/run/researches/NN-<slug>.md`):
A **reference** findings file written by the `research` verb: one cited note per factual question.
Claims only. Optional context for `plan` and `grill`; created on first `research` use; removed with
`.koi/run/` on `consolidate`.
_Avoid_: RESEARCH.md, investigation, phase research, design note

**Review note** (`.koi/run/reviews/review-NN.md`):
The **reference** record of one **review round**: the base used and how it was resolved, the diff
range, spec conformance, the mutation probe, every **finding** grouped by **severity** with
`file:line` and axis, the **verdict**, "Scheduled as" (fix-phase ids) and "Not scheduled". `NN` is
the round. Created on first `review` use; removed with `.koi/run/` on `consolidate`. Never
`FEEDBACK.md` (yokai's file).
_Avoid_: FEEDBACK.md, review comment, judge note, research note

**Finding**:
One defect or gap the `review` verb records: `file:line`, an axis (correctness, readability,
architecture, security, performance, spec, or tests), the problem, and the named fix. Numbered `F1,
F2, …` within a review note. Critical / Required findings are clustered into **fix phases**; the rest
wait under "Not scheduled" until `refine` promotes one.
_Avoid_: comment, issue (a tracker item), FEEDBACK entry, veto

**Severity**:
The one grade every finding carries: **Critical** (blocks merge: security, data loss, broken function,
a weakened bar, a violated lock), **Required** (must change before merge), **Nit** (style; author may
ignore), **Optional** (worth considering), **FYI** (no action). Only Critical and Required are
scheduled. Not a **tier** and not a **status tag**.
_Avoid_: priority, tier, blocking/non-blocking (say the grade), P0/P1 (phase ids)

**Verdict**:
The review round's result, one of two: **Approve** (zero Critical and zero Required; nothing
appended; Next action untouched) or **Request changes** (fix phases appended; Next action set to
`/junji next`). Not the **gate** verdict: the reviewer never runs the verification bar.
_Avoid_: gate result, LGTM, pass/fail, green/red (gate words)

**Review round**:
One invocation of `review`: one note, one verdict, one commit. `goal --review` runs at most three per
goal run, alternating with drains of `next --subagent`. Not a Build **iteration** and not a grill
**round**.
_Avoid_: iteration, grill round, pass, cycle

**Sensor** (`.koi/sensors/*.sh`):
An optional executable check that can implement part of the method’s verification bar.
Yokai requires a reviewed set of sensors for its aggregate gate; Junji can run ordinary commands.
_Avoid_: gate.sh, test script, CI script, check

**Gate** (aggregate):
The verification-bar verdict: green iff every documented check passes. Existing sensors may
implement these checks; sensor files are not required by the method.
_Avoid_: gated phase (`[gated]`), sensor (one script), gate.sh

### Phases and their contract

**Phase**:
One coherent, independently-verifiable unit of work in the phase list: the unit `refine` produces,
`iterate` may append, and `next` runs. (Same meaning the driver uses.)
_Avoid_: task, step, ticket, milestone

**Phase plan** (`.koi/run/phases/phase-NN-<slug>.md`):
The per-phase **how-to contract** `next` writes before implementing, or **`iterate` writes** before
`next`/yokai run: goal & scope, an Explicitly-out list, a numbered Approach, tests/gate, and an Outcome
section added on completion. Not a tutorial. Goal & scope is that phase's in and out list, not the
`goal` verb. `next` reuses a matching file when it already exists.
`phases/` under the working folder is an append-only build log.
_Avoid_: task file, subplan, spec, tutorial

**Phase research**:
Step 2 of `next`: read the exact source files the phase plan names and study idioms for that slice. Not the
`research` verb and not a research note.
_Avoid_: research (the verb), investigate

**Fix phase**:
An ordinary **phase** the `review` verb appends for one cluster of Critical / Required findings
(by subsystem or root cause, Critical first): a `### [todo] PN - Fix: <cluster>` heading continuing
`P{max+1}`, copying the tier tag of the `[done]` phase it mostly touches, plus a full phase plan whose
In scope is those findings. `next`, `goal`, and yokai run it with no special casing. Not a Build
**iteration** and not a FEEDBACK entry.
_Avoid_: follow-up, patch, review task, iteration, FEEDBACK item

**Explicitly out**:
The phase plan's scope-guard list of what a phase deliberately does *not* do: what stops scope creep.
_Avoid_: non-goals, exclusions, out-of-scope (say "Explicitly out")

**Outcome**:
The paragraph `next` appends to a phase plan on completion: what shipped, key findings, gate result,
self-contained so the next window needs nothing else. The **brief** verb synthesizes these into chat; it
does not replace this paragraph.
_Avoid_: result, summary, conclusion

**Gated phase (`[gated]`)**:
A phase prefixed `[gated]` that must not auto-run: destructive, irreversible, or needing a human decision.
`next` stops before one unless the run was pre-authorized.
_Avoid_: blocked, locked, paused

**Status tag**:
The bracket token on a BACKLOG heading: `[todo]` `[planning]` `[building]` `[sealing]` `[done]`. Optional
`[gated]` prefix. Distinct from **tier**, from yokai Build **iteration**, and from the TUI rail's
**stations**.
_Avoid_: pending, in progress

**Tier**:
An optional driver capability band used to select model candidates. Legacy heading annotations
remain usable, but ordinary Junji planning and execution do not require them.
_Avoid_: model, task, role profile, strategy, harness

### Correctness and decisions

**Verification bar**:
The documented, runnable commands that must all succeed for work to count as done.
Sensors may implement those commands, but they are not required by the method.
_Avoid_: acceptance criteria, definition of done, tests, bespoke growing assertion script

**Locked decision**:
A settled choice from grilling, recorded **fact-only** in `CONTEXT.md › Locked decisions` (its rationale
in `PLAN.md › Key decisions`). Binding on every later window; not to be relitigated.
_Avoid_: assumption, note, ADR (a heavier, repo-level record)

**Standing override**:
A durable user directive that outranks the default protocol (branch, push policy, scope boundaries),
recorded in `CONTEXT.md` and honored verbatim by every window.
_Avoid_: setting, preference, flag

**Carry-forward decisions**:
The `BACKLOG.md` section holding non-obvious facts later phases depend on: environment gotchas, chosen
versions/APIs, architectural asymmetries. The memory a fresh window inherits.
_Avoid_: notes, changelog, history

### Output and process

**Deliverable spec model**:
The section outline, native location, and filename convention that `consolidate` follows. `plan` derives these values from the host repository and records them as data.
_Avoid_: output format, template, schema

**Deliverable**:
The final repo-native document `consolidate` writes into the repo's spec home (`specs/`, `docs/adr/`,
`rfcs/`), named for what was delivered: never `SPECIFICATION.md`. Follows the host outline; narrative
default is explanation + locked facts, not a changelog. Distinct from the working folder's `phases/`
build log.
_Avoid_: spec (overloaded: see below), output, artifact

**Chat contract**:
How a junji window chats with a human: lead with position + next action, number steps, show the win, no
preamble. SSOT `references/chat.md`; always-on summary in `SKILL.md › Chat`; `next` windows follow
`METHOD.md › Report`. Not a verb. The **brief** verb still obeys this contract, with an extra three-block
product shape.
_Avoid_: talk contract, tone guide, ADHD mode, style prompt

**Document type**:
The fixed purpose of a working-folder file: **explanation** (PLAN), **reference** (CONTEXT, BACKLOG,
DESIGN, research / design / review notes), **how-to** (METHOD, phase plan). Consolidate follows the host outline. SSOT
`references/docs.md`. Junji does not generate tutorials. Types are method-fixed, not chosen per project.
The **brief** verb writes no file and is not a document type. The **goal** verb writes no file either.
_Avoid_: template kind, genre, outline-approval

**Grilling**:
Junji's relentless frontier-round interview (`verbs/grill.md`) that sharpens the plan *and builds the
domain model as it goes*, writing terms to `CONTEXT.md › Language` and fact-only locks to Locked
decisions immediately. Each round's first line is the ask; it asks every decision whose prerequisites
are settled (numbered, with recommended answers), then waits. If a round would exceed ~5 questions, ask
**ADR-worthy** ones first (hard to reverse, surprising, real trade-off). Facts are explored (or
researched into notes) rather than asked. The engine of `plan` step 3, the `grill` verb, unsettled
visual direction or design-skill choice inside `design`, and `iterate` (where the slice list is part of
the same tree). Maps work as a **design tree** (decision topology: not the `design` verb). Must Skills
rows are not re-litigated.
_Avoid_: review, Q&A, interrogation, one-question-at-a-time, design (the verb)

**Autonomous driver**:
A thin external supervisor that loops `next` unattended: spawning a fresh window per phase and verifying
the on-disk contract: only after a human has run `begin → plan → refine` (and, later, `iterate` if they
want more work). Carries no work-intelligence; it never grills, iterates, briefs, reviews, or runs `goal`. The yokai driver is one
implementation (see [`crates/yokai/CONTEXT.md`](https://github.com/getkoi/koi/blob/main/crates/yokai/CONTEXT.md)). The driver owns optional execution choices; **next** in an interactive window stays one serial phase.
_Avoid_: runner, orchestrator, bot

## Flagged ambiguities

- **"CONTEXT.md"**: distinguish this method glossary from a managed project's execution contract under `.koi/run/`. Always say which. An edit to `.koi/run/CONTEXT.md` uses a span from that file. This glossary and [`crates/yokai/CONTEXT.md`](https://github.com/getkoi/koi/blob/main/crates/yokai/CONTEXT.md) are separate documents.
- **"compact"**: two different operations, kept apart on purpose. *Context compaction* (`/compact`) trims
  ONE long human session to keep it alive; a fresh window per phase makes it unnecessary. *Backlog
  compaction* trims `BACKLOG.md` so finished phases collapse to one line: a content edit `next` does every
  phase, regardless of context length.
- **"spec"**: three overlapping uses: the *deliverable* (`consolidate`'s output), the *deliverable spec
  model* (its recorded shape), and the Build loop's *spec* (which, for junji, *is* the phase plan). Name which.
- **"research"**: two senses: the optional **`research` verb** (writes cited notes under
  `.koi/run/researches/` for plan/grill) vs **phase research** (step 2 of `next`: read the files the
  phase named). Say which; never conflate them.
- **"design"**: four senses: the optional **`design` verb** / run **`DESIGN.md`**; a durable
  **project/root design doc**; grilling's **design tree** (decision topology); and a **design skill**
  (in-repo `SKILL.md` that `design` follows). Say which; never conflate them.
- **"scout"**: **Skill scout** is a `begin` step, not a verb. Begin's whole survey is
  **reconnaissance** (yokai ADR-0007). Yokai **Guide** is feedforward into the coder prompt, not a skill.
- **"step"**: not a method term, though the `next` protocol is numbered 1-7. The unit is the **phase**;
  under yokai the named sub-units are *acts* (Plan/Build/Seal) and *iterations*. Say which; never "step".
- **"iterate" vs "iteration"**: **iterate** is the junji verb that grills a post-execution delta onto the
  backlog. **Iteration** is yokai's Build-loop pass (one coder turn, then sensors, then optional judge).
  Never use one word for the other.
- **"building" vs "iteration" vs "station"**: backlog **`[building]`** is the act-level heading tag.
  A Build **iteration** is one coder→sensors→judge pass. A rail **station** is yokai TUI chrome, not a
  backlog tag.
- **"driver"**: the method's *autonomous driver* is the abstract supervisor concept; *the driver* in the
  root `CONTEXT.md` is the Rust application that implements it.
- **"subagent"**: one host child for `/junji next --subagent` or `/junji review --subagent`. It runs
  `/junji next` (or `/junji review`) and does not delegate that work to a driver verb.
- **"tier"**: the `[low]` / `[medium]` / `[high]` / `[ultra]` heading tag. Not a Model and not a
  role profile. Interactive **next** does not switch Agent/Model; yokai walks
  the tagged band.
- **"brief"**: the optional **`brief` verb** (chat-only product briefing) vs leftover informal "a brief"
  for a **source doc**. Use the verb name; never call a source doc a brief.
- **"goal"**: the **`goal` verb** (a harness goal that repeats `next`) vs a phase plan's **Goal & scope**
  section (that phase's in and out list). Say which.
- **"review"**: three things. The method's **`review` verb** reads a whole PR diff against base and
  spec, writes `reviews/review-NN.md`, and appends **fix phases**; it never writes `FEEDBACK.md`.
  Yokai's **judge** is the advisory read-only reviewer of one Build **iteration** inside a phase; its
  findings go to `FEEDBACK.md` (see [`crates/yokai/CONTEXT.md`](https://github.com/getkoi/koi/blob/main/crates/yokai/CONTEXT.md)).
  **Grilling** is a plan-time interview, not a review. Name which; the Skills by-role index lists
  yokai `judge`, never `review`.

## Example dialogue

**Dev:** I ran `plan` and it documented verification commands. Can I start coding the first phase?
**Expert:** Not yet: `plan` sets the approach and the bar, but the phase list doesn't exist until you run
`refine`. It creates ordered, independently-verifiable phases with dependencies and human gates;
then `next` runs the first one.
**Dev:** And where does a fresh window look to know what to do?
**Expert:** `CONTEXT.md` and `BACKLOG.md`: never `PLAN.md`. PLAN is the human rationale; CONTEXT is the
execution contract a window obeys, and BACKLOG's Next-action pointer says which verb comes next.
**Dev:** What if the agent says the phase is done but the gate is red?
**Expert:** Then it isn't done. The verification bar decides: every documented verification command must exit 0.
Never weaken a sensor to pass; fix the root cause or halt.
**Dev:** Every phase is `[done]` and Next action says consolidate, but I want another slice.
**Expert:** `/junji iterate` with the request. It grills (including how to slice), writes the phase
contracts, commits that markdown, and sets Next action to `/junji next`. Then `next` or yokai. `refine`
will not add work once the list is all `[done]`.
**Dev:** Three phases are `[done]` and I need to show someone what they can use.
**Expert:** `/junji brief`. It reads Outcomes and CONTEXT and returns a short product briefing in chat,
what works, how to run/check, what to watch. It writes nothing and does not move Next action.
**Dev:** The phase plan has a Goal & scope section. Is that `/junji goal`?
**Expert:** Goal & scope is that phase's in and out list. `/junji goal` asks the harness to run runnable
phases one by one with `/junji next --subagent`. It writes nothing and does not move Next action.
**Dev:** The PR is up. Can junji review it before I ask a human?
**Expert:** `/junji review`. Clean tree, nothing in flight. It diffs the branch against its base, checks
the diff against PLAN, CONTEXT locks, DESIGN, and each phase's Outcome, probes the tests once, then
grades findings. Critical and Required become ordinary fix phases on the backlog and Next action is
`/junji next`; the rest wait in `reviews/review-01.md`. `/junji goal --review` repeats drain and
review up to three rounds.
