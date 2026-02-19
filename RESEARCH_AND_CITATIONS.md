# 📚 SCIENTIFIC FOUNDATIONS, RESEARCH & CITATIONS
## *The MrIridescent Forensic ATS Methodology*
### **Authored by David Akpoviroro Oke**
#### *Systems Architect | AI Researcher | Digital Polymath*
**Date**: February 19, 2026

---

## 1. ABSTRACT
Modern recruitment is plagued by "Keyword Arms Races" between candidates using LLMs to optimize resumes and HR departments using legacy boolean search. This research presents the **MrIridescent Forensic Matching Engine**, a hybrid architecture combining **Distributed Semantic Vectors** and **Multi-Agent Meta-Cognition** (CrewAI) to extract authentic professional value. We demonstrate a "Forensic" approach to resume parsing that treats text as evidence rather than mere data.

---

## 2. THEORETICAL FOUNDATIONS

### 2.1 Distributional Semantics & Vector Space Models
The system core relies on the **Distributional Hypothesis**—the idea that words occurring in similar contexts have similar meanings.
- **spaCy & GloVe**: We leverage Global Vectors for Word Representation (GloVe) to map skills into a 300-dimensional vector space.
  - *Citation*: Pennington, J., Socher, R., & Manning, C. D. (2014). GloVe: Global Vectors for Word Representation. *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)*.
- **Cosine Similarity**: Matching is performed by calculating the angular distance between the "Requirement Vector" (JD) and the "Capability Vector" (Resume).
  - *Reference*: Mikolov, T., et al. (2013). Efficient Estimation of Word Representations in Vector Space. *arXiv:1301.3781*.

### 2.2 Agentic Orchestration & Self-Refinement
To solve the "LLM Hallucination" problem, the system implements a **Validator-Auditor Pattern**.
- **CrewAI**: Orchestrates autonomous agents with specific personas (The JD Structurer vs. The Forensic Auditor).
- **Self-Refine Methodology**: The system uses iterative feedback loops where the Auditor Agent critiques the Structurer's output against the raw source PDF text.
  - *Citation*: Madaan, A., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. *arXiv:2303.17651*.

---

## 3. PROPRIETARY ALGORITHMS: "FORENSIC SCORING"

### 3.1 Strict Experience Relevance (SER) Gate
The SER algorithm prevents "Experience Inflation" by verifying that a skill (e.g., "PostgreSQL") is co-located in the text within a relevant Job Title context (e.g., "Backend Engineer").
- **SER Logic**: `Score = (Semantic_Title_Match > 0.8) AND (Tech_In_Job_Description == True)`.

### 3.2 Temporal Verification
The system calculates the duration of specific tech stacks by identifying date-ranges within professional experience nodes, preventing candidates from claiming "5 years of Python" when their history only shows 1 year.

---

## 4. CYBERSECURITY & ADVERSARIAL ROBUSTNESS
As a **Purple Teamer**, I have built this system to be robust against "White-Text Hacking"—the practice of hiding JD keywords in white font on a resume to trick legacy ATS.
- **Raw Text Normalization**: The system extracts raw text using `PyMuPDF` and normalizes all characters, exposing hidden text before it reaches the AI engine.

---

## 5. LITERATURE REVIEW & REFERENCES

1.  **Devlin, J., et al. (2018)**. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. (Theoretical basis for our transformer-based extraction).
2.  **Honnibal, M., & Montani, I. (2017)**. *spaCy 2: Industrial-strength Natural Language Processing in Python*.
3.  **Lewis, P., et al. (2020)**. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. (Inspiration for our RAG-style validation of resume claims).
4.  **Sutton, R. S., & Barto, A. G. (2018)**. *Reinforcement Learning: An Introduction*. (Influenced our agentic feedback loops).

---

## 6. USE CASES & EXPERIMENTAL RESULTS

### 6.1 Abstract Scenario: The "Polymath Match"
In internal testing, the system was tasked with finding a "Renaissance Tech Lead." Legacy systems ranked candidates by the number of languages known. The **MrIridescent Engine** correctly ranked highest a candidate who demonstrated "Architectural Leadership" and "Cross-Domain Competence," identifying semantic overlaps between "Ethical Hacking" and "Secure Coding."

---

*“Logic is the anatomy of thought.”* — **MrIridescent Research Group**
