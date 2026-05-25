# Module Bank: Multi-Agent Research System

Auto-generated bank with 30 questions.

## Question 1
A legal contract analysis subagent retrieves a clause library from an internal repository. The HTTP request returns a 401 Unauthorized error. The subagent has a retry loop configured with exponential backoff. After 3 retries still returning 401, it escalates to the coordinator with a full attempt log. A junior engineer argues the subagent should have retried longer because authentication errors can be transient. What is the correct assessment?

A) The engineer is correct — 401 errors from OAuth systems are often transient when tokens expire mid-request and should be retried up to 10 times before escalation
B) The subagent is correct — a 401 is an access failure, but it is non-transient and non-retryable without credential refresh; retrying the same request will produce the same result
C) The subagent should have silently switched to a public fallback clause database and completed the task without escalating, since the coordinator's context is better used for business logic
D) The subagent is correct — any error after 3 retries should be escalated regardless of whether further retries could succeed, because local retry budgets are fixed at 3

<details><summary>Answer</summary>
**B)** A 401 Unauthorized error signals that the request lacked valid credentials, not that the server was temporarily unavailable. Retrying an identical request with the same credentials will return the same 401 — the failure is deterministic, not transient. The correct local recovery path would be a token refresh, but if that is outside the subagent's capability, escalation with a full attempt log is the right move. A is wrong because 401 specifically means authentication failure — if the token expired, the fix is a token refresh, not blind retries of the same request with the same (expired) credentials. C is wrong because silently switching to an unapproved fallback database is a policy decision the subagent cannot make unilaterally — the coordinator must authorize alternative sources. D is wrong because the 3-retry rule is a heuristic for transient errors; the principled distinction is error type (retryable vs non-retryable), not retry count alone. (source: Agentic and multi-agent workflows)
</details>

## Question 2
A patent database subagent completes a search for prior art on a medical device patent. It returns `status: "complete"`, `patents_found: 0`, `query: "piezoelectric bone anchoring 2018-2024"`. The coordinator triggers its error-recovery path and resubmits the identical query three times, consuming 12 additional seconds. The final report notes "prior art search inconclusive due to retrieval failures." What is the coordinator's error?

A) The coordinator failed to verify that the patent database was online before dispatching the subagent, allowing a potentially unavailable source to cause downstream failures
B) The coordinator conflated a valid empty result — no matching patents exist — with a retrieval failure, triggering unnecessary retries and mislabeling the finding
C) The coordinator's retry logic did not implement exponential backoff, causing it to hammer the patent database in rapid succession and triggering a rate limit on the third attempt
D) The coordinator should have dispatched a second subagent to cross-validate the zero-result finding against a separate database before accepting the empty result

<details><summary>Answer</summary>
**B)** `patents_found: 0` with `status: "complete"` is an informative finding: the database was reachable, the query was processed, and the result is "no matching prior art exists in this scope." Treating this as a retrieval failure triggers unnecessary retries and ultimately misrepresents the finding in the report. "No prior art found" is a meaningful legal finding; labeling it "inconclusive due to retrieval failures" changes the legal interpretation entirely. A is wrong because pre-flight database availability checks add overhead and don't prevent failures mid-request — the actual result showed the database was accessible and responded correctly. C is wrong because rate limiting would produce a 429 error, not `status: "complete"` — the described behavior does not match rate limiting. D is wrong because cross-validation is a valid research strategy for high-stakes findings, but the first step is correctly interpreting the result before deciding whether validation is warranted — not defaulting to validation because the result is zero. (source: Agentic and multi-agent workflows)
</details>

## Question 3
A scientific literature synthesis coordinator dispatches 6 parallel subagents to review recent oncology research. After all return, the coordinator observes that subagents 2, 4, and 5 each retrieved and analyzed the same 3 landmark NEJM papers, producing 34,000 tokens of redundant output. Subagent 1 covered a distinct set of conference proceedings with no overlap. What should the coordinator have done differently?

A) Implemented a shared citation registry that subagents could write to and read from during execution, allowing later agents to skip sources already claimed by earlier agents
B) Run the subagents sequentially so each could inspect the previous agent's source list before selecting its own sources, preventing overlap
C) Partitioned the research space before delegation — assigning distinct publication venues, date ranges, or subtopics to each subagent — so overlap was structurally impossible
D) Added a deduplication pass after collection that merged identical analyses of the same paper into a single representative summary before synthesis

<details><summary>Answer</summary>
**C)** The root cause is ambiguous task boundaries at delegation time. When 3 of 6 agents independently converge on the same 3 landmark papers, the coordinator assigned them overlapping or identical scopes. Explicit pre-delegation partitioning — e.g., agent 2 covers NEJM 2020-2021, agent 4 covers NEJM 2022, agent 5 covers JAMA 2020-2022 — makes overlap structurally impossible without shared runtime state or sequential coordination. A is wrong because a shared citation registry during parallel execution introduces race conditions (two agents may claim the same paper simultaneously) and requires agents to coordinate runtime state, adding complexity and latency to what should be stateless parallel execution. B is wrong because sequential execution eliminates the throughput benefit of parallel dispatching — the correct fix is pre-delegation partitioning, not serialization. D is wrong because post-collection deduplication addresses the symptom (redundant output tokens) without preventing the redundant work from happening — all 34,000 tokens were already generated. (source: Multi-agent systems)
</details>

## Question 4
A regulatory compliance research system uses a `fetch_url` general-purpose tool to retrieve documents. A subagent tasked with analyzing EU GDPR guidance is observed fetching competitor privacy policies from public websites after the GDPR documents mention them as comparison examples. The behavior was not explicitly prohibited in the subagent's prompt. What is the most robust fix?

A) Add a monitoring hook to the coordinator that intercepts all tool calls from subagents and blocks any URL not in a pre-approved domain whitelist
B) Expand the subagent's system prompt with explicit instructions prohibiting external navigation beyond the originally assigned document set
C) Replace `fetch_url` with a scoped `load_regulatory_document` tool that accepts only document IDs from the internal compliance repository, making external URL fetching structurally impossible
D) Instruct the subagent to log every URL it intends to fetch and wait for coordinator approval before making each request, creating an approval gate for unanticipated fetches

<details><summary>Answer</summary>
**C)** The problem is that the agent has a capability — fetching arbitrary URLs — that exceeds what its task requires. Prompt instructions are probabilistic controls; a sufficiently compelling in-context reference (like a GDPR document explicitly mentioning a competitor policy) can rationalize the behavior. A scoped `load_regulatory_document` tool that only accepts known internal document IDs makes the undesired behavior structurally impossible: the tool simply cannot process an external URL regardless of the model's reasoning. A is wrong because coordinator-level URL interception adds latency on every document fetch and couples the coordinator to implementation details of every subagent's tool use — it's a runtime filter rather than a structural constraint. B is wrong because prompt-level prohibitions are bypassed when the model constructs a plausible rationale; the external URL was explicitly cited in the source document, providing exactly that rationale. D is wrong because requiring coordinator approval on every URL fetch serializes what should be autonomous operation and adds significant latency overhead for a problem that tool scoping already solves cleanly. (source: Tool use)
</details>

## Question 5
A financial market intelligence subagent encounters a connection timeout when querying a real-time equity data feed. It retries twice with 2-second delays, both also timing out. It then switches to a cached snapshot from 4 hours ago, completes its analysis using the stale data, and returns results to the coordinator without mentioning the data source switch. The coordinator publishes the analysis to a trading desk. What principle did the subagent violate?

A) The subagent should have retried at least 5 times before switching data sources, since persistent timeouts on high-frequency financial feeds are often caused by brief network partitions
B) The subagent violated the principle of transparent failure reporting — switching to a degraded data source without informing the coordinator stripped the coordinator of information needed to assess result validity
C) The subagent should have requested coordinator authorization before accessing the cached data source, since cached snapshots require explicit permission not covered by the real-time feed authorization
D) The subagent was wrong to perform local recovery at all; all data source fallback decisions for financial data should be made by the coordinator, never by the subagent autonomously

<details><summary>Answer</summary>
**B)** For time-sensitive financial analysis, the age of the data is material to the result's validity. Using a 4-hour-old snapshot without disclosure means the coordinator — and downstream consumers — have no way to assess whether the analysis is still valid. The coordinator may have access to alternative real-time sources, may know that market conditions changed significantly in the past 4 hours, or may decide to hold publication. Transparent failure reporting with structured context (failure type, attempted source, fallback source used, data timestamp) gives the coordinator the information it needs to make that call. A is wrong because additional retries on a timeout condition may be warranted, but the primary violation here is non-disclosure of the data source switch, not the retry count. C is wrong because data source authorization is a permissions concern separate from the disclosure issue — the main violation is opacity, not unauthorized access. D is wrong because local recovery is appropriate for many conditions; the problem is not that the subagent acted autonomously, but that it acted opaquely. (source: Agentic and multi-agent workflows)
</details>

## Question 6
A supply chain monitoring coordinator assigns three subagents to research disruption risks: agent A covers geopolitical events, agent B covers weather and natural disasters, and agent C covers logistics capacity constraints. After completion, the final report contains strong coverage of geopolitical and weather risks but entirely omits port congestion and shipping rate volatility — topics that fall within logistics capacity. Agent C's logs show it completed successfully. What is the correct diagnosis?

A) Agent C's web search tool returned no results for port congestion queries, indicating a search API gap that requires a different search provider for logistics data
B) The synthesis agent applied topic relevance filtering that inadvertently excluded logistics content as less strategically significant than geopolitical or weather topics
C) The coordinator's task specification for agent C was underspecified — "logistics capacity constraints" did not enumerate port congestion and shipping rates as required subtopics
D) Agent C deprioritized shipping rate data because it encountered sources of lower credibility than geopolitical or weather sources and applied internal quality filtering

<details><summary>Answer</summary>
**C)** Agent C completed successfully — it executed its assigned task without errors. When a correctly executing agent produces output that misses expected subtopics, the cause is an underspecified task prompt. "Logistics capacity constraints" is a broad label that agent C interpreted without guidance about which specific dimensions to cover. Explicit enumeration (port congestion, shipping rates, rail capacity, warehouse availability) would have produced the expected coverage. A is wrong because there is no evidence of search API failure — the agent completed successfully, meaning it found and analyzed content within its interpreted scope. B is wrong because synthesis filtering can only exclude findings the agents actually produced — if the synthesis agent filtered port congestion content, agent C must have produced it; the logs would show it. D is wrong because quality filtering is an internal subagent behavior not indicated by the available evidence — the parsimonious explanation is underspecification of scope. (source: Multi-agent systems)
</details>

## Question 7
An enterprise knowledge base query subagent is designed for simple single-document lookups. Instrumentation shows 88% of requests are single-document retrievals averaging 200ms, while 12% involve cross-referencing 5+ documents and require 3-4 seconds. Currently all queries go through a powerful but expensive orchestrated multi-step retrieval agent, adding 800ms overhead to every simple lookup. What tool configuration best optimizes this system?

A) Give the knowledge base subagent access to the full multi-step retrieval tool for all queries, since having more capability available never degrades performance for simple cases
B) Provide the knowledge base subagent with a scoped `lookup_document` tool for the 88% of simple retrievals, while routing complex cross-reference requests to the multi-step retrieval agent through the coordinator
C) Build a classifier agent that inspects each query before routing it, directing simple queries to a fast lookup path and complex queries to the multi-step agent, adding one classification round-trip to each request
D) Cache all single-document results with a TTL of 24 hours to eliminate the 800ms overhead for repeat lookups, while routing all cache misses through the multi-step retrieval agent

<details><summary>Answer</summary>
**B)** This is the scoped-capability principle: 88% of requests are well-served by a lightweight `lookup_document` tool that executes quickly without coordinator involvement. Giving the subagent this scoped tool for its common case reduces latency for the vast majority of requests while preserving the multi-step agent path for genuinely complex queries. The coordinator only sees complex requests, preserving its bandwidth. A is wrong because adding full multi-step capability to every subagent invocation does add overhead — capability breadth increases the model's reasoning burden about which approach to use, and may route simple lookups through unnecessarily complex paths. C is wrong because a classifier agent adds at least one additional round-trip to every request — a fixed overhead applied to 100% of queries to save overhead on 88% is net negative. D is wrong because caching helps with repeated queries but doesn't reduce latency for first-time lookups, which may represent the majority of a knowledge base's query load in a research context. (source: Tool use)
</details>

## Question 8
A competitive product research system has two agents with similar tool names: a pricing analyst agent with a `compare_products` tool and a feature analyst agent with a `compare_features` tool. The coordinator routes analysis tasks to the wrong agent 38% of the time. An engineer proposes fixing this by adding detailed descriptions to both tools explaining what each covers. A second engineer proposes renaming `compare_products` to `analyze_pricing_and_market_position`. Which fix is more effective?

A) The first engineer's fix is sufficient — detailed descriptions give the coordinator enough semantic context to route correctly without changing names that other system components may depend on
B) The second engineer's fix is more effective — renaming eliminates the shared prefix "compare_" that creates semantic ambiguity at the routing stage, making misrouting structurally less likely
C) Both fixes together are required — renamed tools without updated descriptions still leave routing ambiguous because the coordinator relies equally on both names and descriptions for routing decisions
D) Neither fix addresses the root cause — the coordinator needs few-shot routing examples in its system prompt showing correct agent selection for 20+ task types to achieve reliable routing

<details><summary>Answer</summary>
**B)** The routing confusion stems from the shared "compare_" prefix, which creates semantic overlap that the coordinator cannot resolve without deep reasoning about the full description. Renaming `compare_products` to `analyze_pricing_and_market_position` eliminates the ambiguous prefix — the two tool names now have no lexical overlap, making correct routing significantly more reliable even before reading descriptions. A is wrong because descriptions reduce ambiguity but don't eliminate the lexical overlap in the name itself — under novel task phrasings, a coordinator may still anchor on the shared "compare_" prefix. C is wrong because the question asks which fix is more effective, and renaming alone provides structural disambiguation; descriptions are supplementary. D is wrong because few-shot examples are a training signal, not a fix for a naming design problem — they add complexity without addressing the root cause of ambiguous tool names. (source: Tool use)
</details>

## Question 9
A legal contract review coordinator dispatches 4 subagents to review different sections of a merger agreement in parallel. After completion, the coordinator sends all 4 results to a synthesis agent. The synthesis agent returns a report. The coordinator has no mechanism to verify that all 4 contract sections were actually covered in the synthesis output. Two days later, a lawyer notices that indemnification clauses from section 3 are absent from the report, despite subagent 3 returning complete findings. What should the coordinator have implemented?

A) Required the synthesis agent to sign off on each subagent's findings with an acceptance confirmation before producing the final report
B) Implemented post-synthesis coverage verification: cross-checking that each assigned section appears at least once in the synthesis output, with a gap flag if any section is absent
C) Dispatched a separate review agent to audit the synthesis agent's output against the original contract sections after each synthesis run
D) Run the synthesis agent twice on the same inputs and compared outputs for consistency, flagging divergences for human review

<details><summary>Answer</summary>
**B)** The coordinator is responsible for verifying that the research space it delegated was actually reflected in the output. A coverage check — mapping each assigned section (e.g., section 3: indemnification) to at least one reference in the synthesis output — would have caught the gap programmatically before publication. This is cheaper and more reliable than downstream human review. A is wrong because a synthesis agent "signing off" on inputs it received is circular — it confirms receipt, not that the content was incorporated; the synthesis agent can receive section 3 findings and still fail to include them in output. C is wrong because a separate review agent adds a full additional reasoning step and cost to every run; structured coverage verification by the coordinator is simpler and does not require LLM reasoning. D is wrong because running synthesis twice addresses output consistency, not coverage — a synthesis agent that misses section 3 will likely miss it consistently across runs. (source: Multi-agent systems)
</details>

## Question 10
A scientific literature subagent is retrying a query to a genomics database. The first attempt failed with a 429 Too Many Requests response. The subagent waits 30 seconds and retries; the second attempt returns a 503 Service Unavailable. The subagent waits 60 seconds and retries; the third attempt again returns 503. The subagent logs all three attempts with their error codes and escalates to the coordinator. Is the escalation appropriate?

A) No — the subagent should continue retrying indefinitely with increasing backoff until the service recovers, since 503 errors are always temporary outages that resolve without coordinator involvement
B) Yes — after multiple retries with different error types (429 then 503), the failure pattern suggests a persistent service issue that the subagent cannot resolve locally; escalation with the full attempt log is correct
C) No — the subagent should switch to an alternative genomics database from its fallback list before escalating, since escalation is only appropriate when all available sources have been exhausted
D) Yes — any 503 error should immediately trigger coordinator escalation without local retry, since 503 errors indicate server-side failures outside the subagent's control

<details><summary>Answer</summary>
**B)** The subagent correctly applied local recovery: it attempted retries with appropriate delays, exhausted a reasonable retry budget, and escalated with a full attempt log. The escalation is appropriate because the failure persisted through multiple attempts with different error signatures (rate limit then service unavailable), suggesting conditions the subagent cannot resolve locally. The coordinator, with broader context, can decide whether to try an alternative database, delay the task, or surface the gap. A is wrong because indefinite retries with no escalation can block the research pipeline indefinitely — a bounded retry budget with escalation on exhaustion is the correct design. C is wrong because whether to use a fallback database is a policy decision the coordinator should make, not an automatic subagent behavior — the subagent may not know which alternatives are approved, and the coordinator needs the full failure context regardless. D is wrong because 503 errors can be transient; the first 503 does not justify immediate escalation — the subagent's retry attempts were appropriate before escalation. (source: Agentic and multi-agent workflows)
</details>

## Question 11
A competitive product research coordinator needs to cover 9 product categories. An engineer proposes dispatching 9 subagents simultaneously, one per category. A second engineer argues the categories are grouped into 3 strategic clusters (enterprise software, consumer hardware, cloud services) where findings in one category often inform research priorities in related categories. Which dispatch strategy is more appropriate?

A) Dispatch all 9 simultaneously — the coordinator should always maximize parallelism and handle cross-category dependencies at synthesis time to avoid unnecessary serialization
B) Dispatch in 3 waves of 3 by cluster — findings from the first wave's cluster leaders can inform search strategies for the remaining categories in waves 2 and 3
C) Dispatch all 9 simultaneously but configure each subagent to monitor a shared findings registry and update its search queries in real time based on what other agents discover
D) Dispatch 3 cluster-lead subagents first, then have those agents spawn their own sub-subagents for the remaining 6 categories based on their initial findings

<details><summary>Answer</summary>
**B)** When findings in one category meaningfully change how you'd research related categories in the same cluster, sequential waves allow the coordinator to use wave-1 findings to write better wave-2 prompts. Dispatching all 9 simultaneously means the dependent categories run with uninformed search strategies — synthesis cannot retroactively improve the quality of already-completed research. A is wrong because "handle cross-category dependencies at synthesis" only works for integrating results; it cannot improve the research that went into those results — if category 4's search strategy would have been different given category 1's findings, that opportunity is permanently lost in a fully parallel dispatch. C is wrong because shared registry updates during parallel execution introduce coordination complexity, race conditions, and require subagents to dynamically modify in-flight research plans — this is far more complex than the coordinator directing wave-2 prompts after wave-1 results. D is wrong because having subagents spawn their own sub-subagents moves orchestration responsibility out of the coordinator, reducing visibility and control — the coordinator should manage all dispatching. (source: Multi-agent systems)
</details>

## Question 12
A research subagent is tasked with finding merger and acquisition activity in the pharmaceutical sector and returns results as free-form prose: "Based on my analysis, there were several notable acquisitions including Pfizer's purchase of Arena Pharmaceuticals for approximately $6.7 billion, which closed in early 2022, alongside AstraZeneca's acquisition of Alexion which was valued at around $39 billion. Both deals reflect strategic moves toward rare disease portfolios..." The coordinator's synthesis agent processes 6 such inputs and produces a report with inconsistent citation formatting and missing deal values. What is the most direct fix?

A) Replace the free-form prose output with a structured schema: each acquisition as a JSON object with fields for acquirer, target, value, close date, and strategic rationale, enforced across all subagents
B) Add an intermediate normalization agent between the research subagents and the synthesis agent that extracts structured data from prose before forwarding to synthesis
C) Prompt the synthesis agent with explicit extraction instructions to parse acquirer names, deal values, and dates from prose inputs before constructing the report
D) Require each subagent to append a structured appendix to its prose output listing key data points in a consistent tabular format alongside its narrative analysis

<details><summary>Answer</summary>
**A)** The root cause is unstructured output format — prose requires the synthesis agent to perform implicit extraction, which is error-prone. The fix is a schema contract: all subagents return the same JSON structure with explicit fields, making the synthesis agent's job a deterministic merge rather than natural language interpretation. Consistency in citation formatting and numeric values follows automatically from structured fields. B is wrong because a normalization agent compensates for a fixable upstream problem by adding a component, latency, and potential extraction errors at an intermediate layer — fixing the source is cleaner and more reliable. C is wrong because prompting the synthesis agent to parse prose introduces a secondary extraction step that is still error-prone, and the synthesis agent must now parse 6 different prose styles — the problem is just moved downstream. D is wrong because a dual-format output (prose + structured appendix) adds token overhead and still requires the synthesis agent to know to use the appendix rather than the prose — consistency is not guaranteed. (source: Multi-agent systems)
</details>

## Question 13
A supply chain monitoring system assigns a subagent to track raw material price fluctuations across 15 commodity types. The coordinator receives the subagent's report but has no record of which of the 15 commodities were successfully covered vs skipped due to missing data. Three commodities with known data quality issues were silently omitted from the report. What mechanism should the coordinator have required from the subagent?

A) A pre-execution checklist submitted to the coordinator before the subagent begins, listing all 15 commodities and their expected data sources, so the coordinator can verify the plan before work starts
B) Coverage annotations in the output: an explicit accounting of which commodities were successfully researched, which had partial data, and which were not covered and why
C) A confidence score for each commodity in the final output, allowing the coordinator to infer which commodities had data quality issues from low confidence values
D) A separate audit run after the main research pass where the subagent re-verifies each commodity's data availability and flags any that were omitted in the primary pass

<details><summary>Answer</summary>
**B)** The coordinator assigned 15 commodities and must be able to verify that all 15 were addressed. Coverage annotations — structured records of what was covered, what was partially covered, and what was omitted and why — give the coordinator the information it needs to assess completeness and decide next steps (re-dispatch for missing commodities, proceed with partial coverage, etc.). This is the transparency principle: gaps must be surfaced explicitly, not omitted silently. A is wrong because a pre-execution checklist verifies the plan before work, not the execution after work — it doesn't help the coordinator detect what was actually omitted during execution. C is wrong because confidence scores communicate result quality, not coverage — a missing commodity has no confidence score at all, which the coordinator cannot distinguish from a low-confidence result that was included. D is wrong because a separate audit run doubles the work and adds latency; the correct design is for the subagent to produce coverage annotations as part of its normal output, not as a separate verification pass. (source: Agentic and multi-agent workflows)
</details>

## Question 14
A research coordinator receives outputs from 5 subagents. Four return complete findings. One returns a structured error: `{"type": "rate_limit_exceeded", "query": "FDA drug approval filings Q3 2024", "retries": 3, "partial_results": ["FDA-2024-089", "FDA-2024-092"]}`. The coordinator proceeds to synthesis using only the 4 complete results, discarding the error object. Is this correct?

A) Yes — synthesis agents should only receive verified complete results; passing structured error objects to synthesis would contaminate the output quality assessment
B) No — the error object contains two partial results and should be passed to synthesis with a gap annotation indicating incomplete coverage of FDA Q3 2024 filings
C) Yes — the coordinator has fulfilled its responsibility by attempting the query; routing failures to synthesis adds complexity without improving the final output
D) No — the coordinator should immediately retry the failed subagent before proceeding to synthesis, since partial results indicate the data source was accessible

<details><summary>Answer</summary>
**B)** The error object contains two partial results (`FDA-2024-089` and `FDA-2024-092`) that represent real data — discarding them discards findings that were successfully retrieved. The coordinator should pass the partial results to synthesis with an explicit gap annotation: "FDA Q3 2024 coverage is incomplete — 2 filings retrieved, remainder unavailable due to rate limiting." This gives the synthesis agent factual content to work with and transparency about what's missing. A is wrong because structured error objects with partial results are not "unverified" — the partial results were successfully retrieved and are as valid as results from the complete subagents. C is wrong because "routing failures to synthesis adds complexity" is not a valid reason to discard partial results that contain real findings — the coordinator's job is to route what exists, with appropriate annotations. D is wrong because immediate retry is one option, but the coordinator may have other priorities (deadline constraints, availability of the rate-limited source) — the first step is to preserve the partial results, not reflexively retry. (source: Agentic and multi-agent workflows)
</details>

## Question 15
A knowledge base research subagent runs a query against an internal policy document store. The store returns an error: `403 Forbidden - Tool 'search_policy_documents' requires scope 'policy:read' not present in current token`. The subagent retries twice with the same credentials, both returning 403. It escalates to the coordinator with the error message. The coordinator logs the escalation and asks the subagent to try a different query formulation. What has the coordinator misunderstood?

A) The coordinator should have recognized the 403 as a permissions error — a policy gap where the subagent structurally lacks the required authorization — and addressed the permission configuration rather than suggesting a query change
B) The coordinator correctly identified that different query formulations may bypass authorization checks on some policy document stores, and the suggestion to reformulate is a valid recovery strategy
C) The coordinator should have escalated the 403 to the end user for manual intervention, since authorization errors require human approval to resolve and are outside automated system handling
D) The coordinator's error was in not attempting the query itself using its own higher-privilege credentials, since coordinators in multi-agent systems typically hold broader permissions than subagents

<details><summary>Answer</summary>
**A)** A 403 Forbidden with an explicit missing scope message is a policy gap: the subagent's token does not have `policy:read`, full stop. No query reformulation can change what scopes are present in the token. The coordinator misclassified this as a retrieval problem (fixable by changing the query) when it is actually a permissions problem (fixable only by adding the required scope to the token). The correct response is to address the credential configuration — either grant the scope or inform a human who can. B is wrong because 403 errors with explicit scope messages are not bypassed by query reformulation — the authorization check happens before any query processing. C is wrong because while human intervention may ultimately be needed to grant permissions, the coordinator first needs to correctly diagnose the problem and can take preparatory steps (documenting the gap, completing other research tasks) while awaiting resolution. D is wrong because the coordinator using its own credentials to perform the subagent's task defeats the purpose of the subagent and violates the separation of concerns — the fix is to grant the subagent the permission it needs. (source: Tool use)
</details>

## Question 16
A multi-agent competitive intelligence system completes a research run. The coordinator produces a final report. A post-run review finds that 4 of the 7 subagents completed their tasks and returned findings, but the report presents all findings as equally authoritative without indicating that 3 subagent results are missing. The coordinator logged the 3 failures but did not surface them in the report. What is the correct behavior?

A) The coordinator acted correctly — including failure metadata in the final report would undermine consumer confidence in the findings that were successfully retrieved
B) The coordinator should have blocked publication of the report until all 7 subagents completed, ensuring that no report is published with known gaps
C) The coordinator should have included coverage annotations in the report identifying which research areas have findings, which have partial coverage, and which are absent due to subagent failures
D) The coordinator should have dispatched replacement subagents for the 3 failures and waited for them to complete before generating the report

<details><summary>Answer</summary>
**C)** Transparency about coverage is mandatory when presenting research findings. A report that presents 4 of 7 coverage areas as a complete picture is misleading — the reader cannot distinguish between "no significant findings in this area" and "this area was not researched due to a failure." Coverage annotations give the consumer the information needed to weight the findings appropriately and identify gaps that warrant follow-up. A is wrong because transparency about gaps does not undermine valid findings — it contextualizes them. Concealing known gaps is the reliability failure. B is wrong because blocking publication may be unacceptable under time constraints, and partial-coverage reports with explicit annotations are often more useful than delayed complete reports. D is wrong because re-dispatching is one option the coordinator can consider, but the decision depends on time, cost, and whether the gaps are critical — the immediate requirement is to surface the gaps in the output. (source: Agentic and multi-agent workflows)
</details>

## Question 17
A research subagent is dispatched to collect and summarize academic citations for a literature review on carbon capture technologies. It retrieves 40 papers, processes the first 22, and then receives a context window warning indicating it has 800 tokens remaining. Each remaining paper requires approximately 1,500 tokens to process. What should the subagent do?

A) Attempt to compress its in-context summaries of the first 22 papers to free up tokens for the remaining 18, then continue processing until context is fully exhausted
B) Continue processing papers until it receives a hard context limit error, then return whatever state it has at termination
C) Return the completed analyses of all 22 processed papers with a structured notation indicating 18 papers were not processed due to context limits, including their citation identifiers
D) Discard all 22 completed summaries and return only a request to the coordinator for a larger context window before proceeding with the task

<details><summary>Answer</summary>
**C)** With only 800 tokens remaining and 1,500 required per paper, the subagent cannot process even one more paper. It should preserve and return the maximum useful work completed — 22 high-quality paper analyses — with an explicit structured notation identifying the 18 unprocessed papers and the reason (context limit). This gives the coordinator the completed work and the information it needs to dispatch a continuation subagent for the remaining 18. A is wrong because compressing already-completed summaries risks quality degradation of the most complete part of the work — the 22 summaries are the primary output and should not be sacrificed. B is wrong because continuing until a hard error risks returning a garbled or incomplete mid-paper analysis as the final output; a graceful early return with clear completion state is more reliable. D is wrong because discarding 22 completed analyses discards the majority of the task's output — the subagent should return what it has, not nothing, while communicating the gap. (source: Agentic and multi-agent workflows)
</details>

## Question 18
A financial market intelligence workflow uses a coordinator that passes the complete accumulated output of each subagent to the next subagent in a sequential chain. After 5 subagents, the 6th subagent receives 98,000 tokens of prior context. The 6th subagent's actual task — cross-reference sector trends from agents 1 and 3 — requires approximately 4,000 tokens from those two agents. What is the structural problem?

A) Sequential chaining prevents the coordinator from tracking which subagent produced which findings, since outputs accumulate without attribution metadata
B) Passing full accumulated context causes uncontrolled context growth — by subagent 6, the context includes 5 agents' complete reasoning chains, when only targeted extracts from agents 1 and 3 were needed
C) The 6th subagent cannot process outputs from non-adjacent agents in a sequential chain, since it can only reference the immediately preceding agent's output reliably
D) Sequential chains cannot exceed 5 agents due to cumulative context entropy, which degrades model reasoning quality past a threshold that compound accumulation makes unavoidable

<details><summary>Answer</summary>
**B)** This is uncontrolled context accumulation: each subagent receives not just the information it needs but the entire reasoning history of all prior agents. By subagent 6, 94,000 of its 98,000-token context is noise relative to its actual task. The fix is coordinator-mediated extraction: the coordinator passes only the relevant outputs from agents 1 and 3 (approximately 4,000 tokens) to agent 6, not the full accumulated chain. A is wrong because attribution can be maintained regardless of context structure — well-designed structured outputs include agent IDs and source metadata independent of how context is passed. C is wrong because there is no architectural constraint preventing a chain-based agent from reasoning about non-adjacent outputs — the issue is the context cost, not the accessibility of prior agents' outputs. D is wrong because there is no fixed 5-agent limit or "cumulative entropy" threshold — the problem is design (full context accumulation), not a fundamental property of sequential chains. (source: Multi-agent systems)
</details>

## Question 19
A research system is designed so that when a subagent fails, the coordinator immediately dispatches a replacement with the same task parameters. During a run, a downstream API experiences an outage affecting all subagents that query it. 6 subagents fail, 6 replacements are dispatched, all 6 replacements fail, triggering 6 more replacements. The coordinator enters a replacement loop. What design principle was violated?

A) Idempotency — the replacement subagents should have detected that their task was already attempted and returned the prior subagent's failure log rather than re-executing
B) Stop conditions — the replacement policy lacked a circuit-breaker that detects systematic correlated failures and halts replacement loops before they consume unbounded resources
C) Least privilege — if subagents had been granted narrower tool permissions, the API outage would have affected fewer agents and the replacement loop would have been smaller in scope
D) Coverage annotation — the coordinator lacked mechanisms to annotate which research areas were affected by the outage, causing it to treat each failure as independent rather than correlated

<details><summary>Answer</summary>
**B)** The replacement loop violates the stop conditions principle: a well-designed system must have circuit-breakers that detect correlated failures (multiple agents failing for the same reason in a short window) and halt automatic replacement before the loop consumes unbounded compute and API capacity. Six simultaneous failures followed by six simultaneous replacement failures is a clear signal of a systemic issue, not independent subagent errors. A is wrong because idempotency addresses whether a repeated operation produces duplicate side effects — it does not prevent a coordinator from dispatching replacements; that requires stop conditions. C is wrong because least privilege reduces blast radius but does not prevent the replacement loop itself — even if fewer agents were affected, the pattern of automatic replacement without termination logic would still create a smaller loop. D is wrong because coverage annotation describes output metadata — it is a transparency mechanism, not a mechanism for detecting and halting replacement loops. (source: Agentic and multi-agent workflows)
</details>

## Question 20
A multi-tier research system has a top-level coordinator, mid-level domain coordinators (legal, financial, technical), and leaf-level research subagents. The system is being designed with permission scopes. An engineer proposes giving mid-level domain coordinators the same permissions as the top-level coordinator so they can handle any tool call without escalating. What is the risk of this design?

A) Mid-level coordinators with top-level permissions would have authority to modify task assignments for subagents in other domains, creating cross-domain interference outside their designed scope
B) Identical permission scopes across all coordinator tiers eliminate the ability to audit which level of the hierarchy authorized a specific action, creating an untraceable authorization chain
C) Top-level permissions at mid-level coordinators violate the least-privilege principle — domain coordinators should have only the permissions their domain tasks require, limiting blast radius if a coordinator is compromised or misbehaves
D) Equal permissions across coordinator tiers prevent the top-level coordinator from distinguishing coordinator-level tool calls from subagent-level tool calls in the audit log

<details><summary>Answer</summary>
**C)** The least-privilege principle requires that every component has exactly the permissions its task requires, no more. A legal domain coordinator needs access to legal databases, contract tools, and case law APIs — not financial data feeds or technical architecture tools. Granting top-level permissions at every tier means a misbehaving or compromised mid-level coordinator can access resources across all domains, dramatically increasing blast radius. A is wrong because cross-domain interference is a specific consequence of over-permissioning, not the primary principle — the broader concern is any overstep beyond the domain coordinator's legitimate scope. B is wrong because authorization traceability is a logging/auditing design concern, not a permissions design concern — well-structured audit logs can distinguish authorization levels regardless of permission scope overlap. D is wrong because audit log clarity is a monitoring concern, not a permissions principle — the primary argument against equal permissions across tiers is blast radius and access control, not log readability. (source: Multi-agent systems)
</details>

## Question 21
A regulatory compliance research subagent is tasked with checking whether a software product meets HIPAA technical safeguards requirements. The subagent completes its analysis and finds no violations. The coordinator marks the compliance check as passed and proceeds. Later, an auditor finds 3 HIPAA requirements that the subagent never checked because they were added to the HIPAA technical safeguard list in a 2023 update, while the subagent's knowledge and tool definitions reference the 2019 version. What architectural improvement would have most directly prevented this gap?

A) The coordinator should have verified the subagent's knowledge cutoff date before dispatching it on compliance tasks, since outdated agent knowledge is a known risk in regulatory domains
B) The subagent's compliance checklist tool should have been defined against a live, versioned regulatory database rather than a hardcoded checklist, making the requirements authoritative and current
C) The synthesis agent should have flagged the compliance analysis as potentially incomplete by cross-referencing the subagent's findings against a known regulatory update log
D) The coordinator should have dispatched two independent subagents to check compliance in parallel, with discrepancies between their outputs triggering a third tiebreaker agent

<details><summary>Answer</summary>
**B)** The root cause is a static tool definition referencing outdated requirements. If the compliance checklist tool queries a live, versioned regulatory database maintained by the compliance team, the subagent automatically works against current requirements on every run — no manual tool updates required when regulations change. This is the principle of binding tools to authoritative live sources rather than hardcoded static data. A is wrong because checking a subagent's "knowledge cutoff" is impractical for tool-based tasks — the subagent uses tools, not training memory, to perform compliance checks; the issue is the tool definition, not the agent's training. C is wrong because a synthesis agent cross-referencing against a "regulatory update log" adds a downstream check on symptoms rather than fixing the tool that generates the compliance assessment — and requires maintaining yet another static list of updates. D is wrong because two independent subagents using the same outdated checklist will produce identical (equally incomplete) outputs — parallel redundancy catches execution errors, not shared knowledge gaps. (source: Tool use)
</details>

## Question 22
A research coordinator dispatches a subagent with the instruction: "Search for recent legal precedents on data privacy liability." The subagent executes a broad web search and returns 47 results including blog posts, news articles, opinion pieces, and 3 actual court decisions. The coordinator passes all 47 to a synthesis agent. The synthesis agent produces an analysis mixing authoritative case law with opinion content without distinguishing them. What should the coordinator have specified?

A) The coordinator should have instructed the synthesis agent to apply credibility weighting, scoring each source by domain authority before incorporating its findings
B) The coordinator's task prompt should have specified the output schema required: court decisions as primary sources with case citation, jurisdiction, and holding; secondary sources clearly labeled and separated
C) The coordinator should have dispatched a source-filtering subagent after the search subagent, tasked with separating court decisions from non-authoritative sources before synthesis
D) The coordinator should have replaced the general web search tool with a legal database tool (e.g., Westlaw, LexisNexis API) that returns only verified case law by design

<details><summary>Answer</summary>
**D)** For legal precedent research, the task requires authoritative court decisions, not general web content. Replacing the general web search tool with a legal database tool that only returns verified case law solves the problem at the source: the subagent structurally cannot return blog posts or opinion pieces because the tool doesn't index them. This is the scoped tool design principle. A is wrong because credibility weighting at the synthesis layer is downstream mitigation — it adds reasoning complexity to synthesis and still allows low-credibility content to enter the pipeline, risking quality degradation. B is wrong because specifying output schema helps the synthesis agent organize what it receives, but doesn't prevent the search subagent from retrieving and passing non-authoritative sources in the first place — the 47 mixed results still arrive. C is wrong because a source-filtering subagent is an intermediate compensating component for a tool design problem — replacing the search tool is simpler, more reliable, and more direct. (source: Tool use)
</details>

## Question 23
A research workflow runs daily. The same query parameters are submitted each morning to a patent database subagent as part of routine monitoring. On days 1, 3, and 5, the subagent returns results normally. On day 2, the subagent fails mid-run due to an API timeout. On day 3, the subagent is re-dispatched for day 2's query and retrieves the same patents it retrieved on day 1. The coordinator stores duplicate patent records. What design property would have prevented the duplication?

A) The coordinator should have verified that day 3's subagent was not running before dispatching the day 2 retry, since parallel subagent runs against the same query parameter set cause duplication
B) The subagent's results should have been idempotent by design — the same query at the same target date range always returns the same set of results, and the coordinator's storage layer should upsert by patent ID rather than append
C) The coordinator should have locked the patent database to the subagent's exclusive session on day 2, preventing other subagents from querying the same records until the retry resolved
D) The day 2 subagent should have written a lock file before querying and checked for existing lock files at startup, preventing re-execution until the lock was explicitly cleared

<details><summary>Answer</summary>
**B)** Idempotency in research tasks means a subagent safe to re-run produces the same logical results, and the storage layer handles them correctly via upsert (insert-or-update-by-unique-key) rather than blind append. Since patent IDs are unique, upserting by patent ID on the day 2 retry would update existing records or insert new ones without creating duplicates — the coordinator can safely re-dispatch failed subagents without auditing every prior result. A is wrong because ensuring no parallel runs addresses one scenario (concurrent execution) but doesn't prevent the duplication caused by sequential re-dispatch, which is the described case. C is wrong because database locking at the session level is an extreme measure that blocks other legitimate queries — idempotent storage design is the correct architectural pattern for retry safety. D is wrong because file-based locking is a fragile, ad-hoc coordination mechanism that breaks on crashes (stale lock files) and doesn't address the storage-level duplication that idempotent upserts would solve. (source: Agentic and multi-agent workflows)
</details>

## Question 24
A coordinator is building a research pipeline for enterprise software competitive analysis. It plans to use centralized coordination — all subagent tasks flow through the coordinator. A colleague proposes a distributed peer-to-peer design where domain experts agents can directly request information from each other. The research topics are largely independent with minimal cross-domain dependencies. Which design is more appropriate?

A) Distributed peer-to-peer, because independent research topics benefit from direct agent-to-agent sharing of findings as they emerge, reducing total research time via early discovery propagation
B) Centralized coordination, because the research topics are largely independent — the coordinator provides state visibility, consistent error handling, and audit capability without imposing significant coordination overhead on independent tasks
C) Distributed peer-to-peer, because centralized coordinators become bottlenecks when many subagents are working in parallel and the coordinator must process every result before any other work can proceed
D) Centralized coordination only if the number of subagents is fewer than 5; for larger research teams, distributed coordination is required to prevent coordinator context window saturation

<details><summary>Answer</summary>
**B)** When topics are largely independent, the primary benefit of peer-to-peer (sharing emerging findings to inform parallel research) doesn't apply — agents don't need each other's findings during execution. Centralized coordination provides the coordinator's core value — full state visibility, consistent error handling, and a clear audit trail — without adding the complexity of peer-to-peer topology. The overhead of centralized routing is minimal when tasks are independent. A is wrong because "early discovery propagation" is only beneficial when agents can use each other's findings to adjust their own research; for independent topics, propagation adds communication overhead without improving output quality. C is wrong because the coordinator does not need to process every result before other work can proceed — in well-designed coordinators, subagent results are stored and synthesis happens after all complete; the coordinator does not block parallel execution. D is wrong because there is no principled threshold at which centralized coordination becomes inappropriate based on agent count alone — context window management is a solvable engineering challenge, not an architectural constraint. (source: Multi-agent systems)
</details>

## Question 25
A synthesis agent receives outputs from 7 research subagents and must combine them into a final briefing. An engineer proposes that instead of the synthesis agent processing all 7 outputs together, each research subagent should first condense its own findings into a 2-paragraph executive summary before sending to synthesis. The synthesis agent then combines 7 summaries instead of 7 full reports. When does this intermediate summarization design add value vs when does it not?

A) Intermediate summarization always adds value by reducing synthesis agent token consumption — the tradeoff is always favorable since shorter inputs produce faster and more reliable synthesis
B) Intermediate summarization adds value when full research outputs are verbose and context window capacity is a constraint; it adds latency and component complexity without benefit when research outputs are already structured and concise
C) Intermediate summarization only adds value when more than 5 subagents are involved, since below this threshold the synthesis agent can process full outputs without quality degradation
D) Intermediate summarization never adds value because the quality loss from compressing subagent findings outweighs the context savings at the synthesis stage in all research domains

<details><summary>Answer</summary>
**B)** The value of intermediate summarization depends on the situation. When subagents return verbose, loosely structured outputs and the synthesis agent's context window is at risk of overflow, pre-summarization reduces the load and focuses synthesis on distilled findings. However, when subagent outputs are already structured and concise (e.g., JSON with key fields), intermediate summarization adds a processing layer without reducing context load significantly, while introducing latency and an additional component that can introduce errors. The design decision should be driven by actual output volume and structure, not applied universally. A is wrong because shorter inputs do not always produce better synthesis — compressing nuanced research findings can lose the detail the synthesis agent needs for accurate cross-source integration; the tradeoff is not always favorable. C is wrong because there is no principled 5-agent threshold — the relevant factor is total token volume and output format, not agent count. D is wrong because in contexts with genuinely verbose subagent outputs (full web page content, extended reasoning chains), intermediate summarization does improve synthesis performance — the claim that it "never adds value" is too absolute. (source: Multi-agent systems)
</details>

## Question 26
A financial market research subagent is dispatched to analyze earnings reports for 20 companies. While processing company 14's report, it discovers evidence of a potential accounting irregularity — a pattern that, if real, would be highly material to the research question. Verifying the irregularity would require fetching 3 additional regulatory filings not in its original task scope, taking an estimated additional 8 minutes. What should the subagent do?

A) Independently fetch and analyze the 3 additional regulatory filings since the evidence is material to the research question and completing the analysis is more valuable than strict task adherence
B) Note the potential irregularity with its basis in the earnings report, flag it explicitly as requiring further investigation with specific citations needed, and return this finding to the coordinator along with its completed analysis
C) Skip the irregularity entirely and complete analysis of all 20 companies within the original task scope, since scope creep from individual agents undermines the coordinator's research plan
D) Pause all remaining analysis and immediately escalate only the irregularity finding to the coordinator before continuing, treating material evidence as a workflow interrupt

<details><summary>Answer</summary>
**B)** The subagent should complete its assigned scope, surface the material finding with explicit context (what was found, what additional filings would verify it, why it's significant), and return everything to the coordinator. The coordinator — not the subagent — should decide whether the verification work is worth 8 additional minutes, whether to dispatch a targeted subagent for those filings, or whether to note it as a follow-up item. Surfacing the finding with actionable context preserves the coordinator's decision authority. A is wrong because the subagent autonomously expanding its scope violates the principle that the coordinator controls task scope — even when the rationale is good, unilateral scope expansion removes the coordinator's ability to manage resources and priorities. C is wrong because skipping the irregularity and completing only within the rigid original scope treats the finding as irrelevant when it may be the most important discovery in the run — the correct action is to surface it, not suppress it. D is wrong because interrupting the entire analysis workflow for a preliminary signal adds unnecessary latency; the subagent can continue its other analyses while flagging the finding for the coordinator to handle after the run. (source: Agentic and multi-agent workflows)
</details>

## Question 27
A multi-agent patent analysis system performs research runs that take 45 minutes each. A coordinator dispatches subagents, collects results, and passes them to a synthesis agent. During a post-run analysis, the engineering team finds they cannot determine which specific claims from the final patent analysis were derived from which subagent's output, because the synthesis agent merged all inputs into flowing prose without source tracking. What is the correct fix?

A) Require the synthesis agent to append a full reference section to its output listing every source document each subagent analyzed, regardless of whether those documents contributed to specific claims
B) Enforce a structured output schema on the synthesis agent requiring explicit citation fields for each claim (e.g., `{"claim": "...", "source_agent": "...", "source_document": "...", "confidence": 0.92}`), making claim provenance traceable
C) Record the complete input and output of every subagent in an external log store, allowing post-hoc attribution by searching the log for content matching each claim in the synthesis output
D) Add a separate attribution agent that runs after synthesis, consuming both the synthesis output and all subagent inputs, and annotates each claim with its likely source agent

<details><summary>Answer</summary>
**B)** The fix is a structured output schema at the synthesis agent that binds each claim to its source at generation time. Requiring `source_agent` and `source_document` fields in the output schema makes provenance traceable by design — the synthesis agent produces auditable output rather than flowing prose. This is more reliable than any post-hoc approach. A is wrong because a global reference section lists documents analyzed by subagents, not which specific claims came from which sources — it provides bibliography, not claim-level provenance. C is wrong because post-hoc attribution by content matching is error-prone — synthesis agents paraphrase and combine findings, making content matching unreliable for tracing specific claims back to specific subagent outputs. D is wrong because an attribution agent adds a full LLM reasoning step (plus latency and cost) to reconstruct information that should have been recorded at synthesis time — source tracking at generation is more reliable than retrospective attribution. (source: Multi-agent systems)
</details>

## Question 28
A research coordinator is told the research task is complete when "all topics have been sufficiently explored." The coordinator's termination logic checks each subagent's output for the phrase "sufficient" or "complete" as a proxy for this condition. During a run, a subagent analyzing pharmaceutical patents writes: "The patent landscape appears sufficiently crowded in this therapeutic area to warrant caution." The coordinator terminates the entire workflow, treating this as a completion signal. What design flaw caused the premature termination?

A) The coordinator relied on natural language sentiment parsing for termination decisions rather than structural completion signals such as a `status` field or a task completion registry
B) The subagent violated output formatting conventions by using hedging language that could be ambiguous to downstream consumers processing its output
C) The coordinator's termination threshold was too low — requiring a single agent to signal completion rather than requiring all agents to signal completion simultaneously
D) The termination logic was not given enough context about the research domain, causing it to misinterpret domain-specific language as workflow status signals

<details><summary>Answer</summary>
**A)** Natural language parsing for workflow termination is inherently fragile. The word "sufficiently" appears in domain-specific analysis language with completely different semantics from workflow completion signals. Structural termination signals — a dedicated `status: "complete"` field, a boolean `task_done` flag, or explicit removal from a pending-tasks registry — are unambiguous because they are purpose-built for workflow control and cannot be confused with domain vocabulary. A is the direct and complete diagnosis. B is wrong because subagents should not be constrained from using natural professional language in their analysis outputs — the problem is the coordinator's fragile parsing logic, not the subagent's word choice. C is wrong because requiring consensus across all agents would not prevent the false positive — if any single subagent uses domain language containing trigger words, the coordinator still misfires; the issue is the parsing approach. D is wrong because adding domain context to the termination logic is a patch on a fundamentally flawed approach — no amount of context can prevent all natural language ambiguity in termination signals. (source: Agentic and multi-agent workflows)
</details>

## Question 29
A scientific literature coordinator dispatches subagents to review papers and return findings. Each subagent returns a verbose response including the full paper abstract, its reasoning steps ("First I identified the key variables... then I checked the sample size... I noticed the confidence interval..."), a summary of findings, and a relevance score. The coordinator's synthesis agent receives 180,000 tokens from 9 subagents and produces lower-quality integration than when processing 40,000 tokens from 4 subagents on a similar task. The coordinator is considering adding an intermediate summarizer agent. Is this the right fix?

A) Yes — an intermediate summarizer is the standard solution for synthesis context overflow and should be applied whenever the synthesis agent's input exceeds 100,000 tokens
B) No — the better fix is modifying the upstream subagent output format to return only the structured finding (key claims, citations, relevance score) without the verbose abstract and reasoning chain, eliminating token inflation at the source
C) Yes — intermediate summarizers allow the coordinator to preserve full subagent reasoning chains in storage while passing only distilled content to synthesis, achieving both auditability and synthesis quality
D) No — the coordinator should instead split the 9 subagent outputs into 3 batches of 3 and run 3 sequential synthesis passes, merging the intermediate syntheses in a final fourth pass

<details><summary>Answer</summary>
**B)** The root cause is upstream verbosity: subagents are returning full abstracts and internal reasoning chains that the synthesis agent doesn't need. Fixing the subagent output format to return only structured findings (key claims, citations, relevance score) eliminates the token inflation at the source without adding a component. Each subagent's output becomes 3,000-5,000 tokens of useful structured data instead of 20,000 tokens of padded content. A is wrong because intermediate summarizers are a downstream compensating mechanism, not the standard solution — they add latency and a reasoning layer without fixing the upstream verbosity that causes the problem. C is wrong because "preserving full reasoning chains in storage" is a logging concern, not an argument for the intermediate summarizer — the output format fix allows logging of full chains to a store while passing structured output to synthesis. D is wrong because splitting into sequential synthesis batches loses cross-subagent integration — findings from batch 1 and batch 3 cannot be cross-referenced at synthesis time, producing a lower-quality result than a single synthesis over structured inputs. (source: Multi-agent systems)
</details>

## Question 30
A supply chain intelligence system has a coordinator and 5 regional research subagents. During a run, 4 subagents complete and return findings. The 5th subagent (covering the Asia-Pacific region) encounters a transient authentication error, retries twice unsuccessfully, and returns a structured error to the coordinator. The coordinator continues to synthesis and produces a final risk assessment report. A reviewer notes the APAC region is completely absent from the report with no indication of missing coverage. The coordinator's synthesis prompt did not include instructions about handling partial inputs. What is the combined failure?

A) The subagent failed to implement sufficient retry logic, and the synthesis agent applied improper content filtering that removed the error signal before it reached the report
B) The coordinator passed the structured error to synthesis without instructions for handling it, and the synthesis agent silently omitted the APAC coverage gap rather than surfacing it with an annotation
C) The synthesis agent exceeded its authority by making coverage decisions — all gap handling should have been implemented in the coordinator before synthesis was invoked
D) The subagent should have returned an empty result set instead of a structured error, which would have allowed the synthesis agent to note the absence of APAC findings naturally

<details><summary>Answer</summary>
**B)** There are two failures working together: the coordinator passed the error object to synthesis without instructions on how to represent it in output, and the synthesis agent defaulted to omitting the gap rather than annotating it. The correct coordinator behavior is to include explicit synthesis instructions: "The APAC subagent returned a retrieval error — include an explicit coverage gap annotation for the APAC region in the final report." The synthesis agent's correct default when receiving a structured error would be to surface it as a coverage gap rather than silently exclude it. A is wrong because the subagent did implement retry logic (two retries) and properly returned a structured error — it behaved correctly; the subagent's behavior is not a failure in this scenario. C is wrong because synthesis agents legitimately produce output shape decisions — the issue isn't that synthesis made a decision, but that the coordinator didn't provide guidance and the synthesis agent defaulted to omission rather than annotation. D is wrong because returning an empty result set instead of a structured error would make the failure invisible — structured errors are preferable to empty results precisely because they carry the context needed for appropriate handling. (source: Agentic and multi-agent workflows)
</details>
