# SynthSEA — Master Research & Implementation Prompt

## Project Title

**SynthSEA: Multi-Agent Synthetic Instruction Generation for Resource-Uneven Southeast Asian Languages**

### Singapore-Focused Case Study

The primary experimental setting should be Singapore, covering:

1. Singlish / Colloquial Singapore English
2. Singapore Malay / Malay
3. Singapore Tamil / Tamil
4. Singapore Mandarin / Singapore-context Mandarin

**Important:** Do NOT blindly describe all four as "low-resource languages."

Instead, accurately characterize their resource availability using terms such as:

- low-resource
- under-resourced
- resource-constrained
- resource-uneven
- regional variety
- culturally grounded multilingual NLP

only when supported by literature and evidence.

---

# ROLE

Act as a combination of:

- Senior NLP Research Scientist
- Multilingual LLM Researcher
- Low-Resource NLP Specialist
- Synthetic Data Generation Researcher
- Multi-Agent Systems Researcher
- Experimental ML Scientist
- Academic Research Engineer
- ACL/EMNLP reviewer
- Reproducibility engineer

The task is NOT simply to implement a project.

Determine whether the proposed SynthSEA research idea is genuinely novel, scientifically defensible, experimentally feasible, and suitable for submission to RegiCON 2026.

The final system must be research-grade, reproducible, statistically evaluated, and publication-oriented.

---

# CONFERENCE CONTEXT

Target conference:

**RegiCON 2026 — 2nd Regional Conference on Natural Language Processing**

Theme:

**NLP for East India and Southeast Asia – Bridging Borders, Building Resources**

The CFP emphasizes:

- low-resource and endangered languages
- multilingualism and code-switching
- morphology
- speech and ASR
- lexicons and WordNets
- annotated corpora
- machine translation
- cross-lingual NLP
- NER
- language identification
- orthography/transliteration
- digital preservation
- inclusive and culturally sensitive NLP

The paper should clearly map its contributions to this scope.

---

# CORE RESEARCH IDEA

Develop **SynthSEA**, a modular framework for generating high-quality synthetic instruction-following data for Southeast Asian languages and regional linguistic varieties using a coordinated multi-agent architecture.

Core hypothesis:

> A linguistically specialized, culturally grounded, critic-driven multi-agent generation pipeline can produce more diverse, linguistically faithful, culturally appropriate, and downstream-useful instruction data than conventional single-agent or translation-based synthetic data generation.

The framework must not simply generate large amounts of text.

Central research question:

> **Can multi-agent linguistic specialization and iterative quality control produce synthetic instruction data that improves multilingual LLM performance under resource constraints while preserving language-specific and culture-specific characteristics?**

---

# CRITICAL NOVELTY REQUIREMENT

Before implementing anything, conduct a deep literature review.

Do NOT assume the idea is novel.

Explicitly investigate and compare against:

1. Self-Instruct
2. Alpaca-style synthetic instruction generation
3. Evol-Instruct
4. WizardLM-style instruction evolution
5. Self-Play / self-improvement approaches
6. Multi-agent instruction generation
7. Star-Agents
8. MATRIX-Gen
9. Multi-agent synthetic data generation
10. Seed-free synthetic instruction generation
11. Synthetic instruction generation for Thai
12. SeaLLMs and related Southeast Asian multilingual LLM work
13. Singlish NLP datasets
14. Multi-agent Singlish research
15. SEA code-mixing generation
16. Multilingual instruction tuning
17. Culturally grounded synthetic data
18. Language-specific synthetic data generation
19. Low-resource instruction tuning
20. Recent 2025–2026 work that may overlap with SynthSEA

In particular investigate:

- the 2024 Thai seed-free synthetic instruction generation work
- the 2025 ACL Singlish multi-agent work
- the 2025 ACL MATRIX-Gen work
- Star-Agents
- SeaLLMs
- recent 2026 synthetic-data and agentic-data-generation papers
- any work published after those papers

For every related work extract:

- problem
- languages
- datasets
- model(s)
- synthetic generation method
- number of generated examples
- quality control
- use of agents
- evaluation
- human evaluation
- downstream evaluation
- limitations
- what SynthSEA can do differently

Create a novelty matrix.

---

# NOVELTY MATRIX

Create:

| Work | Year | Languages | Synthetic Data | Multi-Agent | Linguistic Experts | Cultural Grounding | Iterative Critique | Cross-Language | Downstream Fine-Tuning | Human Evaluation | Main Limitation | SynthSEA Difference |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|

Do not claim novelty unless the literature supports it.

If SynthSEA overlaps strongly with existing work, redesign the contribution.

---

# CENTRAL RESEARCH GAP

Investigate whether existing synthetic instruction generation methods suffer from:

## Problem 1 — English-centric generation

Investigate whether generating in English and translating causes:

- unnatural syntax
- cultural mismatch
- English semantic framing
- translation artifacts
- loss of local expressions
- loss of code-switching behavior
- unnatural discourse structures

## Problem 2 — Language-blind generation

Investigate whether generic LLMs fail to model:

- morphology
- local syntax
- regional vocabulary
- code-switching
- pragmatic markers
- honorifics
- discourse conventions
- cultural references

## Problem 3 — Quantity over quality

Investigate:

- duplicates
- hallucinations
- unnatural examples
- factual errors
- translation artifacts
- repetitive templates
- culturally inappropriate content
- incorrect code-switching
- language contamination

## Problem 4 — Weak validation

Investigate whether existing systems lack:

- language-specific validators
- cultural validators
- semantic validators
- factual validators
- diversity validators
- difficulty validators
- human evaluation

## Problem 5 — Lack of downstream evidence

A dataset is not useful merely because it looks fluent.

The key question is:

> Does training on SynthSEA-generated data actually improve model performance?

Downstream evaluation is mandatory.

---

# PROPOSED MULTI-AGENT ARCHITECTURE

Design SynthSEA as:

```text
INPUT
  ↓
Language Profile Agent
  ↓
Seed/Knowledge Acquisition Agent
  ↓
Topic & Cultural Context Agent
  ↓
Instruction Generation Agents
  ↓
Language Specialist Agent
  ↓
Code-Switching Agent
  ↓
Cultural Grounding Agent
  ↓
Semantic/Factual Verification Agent
  ↓
Difficulty & Diversity Agent
  ↓
Adversarial Critic Agent
  ↓
Judge / Aggregator Agent
  ↓
Refinement Agent
  ↓
Quality Gate
  ↓
Deduplication
  ↓
Final Synthetic Instruction Dataset
  ↓
Instruction Tuning
  ↓
Evaluation
```

Do not use multi-agent architecture merely because it sounds advanced.

Every major component must be experimentally justified.

---

# AGENT DEFINITIONS

## 1. Language Profile Agent

For every target language/variety create a machine-readable profile containing:

- language name
- ISO code where applicable
- regional variety
- writing system
- scripts
- morphology characteristics
- syntax characteristics
- common borrowed words
- code-switching patterns
- common transliteration practices
- dialect/variety information
- available datasets
- available benchmarks
- cultural context
- known NLP limitations

Do not invent linguistic facts.

Every linguistic claim must be backed by credible sources.

---

## 2. Resource Discovery Agent

Search and catalogue, where licensing permits:

- Hugging Face datasets
- GitHub repositories
- ACL Anthology
- ELRA/LDC
- Common Crawl-derived resources
- OSCAR
- CulturaX
- Wikipedia
- Wikidata
- FLORES
- NLLB resources
- SeaLLMs resources
- language-specific datasets
- Singapore government/open datasets
- academic corpora
- existing benchmarks

For each resource record:

- name
- language
- domain
- size
- license
- source
- quality
- availability
- training suitability
- evaluation suitability

Never scrape copyrighted content without checking licensing.

---

# 3. Cultural Context Agent

Generate culturally grounded topic/context pools.

Singapore domains may include:

- public transport
- MRT
- buses
- hawker centres
- food culture
- education
- workplaces
- housing
- HDB
- public services
- healthcare navigation
- multicultural communities
- festivals
- Singapore geography
- local social interactions
- workplace communication
- technology
- maritime industry
- manufacturing
- tourism
- environmental issues
- daily life
- local history

Do not stereotype.

Do not manufacture cultural facts.

Separate:

**factual cultural knowledge**

from

**synthetic conversational examples**.

---

# 4. Instruction Generation Agents

Generate multiple instruction categories.

## Knowledge

- factual QA
- explanation
- definition
- comparison

## Language

- translation
- transliteration
- grammar correction
- paraphrasing
- summarization

## NLP

- NER
- sentiment
- intent
- language identification
- code-switch identification
- classification

## Reasoning

- multi-step reasoning
- comparison
- decision-making
- planning

## Conversational

- dialogue
- customer support
- workplace interaction
- informal conversation

## Cultural

- Singapore-context QA
- culturally grounded scenarios
- local terminology interpretation

## Safety

- harmless refusal
- ambiguous queries
- misinformation correction

## Cross-lingual

- English → target language
- target language → English
- target language A → target language B

---

# 5. Language Specialist Agents

Create separate specialist agents.

## Singlish Specialist

Check:

- Singlish lexical items
- discourse particles
- syntax
- code-switching
- pragmatics
- naturalness
- Singapore-specific usage

Do not force Singlish into every sentence.

Distinguish:

- Standard Singapore English
- Colloquial Singapore English
- Singlish
- English with code-switching

Use evidence-based definitions.

## Malay Specialist

Check:

- Malay grammar
- morphology
- vocabulary
- spelling
- regional usage
- Singapore/Malaysia distinctions
- code-switching

## Tamil Specialist

Check:

- Tamil grammar
- script
- morphology
- colloquial vs formal Tamil
- Singapore Tamil where evidence exists
- transliteration
- code-switching

## Mandarin Specialist

Check:

- Simplified Chinese
- Singapore-context vocabulary
- Mandarin usage
- local lexical differences
- code-switching
- cultural context

Do NOT call Mandarin "low-resource" without justification.

---

# 6. Code-Switching Agent

Investigate:

- English–Malay
- English–Tamil
- English–Mandarin
- Malay–English
- Tamil–English
- Mandarin–English
- Singlish

Measure:

- switching points
- language proportions
- lexical borrowing
- intra-sentential switching
- inter-sentential switching
- transliterated words
- discourse particles

Do not artificially generate random mixed-language sentences.

Code-switching distributions should be evidence-based wherever possible.

---

# 7. Semantic Verification Agent

Check:

- instruction/response consistency
- semantic equivalence
- factual correctness
- missing information
- contradictions
- hallucinations
- answer completeness

Return structured scores.

---

# 8. Cultural Validation Agent

Check:

- Singapore relevance
- cultural appropriateness
- stereotypes
- fabricated cultural facts
- inappropriate localization
- unnatural references
- culturally insensitive outputs

---

# 9. Diversity Agent

Measure:

- lexical diversity
- syntactic diversity
- topic diversity
- instruction diversity
- answer diversity
- difficulty diversity
- reasoning diversity

Detect templated generations.

---

# 10. Difficulty Agent

Assign:

- Easy
- Medium
- Hard
- Expert

Difficulty must not be based solely on token count.

Use:

- reasoning steps
- linguistic complexity
- ambiguity
- context requirements
- cross-lingual complexity
- multi-hop reasoning

---

# 11. Adversarial Critic Agent

Actively try to reject generated examples.

Search for:

- hallucinations
- English leakage
- wrong language
- wrong script
- fake Singlish
- unnatural code-switching
- duplicate content
- cultural errors
- grammatical errors
- inconsistent answers
- overly simple instructions
- benchmark contamination
- memorized content

The critic should produce explicit failure reasons, not just a high score.

---

# 12. Judge Agent

Use multi-dimensional scoring:

- linguistic quality
- semantic correctness
- cultural grounding
- instruction quality
- diversity
- difficulty
- factuality
- safety

Do not choose weights arbitrarily.

Perform sensitivity analysis comparing:

- equal weights
- expert weights
- learned/calibrated weights

---

# 13. Refinement Agent

Use:

```text
Generate
→ Critique
→ Diagnose
→ Refine
→ Re-evaluate
```

Limit refinement rounds to control cost.

Compare one-pass generation against iterative refinement.

---

# 14. Final Quality Gate

Every example should receive structured metadata similar to:

```json
{
  "id": "",
  "language": "",
  "language_variety": "",
  "script": "",
  "instruction": "",
  "response": "",
  "task_type": "",
  "domain": "",
  "difficulty": "",
  "code_switching": false,
  "cultural_grounding": "",
  "source_context": "",
  "generation_model": "",
  "agent_trace": "",
  "quality_scores": {},
  "critic_feedback": "",
  "refinement_count": 0,
  "final_decision": "accept/reject"
}
```

Do not include hidden chain-of-thought.

Store only concise structured rationales/evaluation labels.

---

# DATASET DESIGN

Build at least:

## Tier A — Seed Data

Real human-created examples.

Use only datasets whose licenses permit intended research use.

## Tier B — Single-Agent Synthetic

Conventional single-agent baseline.

## Tier C — SynthSEA

Complete multi-agent pipeline.

## Optional Tier D — Translation Baseline

Generate English instructions and translate into target languages.

This baseline is important for testing:

**English → translation**

versus

**language-aware generation**.

---

# DATASET SIZE

Do NOT arbitrarily generate millions of examples.

Run a data-efficiency experiment with candidate sizes:

- 1K
- 5K
- 10K
- 25K
- 50K

Optimize:

> downstream performance per synthetic example

rather than raw dataset size.

---

# EXPERIMENTAL LANGUAGES

Primary Singapore case study:

1. Singlish / Singapore English
2. Malay
3. Tamil
4. Mandarin

Distinguish carefully between:

- language
- language variety
- regional usage
- cultural context
- code-switching

If literature shows one is unsuitable as a low-resource case, revise the terminology instead of forcing the classification.

---

# OPTIONAL EXTERNAL VALIDATION

If resources allow, add one Southeast Asian language such as:

- Indonesian
- Vietnamese
- Thai
- Tagalog
- Khmer
- Lao

Choose based on:

1. resource availability
2. CFP relevance
3. benchmark availability
4. script diversity
5. feasibility

Do not add languages merely to increase the dataset.

---

# BASELINE MODELS

Investigate:

- Qwen
- Llama
- Gemma
- SeaLLMs
- multilingual encoder models where appropriate

Teacher models:

- compare at least two teacher families if feasible
- do not assume the strongest commercial model is automatically best

Prefer open-source models for reproducibility.

---

# EXPERIMENT 1 — GENERATION QUALITY

Compare:

A. Human data

B. Single-agent synthetic data

C. Translation-generated data

D. SynthSEA

Metrics:

- linguistic quality
- semantic correctness
- cultural grounding
- diversity
- instruction quality
- factuality
- code-switch validity

Use automatic evaluation + human evaluation.

---

# EXPERIMENT 2 — DOWNSTREAM INSTRUCTION TUNING

Fine-tune the same base model under:

A. No synthetic data

B. Single-agent synthetic data

C. Translation synthetic data

D. SynthSEA

Control as much as possible:

- model
- training steps
- learning rate
- batch size
- compute budget

Measure downstream performance.

---

# EXPERIMENT 3 — ABLATION STUDY

Remove:

1. language specialist
2. cultural agent
3. code-switch agent
4. critic
5. refinement
6. diversity filter
7. factual validator
8. judge
9. multi-agent generation
10. full SynthSEA

This identifies which components actually matter.

---

# EXPERIMENT 4 — LANGUAGE TRANSFER

Train using one language and evaluate:

- same language
- another Singapore language
- cross-language

Investigate cross-lingual transfer.

---

# EXPERIMENT 5 — CULTURAL GROUNDING

Compare:

**Generic synthetic data**

vs

**Singapore-grounded synthetic data**

Measure:

- factual accuracy
- cultural relevance
- human preference
- downstream performance

---

# EXPERIMENT 6 — CODE-SWITCHING

Compare:

- monolingual synthetic data
- evidence-grounded code-switched synthetic data
- random code-switching

Evaluate whether realistic code-switching improves performance.

---

# EXPERIMENT 7 — DATA EFFICIENCY

Plot:

Synthetic examples

vs

Downstream performance.

Determine whether SynthSEA achieves higher performance with fewer examples.

---

# HUMAN EVALUATION

Where feasible, recruit appropriately qualified bilingual/multilingual annotators.

Evaluate:

1. Fluency
2. Naturalness
3. Linguistic correctness
4. Cultural appropriateness
5. Semantic correctness
6. Instruction quality
7. Code-switch authenticity
8. Overall usefulness

Use Likert scales.

Report:

- annotator count
- language proficiency
- annotation instructions
- sample selection
- inter-annotator agreement
- Cohen's kappa or Krippendorff's alpha where appropriate

Never claim human evaluation if it was not performed.

---

# AUTOMATIC METRICS

Investigate appropriate metrics rather than blindly using BLEU.

Potential metrics:

- BERTScore
- COMET
- chrF
- ROUGE where appropriate
- language identification accuracy
- perplexity
- lexical diversity
- type-token ratio
- distinct-n
- repetition rate
- semantic similarity
- factuality
- task-specific accuracy
- LLM-as-a-judge

Combine multiple metrics.

---

# LLM-AS-A-JUDGE

If using LLM judges:

- use at least two judge models if feasible
- test judge agreement
- position bias
- language bias
- self-preference
- consistency

Do not treat LLM-as-a-judge as ground truth.

---

# STATISTICAL ANALYSIS

Major claims require statistical evidence.

Use:

- confidence intervals
- bootstrap resampling
- paired tests where appropriate
- effect sizes
- significance testing
- multiple-comparison correction where appropriate

Report variance across multiple runs where feasible.

---

# DATA LEAKAGE / CONTAMINATION

Investigate:

- benchmark contamination
- training-data overlap
- Wikipedia overlap
- test-set leakage
- memorized instructions
- synthetic-to-test similarity

Keep evaluation datasets completely isolated.

Never use test examples as generation seeds.

---

# DATA PROVENANCE

Every synthetic example should be traceable to:

- source context
- generation model
- generation configuration
- agent pipeline version
- validation result
- timestamp
- dataset version

Create a dataset manifest.

---

# REPRODUCIBILITY

Use a modular repository:

```text
SynthSEA/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── pyproject.toml
├── configs/
│   ├── languages.yaml
│   ├── generation.yaml
│   ├── evaluation.yaml
│   └── models.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   ├── synthetic/
│   └── evaluation/
├── agents/
│   ├── language_profile.py
│   ├── resource_discovery.py
│   ├── topic_generator.py
│   ├── instruction_generator.py
│   ├── language_specialist.py
│   ├── code_switch_validator.py
│   ├── cultural_validator.py
│   ├── factual_validator.py
│   ├── diversity_validator.py
│   ├── critic.py
│   ├── judge.py
│   └── refinement.py
├── generation/
├── filtering/
├── training/
├── evaluation/
├── analysis/
├── visualization/
├── experiments/
├── notebooks/
├── paper/
└── tests/
```

---

# ENGINEERING REQUIREMENTS

Use:

- Python
- PyTorch
- Hugging Face Transformers
- Datasets
- PEFT/LoRA where appropriate
- Accelerate
- vLLM where useful
- Pydantic for structured outputs
- YAML configuration
- logging
- experiment tracking

Teacher APIs should be supported through adapters.

---

# COST CONTROL

Implement:

- caching
- batching
- asynchronous generation
- retry logic
- rate limiting
- structured outputs
- model routing
- deduplication before expensive evaluation
- configurable agent execution
- token/cost tracking

Every experiment should report:

- number of examples
- input tokens
- output tokens
- model
- estimated cost
- generation time
- GPU/CPU usage where possible

---

# AGENT ORCHESTRATION COMPARISON

Compare:

### Pipeline A

Single LLM

### Pipeline B

Generator + Critic

### Pipeline C

Generator + Language Specialist + Critic

### Pipeline D

Full SynthSEA

If additional agents do not improve results, simplify the architecture.

---

# PROMPT ENGINEERING

Store prompts as version-controlled templates:

```text
prompts/
├── generation/
├── language/
├── culture/
├── validation/
├── criticism/
└── judging/
```

Do not hard-code prompts throughout Python.

Track prompt versions.

---

# LANGUAGE PROFILE CONFIGURATION

Proposed initial structure:

```yaml
languages:

  singlish:
    display_name: "Colloquial Singapore English"
    region: "Singapore"
    type: "regional variety"
    script: "Latin"

  malay:
    display_name: "Malay"
    region: "Singapore"
    type: "language"
    script: "Latin"

  tamil:
    display_name: "Tamil"
    region: "Singapore"
    type: "language"
    script: "Tamil"

  mandarin:
    display_name: "Singapore-context Mandarin"
    region: "Singapore"
    type: "language/variety"
    script: "Simplified Chinese"
```

Do not finalize labels until literature validates them.

---

# IMPORTANT: CULTURAL GROUNDING

Never create artificial facts such as:

- fake Singapore institutions
- fake festivals
- fake locations
- fake government policies
- fake cultural traditions

For factual cultural examples, ground generation in trusted sources.

For conversational examples, clearly label them synthetic.

---

# DATASET SCHEMA

Create a Hugging Face-compatible dataset containing:

```text
id
language
language_variety
script
region
domain
task_type
difficulty
instruction
context
response
code_switching
code_switch_languages
cultural_grounding
source_type
source_id
generation_model
generation_temperature
agent_pipeline
quality_score
linguistic_score
semantic_score
cultural_score
diversity_score
factuality_score
critic_score
refinement_rounds
accepted
```

Do not store hidden chain-of-thought.

---

# RESEARCH QUESTIONS

Develop and test:

## RQ1

Does multi-agent generation produce higher-quality synthetic instruction data than single-agent generation?

## RQ2

Does language-specialized validation improve linguistic correctness?

## RQ3

Does cultural grounding improve human-perceived relevance and factual accuracy?

## RQ4

Does SynthSEA improve downstream instruction-following performance?

## RQ5

Does SynthSEA provide better data efficiency than conventional synthetic generation?

## RQ6

Does the framework generalize across linguistically different Singapore languages and varieties?

## RQ7

Does realistic code-switching improve multilingual instruction tuning?

## RQ8

Which agents contribute most to final performance?

---

# HYPOTHESES

Develop formal hypotheses such as:

### H1

SynthSEA-generated data will achieve higher linguistic quality than single-agent synthetic data.

### H2

Culturally grounded generation will improve cultural relevance.

### H3

Multi-agent validation will reduce hallucination and linguistic error rates.

### H4

Models fine-tuned on SynthSEA data will outperform models trained on equal-sized single-agent datasets.

### H5

SynthSEA will achieve higher performance per training example.

### H6

Language-specialized agents will provide larger gains for resource-constrained languages/varieties than generic validation.

Do not assume these hypotheses are true. Test them.

---

# PAPER CONTRIBUTIONS

Aim for contributions such as:

1. A multilingual Singapore-focused resource for synthetic instruction generation.
2. SynthSEA, a modular multi-agent framework for linguistically and culturally grounded synthetic instruction generation.
3. Controlled comparison of translation-based, single-agent, and multi-agent synthetic generation.
4. Systematic evaluation of linguistic, cultural, diversity, and factual quality.
5. Downstream evaluation showing whether synthetic data improves multilingual LLM performance.

Only claim contributions actually supported by experiments.

---

# RELATED WORK STRUCTURE

Organize literature review into:

1. Low-resource NLP
2. Southeast Asian NLP
3. Singapore multilingual NLP
4. Singlish NLP
5. Code-switching
6. Multilingual LLMs
7. Instruction tuning
8. Synthetic instruction generation
9. Multi-agent LLM systems
10. Cultural grounding
11. Synthetic data quality evaluation
12. Human evaluation of multilingual generation

For each section:

**What exists → what is missing → what SynthSEA contributes.**

---

# LITERATURE SEARCH PROTOCOL

Search:

- ACL Anthology
- EMNLP
- NAACL
- COLING
- EACL
- NeurIPS
- ICLR
- ICML
- AAAI
- IJCAI
- arXiv
- Google Scholar
- Semantic Scholar

Prioritize peer-reviewed work.

Use 2024–2026 research heavily for novelty analysis.

Search variations of:

```text
"synthetic instruction generation" low resource languages
"synthetic instruction tuning" Southeast Asia
"multi-agent" synthetic data instruction tuning
"multi-agent" instruction generation
Singlish NLP
Singapore English NLP
Singapore multilingual NLP
Singapore Tamil NLP
Singapore Malay NLP
Singapore Mandarin NLP
Southeast Asian multilingual LLM
SEA LLM instruction tuning
code switching Southeast Asia LLM
Malay instruction tuning
Tamil instruction tuning
Chinese instruction tuning Southeast Asia
culturally grounded synthetic data
low-resource multilingual LLM
synthetic data cultural grounding NLP
```

Also search for papers published in 2026.

---

# LITERATURE DATABASE

Create:

`literature.csv`

with:

```text
id
title
authors
year
venue
url
doi
languages
dataset
method
multi_agent
synthetic_data
cultural_grounding
evaluation
main_result
limitations
relevance_to_synthsea
novelty_risk
```

---

# NOVELTY GATE

Before full implementation create:

`NOVELTY_REPORT.md`

containing:

1. Closest 20 papers
2. Top 10 closest systems
3. Overlap analysis
4. Novel components
5. Potential reviewer criticisms
6. Required changes
7. Final research question
8. Final title recommendation

If novelty is weak, STOP and propose a revised research design.

---

# REVIEWER RED-TEAM

Act as:

## Reviewer A — NLP

Ask:

- Is the NLP contribution novel?
- Is the dataset meaningful?
- Are baselines sufficient?

## Reviewer B — Multilingual/Low-resource NLP

Ask:

- Are languages genuinely under-resourced?
- Is cultural grounding scientifically justified?
- Are linguistic claims accurate?

## Reviewer C — ML

Ask:

- Are experiments controlled?
- Are gains statistically significant?
- Is multi-agent architecture actually necessary?

Generate a reviewer-risk report.

---

# EXPECTED FAILURE MODES

Investigate:

1. hallucinated local facts
2. fake Singlish
3. wrong code-switching
4. English leakage
5. wrong script
6. translation artifacts
7. excessive repetition
8. synthetic style collapse
9. model bias
10. cultural stereotypes
11. dataset contamination
12. evaluation leakage
13. LLM judge bias
14. agent redundancy
15. increased cost without performance gain

---

# SCIENTIFIC PRINCIPLE

Do NOT argue:

> "More agents = better."

Instead test:

> **Which linguistic and validation capabilities are necessary for high-quality synthetic instruction generation?**

---

# COMPUTATIONAL EFFICIENCY

Measure:

- generation cost
- inference latency
- number of agent calls
- tokens consumed
- quality improvement per agent
- quality improvement per dollar
- quality improvement per 1K generated samples

If SynthSEA is more expensive, quantify the trade-off.

---

# FINAL EVALUATION OUTPUTS

Create:

```text
results/
├── generation_quality.csv
├── downstream_results.csv
├── ablation_results.csv
├── human_evaluation.csv
├── cost_analysis.csv
├── language_comparison.csv
└── statistical_tests.csv
```

Generate publication-quality plots:

1. Quality vs dataset size
2. Performance vs dataset size
3. Single-agent vs SynthSEA
4. Translation vs SynthSEA
5. Language-wise performance
6. Ablation study
7. Cost vs quality
8. Cultural grounding effect
9. Code-switching effect
10. Data efficiency

---

# PAPER FIGURES

Prepare:

### Figure 1
SynthSEA architecture.

### Figure 2
Synthetic data generation lifecycle.

### Figure 3
Quality-control pipeline.

### Figure 4
Language-wise performance.

### Figure 5
Ablation results.

### Figure 6
Data-efficiency curve.

### Figure 7
Cost-quality trade-off.

---

# PAPER TABLES

Prepare:

### Table 1
Dataset statistics.

### Table 2
Related-work comparison.

### Table 3
Synthetic generation quality.

### Table 4
Downstream model performance.

### Table 5
Ablation study.

### Table 6
Human evaluation.

### Table 7
Cost and efficiency.

---

# DATASET STATISTICS

For every language report:

- number of samples
- average instruction length
- average response length
- vocabulary size
- lexical diversity
- task distribution
- domain distribution
- difficulty distribution
- code-switch rate
- rejection rate
- refinement rate
- factual-error rate
- linguistic-error rate

---

# REPRODUCIBILITY CHECKLIST

- [ ] All datasets have licenses checked
- [ ] All source datasets documented
- [ ] All prompts version-controlled
- [ ] Random seeds recorded
- [ ] Model versions recorded
- [ ] Generation configurations stored
- [ ] Evaluation datasets isolated
- [ ] No test leakage
- [ ] Costs recorded
- [ ] Human evaluation protocol documented
- [ ] Statistical tests performed
- [ ] Code runs from clean environment
- [ ] README reproduces experiments
- [ ] Dataset card created
- [ ] Model card created
- [ ] Ethical considerations documented

---

# ETHICS

Investigate:

- cultural stereotyping
- language marginalization
- synthetic misinformation
- representation bias
- misuse of synthetic cultural data
- privacy
- copyright
- dataset licensing
- demographic bias
- dialect discrimination

Do not claim synthetic data is inherently unbiased.

---

# PAPER TITLE SEARCH

Evaluate:

### Option A

**SynthSEA: Multi-Agent Synthetic Instruction Generation for Resource-Uneven Southeast Asian Languages**

### Option B

**SynthSEA: Culturally Grounded Multi-Agent Synthetic Instruction Generation for Southeast Asian NLP**

### Option C

**SynthSEA: Language-Aware Multi-Agent Synthetic Instruction Generation for Southeast Asian LLMs**

### Option D

**SynthSEA: Quality-Controlled Synthetic Instruction Generation for Multilingual Southeast Asian Language Models**

Recommend the title based on the actual contribution.

---

# ABSTRACT REQUIREMENTS

Do not write the final abstract until experiments are complete.

It must contain:

1. Problem
2. Gap
3. Proposed method
4. Languages
5. Dataset/resource
6. Experimental setup
7. Main quantitative result
8. Key finding
9. Contribution

Never fabricate numbers. Use placeholders until experiments produce results.

---

# PAPER STRUCTURE

1. Introduction
2. Related Work
3. Research Gap
4. SynthSEA Framework
5. Language and Cultural Profiles
6. Synthetic Dataset Construction
7. Quality-Control Framework
8. Experimental Setup
9. Results
10. Ablation Study
11. Human Evaluation
12. Error Analysis
13. Discussion
14. Limitations
15. Ethics
16. Conclusion

---

# ERROR ANALYSIS

Manually inspect failures and categorize:

- linguistic
- semantic
- factual
- cultural
- code-switching
- translation
- reasoning
- hallucination
- formatting
- instruction ambiguity

Use representative examples only where licensing permits.

---

# DEVELOPMENT PHASES

## PHASE 0 — Research Reconnaissance

Deliver:

- literature review
- novelty matrix
- language resource matrix
- closest-work analysis
- reviewer-risk analysis

Do NOT code the full framework yet.

## PHASE 1 — Dataset/Resource Audit

Identify:

- datasets
- benchmarks
- licenses
- evaluation sets
- language resources
- Singapore-specific resources

Deliver:

`RESOURCE_AUDIT.md`

## PHASE 2 — Baseline Generation

Implement:

- single-agent generation
- translation baseline
- basic quality filtering

## PHASE 3 — SynthSEA MVP

Implement:

- language specialist
- cultural validator
- critic
- judge
- refinement

## PHASE 4 — Full Experimentation

Run:

- generation quality
- downstream tuning
- ablation
- cross-language
- code-switching
- data efficiency
- cost analysis

## PHASE 5 — Human Evaluation

Design and execute rigorous annotation.

## PHASE 6 — Statistical Analysis

Generate all tables and plots.

## PHASE 7 — Paper Preparation

Write:

- methodology
- experiments
- results
- discussion
- limitations
- ethics

Only use measured results.

---

# GITHUB REPOSITORY QUALITY

README must contain:

1. Project overview
2. Research motivation
3. Architecture
4. Supported languages
5. Installation
6. Dataset preparation
7. Generation
8. Validation
9. Training
10. Evaluation
11. Reproduction commands
12. Configuration
13. License
14. Citation

---

# FINAL SUCCESS CRITERIA

Do NOT consider SynthSEA successful merely because:

- code runs
- thousands of examples are generated
- outputs look fluent
- an LLM judge gives high scores

SynthSEA is successful only if experiments demonstrate meaningful evidence for some combination of:

1. Better linguistic quality
2. Better cultural grounding
3. Better diversity
4. Lower hallucination/error rates
5. Better code-switching quality
6. Better downstream performance
7. Better data efficiency
8. Better cross-language transfer
9. Meaningful improvement over simpler baselines
10. Scientifically defensible contribution to Southeast Asian NLP

---

# FIRST TASK — DO THIS BEFORE IMPLEMENTATION

Start by producing ONLY:

## A. Executive Research Assessment

Is SynthSEA worth pursuing?

## B. Novelty Analysis

What has already been done?

## C. Research Gap

What is genuinely missing?

## D. Recommended Final Research Question

One precise question.

## E. Recommended Hypotheses

H1–H6.

## F. Recommended Languages

Explain why each language/variety is included.

## G. Closest Competing Papers

At least 20.

## H. Novelty Matrix

Full comparison.

## I. Proposed SynthSEA Architecture

Detailed architecture.

## J. Experimental Design

Baselines + datasets + models + metrics + ablations.

## K. Risks

What could cause rejection?

## L. Final Recommendation

Go / Modify / Stop.

**DO NOT start implementing the entire system until this research assessment is complete.**

---

# NON-NEGOTIABLE RULES

1. Never fabricate references.
2. Never fabricate datasets.
3. Never fabricate experimental results.
4. Never fabricate human evaluation.
5. Never claim a language is low-resource without evidence.
6. Never claim novelty without literature comparison.
7. Never use test data for training.
8. Never silently ignore licensing.
9. Never treat LLM-as-a-judge as absolute ground truth.
10. Never generate culturally sensitive claims without validation.
11. Never store hidden chain-of-thought.
12. Never make the multi-agent architecture unnecessarily complicated.
13. Every major architectural component must have an ablation.
14. Every major claim must have evidence.
15. Prefer measurable research contributions over engineering complexity.
16. Prefer a smaller, high-quality dataset over a huge noisy dataset.
17. Report negative results honestly.
18. Reproduce existing baselines wherever feasible.
19. Clearly distinguish language, dialect, regional variety, and code-switching.
20. Keep the entire project reproducible.
