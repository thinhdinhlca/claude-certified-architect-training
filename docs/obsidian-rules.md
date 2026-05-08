# Obsidian Rules (Progressive Disclosure)

## Level 1 - Operating Rules
- Use Obsidian as an evidence-linked study system, not a diary.
- Capture only structured artifacts: decisions, mistakes, patterns, and source links.
- One canonical daily study note per date.
- Every note must link to at least one source (`docs`, `practice-tests`, or external docs URL).
- Keep all high-noise logs out of Obsidian; store them in `logs/`.

<details>
<summary>Level 2 - Required Note Types</summary>

### 1) Daily Study Note
- Path: `02-Lanes/CCA-Cert/Daily/YYYY-MM-DD.md`
- Must include:
  - Focus for the day
  - What was read (exact links)
  - Test run command
  - Score and weak domains
  - 3-5 flashcards from mistakes

### 2) Domain Note
- Path: `03-Knowledge/CCA-Domains/domain-N.md`
- One file per domain (`domain-1` ... `domain-5`)
- Must include:
  - Core decision rules
  - Anti-patterns
  - Scenario mappings

### 3) Playbook Note
- Path: `04-Playbooks/`
- Use for operational procedures (for example: full-sim protocol, retest protocol).

</details>

<details>
<summary>Level 3 - Linking and Tagging Standards</summary>

- Prefer wiki-links for internal notes: `[[CCA-6Week-Execution]]`.
- Add frontmatter at minimum:
  - `type`: `daily|domain|playbook|resource`
  - `lane`: `cca-cert`
  - `date`: `YYYY-MM-DD` (for daily notes)
  - `status`: `draft|active|stable`
- Use tags sparingly:
  - `#cca/domain1` ... `#cca/domain5`
  - `#cca/mistake-pattern`
  - `#cca/retest`
- For every claim that can be tested, attach one source link line:
  - `Source: <url-or-local-path>`

</details>

<details>
<summary>Level 4 - Progressive Disclosure Pattern for Markdown Notes</summary>

Use this structure in new Markdown notes:

1. **Level 1 summary** (3-6 bullets max): key actions/decisions.
2. **Level 2 details** (`<details>`): execution notes and command snippets.
3. **Level 3 deep dives** (`<details>`): edge cases, rationale, alternatives.
4. **Level 4 references** (`<details>`): long excerpts, raw links, appendix.

Template skeleton:

```md
# Title

## Level 1 - Summary
- ...

<details>
<summary>Level 2 - Execution</summary>

...

</details>

<details>
<summary>Level 3 - Deep Dive</summary>

...

</details>

<details>
<summary>Level 4 - References</summary>

...

</details>
```

</details>

<details>
<summary>Level 5 - CLI Integration Rules</summary>

- Before study starts:
  - Run `./cca read --date YYYY-MM-DD`.
- After study test:
  - Run `./cca stats --last 10`.
- For full mock:
  - Run `./cca sim --seed <n>`.
- Daily note should copy:
  - exact command used
  - score
  - weakest 2 topics
  - next retest command

</details>
