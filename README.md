# NeuroSymbolic Abductive Reasoning for Disease–Symptom Diagnosis

**A Hybrid NLP–Symbolic Framework for Transparent Clinical Reasoning**

---

## Overview

This repository implements a **neurosymbolic AI NLP pipeline** that integrates deep neural natural language processing with symbolic logic programming for interpretable clinical diagnosis. Our system ingests free-text patient descriptions, automatically extracts biomedical symptoms via advanced NLP, and performs **abductive inference** over a structured disease–symptom knowledge base using Prolog. Differential diagnoses are ranked and explained using UMLS codes, offering both accuracy and transparency.

> **Scientific motivation:**
> Bridging neural and symbolic AI enables interpretable, data-driven clinical support that is accessible, extensible, and compatible with biomedical ontologies. This repository aims to facilitate reproducible research at the intersection of NLP, explainable AI, and medical reasoning.

---
## The work uses dataset as prepared in below github

  * Dataset [https://github.com/ParthaPRay/Disease-Symptom-Knowledge-Database_Flattening](https://github.com/ParthaPRay/Disease-Symptom-Knowledge-Database_Flattening)  
---

## Key Features

* **End-to-End Neurosymbolic Pipeline:**

  * State-of-the-art symptom extraction using `spaCy` (transformer-based) with custom entity ruler for biomedical concepts.
  * Symbolic abductive inference for (disease, symptom) mapping, leveraging SWI-Prolog via `pyswip`.
  * UMLS-compatible output with flexible code–label display.

* **Transparent and Interpretable Outputs:**

  * Ranks candidate diagnoses by coverage and presents matched and unmatched symptoms.
  * Clear tabular display of diagnostic reasoning steps.

* **Data-Driven and Extensible:**

  * Disease–symptom relations are loaded dynamically from a user-editable Excel sheet (`flattened_url.xlsx`), supporting easy knowledge base updates and domain adaptation.
  * Compatible with standard clinical vocabularies (UMLS).

* **Reproducible and Modular:**

  * Pythonic pipeline with open-source dependencies.
  * CLI interface for rapid testing and integration.

---

## Installation

### Prerequisites

* **Python 3.8+**
* **SWI-Prolog** (for symbolic reasoning)

  * Ubuntu: `sudo apt install swi-prolog`
  * MacOS: `brew install swi-prolog`
  * Windows: [Official Download](https://www.swi-prolog.org/Download.html)

### Python Dependencies

Add to `requirements.txt`:

```
spacy
pandas
openpyxl
pyswip
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

Install spaCy transformer pipeline and model:

```bash
pip install spacy[transformers]
python -m spacy download en_core_web_trf
```

---

## Knowledge Base Format

Prepare an Excel file named `flattened_url.xlsx` with at least the following columns:

* **Disease** (string): Disease or disorder name (optionally UMLS code).
* **Symptom** (string): One or more symptoms per row, comma-separated (optionally UMLS codes).

Example row:

| Disease               | Symptom                                |
| --------------------- | -------------------------------------- |
| Myocardial Infarction | pain chest, rale, palpitation, syncope |
| Alzheimer's Disease   | agitation, drool, frail, tremor        |

Place this file in the project directory.

---

## Usage

```bash
python your_script.py
```

Example CLI session:

```
Welcome to the XLSX-Driven Medical Abductive Reasoning System (UMLS code format)!

Enter patient symptoms or description: polyuria, polydipsia, pain chest, syncope

=== Differential Diagnosis ===
Observed symptoms:
  - C0034642: rale
  - C0030252: palpitation
  - C0039070: syncope
  - C0008031: pain chest

Rank | Disease                        | #Match/Total | %     | Matched Symptoms
------------------------------------------------------------------------------------------
   1 | C0027051: myocardial infarction | 4/4         | 100.0 | ...
   ...
```

---

## Methodology

* **Symptom Extraction:**
  Free-text input is processed with a spaCy transformer pipeline augmented with a custom entity ruler, mapping recognized entities to canonical symptom forms.
* **Symbolic Reasoning:**
  Disease–symptom relations are compiled from the Excel file into SWI-Prolog. The system queries which diseases can best explain the observed symptoms (abductive inference), ranks candidates, and provides transparent, step-wise outputs.
* **Interpretability:**
  All outputs use UMLS codes (if available) with human-readable labels. The system highlights both covered and uncovered symptoms for complete diagnostic traceability.

---

## Reproducibility Checklist

* [x] Fully open-source Python code
* [x] Complete dependency list
* [x] Minimal configuration: Excel-based KB, standard NLP models
* [x] Platform tested: Linux, macOS, Windows (with SWI-Prolog)

---

## Applications

* **Clinical Decision Support** (for research and prototyping)
* **Medical NLP Benchmarking**
* **Explainable AI Experiments**
* **Curriculum for AI–XAI in Healthcare**

---

## Citation

If you use or adapt this work, please cite:

```
@software{ray2025neurosymbolic,
  author = {Partha Pratim Ray},
  title = {NeuroSymbolic Abductive Reasoning for Disease--Symptom Diagnosis},
  year = {2025},
  url = {https://github.com/your-repo-url}
}
```

---

## Disclaimer

This software is **for research and educational use only**.
**It is not a substitute for professional medical advice, diagnosis, or treatment.**

---

## Author

**Partha Pratim Ray**
Assistant Professor, Department of Computer Applications, Sikkim University
Contact: [parthapratimray1986@gmail.com](mailto:parthapratimray1986@gmail.com)
[LinkedIn](https://www.linkedin.com/in/parthapratimray1986/) | [ORCID](https://orcid.org/0000-0003-2306-2792)

---

## Contributing

Contributions, bug reports, and scientific collaborations are highly welcome.
Please open an issue or pull request to get involved.

---

**Empowering explainable, data-driven medicine through neurosymbolic AI.**

