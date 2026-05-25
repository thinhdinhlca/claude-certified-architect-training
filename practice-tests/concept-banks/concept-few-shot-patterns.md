# Few-Shot & Prompt Patterns — Question Bank

> 30 questions covering few-shot vs self-critique vs preprocessing diagnosis, chain-of-thought, example placement, and parallel decomposition.
> Generated: 2026-05-24

---

## Question 1
A customer support agent produces responses with inconsistent structure — sometimes leading with the resolution, sometimes with an apology, sometimes with a policy reference. The behavior varies even on identical issue types. The team wants uniform response structure across all cases. What is the most direct fix?

A) Add a self-critique step asking the model to verify its response meets format requirements before sending.
B) Add a preprocessing layer that classifies the issue type and routes to specialized sub-prompts.
C) Provide 3–5 few-shot examples in the system prompt that demonstrate the target input→output structure for common case types.
D) Enable extended thinking so the model deliberates on format before generating a response.

<details>
<summary>Answer</summary>

**C)** Inconsistent format on predictable case types is exactly the use case for few-shot examples — they directly show the model what input→output structure looks like. A is wrong because self-critique catches accuracy or completeness gaps, not format inconsistency. B is wrong because routing adds architectural complexity when the issue is purely format guidance. D is wrong because extended thinking addresses reasoning depth, not output structure. (source: Prompt engineering)

</details>

---

## Question 2
A code review agent sometimes omits security considerations from its output, sometimes skips edge-case coverage, and sometimes fails to mention performance tradeoffs. The pattern is unpredictable — each omission is different. What technique is best suited to catch these variable gaps?

A) A self-critique pass instructing the model to review its draft against a checklist: security, edge cases, performance, correctness.
B) Few-shot examples covering the five most common review types.
C) Preprocessing to extract function signatures before sending to the review prompt.
D) XML-structured output schema with required fields for each review category.

<details>
<summary>Answer</summary>

**A)** Variable, case-specific omissions are the signal for self-critique — a checklist review pass catches gaps regardless of which category was missed in the first pass. B is wrong because few-shot examples only help with predictable patterns and can't cover the variability described. C is wrong because preprocessing improves input quality but does not address what the model omits in its output. D is wrong because required schema fields force structure but do not diagnose which content is actually missing. (source: Prompt engineering)

</details>

---

## Question 3
A legal document summarizer is tasked with summarizing contracts. The input documents sometimes include scanned OCR text with artifacts, garbled clause numbering, and inconsistent section headers. The model's summaries are unreliable. What is the highest-leverage first step?

A) Few-shot examples showing correct summaries for well-formed contracts.
B) A self-critique step asking the model to flag uncertain content in its summary.
C) A preprocessing layer that normalizes OCR artifacts, fixes clause numbering, and standardizes section headers before the document reaches the summarization prompt.
D) Extended thinking to allow the model more reasoning tokens when encountering malformed input.

<details>
<summary>Answer</summary>

**C)** The root problem is input quality — the model cannot reliably summarize documents when the input is noisy. Preprocessing fixes the input before it reaches the model, addressing the actual failure point. A is wrong because few-shot examples don't help when the problem is malformed input the model cannot parse reliably. B is wrong because self-critique addresses output accuracy, not the upstream input quality issue. D is wrong because extended thinking does not compensate for structurally broken input. (source: Prompt engineering)

</details>

---

## Question 4
A content moderation system routes posts to one of five category labels. Reviewers report that the label distribution is correct but the written justification format varies widely — sometimes bullet points, sometimes prose, sometimes numbered lists. A junior engineer suggests adding a second LLM call to review the output format. What is the better approach?

A) Add a self-critique step where the model evaluates whether its justification follows the required format.
B) Add few-shot examples to the prompt showing the required justification format for each category label.
C) Add a preprocessing step to normalize the post text before classification.
D) Switch to a structured output schema with a required `justification` string field.

<details>
<summary>Answer</summary>

**B)** Format inconsistency across predictable categories is directly addressed by few-shot examples that demonstrate the target format — cheaper and more reliable than a second LLM call for self-critique. A is wrong because self-critique adds latency and is better suited to content gaps than format consistency issues. C is wrong because the problem is output format, not input quality. D is wrong because a required string field enforces presence but not the internal format of the justification. (source: Prompt engineering)

</details>

---

## Question 5
An agent generating financial reports occasionally includes incorrect figures — using prior quarter data when current quarter data is available in the context. The errors are factual, not formatting problems. The figures that are wrong vary by report. What is the most effective fix?

A) Add few-shot examples showing correct reports for the two most common report types.
B) Add a self-critique pass asking the model to verify each figure in the draft against the source data.
C) Wrap the report prompt in XML tags to improve context parsing.
D) Add a preprocessing step to extract all numerical figures into a structured table before generation.

<details>
<summary>Answer</summary>

**B)** Factual accuracy errors that vary by report — using wrong figures — are the canonical use case for self-critique. The model has the correct data in context but uses the wrong value; a verification pass directly catches this. A is wrong because few-shot examples address format and pattern, not factual accuracy against live data. C is wrong because XML tags improve prompt parsing but do not address factual verification. D is wrong because preprocessing structures the input but does not prevent the model from using wrong values in output. (source: Prompt engineering)

</details>

---

## Question 6
A sentiment classifier receives customer feedback that may be a single sentence, a multi-paragraph essay, or a table of ratings. The classifier works well when the input follows a consistent format. Performance degrades significantly on the multi-format inputs. What is the right approach?

A) Few-shot examples showing classifications for each of the three input formats.
B) Increase the system prompt specificity to describe all three input formats the model may encounter.
C) A self-critique step asking the model to reconsider its classification given input complexity.
D) A preprocessing layer that normalizes all input formats into a consistent structure before classification.

<details>
<summary>Answer</summary>

**D)** When performance degrades specifically due to input format variation, preprocessing is the correct tool — it transforms diverse inputs into a consistent structure the classifier handles reliably. A is wrong because few-shot examples help with output patterns, not input normalization across radically different formats. B is wrong because describing input formats in prose does not normalize them — the model still receives variable-format input. C is wrong because self-critique adds a second pass but doesn't address the root cause of inconsistent input structure. (source: Prompt engineering)

</details>

---

## Question 7
A developer asks: "I want to add few-shot examples to my prompt. Where should I place them relative to the task instructions?" The examples are input→output demonstrations for a classification task. What is the documented best practice?

A) Place examples after the task instructions, wrapped in `<examples>` tags so Claude can distinguish them from instructions.
B) Place examples before task instructions so Claude reads them before encountering the constraints.
C) Place examples at the end of the human turn, after the actual input to classify.
D) Place examples in a separate system prompt turn, distinct from the task instructions turn.

<details>
<summary>Answer</summary>

**A)** Anthropic's documented guidance places examples after instructions, wrapped in `<examples>` tags (individual examples in `<example>` tags) to clearly separate them from the instructions themselves. B is wrong because examples before instructions can cause Claude to over-weight example patterns before reading the full constraints. C is wrong because placing examples after the live input to classify creates ambiguity about which content is the target. D is wrong because splitting into separate system prompt turns is not the documented pattern and may reduce instruction coherence. (source: Prompt engineering)

</details>

---

## Question 8
A team is debating how many few-shot examples to include. The task is a structured data extraction from support tickets. They currently have 1 example and are seeing inconsistent field population. The Anthropic documentation gives a specific recommendation. What is it?

A) Include 3–5 examples for best results, covering edge cases and format variation.
B) 1–2 examples are sufficient for any task; more adds unnecessary token cost.
C) Include at least 10 examples to ensure full coverage of all task variations.
D) Use as many examples as fit within the context window without truncation.

<details>
<summary>Answer</summary>

**A)** Anthropic's prompt engineering documentation explicitly states "Include 3–5 examples for best results." B is wrong because 1–2 examples often underconstrain format and miss edge cases. C is wrong because 10+ examples are not the recommendation and add significant token cost. D is wrong because maximizing example count is not the guidance — quality and diversity within a reasonable count is. (source: Prompt engineering)

</details>

---

## Question 9
An agent that schedules calendar events receives requests like: "Set up a sync with the team sometime next week, maybe Tuesday or Wednesday afternoon, keep it short." This request is ambiguous on date, time, and duration. The agent frequently books incorrect times. What is the correct diagnostic?

A) The agent needs few-shot examples showing how to handle ambiguous scheduling requests.
B) The agent needs a self-critique pass to re-evaluate its scheduled time before confirming.
C) The input needs a preprocessing step to extract and disambiguate intent (date range, duration, participants) before the scheduling prompt runs.
D) The agent needs chain-of-thought prompting to reason through the scheduling decision step by step.

<details>
<summary>Answer</summary>

**C)** The core problem is ambiguous input — the request has undefined date, time, and duration. Preprocessing extracts and normalizes intent before the scheduling prompt runs, addressing the root cause. A is wrong because few-shot examples don't resolve ambiguous input; the model still lacks definitive field values. B is wrong because self-critique checks the output, not the missing input fields that caused the wrong booking. D is wrong because chain-of-thought helps with reasoning complexity, not disambiguation of genuinely missing information. (source: Prompt engineering)

</details>

---

## Question 10
A pipeline generates product descriptions. The engineering team finds that Claude's first-pass descriptions are 85% correct on content but 30% of them fail to follow the required tone and structure (brand voice, bullet-point format, maximum word count). A single-pass prompt is currently used. What is the most efficient improvement?

A) Switch to extended thinking to give the model more reasoning capacity for tone.
B) Add a self-critique step that checks the draft against a tone and format checklist.
C) Add few-shot examples demonstrating the target tone, structure, and word count for three product categories.
D) Add a preprocessing step to extract product attributes before description generation.

<details>
<summary>Answer</summary>

**C)** Format and tone inconsistency across predictable product categories is the use case for few-shot examples — they directly demonstrate what correct output looks like. B is wrong because self-critique adds latency and a second LLM call; when the issue is predictable format/tone, few-shot is cheaper and more reliable. A is wrong because extended thinking addresses reasoning depth, not output style. D is wrong because preprocessing helps with input quality; the product attributes are presumably already available. (source: Prompt engineering)

</details>

---

## Question 11
A complex reasoning task involves a multi-step math proof with several dependent intermediate results. The model often makes errors in intermediate steps that propagate to the wrong final answer. What is the most effective technique?

A) Chain-of-thought prompting, explicitly instructing the model to show its work at each step.
B) Few-shot examples showing complete proofs for similar problem types.
C) A self-critique pass asking the model to re-check its final answer.
D) Preprocessing to reformat the problem statement into a structured form.

<details>
<summary>Answer</summary>

**A)** Multi-step reasoning with intermediate dependencies is the canonical use case for chain-of-thought — making reasoning explicit allows errors to surface at the step where they occur rather than propagating silently to the final answer. B is wrong because few-shot examples help with format and pattern but do not force explicit intermediate reasoning. C is wrong because self-critique at the final answer level may not surface where an intermediate step went wrong. D is wrong because the problem is reasoning quality, not input structure. (source: Prompt engineering)

</details>

---

## Question 12
Extended thinking (budget_tokens) is enabled on a Claude model for a complex analysis task. The team notices the model is spending most of its thinking budget deliberating on minor formatting decisions. How should this be addressed?

A) Increase the budget_tokens parameter to give the model more room.
B) Add prompt instructions telling the model that thinking should only be used for reasoning-intensive steps, not formatting decisions.
C) Disable extended thinking and add few-shot examples for format guidance instead.
D) Add a self-critique pass after the thinking block to fix the resulting format.

<details>
<summary>Answer</summary>

**B)** Anthropic's extended thinking documentation explicitly states the thinking trigger is steerable — adding guidance like "Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning" steers the model away from wasting budget on minor decisions. A is wrong because more budget tokens will not redirect where the model spends its thinking — it may spend more time on formatting. C is wrong because disabling thinking may hurt the complex reasoning the budget was intended for. D is wrong because a self-critique pass does not fix the root cause of misdirected thinking. (source: Extended thinking)

</details>

---

## Question 13
A customer support agent produces correct responses but the responses never include next-step instructions or escalation paths, even when the policy clearly requires them. The omission is consistent — every response is missing these elements, not just some. What is the most direct fix?

A) Few-shot examples where each demonstrated response includes next steps and escalation paths.
B) Self-critique pass asking the model to check whether its response includes required next steps.
C) Preprocessing to identify case types that require escalation before routing to the main prompt.
D) Extended thinking to allow the model to reason through policy requirements before responding.

<details>
<summary>Answer</summary>

**A)** A consistent, predictable omission — the same element is always missing — is the signal for few-shot examples. Showing the model what complete responses look like directly teaches it the required output structure. B is wrong because self-critique adds a second pass and is better suited for variable, case-specific gaps — not a consistent omission that examples can directly fix. C is wrong because preprocessing helps with input quality, not missing output elements. D is wrong because reasoning budget does not fix a structural gap in what the model outputs. (source: Prompt engineering)

</details>

---

## Question 14
An architect is designing a pipeline where multiple independent sub-tasks (summarize, classify, extract entities) must all run on the same document. The tasks do not depend on each other's outputs. What is the preferred architectural approach?

A) Chain the tasks sequentially — summarize first, then classify, then extract — to keep context clean.
B) Send the document to a single prompt that performs all three tasks in one call.
C) Decompose into three parallel prompts, each receiving the shared document context and running independently.
D) Use a preprocessing step to create three versions of the document optimized for each task.

<details>
<summary>Answer</summary>

**C)** When tasks are independent and do not require each other's outputs, parallel decomposition with shared context eliminates sequential latency and reduces total wall-clock time. B is wrong because a single prompt handling three distinct tasks increases complexity and makes it harder to optimize or debug each task independently. A is wrong because sequential chaining on independent tasks is slower with no accuracy benefit. D is wrong because creating separate document versions adds preprocessing cost without addressing the parallelization opportunity. (source: Prompt engineering)

</details>

---

## Question 15
Two agents are running in parallel to research the same topic from different source types. Agent A searches academic papers; Agent B searches news articles. Both need the same user query, session ID, and research criteria. Neither needs to see the other's intermediate findings. What is the correct context management pattern?

A) Share the full conversation history with both agents so they have complete context.
B) Pass only the shared inputs (query, session ID, criteria) to each agent explicitly; do not pass each other's intermediate outputs.
C) Run agents sequentially — Agent A then Agent B — so B can incorporate A's findings.
D) Use a preprocessing step to merge both agents' inputs into a single context block before forking.

<details>
<summary>Answer</summary>

**B)** Parallel decomposition with shared context means each agent receives only what it needs (the common inputs) and is isolated from the other's intermediate work. Sharing full conversation history risks context pollution. A is wrong because sharing full history exposes intermediate outputs that could bias the parallel agent. C is wrong because sequential execution eliminates the latency benefit of parallelism when the tasks are independent. D is wrong because merging inputs before forking defeats the purpose of isolation. (source: Prompt engineering)

</details>

---

## Question 16
A self-critique pass is added to a summarization pipeline. After running in production for a week, the team notices that the critique step often rewrites perfectly good summaries, increasing latency and sometimes introducing errors. What is the likely cause?

A) The critique prompt lacks specific evaluation criteria — it is too vague, causing the model to critique indiscriminately.
B) The model's base summarization capability is insufficient; a better base model is needed.
C) The self-critique pass needs more budget_tokens to evaluate the summary properly.
D) Few-shot examples should replace the self-critique step entirely.

<details>
<summary>Answer</summary>

**A)** A self-critique step without specific criteria (e.g., "Check for factual accuracy, missing key points, and constraint compliance") causes the model to apply arbitrary standards, rewriting good outputs. The fix is scoped criteria. B is wrong because the base summarization is presumably working — the problem is the unguided critique step. C is wrong because more budget tokens do not provide the missing evaluation criteria. D is wrong because replacing with few-shot addresses format consistency, not the broken self-critique configuration. (source: Prompt engineering)

</details>

---

## Question 17
An e-commerce agent receives user messages that mix product questions, order status queries, and return requests in a single message — e.g., "Where's my order #12345 and do you have the blue version in size M?" The agent's accuracy on combined messages is 61% vs 94% on single-topic messages. A teammate suggests adding few-shot examples for multi-topic messages. Another suggests preprocessing to decompose multi-topic messages before routing. The baseline for single-topic is already strong. Which is correct?

A) Few-shot examples demonstrating the correct handling of 5–6 multi-topic message patterns.
B) Preprocessing to decompose multi-topic messages into individual requests before they reach the routing agent.
C) Extended thinking to allow the agent more reasoning tokens when processing complex messages.
D) Self-critique pass where the agent re-evaluates its initial routing decision for completeness.

<details>
<summary>Answer</summary>

**A)** The strong single-topic baseline (94%) indicates the agent already understands individual concerns well — it just needs guidance on multi-concern patterns. Few-shot examples for multi-topic handling provide that pattern guidance with minimal architectural change. B is wrong because preprocessing adds architectural complexity (latency, cost, new component) when the existing agent already handles individual topics well — this is over-engineering relative to the problem. C is wrong because extended thinking increases reasoning depth, not the agent's ability to identify and handle multiple topics per message. D is wrong because self-critique checks output quality, not whether all topics in a multi-concern message were addressed. (source: Prompt engineering)

</details>

---

## Question 18
A pipeline generates medical triage summaries. Nurse reviewers report that summaries occasionally miss documenting patient-reported allergies even though the allergy information is present in the patient intake form attached to each case. The omission pattern is variable — some case types miss it, others don't. What is the best approach?

A) Few-shot examples showing complete summaries for the five most common triage case types.
B) A preprocessing step to extract allergy information into a structured field before summarization.
C) XML tags around the intake form to help the model locate allergy data.
D) A self-critique pass instructing the model to verify the draft against a checklist that includes: allergies, current medications, chief complaint, and vital signs.

<details>
<summary>Answer</summary>

**D)** Variable omissions across case types — sometimes missing allergies, sometimes not — match the self-critique pattern. A checklist-based review pass catches case-specific gaps regardless of type. A is wrong because few-shot examples help with predictable patterns; they cannot cover the variability described. B is wrong because preprocessing structured extraction is useful but doesn't prevent the model from ignoring the extracted field in its output. C is wrong because XML tags improve parsing but do not cause the model to include allergy information it might otherwise omit. (source: Prompt engineering)

</details>

---

## Question 19
An agent is receiving user queries where the same entity appears with inconsistent spelling — "OpenAI", "Open AI", "openai", "Open Ai" — causing tool lookups to fail silently. The downstream lookup tool is case-sensitive and requires canonical company names. What is the correct fix?

A) Few-shot examples showing the agent how to handle each spelling variant.
B) A self-critique pass after the tool lookup to re-try with an alternative spelling if the first fails.
C) A preprocessing step that normalizes entity mentions to canonical form before the query reaches the lookup tool.
D) Prompt instructions telling the model to always use the correct spelling of company names.

<details>
<summary>Answer</summary>

**C)** Entity normalization — resolving spelling variants to canonical form — is a preprocessing responsibility. The input has a data quality problem that must be fixed before it reaches the case-sensitive tool. A is wrong because few-shot examples can't enumerate all spelling variants and don't fix the normalization problem. B is wrong because self-critique after failure is reactive; preprocessing prevents the failure. D is wrong because prompt instructions rely on the model knowing the correct spelling, which it may not for all entities. (source: Prompt engineering)

</details>

---

## Question 20
A Q&A system is tasked with answering questions about a company's 50-page policy manual. The document is included in the context. The model sometimes answers with outdated policy language rather than the current version in the provided document. What is the best diagnostic and fix?

A) Add few-shot examples showing correct answers for the 10 most common question types.
B) Move the document to the top of the prompt (before instructions and query) per long-context best practices.
C) Add a preprocessing step to extract relevant policy sections before passing to the Q&A prompt.
D) Add a self-critique pass asking the model to verify its answer against the source document before responding.

<details>
<summary>Answer</summary>

**B)** Anthropic's long-context documentation specifically states placing longform data at the top of the prompt improves performance — "queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs." The model is using outdated internal knowledge rather than the provided document, which is a position-sensitivity issue. D is wrong because self-critique is a valid second choice but B directly addresses the root cause (position sensitivity) more efficiently. A is wrong because few-shot examples do not help the model prefer document content over training knowledge. C is wrong because extracting sections adds complexity; correct document positioning is simpler and addresses the root cause. (source: Prompt engineering)

</details>

---

## Question 21
An agent that writes email responses has access to customer history, order data, and return policies. A product manager reports that 40% of emails use an overly formal tone that doesn't match the brand voice. The emails are factually correct. What is the most direct fix?

A) Enable extended thinking so the model deliberates on tone before writing.
B) Add a self-critique step asking the model to re-check the email's tone against brand guidelines.
C) Add few-shot examples that demonstrate the target brand voice across three common email types.
D) Add a preprocessing step to analyze the customer's communication style and adjust accordingly.

<details>
<summary>Answer</summary>

**C)** Tone inconsistency on predictable email types — where the content is correct but the voice is wrong — is directly addressed by few-shot examples that demonstrate the target voice. The Anthropic docs note "positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples." B is wrong because self-critique adds latency for a consistent, teachable style gap that few-shot handles more efficiently. A is wrong because extended thinking addresses reasoning complexity, not output style. D is wrong because analyzing customer style adds complexity without addressing the model's own default formality. (source: Prompt engineering)

</details>

---

## Question 22
A research assistant is tasked with comparing two technical papers on a complex topic. It must identify agreements, contradictions, and evidence gaps. The team finds the model often confuses which paper made which claim. What technique is most targeted at this failure?

A) Chain-of-thought prompting where the model extracts all claims from Paper 1, then Paper 2, before comparing.
B) Few-shot examples showing correct comparisons for two prior paper pairs.
C) Self-critique pass asking the model to verify each claim is attributed to the correct paper.
D) Preprocessing to extract claims from both papers into labeled structured lists before comparison.

<details>
<summary>Answer</summary>

**A)** Cross-document attribution errors during comparison are a multi-step reasoning problem — the model needs to maintain separate claim sets before comparing them. Chain-of-thought with explicit intermediate steps (extract Paper 1 claims, extract Paper 2 claims, then compare) directly prevents mixing. D is also useful but addresses input preprocessing, not the reasoning structure; A is more targeted at the comparison reasoning itself. B is wrong because few-shot examples for comparison pairs don't prevent attribution mixing in novel paper pairs. C is wrong because self-critique after mixing claims doesn't reliably un-mix them. (source: Prompt engineering)

</details>

---

## Question 23
A pipeline uses a self-critique step. The initial generation prompt and the self-critique prompt are fed to the same model in the same conversation session, with the original response visible. A reviewer notes the self-critique often approves poor outputs. What is the likely cause and fix?

A) The self-critique prompt needs more specific evaluation criteria.
B) The budget_tokens for the thinking step needs to be increased.
C) The self-critique prompt should include few-shot examples of good vs bad outputs.
D) The same model reviewing its own work in the same session is a known limitation — the model cannot objectively evaluate output it just generated; use a separate model or session.

<details>
<summary>Answer</summary>

**D)** Same-session self-review is a recognized anti-pattern — the model tends to confirm its own recent output rather than evaluate it objectively. The exam debrief explicitly flags "same-session self-review" as an anti-pattern. A is wrong because criteria specificity helps but doesn't overcome the fundamental same-session confirmation bias. B is wrong because more thinking tokens don't resolve the architectural issue of reviewing one's own work. C is wrong because few-shot examples of good/bad outputs help calibrate the critique but don't fix the same-session bias. (source: Prompt engineering)

</details>

---

## Question 24
A complex agent task involves determining which of 12 possible action types to take based on a user request. The model must reason through eligibility rules, priority ordering, and constraint checks before selecting an action. Single-pass responses frequently pick ineligible actions. What is the best approach?

A) Preprocessing to extract the relevant eligibility fields from the user request before the action selection prompt.
B) Self-critique asking the model to verify its action selection is eligible.
C) Few-shot examples covering the 12 action types.
D) Chain-of-thought prompting instructing the model to work through eligibility rules, then priority, then constraints step by step before selecting.

<details>
<summary>Answer</summary>

**D)** Multi-step eligibility reasoning with ordered rules and constraints is the canonical chain-of-thought use case — making each reasoning step explicit prevents the model from jumping to an ineligible action. C is wrong because 12 few-shot examples cannot enumerate the combinatorial space of eligibility conditions. A is wrong because preprocessing helps with input structure but does not enforce the reasoning sequence. B is wrong because self-critique is a second pass; chain-of-thought addresses the reasoning process itself in the first pass. (source: Prompt engineering)

</details>

---

## Question 25
A team wants to add few-shot examples to a long prompt that already contains system instructions, context documents, and variable user input. A teammate argues examples should go at the very top. Another argues they should go after instructions but before the variable input. Who is correct and why?

A) Top of the prompt — examples before instructions let the model learn by example before encountering rules.
B) In a separate system turn — examples belong in the system prompt, not the human turn.
C) After the variable input — examples should come last so they are freshest in context when the model responds.
D) After instructions, before the variable input — examples follow instructions and wrap them in `<examples>` tags, with the actual input at the end for processing.

<details>
<summary>Answer</summary>

**D)** Anthropic's prompt engineering guidance places examples after task instructions, wrapped in `<examples>` tags, with the actual variable input at the end. This structure: instructions → examples → input mirrors the documented pattern and aligns with long-context best practices (queries at the end). A is wrong because leading with examples before instructions causes the model to over-anchor on example patterns before reading constraints. B is wrong because splitting into separate turns is not the documented pattern. C is wrong because examples after the variable input create ambiguity about which content is the target. (source: Prompt engineering)

</details>

---

## Question 26
An agent must perform a long-horizon task: research a topic, draft a report, verify factual claims, and format the output. These steps are strictly dependent — each step requires the previous one's output. A colleague suggests parallel decomposition. Is this appropriate here?

A) Yes — parallel decomposition always reduces latency and should be used when multiple steps are involved.
B) Yes — run all four agents in parallel and use a coordinator to merge outputs.
C) No — the task should use a single prompt to keep context unified.
D) No — because the steps are strictly sequential (each depends on the prior output), parallel decomposition would require passing undefined outputs to downstream steps.

<details>
<summary>Answer</summary>

**D)** Parallel decomposition is appropriate for independent tasks. When steps are strictly sequential (research → draft → verify → format), each step requires the prior step's output — parallelization is not viable without undefined inputs to downstream steps. A is wrong because parallelization only benefits independent tasks; it creates architectural problems on dependent chains. B is wrong because you cannot run verify before draft exists or format before verify is complete. C is wrong because single-prompt handling of long-horizon tasks hits context limits and mixes concerns; sequential chaining (not parallelism) is the right answer. (source: Prompt engineering)

</details>

---

## Question 27
A classification agent is occasionally receiving inputs where the text is a mix of English and Vietnamese with no language tag. The agent is English-only trained and produces degraded output on the mixed-language inputs. What is the correct intervention?

A) Few-shot examples showing the agent how to handle bilingual inputs.
B) A self-critique step asking the agent to flag low-confidence classifications.
C) A preprocessing layer that detects the primary language, translates Vietnamese sections to English, and passes clean text to the classifier.
D) Extended thinking to give the model more capacity to process bilingual text.

<details>
<summary>Answer</summary>

**C)** Language mixing is an input quality problem — the classifier degrades because its input doesn't match what it was designed for. Preprocessing detects and normalizes the language before classification, fixing the root cause. A is wrong because few-shot examples can't teach the model to reliably process language it wasn't designed for. B is wrong because self-critique flags the output problem but doesn't fix the input. D is wrong because extended thinking does not compensate for language capability limitations. (source: Prompt engineering)

</details>

---

## Question 28
An evaluator-optimizer pattern is set up: a generator produces a draft and an evaluator critiques it. The evaluator is instructed to "check the response." After a week, the team finds the evaluator approves nearly every draft, even mediocre ones. What is the most likely root cause?

A) The evaluator model needs to be a larger model than the generator.
B) The generator prompt needs more few-shot examples to produce better initial drafts.
C) The evaluator needs chain-of-thought instructions to deliberate before approving.
D) The evaluator instruction is too vague — without specific criteria, the model defaults to approving.

<details>
<summary>Answer</summary>

**D)** A vague instruction like "check the response" without criteria (accuracy, completeness, constraint compliance) gives the evaluator no basis to reject — it defaults to approval. Specific, enumerated criteria are required for effective self-critique. A is wrong because model size is not the documented issue; evaluation quality depends on criteria clarity. B is wrong because improving the generator does not fix the evaluator's lack of standards. C is wrong because chain-of-thought helps reasoning but doesn't replace the missing evaluation criteria. (source: Prompt engineering)

</details>

---

## Question 29
A team is debating whether to decompose a complex multi-step task into parallel sub-agents or keep it as a single long prompt. The task involves analyzing a dataset, identifying anomalies, and writing a root cause explanation for each anomaly. The anomalies are independent of each other. What is the correct architectural choice?

A) Single prompt — parallel decomposition increases coordination complexity for marginal gain.
B) Parallel decomposition — each anomaly's analysis is independent, so all can run simultaneously with shared dataset context.
C) Parallel decomposition — but only if the number of anomalies exceeds 10.
D) Sequential chaining — anomaly identification must complete before any explanation is written.

<details>
<summary>Answer</summary>

**B)** When sub-tasks are independent — each anomaly analysis doesn't depend on others — parallel decomposition with shared context (the dataset) reduces total latency proportionally. A is wrong because the coordination overhead is low when tasks are clearly independent and outputs are structurally uniform (one explanation per anomaly). C is wrong because the threshold is not "10 anomalies" — independence of tasks is the criterion, not count. D is wrong because the identification phase can be structured to emit all anomalies first, then explanations for each run in parallel. (source: Prompt engineering)

</details>

---

## Question 30
A developer is tuning extended thinking on Claude Opus 4.7. They call the API with `thinking: {type: "enabled", budget_tokens: 10000}`. The API returns a 400 error. What is the correct diagnosis and fix?

A) The budget_tokens value is too high; lower it to 5000.
B) Extended thinking is not supported on the model being called. For Claude Opus 4.7, manual extended thinking (`type: "enabled"`) is deprecated — use adaptive thinking (`thinking: {type: "adaptive"}`) with the effort parameter instead.
C) The `thinking` parameter must be placed in the system prompt, not the API call body.
D) The model requires the `extended_thinking: true` flag in addition to the thinking configuration object.

<details>
<summary>Answer</summary>

**B)** The extended thinking documentation explicitly states: "Manual extended thinking (`thinking: {type: 'enabled', budget_tokens: N}`) is no longer supported on Claude Opus 4.7 and returns a 400 error." The correct approach for Opus 4.7 is adaptive thinking with the effort parameter. A is wrong because the error is not caused by token budget size. C is wrong because the `thinking` parameter belongs in the API call body, not the system prompt. D is wrong because `extended_thinking: true` is not a documented parameter. (source: Extended thinking)

</details>

---
