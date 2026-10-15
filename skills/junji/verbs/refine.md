# Verb: refine — decompose or reshape executable cards

Read references/board.md. Read PLAN and CONTEXT; decompose approved work into coherent, independently
verifiable cards. Use junji-board show, then apply with its exact revision. Each new card has phase_id,
title, description, dependencies and a gated boolean. The helper assigns stable IDs. Keep completed
cards, outcomes and user fields intact. Set next_action to /junji next in the same patch.
Runtime tier/strategy choices belong in Yokai YAML. Never edit BACKLOG.md or write product code.

Later refine may split, merge or reorder unfinished work. Do not silently renumber existing phases;
reconcile referenced YAML overrides if identity changes are necessary. Changed locks go in CONTEXT
as facts and PLAN as rationale. After all cards are done, use iterate to add work.
When publication is enabled, review the initial board and adapter profile, then publish the complete
hierarchy per references/visibility.md. Card publication does not authorize gated execution.
