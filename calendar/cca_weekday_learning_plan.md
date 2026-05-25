# CCA Weekday Learning Plan (Going Forward)

- Applies to weekday entries from 2026-05-18 onward
- Small quiz format: 8 questions, 20 minutes, same playbook standards

| Date | Block | Learning Objective | Small Quiz Command |
|---|---|---|---|
| 2026-05-18 | Block 1: Context Isolation - scenario-pattern sprint | Detect context-pollution signals and pick the right isolation primitive (`context: fork`, Explore subagent, on-demand skills). | `./cca test --date 2026-05-18 --count 8 --timed-minutes 20` |
| 2026-05-19 | Block 1: Context Isolation - scenario-pattern sprint | Differentiate always-loaded vs on-demand context (`CLAUDE.md` vs Skills vs `.claude/rules/`). | `./cca test --date 2026-05-19 --count 8 --timed-minutes 20` |
| 2026-05-20 | Block 1: Context Isolation - scenario-pattern sprint | Apply path-scoped rule selection with glob-style reasoning for mixed file types. | `./cca test --date 2026-05-20 --count 8 --timed-minutes 20` |
| 2026-05-21 | Block 1: Context Isolation - scenario-pattern sprint | Resolve multi-symptom config failures with deterministic frontmatter (`argument-hint`, `allowed-tools`, `context: fork`). | `./cca test --date 2026-05-21 --count 8 --timed-minutes 20` |
| 2026-05-22 | Block 1: Context Isolation - scenario-pattern sprint | Practice context-preserving design tradeoffs under token pressure with concise output contracts. | `./cca test --date 2026-05-22 --count 8 --timed-minutes 20` |
| 2026-05-25 | Block 2: Error Propagation - scenario-pattern sprint | Classify error outcomes: retryable access failure vs valid empty result vs policy gap. | `./cca test --date 2026-05-25 --count 8 --timed-minutes 20` |
| 2026-05-26 | Block 2: Error Propagation - scenario-pattern sprint | Return structured error context (failure type, attempted query, partial results, next options). | `./cca test --date 2026-05-26 --count 8 --timed-minutes 20` |
| 2026-05-27 | Block 2: Error Propagation - scenario-pattern sprint | Apply local recovery before escalation and log exact attempted remediations. | `./cca test --date 2026-05-27 --count 8 --timed-minutes 20` |
| 2026-05-28 | Block 2: Error Propagation - scenario-pattern sprint | Use coverage annotations to preserve value while exposing uncertainty. | `./cca test --date 2026-05-28 --count 8 --timed-minutes 20` |
| 2026-05-29 | Block 2: Error Propagation - scenario-pattern sprint | Partition tasks up-front to reduce duplicate work and improve error observability. | `./cca test --date 2026-05-29 --count 8 --timed-minutes 20` |
| 2026-06-01 | Block 3: Batch vs Sync - scenario-pattern sprint | Apply blocking vs deferred decision boundary for synchronous API vs Message Batches. | `./cca test --date 2026-06-01 --count 8 --timed-minutes 20` |
| 2026-06-02 | Block 3: Batch vs Sync - scenario-pattern sprint | Identify technical incompatibility: batch cannot support iterative tool-calling loops. | `./cca test --date 2026-06-02 --count 8 --timed-minutes 20` |
| 2026-06-03 | Block 3: Batch vs Sync - scenario-pattern sprint | Tune review trust by isolating high-FP categories instead of uniform threshold changes. | `./cca test --date 2026-06-03 --count 8 --timed-minutes 20` |
| 2026-06-04 | Block 3: Batch vs Sync - scenario-pattern sprint | Encode CI output contracts with `-p`, `--output-format json`, and `--json-schema` reasoning. | `./cca test --date 2026-06-04 --count 8 --timed-minutes 20` |
| 2026-06-05 | Block 3: Batch vs Sync - scenario-pattern sprint | Run multi-pass review architecture decisions (per-file pass then integration pass). | `./cca test --date 2026-06-05 --count 8 --timed-minutes 20` |
| 2026-06-08 | Block 4: Tool Selection - scenario-pattern sprint | Diagnose misrouting via tool-description ambiguity before adding architecture layers. | `./cca test --date 2026-06-08 --count 8 --timed-minutes 20` |
| 2026-06-09 | Block 4: Tool Selection - scenario-pattern sprint | Enforce prerequisite tool sequences programmatically for high-risk actions. | `./cca test --date 2026-06-09 --count 8 --timed-minutes 20` |
| 2026-06-10 | Block 4: Tool Selection - scenario-pattern sprint | Choose user disambiguation over heuristic confidence when identity ambiguity exists. | `./cca test --date 2026-06-10 --count 8 --timed-minutes 20` |
| 2026-06-11 | Block 4: Tool Selection - scenario-pattern sprint | Detect keyword-steering prompt bias and correct root cause without overfitting. | `./cca test --date 2026-06-11 --count 8 --timed-minutes 20` |
| 2026-06-12 | Block 4: Tool Selection - scenario-pattern sprint | Design multi-concern handling with shared context and parallel decomposition. | `./cca test --date 2026-06-12 --count 8 --timed-minutes 20` |
| 2026-06-15 | Block 5: Config Scope - scenario-pattern sprint | Apply project vs user config precedence correctly across `.claude/*` and `~/.claude/*`. | `./cca test --date 2026-06-15 --count 8 --timed-minutes 20` |
| 2026-06-16 | Block 5: Config Scope - scenario-pattern sprint | Map commands, skills, rules, and MCP config to the correct shared scope. | `./cca test --date 2026-06-16 --count 8 --timed-minutes 20` |
| 2026-06-17 | Block 6: Prompt Boundaries - scenario-pattern sprint | Choose among few-shot vs self-critique vs preprocessing using case-variability signals. | `./cca test --date 2026-06-17 --count 8 --timed-minutes 20` |
| 2026-06-18 | Block 6: Prompt Boundaries - scenario-pattern sprint | Spot when "add instructions to the prompt" is a distractor and prefer deterministic controls. | `./cca test --date 2026-06-18 --count 8 --timed-minutes 20` |
| 2026-06-19 | Block 6: Prompt Boundaries - scenario-pattern sprint | Apply structured-output and validation-retry boundaries for extraction reliability. | `./cca test --date 2026-06-19 --count 8 --timed-minutes 20` |
