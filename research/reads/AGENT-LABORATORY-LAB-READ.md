# Research-Lab read of Agent Laboratory (an open-source autonomous research pipeline), 2026-11-12

Asked by the owner in this session's chat on 2026-11-11 ("how can we benefit from this repo"); the fetch approved by the
owner on 2026-11-12 ("Fetch and record"). Input: one read-only GET of the repository page the owner named, parsed with a
standard-library HTML parser in the session scratch; the page's README text and sidebar facts. Nothing else was
fetched: no clone, no paper, no sub-page, no second request. Statements about the code's internals come from the lab's
prior knowledge of the January 2025 paper and are marked (prior); they are "as recalled" until a paper fetch pins them.
No run. The fetched copy stays in the scratch; nothing of it is copied onto the bridge beyond short phrases. The page
carries a contact e-mail address and a clone address; neither is reproduced here.

## 0. Fetch record

| line | request URL | HTTP | final URL | type | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|---|---|---|
| AL-1 | github.com/SamuelSchmidgall/AgentLaboratory | 200 | same (github.com, no redirect) | text/html | 304,076 | 6b76db5fd493114691f1d65d3a6964d9a1eb4641812bae14719ab5184734cffe | 2026-11-12T01:41:44Z |

Client: a generic command-line client, one request, no cookies, no personal data. The page's embedded data names the
default branch head `d9017d90e329112d2a80b7712f37ee9094d2cd27`; every fact in section 1 is pinned to that head.

## 1. What the page says (pinned to d9017d90)

| fact | value |
|---|---|
| Title and description | "Agent Laboratory: Using LLM Agents as Research Assistants"; an end-to-end autonomous research workflow meant to assist the human researcher |
| Licence, size, uptake | MIT; 44 commits; 5,931 stars; README in 17 languages under `readme/` |
| Top-level files | `ai_lab_repo.py` (entry), `agents.py`, `mlesolver.py`, `papersolver.py`, `inference.py`, `tools.py`, `utils.py`, `common_imports.py`, `app.py`, `experiment_configs/`, `media/`, `requirements.txt` |
| Phases | (1) Literature Review, (2) Experimentation, (3) Report Writing; specialised agents per phase; external tools arXiv, Hugging Face, Python, LaTeX (pdflatex optional, `--compile-latex`) |
| Models | OpenAI o1, o1-preview, o1-mini, gpt-4o, o3-mini; DeepSeek deepseek-chat (v3); chosen by `--llm-backend`; hosted endpoints only |
| Run form | Python 3.12 venv; `ai_lab_repo.py --yaml-location experiment_configs/MATH_agentlab.yaml`; copilot mode and language set in the YAML |
| Steering | per-phase "task notes" edited in the entry script (plan-formulation, data-preparation, ...); the README's own example asks for notes to include compute limits and "providing API keys" |
| Checkpoints | every phase saved to `state_saves`; a run resumes from any checkpoint after a failure or a lost connection |
| AgentRxiv | news item dated 2025-03-24: a framework where research agents upload, retrieve and build on each other's research; its paper is arXiv 2503.18102 |
| Citation | Schmidgall et al., 2025, arXiv 2501.04227 (cs.HC) |

(prior, not on the page): role agents (PhD student, postdoc, professor, ML engineer, software engineer, reviewers); the
experiment solver is an edit/replace loop over generated Python scored by an LLM reward model with error repair; the paper
solver is the same loop over LaTeX sections; three reviewer agents score with a NeurIPS-style rubric; the paper reports
that the automated reviewer scores run above human scores, that the strongest reasoning model produced the best-rated
papers, and a per-paper cost of a few dollars on gpt-4o; generated code runs in the pipeline's own process; AgentRxiv is a
local preprint server with parallel laboratories.

## 2. Ruling: a method reference and a later workload, not a component

Three uses with value, in order of value for cost, then the non-use. Each names its frequency and cost (rule G).

- U1, reviewer custody (rule D, in force). The three-reviewer rubric is a ready second reviewer family for PREREG
  review: originality, quality, clarity, significance, soundness, presentation, overall and confidence, applied to a
  PREREG rather than a paper, with the lab's existing requirement of a FAIL class per note. The paper's own calibration
  finding (prior: agent reviewers overrate) is the reason the brief asks for classed findings, not scores. Frequency:
  every PREREG review round. Cost: one section in the monitor's reviewer brief; no compute. Enters the resume plan.
- U2, cost ledger (rule J, on resume). A per-phase, per-model token and cost table (prior: the inference layer keeps
  one) is the shape for the register's minutes and tokens columns from RL-23: phase, model, prompt and completion
  tokens, cost, wall seconds; one row per phase per round. Frequency: every experiment and review round. Cost: a
  column set and a collector line in `outcome_record.py`; no compute.
- U3, progress view (rule I, on resume). Phase checkpoints with resume are the form for the generated progress view:
  per experiment, the phases PREREG, review rounds, run, result, report with the last checkpoint and its digest, rendered
  by `build_research.py` from the OUTCOME records the lab already writes at every stop (RL-23). Frequency: every
  rebuild. Cost: a builder change; no compute.
- U4, a tenant workload (later, heavy). Candidate hypothesis under rule A, basis = a release-gate claim (the estate's
  egress-deny log in REF-0; TRUST-IDENTITY-001's network edges): "A multi-agent research pipeline run as a tenant
  workload under the harness's egress policy fails closed at its first external call (arXiv or Hugging Face), the
  denial is logged against the tenant, and the run resumes from its last checkpoint once the policy admits a test
  double." Needs R14's doubles for arXiv and Hugging Face, a model endpoint inside the tenant (the page lists hosted
  endpoints only, so routing through inference-api or a local model), and a heavy slot. Not registered now: rule B
  (one question at a time), SC-D1 F (heavy share paused), and the doubles do not exist. Register it when R14's doubles
  exist and a heavy slot opens; frequency then: one run per estate profile.
- Non-use. Not a product component and not an adoption baseline: a single-process prototype of nine Python modules
  and 44 commits, hosted APIs only, generated code executed in-process (prior), pickled state (prior), and API keys
  passed through free-text notes per the README. The roadmap's intake rule (SC-D1 A) requires a release-path item, the
  adoption policy requires a qualified baseline, and a design-reference record alone is now one index line (SC-D1 D).
  Recommendation to the visionary: no roadmap item, no codebase record; this read is the index line.

## 3. Options for the owner

(a) Record this read; U1 enters the monitor's reviewer brief at the first resumed review; U2 and U3 enter the resume
plan; U4 stays a candidate in this read until R14's doubles exist. No fetch beyond AL-1. Recommended.
(b) As (a), plus two approved fetches (arXiv 2501.04227 and 2503.18102) to pin the (prior) claims, chiefly the reviewer
calibration figure for the U1 brief.
(c) Record nothing beyond this read's index line.

## 4. Not claimed

No claim about the code's current behaviour (not cloned, not run); no figure from the paper beyond "prior"; nothing
about AgentRxiv's server beyond the page's one sentence; no licence evaluation beyond the page's MIT statement; no
claim that any of U1 to U3 changes a lab result.
