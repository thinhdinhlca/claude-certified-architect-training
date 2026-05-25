# CCA Schedule Refactor Rationale

## Input Signal Used
- First pass debrief: 60 questions in 90 minutes, 4 scenarios analyzed (`docs/exam-debrief-1.md`)
- Pattern framework: 28 construction patterns (`PREPARATION-GUIDE.md`)
- Real scenario artifacts:
  - `practice-tests/real-exam-questions/scenario-01-code-generation.md`
  - `practice-tests/real-exam-questions/scenario-02-multi-agent-research.md`
  - `practice-tests/real-exam-questions/scenario-03-ci-cd.md`
  - `practice-tests/real-exam-questions/scenario-04-customer-support.md`
- Remaining canonical scenarios from `README.md`:
  - Scenario 4: Developer Productivity with Claude
  - Scenario 6: Structured Data Extraction

## Structural Changes (What Changed and Why)
1. Replaced domain-silo weeks with scenario-pattern blocks.
Why: Real exam questions are cross-domain and constraint-dense. Pattern blocks better match actual decision behavior tested.

2. Reordered study progression to your specified priority.
Order applied exactly: context isolation -> error propagation -> batch vs sync -> tool selection -> config scope -> prompt boundaries.

3. Inserted ten 30-minute anti-pattern drills.
Why: Debrief and guide show anti-pattern spotting as a repeated elimination mechanism. One drill per weekday for the first 10 weekdays.

4. Added dedicated few-shot decision-boundary sessions.
Why: You specifically missed points here (few-shot vs self-critique vs preprocessing). Dedicated blocks were placed on 2026-06-12, 2026-06-16, and 2026-06-18.

5. Built four timed full-scenario exams.
Spec: 15 questions, 22 minutes each.
Pattern alignment:
- Exam 1 (2026-05-23): patterns 1-7 (Scenario 1)
- Exam 2 (2026-05-30): patterns 8-15 (Scenario 2)
- Exam 3 (2026-06-06): patterns 16-20 (Scenario 3)
- Exam 4 (2026-06-13): patterns 21-28 (Scenario 4)

6. Added flashcard-generation cadence for repeated concepts.
Why: Repeated cross-scenario concepts need short retrieval cycles. Flashcard generation now occurs twice weekly plus weekends, and after each full-scenario exam.

7. Enforced weekday time window and weekend flexibility.
- Weekdays: explicit 8:00-10:00 PM timebox in every weekday entry.
- Weekends: flexible timing with mandatory quiz + review block.

8. Compressed timeline behavior without dropping coverage.
Why: You move fast through known material.
How: higher-frequency timed blocks, less passive reading, direct artifact drills, and tighter scenario rotation.

9. Mapped each day to concrete artifacts.
Why: Prevent vague "study topic" blocks.
How: every day includes explicit file-backed reading artifacts and explicit `test_sources`.

## Six-Scenario Coverage Proof
- Scenario 1 (Code Generation): `scenario-01-code-generation.md` in Block 1 + Exam 1
- Scenario 2 (Multi-Agent Research): `scenario-02-multi-agent-research.md` in Block 2 + Exam 2
- Scenario 3 (Customer Support Resolution Agent): `scenario-04-customer-support.md` in Block 4 + Exam 4
- Scenario 4 (Developer Productivity with Claude): `README.md` scenario section + `test-04-tool-design-mcp.md`
- Scenario 5 (CI/CD): `scenario-03-ci-cd.md` in Block 3 + Exam 3
- Scenario 6 (Structured Data Extraction): `test-08-validation-multipass.md` + `test-10-advanced-context.md` in Block 6

## Flashcard Concepts Generated (Repeated Across Scenarios)
1. `stop_reason` loop control and termination safety fallback
2. Context isolation levers (`context: fork`, Explore subagent, on-demand skills)
3. Structured error taxonomy (retryable vs informative empty)
4. Batch vs synchronous API boundary (blocking vs deferred)
5. Tool selection reliability (description clarity vs prompt steering)
6. Config scope precedence (`.claude/*` project vs `~/.claude/*` user)
7. Programmatic enforcement vs prompt guidance
8. Few-shot vs self-critique vs preprocessing boundary
9. Multi-pass review architecture and self-review bias
10. Coverage annotations and uncertainty propagation

## Distractor/Explanation Rule Integration
Full-scenario blocks and prompt-boundary drills explicitly reference the PREPARATION-GUIDE rules:
- Similar option length, no all/none, no extreme language
- Each distractor maps to a real misconception
- A question constraint invalidates each distractor
- "Add instructions to the prompt" treated as a common distractor
- Explanations always include: why correct, why each distractor is wrong, principle



## Exam Execution Note
- The raw `practice-tests/real-exam-questions/scenario-0x-*.md` files are analysis artifacts and are not parser-native quiz banks.
- Each 15Q/22m full-scenario exam therefore keeps the raw scenario artifact for pattern anchoring but executes from parser-compatible `practice-tests/test-*.md` banks mapped to the same pattern ranges.
- This keeps the schedule runnable with `./cca test --date ...` and `python3 tools/cca_quiz.py --date ...`.


## Prep-Style Exam Upgrade
- Full-scenario exam days now use `./cca exam-html` to generate a single self-contained HTML file with prep-test structure: 60 questions, 90 minutes, 4 modules randomly selected, 15 questions per selected module.
- Module banks are expanded to 30 questions each under `practice-tests/module-banks/` to support rotation and reduce repetition.
