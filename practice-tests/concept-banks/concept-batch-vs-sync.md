# Batch vs Sync API — Question Bank

## Question 1
Your CI pipeline runs nightly security audits on 8,000 code repositories. Each audit is a standalone Claude API call with no dependency on other audit results. The pipeline runs at 2 AM and results are reviewed at 9 AM. Which API approach is optimal?

A) Synchronous API with a thread pool of 50 concurrent workers to maximize throughput
B) Message Batches API to process all 8,000 requests asynchronously with a 50% cost reduction
C) Synchronous API with exponential backoff to handle rate limits automatically
D) Message Batches API with streaming enabled to get results as they complete

<details>
<summary>Answer</summary>

**B)** The workload has all batch-optimal characteristics: high volume, independent requests, no real-time requirement, and a 7-hour window before results are needed. The Batches API delivers 50% cost savings and higher throughput for exactly this pattern. A is wrong because synchronous concurrent calls forgo the 50% discount and add infrastructure complexity without any latency benefit when results aren't needed until morning. C is wrong because synchronous processing with backoff still pays full price and introduces rate-limit management burden the Batches API handles automatically. D is wrong because streaming is not supported for batch requests — it is a documented incompatibility of the Batches API. (source: Message batches)

</details>

---

## Question 2
A developer builds a code review tool that runs in a pre-merge GitHub Actions workflow. When a developer pushes a commit, the workflow calls the Claude API to analyze the diff and must post a blocking status check before the PR can be merged. The developer is considering switching to the Batches API to reduce costs. What is the critical reason this switch is not appropriate?

A) The Batches API does not support code analysis tasks
B) The Batches API requires a minimum of 100 requests, which a single PR diff does not satisfy
C) GitHub Actions does not support polling-based workflows required by the Batches API
D) The Batches API processes asynchronously and can take up to 24 hours, making it incompatible with a blocking pre-merge gate that developers are waiting on

<details>
<summary>Answer</summary>

**D)** The Batches API is explicitly designed for latency-tolerant workloads. A pre-merge gate that blocks developer merges requires an immediate response — waiting up to 24 hours would halt all development. The synchronous API is the correct choice for any workflow where a human is waiting for the result. A is wrong because the Batches API supports all request types available in the Messages API, including code analysis. B is wrong because the Batches API has no minimum request count — it accepts a single request up to 100,000 requests per batch. C is wrong because polling is a standard pattern in CI systems and GitHub Actions supports it natively. (source: Message batches)

</details>

---

## Question 3
Your platform processes customer feedback submissions. For each submission you need Claude to: (1) classify the sentiment, (2) based on that classification, decide whether to escalate, and (3) if escalating, generate a draft response tailored to the sentiment. Steps 2 and 3 depend on the output of step 1. Which API strategy is correct?

A) Use the synchronous API for all three steps because the chain of dependent calls requires each step's output to feed into the next
B) Use the Batches API for all three steps since they can be submitted together in one batch
C) Use the Batches API for steps 1 and 3, and synchronous API for step 2 only
D) Use the Batches API for step 1 across all submissions, then make synchronous calls for steps 2 and 3

<details>
<summary>Answer</summary>

**A)** Chained dependent calls are fundamentally incompatible with the Batches API. Each request in a batch is processed independently with no mechanism to pass results between steps within a single logical workflow. Steps 2 and 3 require the output of prior steps, which requires synchronous execution where each response is available before the next call is made. B is wrong because the Batches API cannot wire outputs of one request as inputs to another within the same batch — each request is entirely independent. C is wrong because step 3 also depends on step 2's output, making asynchronous processing of step 3 impossible without first completing step 2 synchronously. D is wrong because even if step 1 runs as a batch, the results still need to feed into steps 2 and 3 sequentially for each submission, making a batched step 1 add complexity without enabling the dependent steps. (source: Message batches)

</details>

---

## Question 4
A team is running large-scale evaluations of a new prompt template against 50,000 test cases. Each evaluation is a single Claude API call comparing the model's output to a reference answer. The team wants to minimize cost. One engineer suggests using the synchronous API with aggressive parallelism. Another proposes the Batches API. What is the decisive factor favoring the Batches API?

A) The Batches API can process more than 50,000 requests in a single batch submission
B) The Batches API guarantees results within 1 hour for batches of this size
C) The Batches API provides a documented 50% cost reduction on all usage compared to standard API prices
D) The Batches API eliminates the need for custom retry logic on individual request failures

<details>
<summary>Answer</summary>

**C)** The 50% cost reduction is the documented, concrete financial advantage of the Batches API for exactly this type of high-volume, latency-tolerant evaluation workload. At 50,000 requests, this is a substantial savings. A is wrong because a single Message Batch is limited to 100,000 requests or 256 MB, whichever comes first — 50,000 is within range but the batch limit is not the deciding factor for the comparison. B is wrong because the Batches API documentation states most batches finish within 1 hour but explicitly does not guarantee it — processing can take up to 24 hours. D is wrong because while the Batches API does isolate per-request failures, the synchronous API with retry logic also handles errors — this is not the decisive differentiator. (source: Message batches)

</details>

---

## Question 5
An engineer wants to use the Batches API for an agentic pipeline that performs web research. The pipeline submits a research question, receives an answer, calls a `search_web` tool to gather more data, feeds the search results back to Claude, and iterates until sufficient evidence is collected. Why is this incompatible with the Batches API?

A) Web search tools exceed the Batches API's per-request token limit
B) The Batches API uses a fire-and-forget model — there is no mechanism to intercept a tool call mid-request, execute the tool externally, and return results to continue the same logical interaction
C) The Batches API does not accept requests with tool definitions
D) The Batches API does not support multi-turn conversations in a single request

<details>
<summary>Answer</summary>

**B)** The Batches API's asynchronous fire-and-forget architecture means each request completes in isolation. An agentic tool loop requires the model to pause at a tool call, have the tool executed externally, receive the result, and continue reasoning — this iterative interception is structurally impossible in the batch model. A is wrong because token limits apply uniformly and are not specific to web search tools or incompatible with the Batches API. C is wrong because the Batches API supports tool definitions and tool use within a single batch request — the limitation is iterative multi-turn tool loops, not the presence of tools. D is wrong because the Batches API does support multi-turn conversations passed in the `messages` parameter — what it cannot do is extend a conversation mid-processing via external tool results. (source: Message batches)

</details>

---

## Question 6
You are designing a content moderation system for a social media platform. New posts arrive continuously and must be reviewed within 2 seconds to prevent harmful content from being visible to users. Your initial design submits each post to the Batches API. A colleague flags this as wrong. What is the correct reason?

A) The Batches API is asynchronous and cannot guarantee sub-second or even sub-hour response times, making it incompatible with a 2-second SLA for real-time moderation
B) Content moderation is a use case the Batches API explicitly excludes from its terms of service
C) The Batches API cannot handle the volume of social media posts efficiently due to its 100,000-request batch limit
D) The Batches API does not support the text classification task type required for moderation

<details>
<summary>Answer</summary>

**A)** The Batches API is designed for latency-tolerant workloads. Its documentation states batches can take up to 24 hours and provides no guaranteed SLA for completion time. A 2-second requirement demands synchronous API calls with immediate responses. B is wrong because content moderation is explicitly listed as a valid Batches API use case — it is appropriate when moderation is asynchronous (e.g., post-publication review), just not for real-time blocking moderation. C is wrong because 100,000 requests per batch is a high-capacity limit that would handle most moderation volumes — the limitation is latency, not capacity. D is wrong because text classification is fully supported by the Batches API, which accepts any Messages API request type. (source: Message batches)

</details>

---

## Question 7
A streaming use case requires real-time token-by-token output from Claude to power a live typing indicator in a user-facing chat interface. A cost-conscious developer proposes routing these requests through the Batches API to take advantage of the 50% discount. What is the problem?

A) The Batches API requires a minimum batch size of 10 requests before processing begins
B) Streaming requests require a different API key scope than the Batches API accepts
C) Streaming is explicitly not supported for batch requests — the Batches API cannot return incremental token output
D) The Batches API does not support models capable of streaming

<details>
<summary>Answer</summary>

**C)** The Anthropic documentation explicitly states streaming is not supported for batch requests. The Batches API returns complete responses only, making it structurally incompatible with streaming use cases that require incremental token delivery. A is wrong because the Batches API has no minimum batch size requirement and will process a batch with a single request. B is wrong because the Batches API uses standard API keys — there is no special scope distinction for streaming versus batch requests. D is wrong because the Batches API supports all active Claude models — model support is not the constraint. (source: Message batches)

</details>

---

## Question 8
After submitting a Message Batch containing 5,000 requests, your application needs to retrieve results. Which is the correct retrieval pattern?

A) Stream results using server-sent events on the same connection used to create the batch
B) Results are returned inline in the response to the POST /v1/messages/batches request once all requests complete
C) Subscribe to a webhook URL registered at batch creation time to receive results as they become available
D) Poll the batch status endpoint to check processing state, then fetch results from the separate results endpoint when the batch shows a completed status

<details>
<summary>Answer</summary>

**D)** The Batches API is asynchronous. After submission, you poll the batch status endpoint to monitor processing. When all requests have completed, results are retrieved via a separate results endpoint — they are not returned inline in the creation response. A is wrong because server-sent events and streaming are explicitly not supported for batch requests; the connection used to create the batch does not stay open for result delivery. B is wrong because the batch creation response returns only the batch object (ID, status, counts) — results are never returned inline in the creation call. C is wrong because the Batches API does not support webhooks — there is no documented mechanism to register a callback URL for result delivery. (source: Message batches)

</details>

---

## Question 9
You submit a Message Batch with 1,000 requests and assign each request a `custom_id`. Results come back in a different order than the requests were submitted. How should you match each result to its original request?

A) Re-sort results by `created_at` timestamp, which corresponds to submission order
B) Use the `custom_id` field in each result object to match it back to the original request with the same `custom_id`
C) Results are always returned in submission order, so array index position corresponds to submission order
D) Use the numeric sequence embedded in the batch's result `id` field, which mirrors submission order

<details>
<summary>Answer</summary>

**B)** The `custom_id` is specifically designed for result matching. Since batch results are not guaranteed to arrive in submission order, each result carries the `custom_id` assigned at request time to enable reliable correlation. The docs explicitly note that order is not guaranteed and recommend meaningful `custom_id` values. A is wrong because `created_at` timestamps reflect when the batch was created, not individual request processing order, and sorting by them does not reliably recover submission order. C is wrong because the documentation explicitly states order is not guaranteed — results can arrive in any order depending on processing. D is wrong because the batch result `id` field is the unique identifier of the result object itself, not a sequential mirror of submission order. (source: Message batches)

</details>

---

## Question 10
Your team submits a batch of 10,000 document summarization requests. After 26 hours, you check the batch and find its status is `expired` with only 7,400 requests completed. What does this mean and what is the correct handling?

A) The batch errored due to a service outage — all 10,000 requests need to be resubmitted in a new batch
B) The 2,600 incomplete requests were automatically moved to a retry queue and will complete within 48 hours
C) Expired status means the batch is still processing but has exceeded the expected SLA — wait another 24 hours for it to complete
D) The batch exceeded the 24-hour processing window and expired. The 7,400 completed results are available; the remaining 2,600 requests must be resubmitted in a new batch

<details>
<summary>Answer</summary>

**D)** Batches expire after 24 hours if processing has not completed. Results for completed requests within the expired batch are still available for 29 days from batch creation. Incomplete requests get an `expired` result status and must be collected and resubmitted in a new batch. A is wrong because this is not a service outage — the 7,400 completed results are available and should not be discarded by resubmitting all 10,000. B is wrong because there is no automatic retry queue for expired requests — the caller is responsible for identifying incomplete requests and resubmitting them. C is wrong because `expired` is a terminal state, not an in-progress one — the batch will not continue processing. (source: Message batches)

</details>

---

## Question 11
A Message Batch containing 500 requests is in progress. Request #247 encounters an API error due to invalid parameters in its `params` object. What happens to the other 499 requests?

A) The entire batch is paused and marked `failed` until the error is corrected and the batch resubmitted
B) The batch is automatically retried from request #247 onward after a 5-minute delay
C) The other 499 requests continue processing independently — individual request failures do not abort the batch
D) Requests after #247 in submission order are skipped; requests before it continue normally

<details>
<summary>Answer</summary>

**C)** The documentation explicitly states that the failure of one request in a batch does not affect the processing of other requests. Each request is independent. The failed request receives an `errored` result status, and all other requests proceed to completion. A is wrong because batch-level failure on a single request error would make the Batches API impractical for large workloads — this is explicitly not how it behaves. B is wrong because the Batches API does not perform automatic per-request retries — the caller must inspect result statuses and resubmit failed requests as needed. D is wrong because requests are not processed in strict submission order and there is no positional dependency between requests in a batch. (source: Message batches)

</details>

---

## Question 12
After a Message Batch completes, you retrieve results and find that 23 requests have a result type of `errored`. The rest succeeded. What is the correct approach?

A) Resubmit the entire batch since partial results may be inconsistent with complete results
B) Retry the entire batch immediately since transient errors may have caused the failures
C) Treat the 23 failed requests' results as empty and continue processing with only successful results
D) Inspect the error details in each `errored` result, then create a new batch containing only those 23 requests after fixing any parameter issues

<details>
<summary>Answer</summary>

**D)** Each result object contains error information for `errored` results. The correct pattern is to inspect the error, fix any parameter issues identified, then resubmit only the failed requests — not the entire batch — since the other 477 requests already completed successfully. A is wrong because successful results are independent and valid; discarding them wastes cost and time. B is wrong because retrying the entire 500-request batch to fix 23 failures wastes resources and incurs unnecessary cost for the 477 already-completed requests. C is wrong because silently treating errors as empty results produces incorrect downstream behavior and hides failures that may need to be addressed. (source: Message batches)

</details>

---

## Question 13
A batch of 2,000 requests is submitted. When you retrieve results, you find requests with result types: `succeeded`, `errored`, `canceled`, and `expired`. You need to build a reconciliation report. Which statement about these statuses is correct?

A) `succeeded` results contain a full message response; `errored` results contain error details; `canceled` results occur if the batch was explicitly canceled; `expired` results occur when individual requests did not complete before the 24-hour batch window closed
B) `canceled` and `expired` requests have the same underlying cause — they both indicate the batch ran out of time
C) `errored` results automatically retry within the same batch for up to 3 attempts before finalizing
D) All non-`succeeded` results must be treated as data loss — no information is retrievable from them

<details>
<summary>Answer</summary>

**A)** Each result type has a distinct meaning: `succeeded` contains the full model response; `errored` contains structured error information about what went wrong; `canceled` occurs when the batch was explicitly canceled by the caller; `expired` occurs when individual requests did not complete before the 24-hour window. Understanding these distinctions is required to build correct reconciliation logic. B is wrong because `canceled` and `expired` have different causes — `canceled` is triggered by an explicit API call to cancel the batch, while `expired` is a time-limit consequence. C is wrong because the Batches API does not implement automatic per-request retries — `errored` requests remain errored and must be resubmitted by the caller. D is wrong because `errored` results contain error detail information that is retrievable and useful for debugging and resubmission decisions. (source: Message batches)

</details>

---

## Question 14
Your product has two workflows: (A) a user clicks "Analyze" in the UI and waits for a result in real time, and (B) a nightly job that generates weekly analytics reports for 3,000 customers at 1 AM. What is the correct API strategy for each?

A) Synchronous API for A; Message Batches API for B
B) Message Batches API for both — 50% savings apply to both cases
C) Message Batches API for A; Synchronous API for B
D) Synchronous API for both — consistency makes the codebase simpler

<details>
<summary>Answer</summary>

**A)** Workflow A has a human waiting for an immediate result — this requires the synchronous API. Workflow B has no real-time requirement (1 AM run, reports reviewed in the morning) and processes 3,000 independent requests, making it ideal for the Batches API with its 50% cost reduction. B is wrong because Workflow A is user-facing and real-time — the Batches API cannot meet that latency requirement regardless of cost savings. C is wrong because routing real-time user-facing requests through the Batches API would make users wait up to 24 hours for their "Analyze" click result. D is wrong because using synchronous for B forgoes a 50% cost savings on a high-volume, latency-tolerant workload — this is exactly the tradeoff the Batches API is designed to capture. (source: Message batches)

</details>

---

## Question 15
A team has an AI pipeline with three stages: Stage 1 generates product descriptions for 10,000 SKUs (independent, runs overnight). Stage 2 immediately uses those descriptions to answer live customer chat questions (real-time, dependent on Stage 1 outputs). Stage 3 runs a weekly quality audit on all Stage 1 outputs (independent, non-blocking). Which API mix is correct?

A) Sync for Stage 1, Batch for Stage 2, Sync for Stage 3
B) Batch for all three stages — all involve large volumes
C) Sync for Stage 1, Sync for Stage 2, Batch for Stage 3
D) Batch for Stage 1, Sync for Stage 2, Batch for Stage 3

<details>
<summary>Answer</summary>

**D)** Stage 1 is overnight, high-volume, independent — ideal for Batch (50% savings). Stage 2 is real-time user-facing chat — requires Sync. Stage 3 is a scheduled quality audit with no time pressure — ideal for Batch. A is wrong because swapping Stage 1 to Sync and Stage 2 to Batch inverts the correct decision for both — the overnight precomputation should be batch, not the real-time chat. B is wrong because Stage 2 requires real-time responses for active customer conversations — the Batches API cannot meet this requirement. C is wrong because Stage 1 is overnight, independent, and high-volume — using sync here forgoes significant cost savings. (source: Message batches)

</details>

---

## Question 16
Your pipeline first uses the Batches API to classify 50,000 documents into categories, then needs to route each document to a different downstream processor based on its classification. The routing logic requires reading each batch result as it becomes available. What is the limitation you must design around?

A) Batch results expire immediately after first read and cannot be accessed again
B) The Batches API charges an additional retrieval fee per result accessed
C) Batch results cannot be read until all 50,000 requests in the batch have completed
D) Batch results are delivered in submission order, requiring re-sorting before routing

<details>
<summary>Answer</summary>

**C)** Batch results become available for download only after all requests in the batch have completed (or after 24 hours, whichever comes first). You cannot stream individual results as they finish — the entire batch must reach a terminal state. A is wrong because batch results are retained for 29 days after creation — they can be accessed multiple times within that window. B is wrong because there is no additional retrieval fee; results are included in the standard Batches API pricing. D is wrong because results are explicitly not guaranteed to be in submission order — `custom_id` is the matching mechanism, not positional order. (source: Message batches)

</details>

---

## Question 17
A batch pipeline for generating legal document summaries needs to ensure that if the batch processing API goes down temporarily, the work is not lost. What is the correct retention window to design around?

A) Batch results must be retrieved within 1 hour of batch completion or they are deleted
B) Batch results persist indefinitely and are only removed when explicitly deleted
C) Batch results are available for 7 days after the batch processing ends
D) Batch results are available for 29 days after batch creation, providing ample time for retrieval

<details>
<summary>Answer</summary>

**D)** The Batches API retains results for 29 days after batch creation (not after processing completion). This provides a substantial buffer for systems with retry logic or delayed processing. A is wrong because the 1-hour window does not exist — this would make batch results impractical for many asynchronous workflows. B is wrong because results do not persist indefinitely — after 29 days from creation, results are no longer available for download (though the batch itself remains viewable). C is wrong because the 7-day window is incorrect — the documented retention is 29 days, and it is measured from batch creation, not from when processing ended. (source: Message batches)

</details>

---

## Question 18
You are architecting a multi-stage analysis pipeline: Stage A uses the Batches API to run 20,000 independent document analyses overnight. The results must feed into Stage B, which runs a synchronous summarization across all Stage A outputs during a 9 AM executive briefing. How should you architect the Stage A to Stage B handoff?

A) Configure Stage A to push results directly into Stage B via the Batches API webhook callback
B) After Stage A batch completes, retrieve all results, then feed the aggregated outputs as context into Stage B's synchronous API calls
C) Run Stage B inside the same batch as Stage A by chaining requests with dependency references
D) Use streaming on Stage A's batch to pipe outputs directly into Stage B as they complete

<details>
<summary>Answer</summary>

**B)** The correct handoff pattern is: wait for Stage A batch to reach completed status, retrieve all results via the results endpoint, then use those results as inputs to Stage B's synchronous calls. This is the standard mix-and-match architecture. A is wrong because the Batches API does not support webhooks — there is no push mechanism for result delivery. C is wrong because batch requests cannot reference each other's outputs within the same batch — all requests are processed independently with no inter-request dependencies. D is wrong because streaming is explicitly not supported in the Batches API — batch results cannot be piped as they complete. (source: Message batches)

</details>

---

## Question 19
An engineer proposes this architecture: submit 1,000 independent translation tasks to the Batches API, then poll every 5 minutes until the batch status is `ended`, then download results. A senior architect reviews it and says one aspect is suboptimal. What is the issue?

A) The architecture is correct — polling every 5 minutes with the right terminal status check is the documented retrieval pattern
B) Results should be retrieved during batch processing, not after it completes, to reduce latency
C) The batch status `ended` does not exist — the correct terminal status name should be verified against the API documentation before implementation
D) Polling every 5 minutes is too frequent and will exceed API rate limits for status checks

<details>
<summary>Answer</summary>

**C)** The specific status field names must be verified against the API documentation. Using an incorrect status string (e.g., `ended` vs. the actual documented terminal status) means the polling loop never terminates or terminates incorrectly. The architecture pattern (submit → poll status → retrieve results) is correct, but exact field values must match the API spec. A is wrong because status field names are not implementation details that can be assumed — exact values must be verified. B is wrong because results are only accessible after the batch reaches a terminal state — there is no mechanism to retrieve partial results during processing. D is wrong because polling every 5 minutes for a batch that takes up to 24 hours is not a high-frequency pattern — status check endpoints are not subject to restrictive rate limits that would be triggered by this interval. (source: Message batches)

</details>

---

## Question 20
You have a batch of 500 requests. After retrieval, you discover 30 requests failed with `errored` status. You build a reconciliation script that resubmits them. What `custom_id` values should the resubmitted requests use?

A) New unique `custom_id` values, since the original IDs are now consumed and cannot be reused
B) Incrementing numeric IDs starting from 501 to avoid collision with the original 500
C) The same `custom_id` values as the original failed requests, since you will look up results by `custom_id` in your database
D) The batch's ID prefixed to the original `custom_id` to create a globally unique identifier

<details>
<summary>Answer</summary>

**C)** `custom_id` values are only scoped to a single batch and are not globally consumed. Reusing the same `custom_id` values in a new batch allows your reconciliation system to use consistent identifiers when updating results in your database. A is wrong because `custom_id` values are not globally unique identifiers — the same value can be reused in a different batch without conflict. B is wrong because there is no sequential collision risk between batches — each batch is independent, and `custom_id` uniqueness is only required within a single batch submission. D is wrong because prefixing adds unnecessary complexity — the `custom_id` only needs to be unique within a single batch, and using the same identifiers across batches is intentionally supported for reconciliation workflows. (source: Message batches)

</details>

---

## Question 21
A CI/CD pipeline runs `claude` CLI commands inside a GitHub Actions workflow. The pipeline hangs indefinitely during execution, waiting for user input that never comes because the workflow runs unattended. What is the fix?

A) Set the environment variable `CLAUDE_HEADLESS=true` before running the command
B) Add the `--batch` flag to switch Claude CLI into CI-compatible batch processing mode
C) Redirect stdin from `/dev/null` to suppress input waiting: `claude < /dev/null`
D) Use the `-p` flag (print mode) to run Claude in non-interactive mode: `claude -p "your prompt here"`

<details>
<summary>Answer</summary>

**D)** The `-p` / `--print` flag is the documented non-interactive mode for Claude Code. It processes the prompt, writes output to stdout, and exits without waiting for interactive input — exactly what a CI/CD pipeline requires. A is wrong because `CLAUDE_HEADLESS=true` is not a documented Claude Code environment variable — it does not exist in the CLI documentation and would have no effect. B is wrong because `--batch` is not a valid Claude Code CLI flag — the non-interactive mode is controlled by `-p` / `--print`. C is wrong because redirecting stdin from `/dev/null` may not prevent all interactive prompts that Claude Code might generate, and it is not the designed mechanism for CI mode. (source: Claude Code settings)

</details>

---

## Question 22
A DevOps engineer wants Claude Code to produce structured JSON output in a CI pipeline so downstream scripts can parse the findings without regex. The engineer writes a detailed prose prompt asking Claude to "please respond in JSON format." During testing, Claude occasionally responds in prose instead. What is the correct approach?

A) Use the `--output-format json` flag to enforce structured JSON output at the CLI level
B) Add more examples of the desired JSON format in the prompt to make the instruction clearer
C) Add a post-processing step that uses `jq` to extract JSON from Claude's prose response
D) Run Claude twice and compare both outputs to ensure JSON consistency

<details>
<summary>Answer</summary>

**A)** `--output-format json` is a CLI-level enforcement mechanism that guarantees well-formed JSON output regardless of prompt phrasing. Prompt instructions are probabilistic — they can produce prose even when JSON is requested. CLI-level flags enforce the format deterministically. B is wrong because more examples in the prompt still rely on probabilistic compliance — the model may still deviate under varied inputs, which is the exact problem being described. C is wrong because extracting JSON from prose with `jq` is fragile and fails when Claude produces prose that contains no parseable JSON structure. D is wrong because running Claude twice and comparing outputs does not fix the format inconsistency — it only detects it after the fact without resolving it. (source: Claude Code settings)

</details>

---

## Question 23
A CI pipeline uses `claude -p "review this PR diff for security issues" --output-format json`. The downstream GitHub Actions step fails because the JSON output does not contain the required fields (`severity`, `location`, `description`) expected by the GitHub API integration. What additional flag addresses this?

A) `--validate-json` to enable runtime validation against expected fields
B) `--required-fields severity,location,description` to specify mandatory output fields
C) `--json-schema path/to/schema.json` to provide a JSON schema that Claude must conform to in its output
D) `--output-template` to provide a template JSON structure Claude fills in

<details>
<summary>Answer</summary>

**C)** The `--json-schema` flag accepts a path to a JSON schema file and constrains Claude's output to conform to that schema, ensuring required fields are present and correctly typed. Combined with `--output-format json`, this provides full structural enforcement for CI integration. A is wrong because `--validate-json` is not a documented Claude Code CLI flag. B is wrong because `--required-fields` is not a documented flag — field requirements are expressed through JSON schema, not a comma-separated list. D is wrong because `--output-template` is not a documented Claude Code CLI flag — schema-based enforcement is the correct mechanism. (source: Claude Code settings)

</details>

---

## Question 24
A team runs Claude Code in CI using `claude -p "analyze tests" --output-format json`. During a deployment pipeline, the command exits with a non-zero status code even though Claude returned valid JSON analysis. The pipeline treats any non-zero exit as a failure. What should the team verify?

A) Whether `--output-format json` requires an additional `--exit-zero` flag to suppress error codes
B) Whether Claude identified actual issues in the analysis — Claude Code may exit non-zero to signal that actionable findings were detected, separate from execution errors
C) Whether the `-p` flag is compatible with `--output-format json` in the current CLI version
D) Whether the JSON output needs to be explicitly acknowledged via a `--confirm` flag before the process exits cleanly

<details>
<summary>Answer</summary>

**B)** Claude Code's exit codes convey meaningful information. A non-zero exit may indicate Claude detected issues worth flagging, not just execution failures. Teams integrating Claude into CI pipelines must understand exit code semantics and handle them appropriately — distinguishing between "Claude errored" and "Claude found problems." A is wrong because `--exit-zero` is not a documented flag and exit code behavior is not toggled this way. C is wrong because `-p` and `--output-format json` are independently documented flags that work together — compatibility is not the issue. D is wrong because `--confirm` is not a documented Claude Code flag and exit behavior is not acknowledgment-dependent. (source: Claude Code settings)

</details>

---

## Question 25
A pipeline architect wants to use Claude Code in a CI workflow where each PR triggers analysis. The architect wants to pass the PR diff as a file input rather than inline in the prompt string. Which invocation pattern is correct for non-interactive CI mode?

A) `claude -p "$(cat diff.txt)" --output-format json` or pipe the file content as stdin with the `-p` flag
B) `claude -p "analyze this diff" --context-file diff.txt --output-format json`
C) `CLAUDE_INPUT=diff.txt claude -p "analyze the provided input" --output-format json`
D) `claude --batch --input-file diff.txt "analyze this diff"`

<details>
<summary>Answer</summary>

**A)** In non-interactive mode with `-p`, the prompt can be constructed by shell command substitution (`$(cat diff.txt)`) to embed file contents inline, or the file can be piped as stdin. This is the standard Unix pattern for feeding file content to CLI tools in CI environments. B is wrong because `--context-file` is not a documented Claude Code CLI flag for providing additional file context. C is wrong because `CLAUDE_INPUT` is not a documented environment variable for Claude Code — file input is handled through prompt construction or stdin. D is wrong because `--batch` and `--input-file` are not documented Claude Code CLI flags — the correct non-interactive flag is `-p`. (source: Claude Code settings)

</details>

---

## Question 26
A security team wants to run Claude Code weekly to audit all Python files in a repository for known vulnerability patterns. The audit does not need to block any development workflow and results are reviewed in a weekly meeting. There are approximately 2,000 files. Should the team use Claude Code CLI with `-p` or the Message Batches API directly, and why?

A) Claude Code CLI with `-p` — CLI tools always outperform direct API calls for code analysis
B) Message Batches API directly — the Claude Code CLI does not support processing multiple files in a single invocation
C) Message Batches API directly — for 2,000 independent files with no real-time requirement, the Batches API provides 50% cost savings and handles high-volume independent requests optimally
D) Claude Code CLI with `-p` — the `-p` flag enables batch processing mode that sends all files to the Batches API automatically

<details>
<summary>Answer</summary>

**C)** The Message Batches API is the correct choice for this workload: 2,000 independent file analyses, no real-time requirement, weekly cadence. It provides 50% cost savings and handles concurrent processing efficiently. A is wrong because "CLI always outperforms direct API" is not a documented principle — the correct tool depends on workload characteristics, and this workload clearly fits batch criteria. B is wrong because the Claude Code CLI can process multiple files through shell scripting — that is not the reason to prefer the Batches API; the reason is cost and throughput optimization. D is wrong because `-p` is the non-interactive print mode flag — it does not enable batch processing or route requests through the Message Batches API. (source: Message batches)

</details>

---

## Question 27
A developer runs `claude -p "summarize this document"` in a CI pipeline and gets back unstructured prose. The downstream step expects a JSON object with keys `title`, `summary`, and `key_points`. Which combination of flags produces schema-validated JSON output?

A) `claude -p "summarize this document" --structured-output summary.json`
B) `claude -p "summarize this document" --json --required title,summary,key_points`
C) `claude -p "summarize this document" --format structured --schema summary.json`
D) `claude -p "summarize this document" --output-format json --json-schema summary.json`

<details>
<summary>Answer</summary>

**D)** The correct combination is `--output-format json` (enforce JSON format) plus `--json-schema path` (constrain output to a specific schema). Together these flags guarantee structured, schema-validated output suitable for pipeline consumption. A is wrong because `--structured-output` is not a documented Claude Code CLI flag. B is wrong because `--json` (without `output-format`) and `--required` are not documented flags in the Claude Code CLI. C is wrong because `--format structured` and `--schema` are not documented Claude Code CLI flags. (source: Claude Code settings)

</details>

---

## Question 28
A team is evaluating the Batches API for a new use case: a customer chatbot that needs to handle 500 simultaneous users, each in a multi-turn conversation that may involve tool calls to retrieve account data. Each turn requires a response within 3 seconds. Is the Batches API appropriate?

A) Yes — tool calls are supported in the Batches API, so multi-turn tool conversations are compatible
B) No — the Batches API only supports up to 100 simultaneous requests, making 500 users exceed its capacity
C) No — the Batches API is incompatible with this use case because it cannot meet 3-second latency requirements and cannot support multi-turn tool loops within a single batch request
D) Yes — 500 simultaneous requests is exactly the high-volume scenario the Batches API is designed for

<details>
<summary>Answer</summary>

**C)** This use case fails on two separate batch incompatibility criteria. First, the 3-second latency requirement is impossible with the Batches API, which can take up to 24 hours. Second, multi-turn tool loops where each turn feeds the previous tool result back into the model require iterative synchronous calls — the fire-and-forget batch model cannot support this interaction pattern. A is wrong because while tool definitions are accepted in batch requests, an iterative multi-turn tool calling loop requires results to be fed back mid-conversation, which the async batch model cannot support. B is wrong because the Batches API supports up to 100,000 requests per batch — 500 users is far within its capacity limits. D is wrong because high volume alone does not make a workload batch-appropriate — latency and interaction pattern requirements disqualify this use case entirely. (source: Message batches)

</details>

---

## Question 29
A platform engineer is designing a hybrid pipeline. Step 1: Use the Batches API to pre-compute embeddings and initial analyses for 10,000 documents (overnight). Step 2: The next morning, a user queries the system and expects a synthesized answer in under 2 seconds, drawing on the pre-computed analyses. Step 3: The answer is logged and a quality evaluation batch runs nightly. What is the API profile for each step?

A) Sync, Sync, Batch
B) Batch, Sync, Batch
C) Batch, Batch, Sync
D) Sync, Batch, Sync

<details>
<summary>Answer</summary>

**B)** Step 1 is a high-volume overnight computation with no real-time requirement — Batch API with 50% savings. Step 2 is a user query with a 2-second SLA — must be Sync. Step 3 is a nightly quality audit, independent, latency-tolerant — Batch API with 50% savings. A is wrong because Step 1 is overnight, independent, and high-volume — using sync here forgoes substantial cost savings with no benefit. C is wrong because Step 2 has a user-facing 2-second latency requirement — routing it through the Batches API would make users wait hours for a response. D is wrong because swapping Step 1 to Sync and Step 2 to Batch is precisely the wrong assignment — the overnight precomputation should be batch, not the real-time user query. (source: Message batches)

</details>

---

## Question 30
A CI pipeline uses: `claude -p "$(cat pr_diff.txt)" --output-format json --json-schema findings.json`. During a run, the schema validation fails because Claude produced a JSON array at the top level, but `findings.json` specifies an object with a `findings` array property. The team wants to fix this without changing the schema file. What is the correct fix?

A) Switch from `--json-schema` to `--json-template` to provide a fill-in template instead of a validation schema
B) Update the prompt to explicitly describe the expected JSON object structure, matching the schema's top-level shape
C) Add `--wrap-array findings` flag to tell the Claude CLI to wrap array output in the required object structure
D) Disable `--output-format json` and handle the wrapping in a post-processing jq command

<details>
<summary>Answer</summary>

**B)** When schema validation fails due to structural mismatch, the prompt should describe the expected output structure. The schema enforces the structure, but Claude generates based on the prompt — if the prompt does not specify the expected object shape, Claude may default to an array. Aligning the prompt description with the schema's top-level expectation is the direct fix. A is wrong because `--json-template` is not a documented Claude Code CLI flag. C is wrong because `--wrap-array` is not a documented Claude Code CLI flag. D is wrong because disabling `--output-format json` and using post-processing introduces the same fragility the schema was meant to eliminate — plus it requires modifying the pipeline architecture rather than fixing the root cause. (source: Claude Code settings)

</details>

---
