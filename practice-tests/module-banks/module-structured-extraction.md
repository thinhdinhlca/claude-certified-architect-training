# Module Bank: Structured Data Extraction

Auto-generated bank with 30 questions.

## Question 1
You are building a pipeline to extract structured data from job postings. The `employment_type` field should always be one of: `"full_time"`, `"part_time"`, `"contract"`, `"internship"`. Many postings use phrases like "temp-to-hire," "freelance," and "casual." Your strict enum rejects 18% of valid postings at the validation gate. What is the best schema design fix?

A) Replace the enum with a free-text `employment_type` string and normalize values offline in a weekly batch job that clusters similar strings together.
B) Add every known synonym as a distinct enum value, including "temp-to-hire," "freelance," "casual," and all future variants you can anticipate.
C) Extend the enum with an `"other"` value and add a companion `employment_type_raw` string field that captures the exact source phrase, preserving both structured classification and original language.
D) Add a prompt instruction listing each synonym mapping: "freelance maps to contract, temp-to-hire maps to contract" for every variant observed in the dataset.

<details><summary>Answer</summary>
**C)** The `"other"` + raw field pattern keeps controlled vocabulary for downstream analytics while preserving unrecognized source terms for prompt refinement and human review. A) loses real-time structured classification. B) synonym explosion creates enum maintenance debt and treats equivalent concepts as distinct categories. D) prompt synonym lists grow linearly with vocabulary, miss novel variants, and are less reliable than schema-level design. (source: Schema design, Enum constraints)
</details>

## Question 2
You are extracting financial data from quarterly earnings reports. The schema has `revenue`, `operating_income`, and `net_income` fields. During validation you discover that in 6% of documents `net_income` is greater than `operating_income`, violating standard accounting relationships. Both values are faithfully extracted from the source document. What should your validation layer do?

A) Auto-correct `net_income` to be the smaller of the two values, since this accounting relationship is a universal constraint that overrides whatever the document states.
B) Fail the document and discard the extraction, since violating a fundamental accounting identity signals the model produced fabricated values.
C) Add a `financial_anomaly` flag alongside both extracted values, preserving accurate extraction while signaling to downstream reviewers that the source document may contain a restatement or non-standard line item.
D) Swap `net_income` and `operating_income` values and log a correction, since transposition is the most common cause of this relationship violation in extraction pipelines.

<details><summary>Answer</summary>
**C)** When validly extracted values violate a business rule, the violation may exist in the source document itself — restatements, non-GAAP metrics, one-time items. Preserving both values and flagging the anomaly gives reviewers accurate data to investigate. A) overwrites faithful extraction with an assumption. B) discards accurate data without confirming a model error. D) swapping without evidence introduces errors where the document was correctly extracted. (source: Validation and retry logic, Conflicting signals)
</details>

## Question 3
You are normalizing product catalog data extracted from 15 supplier spreadsheets, each using different column naming conventions. The target schema has a `unit_of_measure` enum: `"each"`, `"kg"`, `"liter"`, `"meter"`, `"box"`. Supplier A uses `"pc"`, Supplier B uses `"piece"`, and Supplier C uses `"unit"` — all meaning `"each"`. These appear as validation failures. What is the most maintainable fix?

A) Train the prompt with supplier-specific few-shot examples for each of the 15 suppliers, demonstrating the correct enum mapping for each supplier's terminology.
B) Create a separate extraction schema for each supplier with supplier-specific enum values, then transform to the canonical schema in a downstream ETL step.
C) Accept free-text in `unit_of_measure` at extraction time and run a nightly scheduled job that maps raw strings to canonical enum values using fuzzy string matching.
D) Add a post-extraction normalization map (`"pc" → "each"`, `"piece" → "each"`, `"unit" → "each"`) applied before schema validation, and log unmapped values as new variants requiring human review.

<details><summary>Answer</summary>
**D)** A normalization map applied before validation is explicit, auditable, and maintainable — new variants require only an entry in the map. It cleanly separates extraction (getting the text) from normalization (mapping to canonical form). A) multiplies prompt complexity linearly with suppliers. B) requires maintaining 15 schemas and 15 ETL transforms. C) delays normalization and fuzzy matching produces ambiguous results for novel variants. (source: Post-processing, Multi-document extraction)
</details>

## Question 4
You are extracting action items from meeting transcripts. Each action item should have `assignee`, `task`, and `due_date` fields. In long transcripts covering 2–3 hours of discussion, the model consistently misses action items mentioned in the first 30 minutes of the recording, even though those items are clearly stated. What is the most likely cause and fix?

A) The model has a recency bias for final speaker turns; add a prompt instruction "search the entire transcript from beginning to end before identifying action items" to counteract this.
B) Long transcripts cause the model to over-summarize early content; switch to streaming extraction where each speaker turn is processed as it arrives.
C) The first 30 minutes of content sits far from the end of the context window; the model attends less reliably to content in the middle of long contexts, so chunk the transcript by time segment and extract action items per chunk, then merge.
D) Action items in early transcript sections use future-tense constructions the schema's `task` field pattern does not capture; add future-tense variants to the extraction prompt.

<details><summary>Answer</summary>
**C)** The "lost in the middle" effect is well-documented: models attend less reliably to content positioned in the middle of very long contexts. Chunking the transcript by time segment and extracting action items per chunk, then merging and deduplicating results, addresses this reliably. A) adds a prompt instruction that does not overcome attention distribution issues. B) streaming per speaker turn fragments context and breaks multi-speaker action assignments. D) invents a specific linguistic cause that does not explain the early-segment miss pattern. (source: Multi-pass processing, Long document handling)
</details>

## Question 5
You are building a legal citation extractor for appellate court opinions. Each opinion cites 15–80 cases. Your schema has a `citations` array where each item has `case_name`, `reporter`, `volume`, `page`, and `year`. After extraction, 9% of citations have `volume` and `page` transposed: `{"volume": "421", "page": "8 F.3d"}` instead of `{"volume": "8", "page": "421"}`. What validation rule most directly catches this class of error?

A) Add a `pattern` constraint on `volume` enforcing `^\d+$` (digits only) and a `pattern` on `reporter` matching known reporter abbreviation formats, so transposed values fail the format check and trigger targeted re-extraction.
B) Add a `minLength: 3` constraint on `reporter` to reject short strings that might be misclassified volume numbers.
C) Add a cross-field post-validation rule: if `volume` contains a space or letter, flag the record as a transposition candidate.
D) Increase `budget_tokens` for extended thinking so the model deliberates more carefully about field order before populating citation arrays.

<details><summary>Answer</summary>
**A)** Pattern constraints on `volume` (must be digits only) and `reporter` (must match abbreviation formats like `"F.3d"`, `"U.S."`) enforce structural correctness at the schema level. A transposed value like `"8 F.3d"` in `volume` fails the `^\d+$` pattern, triggering a schema validation failure and retry. C) is a reasonable complement but does not prevent the error from initially passing schema validation. B) `minLength` on reporter does not address numeric-string confusion. D) extended thinking reduces upfront errors but does not validate output after generation. (source: Validation and retry logic, Schema design)
</details>

## Question 6
You need to extract all parties, their roles, and effective dates from commercial contracts. Some contracts name 2 parties; others name 12. Your current schema has `party_1` through `party_5` as fixed fields, which fails for contracts with more than 5 parties and wastes schema space for 2-party contracts. What schema redesign best handles variable party count?

A) Keep `party_1` through `party_10` fixed fields as a conservative upper bound, accepting that most fields will be null for simple contracts.
B) Replace fixed fields with a single `parties_text` string containing a pipe-delimited serialized list of parties, parsed by downstream code after extraction.
C) Add an overflow `additional_parties` string field for parties beyond `party_5`, containing concatenated party data in freeform format.
D) Replace fixed party fields with a `parties` array where each item has `party_name`, `role`, and `effective_date`, with no upper bound on array length.

<details><summary>Answer</summary>
**D)** An unbounded array with a typed per-item sub-schema handles 2-party and 12-party contracts with equal fidelity. Each party gets the same structured representation regardless of cardinality. A) wastes schema space and silently truncates contracts with more than 10 parties. B) trades structured extraction for string parsing, losing type guarantees and schema enforcement. C) creates an inconsistent structure where parties 1–5 are typed objects and beyond-5 parties are unstructured strings with no schema enforcement. (source: Schema design, Array cardinality)
</details>

## Question 7
You are extracting structured metadata from scientific papers: `title`, `authors`, `journal`, `publication_year`, `doi`, and `keywords`. For preprints posted on arXiv, `journal` and `doi` are frequently absent. Your retry budget is being exhausted on documents where these fields will never be present. What is the correct first-pass fix?

A) Make `journal` and `doi` optional (nullable) in the schema so the model returns null for genuinely absent fields without triggering a required-field validation failure.
B) Add a document classifier that identifies preprints before extraction and routes them to a reduced schema that omits `journal` and `doi` entirely.
C) Add a prompt instruction: "For preprints, set journal to 'arXiv' and doi to the arXiv identifier if available, otherwise return an empty string."
D) Implement a cascading validation rule: only validate `journal` and `doi` if `publication_year` indicates a peer-reviewed publication era (post-2000).

<details><summary>Answer</summary>
**A)** Making fields nullable is the correct schema design when source documents legitimately lack those fields. Required-field failures for absent data are a schema design error — retries cannot resolve them because the information does not exist. B) adds upstream complexity and requires maintaining two schemas. C) fabricates `journal` values for preprints and encodes extraction logic as fragile prose. D) `publication_year` does not reliably predict whether a paper was published in a journal. (source: Schema design, Missing required fields)
</details>

## Question 8
You are processing email threads to extract structured summaries: `topic`, `decision_reached`, `open_questions`, and `next_steps`. A single thread contains 47 messages spanning 3 weeks. The extraction consistently misses decisions made in messages 10–25, confirmed to be within the context window. What multi-pass strategy addresses this?

A) Run a first pass extracting a one-sentence summary of each message, then a second pass extracting `decision_reached` and `open_questions` from the summaries, where each decision is explicitly stated in normalized form.
B) Process the thread in reverse chronological order so the most recent messages appear at the start of context and anchor extraction through backward references to earlier decisions.
C) Run extraction three times with different random seeds and take the union of all extracted decisions, deduplicating by string similarity.
D) Truncate the thread to the first 15 and last 15 messages, which statistically capture most decisions, and note the truncation in the output metadata.

<details><summary>Answer</summary>
**A)** A two-pass approach where the first pass produces per-message summaries creates a dense, normalized representation of the entire thread. The second pass extracts structured fields from these summaries, where decisions are explicitly stated rather than buried in conversational noise across 47 messages. B) reverse ordering distorts temporal context and breaks causal references to earlier decisions. C) multiple random-seed runs introduce non-determinism without addressing the attention issue. D) truncation discards exactly the middle messages where decisions are known to be missed. (source: Multi-pass processing)
</details>

## Question 9
You are extracting named entities from news articles: people, organizations, and locations. Each entity should have `name`, `type`, and a `confidence` score (0–1 float). You want to route low-confidence entities to a human review queue without modifying the entity value itself. What schema design best supports this?

A) Add a `confidence` property to each entity object alongside `name` and `type`, so each entity carries its own score as a self-contained unit suitable for threshold-based routing.
B) Add a parallel `entity_confidence` array of floats in the same order as `named_entities`, relying on index alignment to pair entities with their scores.
C) Add a root-level `extraction_confidence` float representing the average confidence across all entities for the article.
D) Add an inline annotation syntax to each entity name string: `"Apple Inc. [conf:0.92]"` and parse the score from the string during post-processing.

<details><summary>Answer</summary>
**A)** Embedding `confidence` as a property of each entity object is self-contained and robust: each entity carries its score with no positional alignment dependency. Downstream code can check `entity.confidence < 0.7` and queue that specific entity for review. B) relies on index alignment between parallel arrays — fragile if either array is reordered or truncated during merging. C) averaging destroys per-entity signal and makes targeted entity-level routing impossible. D) encodes structured data in a string requiring fragile parsing and is rejected by standard JSON validators. (source: Confidence and uncertainty, Schema design)
</details>

## Question 10
Your pipeline extracts contract clause data. The `penalty_amount` field is sometimes expressed as a fixed dollar amount ("$50,000") and sometimes as a percentage formula ("2% of monthly contract value"). Downstream code expects a `number` type. The model returns null for formula-based penalties, causing downstream systems to treat them as "no penalty." What schema design preserves both types of penalties?

A) Change `penalty_amount` to a string type and parse numeric values downstream, using `"null"` as the string sentinel for absent penalties.
B) Add a pre-extraction step that evaluates formula-based penalties against an average contract value estimate, converting them to a numeric approximation before populating the field.
C) Split into `penalty_amount_fixed` (nullable number) and `penalty_amount_formula` (nullable string), with a `penalty_type` enum (`"fixed"`, `"formula"`, `"none"`) indicating which field applies.
D) Keep `penalty_amount` as a number and add a `has_formula_penalty` boolean flag so downstream code knows when null means "formula exists" versus "no penalty."

<details><summary>Answer</summary>
**C)** Separating fixed amounts from formula strings into typed fields with a discriminator enum preserves both the structured numeric type and the original formula text while making the distinction explicit. A) degrades type safety across the entire field. B) introduces approximations that may be far from actual values and requires external contract value data. D) a boolean flag preserves intent but loses the formula text itself, making it impossible to evaluate the actual penalty. (source: Schema design, Output constraints)
</details>

## Question 11
You are building a pipeline to extract structured data from vendor RFP responses. Each response is 80–200 pages with sections in inconsistent order. You want to extract 12 specific sections by heading name. The model sometimes extracts content from the wrong section when headings are non-standard. What is the most effective extraction strategy?

A) Add a first pass that identifies and maps all heading locations in the document, then a second pass that uses the heading map as explicit positional context to extract each section's content to the correct schema field.
B) Use keyword search to locate each of the 12 target headings, extract the paragraph following each keyword match, and pass only those paragraphs to the model for field extraction.
C) Add a prompt instruction listing all known heading variants for each section: "Section 3 may also appear as 'Technical Approach', 'Solution Overview', or 'Proposed Methodology'."
D) Extract all 12 sections in parallel with 12 separate API calls, each receiving the full document with a targeted prompt asking for only that section.

<details><summary>Answer</summary>
**A)** A two-pass approach where the first pass builds an explicit heading map creates a structural index of the document. The second pass uses this map to anchor section extraction to specific positions, preventing content spillover from an adjacent section with a similar heading. B) keyword search is fragile for non-standard headings, which is the stated problem. C) a synonym list grows without bound and misses novel variants encountered in the wild. D) parallel full-document extraction with 12 separate calls is expensive and each call still faces the same heading confusion problem. (source: Multi-pass processing, Document handling)
</details>

## Question 12
You are extracting product specifications from a manufacturer's website. Products are grouped by category pages, each listing 20–60 products. After extraction you find that `product_weight` values for 15% of products in the "Electronics" category belong to adjacent products on the page — a spillover where the model attributes a nearby product's weight to the current product. What is the root cause and fix?

A) The density of attribute values in the page layout causes the model to associate values with the wrong product; restructure the extraction to process one product object at a time rather than an entire category page.
B) The model hallucinated weight values because electronics weight specifications require niche domain knowledge not well represented in training data.
C) The `product_weight` pattern constraint is too permissive, accepting values from any part of the page; add a stricter regex to reject implausible weight ranges.
D) Increase extraction temperature to 0.8 so the model explores more of the attribute space per product and reduces fixation on adjacent values.

<details><summary>Answer</summary>
**A)** Extracting an entire category page in one prompt forces the model to track which attributes belong to which product across 20–60 products simultaneously, causing spillover. Processing one product at a time — or chunking pages into individual product blocks before extraction — eliminates the cross-product attribution problem. B) the model has broad knowledge of electronics specifications; this is a context management issue. C) a regex constraint narrows the value format but does not fix which product the value is assigned to. D) higher temperature increases randomness and would worsen, not improve, attribute attribution. (source: Document preprocessing, Context and document handling)
</details>

## Question 13
You are extracting financial data from annual reports in a batch of 800 documents. You want to measure extraction quality before scaling to 10,000 documents. You have a ground-truth labeled set of 200 documents. After running evaluation, overall field accuracy is 94%. A colleague says "that's good enough — ship it." What additional evaluation step is most important before proceeding?

A) Run the evaluation on a different random sample of 200 documents to confirm the 94% result is stable and not a statistical artifact of the particular sample chosen.
B) Increase the labeled evaluation set to 500 documents so the confidence interval on the 94% accuracy estimate is statistically narrow enough to support a go/no-go decision.
C) Evaluate on the 10,000-document production set directly — real-world performance on the full distribution is more informative than a curated labeled set.
D) Break down the 94% accuracy by document subcategory (e.g., US GAAP vs. IFRS vs. non-standard reporting) and by individual field to detect hidden performance gaps before committing to scale.

<details><summary>Answer</summary>
**D)** Aggregate accuracy masks segment-level performance gaps. A 94% overall accuracy could hide a 60% accuracy on IFRS documents if they are 8% of the evaluation set. Breaking down by subcategory and by individual field before scaling ensures the system performs consistently across all segments, not just on average. A) re-sampling adds confidence but does not reveal hidden gaps. B) a larger sample reduces variance but still produces an aggregate metric hiding the same gaps. C) evaluating on unlabeled production data provides no ground-truth comparison. (source: Evaluation, Consistency and scale)
</details>

## Question 14
You are extracting structured data from technical job postings to build a skills taxonomy. The `required_skills` field is an array of strings. On long postings, the model extracts an average of 8 skills per posting. On short postings, it extracts an average of 22 skills per posting. Investigation shows short postings have lower extraction precision — the model includes soft skills, tool preferences, and nice-to-haves alongside hard requirements. What is the most effective fix?

A) Add a `maxItems: 15` constraint on the `required_skills` array to force the model to prioritize and limit output.
B) Switch to a higher-capability model for short postings, where information density is higher and precision requires stronger contextual reasoning.
C) Post-process all extractions with an NLP classifier that scores each extracted skill for "requirement strength" and discards items below a threshold score.
D) Refine the extraction prompt with explicit criteria distinguishing required skills ("must have," "required," "minimum qualification") from preferred skills, and add a separate `preferred_skills` array.

<details><summary>Answer</summary>
**D)** The core problem is that the model conflates required and preferred skills because the schema and prompt do not distinguish them. Adding explicit criteria for what constitutes a required skill and creating a separate `preferred_skills` field resolves the precision problem structurally. A) `maxItems` forces truncation without improving discrimination between required and preferred. B) the issue is prompt ambiguity, not model capability. C) adds post-processing complexity that treats the symptom rather than the cause. (source: Schema design, Prompt engineering)
</details>

## Question 15
You are processing scanned PDF contracts from the 1990s. OCR quality varies significantly: some pages have 98% character accuracy while others (faxed copies) have 70% character accuracy. Your extraction pipeline treats all pages identically. After deployment, critical clause fields from low-quality pages have a 40% extraction error rate. What is the most targeted improvement?

A) Upgrade the OCR engine for the entire pipeline to improve average character accuracy from 85% to 93%, which will proportionally reduce extraction errors on low-quality pages.
B) Add an OCR confidence score per page and route pages below a quality threshold to an enhanced extraction path: include the raw OCR output alongside a prompt note about likely character errors, asking the model to reason about possible transcription artifacts.
C) Reject all documents with pages below 80% OCR confidence and return them to a human scanning queue for rescanning before extraction.
D) Replace the extraction pipeline with a multimodal model that accepts the raw scanned page images directly, bypassing OCR and letting the model handle handwriting and poor print quality natively.

<details><summary>Answer</summary>
**B)** Routing low-quality pages to an enhanced extraction path that explicitly surfaces OCR uncertainty allows the model to reason about likely transcription artifacts (e.g., `"0"` vs `"O"`, `"l"` vs `"1"`). This targets the treatment specifically to documents that need it. A) better OCR reduces the problem but does not eliminate it for the worst pages and improves the whole pipeline cost for marginal gain on the tail. C) rejection loses documents the business needs processed. D) multimodal processing is promising for image inputs but introduces a new pipeline and does not address the existing OCR-based infrastructure. (source: Document preprocessing, OCR quality)
</details>

## Question 16
Your team extracts structured data from news articles at scale. After three months, editorial style changes at a major news source cause `author_byline` extraction to fail for 12% of articles from that source — the byline is now formatted as "Reported by First Last" instead of "By First Last." This is caught only when users complain. What monitoring approach would have detected this earlier?

A) Add a schema version field to each extraction so changes in output structure can be detected by comparing schema version distributions over time.
B) Subscribe to editorial style guides from all major news sources and update extraction prompts proactively whenever a source announces format changes.
C) Add a `source_format_confidence` field to the schema that the model populates with a 0–1 score estimating how well the document matches the expected format for its source.
D) Implement continuous per-source field-level extraction quality monitoring: track null rates, format distribution, and validation failure rates per source on a rolling weekly basis, alerting when metrics shift beyond a threshold.

<details><summary>Answer</summary>
**D)** Per-source field-level monitoring detects schema drift by surfacing statistical changes in extraction output — a spike in null `author_byline` values from a specific source, or a drop in format compliance — before user complaints surface the issue. A) schema version tracks intentional changes by developers, not source format drift. B) monitoring editorial style guides is not scalable for hundreds of sources and byline format changes are not typically announced. C) model self-assessment of format confidence is poorly calibrated and does not provide the per-source trend signal needed. (source: Schema drift, Consistency and scale)
</details>

## Question 17
You are extracting structured data from scientific paper PDFs using a pipeline that converts PDFs to text first. After conversion, tables appear as garbled sequences of numbers with no alignment information. Your extraction for `experimental_results` — which lives almost entirely in tables — fails on 70% of papers. What is the most effective approach?

A) Use a table-aware PDF parser or multimodal model to extract table content as structured HTML or Markdown before passing to the extraction pipeline, preserving row/column relationships.
B) Increase retry budget for `experimental_results` to 5 attempts and include the garbled table text alongside an instruction: "Reconstruct the table structure from the raw text before extracting."
C) Add a prompt instruction: "When you see numbers separated by whitespace, assume they form a table and reconstruct rows based on alignment patterns."
D) Mark `experimental_results` as nullable and return null for papers with tables, routing them to a human data entry queue.

<details><summary>Answer</summary>
**A)** The root cause is PDF-to-text conversion that destroys table structure. Addressing this at the preprocessing layer — using a table-aware parser that produces structured HTML or Markdown tables — preserves row/column relationships before extraction. B) more retries with garbled input cannot recover structure that was lost in conversion. C) whitespace-alignment reconstruction is unreliable and varies by PDF layout and font. D) routing to human entry is a fallback, not a solution — it does not scale and abandons 70% of papers. (source: Document preprocessing, Table parsing)
</details>

## Question 18
You batch-process 5,000 job postings nightly to populate a talent intelligence database. The extraction schema has 20 fields. After 3 months, a downstream analyst reports that `seniority_level` values have shifted: `"senior"` extractions dropped 40% while `"mid"` extractions increased by the same amount. No prompt changes were made. What is the most likely explanation and response?

A) The model API was silently updated to a new version with different output tendencies; roll back to the previous model version to restore the original classification behavior.
B) The source job posting distribution shifted — fewer senior roles in the market — which is a real signal, not an extraction error; verify by comparing source document text before concluding the pipeline is broken.
C) Batched API calls introduce ordering artifacts where documents processed early in the batch influence classification of later documents through shared sampling state.
D) The `seniority_level` enum lost the `"senior"` value in a schema update; the model is downgrading classifications to avoid validation failures.

<details><summary>Answer</summary>
**B)** Distribution shifts in extracted values may reflect real-world changes in the data rather than extraction errors. Before diagnosing a pipeline problem, verify by sampling affected documents and checking whether the source text actually contains fewer senior-level indicators. If the source text confirms the shift, it is a real market signal. A) silent model updates are possible but should be confirmed before rollback. C) batched API calls do not share sampling state between documents. D) schema changes would produce validation errors, not silent downgrading — check the change log before assuming this. (source: Schema drift, Evaluation)
</details>

## Question 19
You are building a contract clause extractor where `termination_clause` extraction is used as input to extract `termination_notice_period` in a second pass. In 20% of documents, `termination_notice_period` extractions are wrong because `termination_clause` was extracted incorrectly in the first pass — but the second pass proceeds anyway. What validation design prevents error propagation?

A) Run both extraction passes simultaneously in a single API call, giving the model full document context for both fields to eliminate the dependency between passes.
B) Add a confidence threshold gate between passes: if `termination_clause` confidence is below 0.8, pause the pipeline and route the document to human review before running the second pass.
C) Validate `termination_clause` completeness and plausibility (e.g., non-null, minimum length, contains termination-relevant keywords) before using it as context for the second pass; on failure, retry pass 1 or flag for review before proceeding.
D) Add a prompt instruction in pass 2: "If the termination clause provided seems incomplete or incorrect, extract `termination_notice_period` directly from the full document instead."

<details><summary>Answer</summary>
**C)** Cascading validation — verifying that pass 1 output meets quality criteria before it is used as context for pass 2 — prevents error propagation. A structural validation check (non-null, minimum length, keyword presence) catches likely extraction failures before they corrupt downstream passes. A) combining passes loses the precision benefit of multi-pass extraction and may produce worse results. B) confidence thresholds are useful but model self-reported confidence is poorly calibrated; structural checks are more reliable. D) instructs the model to self-correct in pass 2 but this is unreliable and does not prevent the error from entering the pipeline. (source: Cascading validation, Multi-pass processing)
</details>

## Question 20
You are extracting structured data from a corpus of 50,000 historical real estate deeds dating from 1880 to 1990. Legal language conventions, abbreviations, and measurement units change significantly across this period. A single extraction prompt performs well on post-1970 deeds but poorly on pre-1930 deeds. What is the most robust approach?

A) Fine-tune the model on a labeled set of pre-1930 deeds to internalize the archaic conventions, then use the fine-tuned model for the full corpus.
B) Increase the context window budget and include a 50-page historical legal conventions reference document in every extraction request to give the model background on period-specific terminology.
C) Accept lower accuracy for pre-1930 deeds and add a `era_confidence_penalty` field that downstream code uses to discount old deed extractions proportionally.
D) Add a document era classifier as the first step, routing pre-1930 deeds to a prompt with era-specific few-shot examples and a glossary of archaic terms, and post-1970 deeds to the existing prompt.

<details><summary>Answer</summary>
**D)** A document era classifier routes deeds to era-appropriate extraction prompts, each with few-shot examples reflecting the conventions of that period. This targeted approach handles distribution shift without requiring fine-tuning. A) fine-tuning is expensive and requires a large labeled dataset; few-shot prompting is a faster, cheaper fix. B) including a 50-page reference document in every request increases cost substantially and may not be processed reliably. C) accepting lower accuracy and applying a penalty flag does not improve extraction quality and discards historical data value. (source: Multi-document extraction, Document preprocessing)
</details>

## Question 21
You extract structured metadata from academic conference papers and store results in a search index. After 6 months, users report that author affiliation search frequently returns wrong results. Investigation shows `author_affiliations` is correctly extracted from the PDF but inconsistently formatted: "MIT", "Massachusetts Institute of Technology", "M.I.T.", and "MIT CSAIL" all appear as separate affiliations for the same institution. How should this be addressed?

A) Add an enum constraint listing all known institution names in full canonical form, requiring the model to map extracted affiliations to the nearest enum value during extraction.
B) Add a prompt instruction: "Always use the full official institution name in extracted affiliations, never abbreviations or acronyms."
C) Add a post-extraction normalization step that uses an institution name resolution service (e.g., ROR API) to map variant forms to canonical identifiers, applied after extraction and before indexing.
D) Add an `affiliation_aliases` array alongside the primary `affiliation` field to capture all variant forms encountered in the document, then deduplicate at query time.

<details><summary>Answer</summary>
**C)** Institution name normalization is a known hard problem with thousands of institutions and countless variant forms. A post-extraction resolution service maps extracted strings to stable canonical identifiers (like ROR IDs), which is more comprehensive and maintainable than an enum or prompt instruction. A) an enum of all institutions is impractical at global scale and requires constant maintenance. B) model output consistently using full official names is unreliable — the model extracts what appears in the document, which often contains abbreviations. D) storing aliases improves recall but does not solve the canonical identity problem for search. (source: Post-processing, Consistency and scale)
</details>

## Question 22
You are building a pipeline to extract line items from purchase orders. Each line item has `sku`, `description`, `quantity`, `unit_price`, and `line_total`. Your schema validation checks that `quantity * unit_price == line_total` for every line item. In practice, 4% of line items fail this check due to rounding (e.g., quantity 3 × unit_price $33.333 rounds to $100.00 not $99.999). How should the validation rule be adjusted?

A) Change the equality check to an approximate equality check: flag the line item only when `abs(quantity * unit_price - line_total) > 0.05`, accepting rounding differences up to 5 cents as valid.
B) Remove the cross-field validation rule entirely to avoid false positives from rounding, relying solely on schema type validation.
C) Add a `rounding_adjustment` nullable float field and require `quantity * unit_price + rounding_adjustment == line_total` as the validation rule.
D) Store `quantity`, `unit_price`, and `line_total` as strings rather than numbers, deferring arithmetic validation to a downstream system that can apply business-specific rounding rules.

<details><summary>Answer</summary>
**A)** Approximate equality with a tolerance threshold (e.g., ±$0.05) handles floating-point rounding and minor price rounding conventions while still catching genuine arithmetic errors (a $500 discrepancy). B) removing the rule loses a valuable semantic check on extraction quality. C) adds schema complexity and requires the model to compute an adjustment it cannot reliably derive. D) deferring to strings loses type-level guarantees across the pipeline. (source: Validation and retry logic, Business-rule validation)
</details>

## Question 23
You are extracting structured data from a mix of press releases, earnings call transcripts, and analyst reports to build a financial events database. Each document type has a different structure and terminology for the same concepts. Your current single-prompt approach has high recall but low precision — it extracts too many false positive events. What architectural change improves precision most directly?

A) Add `tool_choice: "any"` with three document-type-specific extraction tools and rely on the model to select the right tool based on detected document characteristics.
B) Switch from `tool_use` to direct JSON text output to give the model more flexibility to express uncertainty about whether a detected pattern is a genuine financial event.
C) Increase the schema's required field count so only clearly complete events pass validation, using failed required-field validation as a filter for low-confidence events.
D) Add a document-type classifier as the first step, then route each document to a type-specific extraction prompt with few-shot examples and field definitions tuned to that document type's conventions.

<details><summary>Answer</summary>
**D)** Different document types use different language to describe the same financial events. A classifier routing documents to type-specific prompts with tailored few-shot examples dramatically improves precision by training the model on what constitutes a genuine event in each format. A) `tool_choice: "any"` relies on the model detecting document type without a dedicated classifier — less reliable. B) text-based JSON is less reliable structurally and does not address the precision problem. C) required-field strictness creates more validation failures but does not improve the model's ability to distinguish genuine events from false positives. (source: Multi-document extraction, Schema design)
</details>

## Question 24
You are extracting structured summaries from grant applications. Each application has a `project_abstract` (free text) and `requested_budget` (number). The `requested_budget` field appears in multiple places: once in the application cover sheet and once in the detailed budget narrative. In 8% of applications, these two figures differ. The model sometimes extracts the cover sheet figure and sometimes the narrative figure, creating inconsistency across documents. What is the most reliable fix?

A) Add a prompt instruction: "Always prefer the cover sheet figure over the budget narrative figure when they differ."
B) Extract both figures into separate fields — `budget_cover_sheet` and `budget_narrative` — add a `budget_discrepancy` boolean flag, and let reviewers resolve the conflict with source context.
C) Add a business rule in the prompt: "If two budget figures appear in the document and they differ, use the larger value as the authoritative figure."
D) Run a second pass specifically targeting budget figures, using the first-pass extraction as context to resolve the discrepancy within the extraction step.

<details><summary>Answer</summary>
**B)** When the same field appears in multiple document locations with potentially different values, extracting both with provenance and flagging discrepancies preserves accuracy and surfaces real application inconsistencies for human review. A) a prompt instruction creates a policy the organization may not have sanctioned and masks genuine discrepancies. C) choosing the larger value arbitrarily may systematically bias budget figures. D) a second pass does not resolve genuine document-level ambiguity — the conflict is in the source, not the extraction. (source: Conflicting signals, Source traceability)
</details>

## Question 25
You maintain a pipeline that extracts structured data from vendor invoices. The pipeline has been running for 8 months. A new vendor starts sending invoices in a format you have not seen before — multi-currency with a separate FX rate table at the bottom. Extractions from this vendor have a 55% field accuracy rate. What is the fastest path to acceptable accuracy without rebuilding the pipeline?

A) Build a dedicated extraction sub-pipeline for multi-currency invoices with a custom schema that includes `fx_rate_table` and `base_currency` fields, routing only this vendor's invoices through it.
B) Increase the retry budget to 5 attempts for this vendor's invoices, since multiple extraction passes on the same document will eventually converge on the correct values.
C) Collect 5–10 labeled examples from this vendor's format, add them as targeted few-shot examples to the extraction prompt, and re-evaluate on a hold-out set before deploying.
D) Contact the vendor and request they switch to a simpler invoice format compatible with the existing pipeline before extending the extraction system.

<details><summary>Answer</summary>
**C)** Targeted few-shot examples demonstrating the new format — including the FX rate table layout and how multi-currency fields map to schema fields — is the fastest fix with minimal pipeline changes. Few-shot examples teach the model the format-specific extraction patterns quickly. A) a dedicated sub-pipeline is more thorough but takes significantly more time. B) retries on the same prompt cannot teach the model a format it has not seen demonstrated. D) requesting vendor format changes is slow, may not be accepted, and does not solve the existing backlog. (source: Multi-document extraction, Prompt engineering)
</details>

## Question 26
You are extracting structured data from a large corpus of legal briefs to identify cited statutes. Each citation should have `statute_title`, `code`, `section`, and `subsection`. The `subsection` field is present in roughly 30% of citations. After deployment, you find the model is inventing subsection values in 12% of cases where no subsection exists in the source text. What schema and prompt combination most reliably eliminates fabrication?

A) Add a `cite_literally` instruction: "Copy the exact statute citation string from the source text character by character rather than parsing it into fields."
B) Make `subsection` nullable in the schema AND add a prompt instruction with an example showing a citation with no subsection returning null for that field: `{"subsection": null}`.
C) Add a `minimum: 1` character length constraint on `subsection` so empty strings fail validation, forcing the model to use null when nothing is extracted.
D) Add a post-extraction step that cross-references each extracted `subsection` against a statutory database and replaces unverified subsections with null.

<details><summary>Answer</summary>
**B)** The combination of a nullable schema field and a few-shot example showing null as the correct output for absent subsections is more effective than either alone. The nullable schema removes the fabrication pressure from the required constraint; the example demonstrates the expected null behavior concretely. A) literal copying produces raw citation strings, not structured field values. C) `minimum: 1` prevents empty strings but not plausible-sounding fabricated subsection values. D) a statutory database cross-reference adds expensive infrastructure and may not cover all statutes. (source: Absence vs. unknown, Schema design)
</details>

## Question 27
You are building an extraction pipeline for job applications. Each application PDF contains work experience entries, each with `company`, `title`, `start_date`, `end_date`, and `responsibilities`. For current positions, `end_date` is absent (the position is ongoing). The model returns `end_date: "Present"` as a string for current positions, but your schema expects a date or null. What is the most complete fix?

A) Add a `pattern` constraint on `end_date` enforcing ISO 8601 format, so the string `"Present"` fails validation and the model is forced to return null instead.
B) Change `end_date` to a string type, accept `"Present"` as a valid value, and handle date parsing downstream.
C) Make `end_date` nullable AND add a companion `is_current_position` boolean field, so downstream code has a typed signal for ongoing employment without needing to parse sentinel strings.
D) Add a prompt instruction: "Return null for end_date when a position is current. Do not return the word 'Present' or any string."

<details><summary>Answer</summary>
**C)** Adding a nullable `end_date` with an explicit `is_current_position` boolean gives downstream systems a typed signal for ongoing employment. The prompt instruction from D) plus the schema constraint from A) address the immediate symptom, but without an explicit field for "currently employed," downstream code must infer this from a null date — which is ambiguous (null could also mean the date was not extractable). B) degrades type safety across the field. (source: Absence vs. unknown, Schema design)
</details>

## Question 28
You are extracting structured metadata from 10,000 scientific papers across 8 research domains. You sample 50 papers per domain and evaluate extraction quality before scaling. Results show 96% average accuracy, but the Geophysics domain has 71% accuracy for `methodology` and `instrumentation` fields, while all other domains exceed 92%. You have no labeled Geophysics data beyond this sample. What is the most targeted and cost-effective response?

A) Accept the 71% accuracy for Geophysics papers and surface the domain in the output schema with a `domain_confidence_flag` field, letting downstream researchers self-select for manual review.
B) Collect 15–20 labeled Geophysics examples, add domain-specific few-shot examples for `methodology` and `instrumentation`, and re-evaluate on a new hold-out set before proceeding.
C) Exclude Geophysics papers from the batch and submit only the other 7 domains at scale, processing Geophysics separately after quality improvement work.
D) Switch to a specialized scientific language model for Geophysics papers only, since the performance gap indicates the general model lacks sufficient domain training data.

<details><summary>Answer</summary>
**B)** Targeted few-shot examples for the underperforming domain and fields are the fastest, cheapest fix with no pipeline changes. The performance gap reflects that Geophysics uses specialized terminology for `methodology` and `instrumentation` that was not represented in the initial few-shot examples. A) accepting 71% accuracy for a knowable fix is premature. C) excluding an entire domain is not required when targeted prompt improvement is available. D) a specialized model adds pipeline complexity and cost before simpler prompt-level fixes are exhausted. (source: Evaluation, Consistency and scale)
</details>

## Question 29
You are extracting structured data from analyst research reports and need to link each extracted claim back to the specific paragraph in the source document where it was stated (for compliance and audit purposes). After extraction, source linking is unreliable — some claims have no source reference, others point to wrong paragraphs. What architectural change makes source traceability reliable?

A) Add a post-extraction step that uses semantic similarity to match each extracted claim back to the most similar paragraph in the source document.
B) Pre-process the document by numbering each paragraph, include the numbered text in the extraction prompt, and require the schema to include a `source_paragraph_id` field alongside each extracted claim.
C) Add a prompt instruction: "For each claim you extract, identify the paragraph you found it in and include a brief quote in the `source_quote` field."
D) Run extraction twice and take the intersection of source references reported in both runs, discarding claims where the two runs cite different paragraphs.

<details><summary>Answer</summary>
**B)** Pre-numbering paragraphs and requiring the model to cite `source_paragraph_id` makes source traceability a structured schema requirement rather than a prose instruction. The model can reliably reference `paragraph_14` when the document's paragraphs are explicitly numbered in the input. A) semantic similarity matching is a reasonable fallback but is less precise than direct citation and adds post-processing complexity. C) prose instructions for source attribution are less reliable than a schema field with an explicit reference system; quote extraction adds length and is less stable than a paragraph ID. D) intersection of two runs discards valid claims where the model correctly cites different paragraphs for the same claim across runs. (source: Source traceability, Document handling)
</details>

## Question 30
You are running an extraction pipeline that processes 2,000 news articles per day to populate a structured events database. After 4 months, you notice that a field called `event_category` has gradually shifted: the category `"economic_policy"` is appearing in 35% of articles (up from 12% at launch) while `"politics"` has dropped from 28% to 8%. No schema or prompt changes were made. What is the correct first diagnostic step?

A) Check whether a recent API model update changed the model's classification tendencies for the `event_category` enum, and roll back to the previous model version if a change is confirmed.
B) Sample 30–50 articles from the current period that are classified as `"economic_policy"` and manually verify whether the classification is correct, distinguishing a real news cycle shift from an extraction drift.
C) Add a `classification_confidence` field and reprocess the last 4 months of articles to retroactively score each `event_category` assignment, then investigate low-confidence shifts.
D) Compare the current month's prompt against the launch-month prompt in version control, since undocumented prompt edits are the most common cause of gradual category distribution drift.

<details><summary>Answer</summary>
**B)** Before diagnosing a pipeline problem, verify whether the distribution shift reflects a genuine change in news coverage (economic policy news has been genuinely dominant) or an extraction error. Sampling and manually reviewing a batch of current-period classifications directly answers this question. A) model API updates are possible but should be investigated after confirming the shift is not real-world. C) retroactive reprocessing is expensive and assumes the shift is an error before verifying. D) undocumented prompt edits are worth checking but are a secondary hypothesis after confirming the shift is not a real signal. (source: Schema drift, Evaluation)
</details>
