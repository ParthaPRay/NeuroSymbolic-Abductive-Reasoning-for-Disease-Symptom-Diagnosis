# Ranking of Neurosymbolic Abductive Reasoning for NLP Pipeline for Disease Symptom
# Partha Pratim Ray, parthapratimray1986@gmail.com
# 29/07/2025

import logging
import spacy
import pandas as pd
import re
from pyswip import Prolog

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

SHOW_CODE = True  # Set to True to display UMLS code + human name, False for just names

def slugify(text):
    """Generate a unique ASCII-safe slug for Prolog use."""
    text = str(text).strip()
    text = re.sub(r'^UMLS:', '', text, flags=re.IGNORECASE)
    text = text.replace(':', '_').replace(' ', '_').lower()
    text = re.sub(r'[^a-z0-9_]', '', text)
    if not text.startswith("umls_"):
        text = "umls_" + text
    return text

def as_pystr(x):
    """Force a native ASCII Python string."""
    if isinstance(x, bytes):
        x = x.decode('utf-8', errors='ignore')
    s = str(x) if not isinstance(x, str) else x
    return s.encode('ascii', errors='ignore').decode()

def human_label(slug, show_code=SHOW_CODE):
    """Convert 'umls_c0008031_pain_chest' -> 'pain chest' or 'C0008031: pain chest' if show_code."""
    slug = as_pystr(slug)
    code_match = re.match(r'^umls[_:](c[0-9]+)_(.+)', slug, flags=re.IGNORECASE)
    if code_match:
        code, label = code_match.groups()
    else:
        label = re.sub(r'^umls[_:]', '', slug, flags=re.IGNORECASE)
        label = re.sub(r'^c[0-9]+_', '', label)
        code = None
    label = label.replace('_', ' ')
    if show_code and code:
        return f"{code.upper()}: {label}"
    return label

nlp = spacy.load("en_core_web_trf")  # Transformer pipeline
ruler = nlp.add_pipe("entity_ruler", before="ner")

XLSX_FILE = "flattened_url.xlsx"

def load_symptoms_for_ruler(xlsx_file):
    unique_symptoms = set()
    df = pd.read_excel(xlsx_file, dtype=str)
    for row in df.itertuples(index=False):
        for s in as_pystr(row.Symptom).split(','):
            s = as_pystr(s).strip()
            label = re.sub(r'^UMLS:[^_]*_', '', s, flags=re.IGNORECASE)
            if label:
                unique_symptoms.add(label.lower())
    patterns = [{"label": "SYMPTOM", "pattern": s} for s in unique_symptoms]
    return patterns

biomedical_patterns = load_symptoms_for_ruler(XLSX_FILE)
ruler.add_patterns(biomedical_patterns)

prolog = Prolog()
disease_label_map = {}
symptom_label_map = {}

def load_prolog_from_xlsx(xlsx_file):
    df = pd.read_excel(xlsx_file, dtype=str)
    for row in df.itertuples(index=False):
        d_raw = as_pystr(row.Disease).strip()
        d_slug = slugify(d_raw)
        disease_label_map[d_slug] = d_raw
        for s_raw in as_pystr(row.Symptom).split(','):
            s_raw = as_pystr(s_raw).strip()
            s_slug = slugify(s_raw)
            symptom_label_map[s_slug] = s_raw
            try:
                prolog.assertz("has_symptom(%p, %p)", as_pystr(d_slug), as_pystr(s_slug))
            except Exception as e:
                logging.error(f"Error asserting fact: has_symptom({d_slug}, {s_slug}) - {e}")

load_prolog_from_xlsx(XLSX_FILE)

def extract_symptoms(text):
    doc = nlp(text)
    matches = []
    for ent in doc.ents:
        if ent.label_ == "SYMPTOM":
            ent_label = ent.text.strip().lower()
            ent_slug = slugify(ent_label)
            found = False
            for slug, full_label in symptom_label_map.items():
                if ent_label in as_pystr(full_label).lower() or ent_label.replace(' ', '_') in slug:
                    matches.append(as_pystr(slug))
                    found = True
                    break
            if not found:
                matches.append(as_pystr(ent_slug))
    return matches

def abductive_explanation(symptoms):
    explanation = {}
    for symptom in symptoms:
        try:
            for result in prolog.query("has_symptom(Disease, %p)", as_pystr(symptom)):
                disease = result["Disease"]
                explanation.setdefault(disease, set()).add(symptom)
        except Exception as e:
            logging.error(f"Error querying for symptom {symptom}: {e}")
    return explanation

def differential_diagnosis(symptoms):
    explanation = abductive_explanation(symptoms)
    ranked = sorted(explanation.items(), key=lambda x: len(x[1]), reverse=True)
    return ranked

def show_differential(ranked, symptoms):
    print("\n=== Differential Diagnosis ===")
    if not ranked:
        print("No diseases in the knowledge base explain any of the observed symptoms.")
        return
    print("Observed symptoms:")
    for s in symptoms:
        print(f"  - {human_label(s)}")
    print("\nRank | Disease                        | #Match/Total | %   | Matched Symptoms")
    print("-"*90)
    for i, (disease, syms) in enumerate(ranked, 1):
        d_label = human_label(disease)
        percent = 100 * len(syms) / len(symptoms) if symptoms else 0
        sym_labels = [human_label(sym) for sym in syms]
        print(f"{i:>4} | {d_label:<30} | {len(syms)}/{len(symptoms):<9} | {percent:4.1f} | {', '.join(sym_labels)}")
    # Most plausible (explains all symptoms)
    top = [(i+1, d, s) for i, (d, s) in enumerate(ranked) if len(s) == len(symptoms)]
    if top:
        print("\nMost plausible (explain all symptoms):")
        print("Rank | Disease                        | #Match/Total | %   | Matched Symptoms")
        print("-"*90)
        for rank, d, syms in top:
            d_label = human_label(d)
            sym_labels = [human_label(sym) for sym in syms]
            print(f"{rank:>4} | {d_label:<30} | {len(syms)}/{len(symptoms):<9} | 100.0 | {', '.join(sym_labels)}")
    else:
        print("\nNo single disease explains all symptoms. Highest coverage shown above.")
    # Highlight unexplained symptoms
    explained = set(sym for r in ranked for sym in r[1])
    unexplained = [s for s in symptoms if s not in explained]
    if unexplained:
        print("\nUnexplained symptoms:", ", ".join(human_label(s) for s in unexplained))

if __name__ == "__main__":
    print("Welcome to the XLSX-Driven Medical Abductive Reasoning System (UMLS code format)!\n")
    print("Type a symptom list or clinical text. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nEnter patient symptoms or description: ")
            if user_input.strip().lower() == "exit":
                print("Goodbye!")
                break
            symptoms = extract_symptoms(user_input)
            if not symptoms:
                print("No symptoms recognized in your input.")
                continue
            ranked = differential_diagnosis(symptoms)
            show_differential(ranked, symptoms)
        except Exception as e:
            logging.error(f"Error in diagnosis: {e}")

