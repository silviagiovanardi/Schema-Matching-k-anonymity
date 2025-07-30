
import pandas as pd
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.generalization import generalize_year_to_decade
from lib.file_utils import save_csv

def refined_generalize_label(label):
    if pd.isna(label):
        return "Unknown"
    label = label.lower()

    if any(word in label for word in ["diabetes", "hyperglycemia", "obesity", "lipid", "metabolic", "glucose"]):
        return "Metabolic"

    if any(word in label for word in ["heart", "cardiac", "hypertension", "coronary", "vascular", "myocardial"]):
        return "Cardiovascular"

    if any(word in label for word in ["depression", "anxiety", "bipolar", "mental", "schizophrenia", "mood"]):
        return "Mental Health"

    if any(word in label for word in ["asthma", "bronchitis", "respiratory", "copd", "pneumonia", "lung"]):
        return "Respiratory"

    if any(word in label for word in ["vaccine", "vaccination", "immunization", "influenza", "booster"]):
        return "Vaccination"

    if any(word in label for word in ["cancer", "neoplasm", "tumor", "malignancy", "leukemia"]):
        return "Neoplastic"

    if any(word in label for word in ["fracture", "injury", "accident", "trauma", "wound"]):
        return "Trauma"

    if any(word in label for word in ["surgery", "operation", "appendectomy", "bypass", "surgical"]):
        return "Surgical"

    if any(word in label for word in ["eye", "vision", "hearing", "dental", "ear", "sensory"]):
        return "Sensory"

    if any(word in label for word in ["infection", "viral", "bacterial", "fever", "infectious", "sepsis"]):
        return "Infectious"

    return "Other"

def anonimizza_k5():

    print("Anonimizzazione k=5 in corso…")
    df = pd.read_csv("data1/omop_synthetic_patients_with_labels.csv")

    df["year_decade"] = df["year_of_birth"].apply(generalize_year_to_decade)

    condition_cols = ["condition_1_name", "condition_2_name"]
    procedure_cols = ["procedure_1_name", "procedure_2_name"]
    observation_cols = ["observation_1_name", "observation_2_name"]

    for col in condition_cols + procedure_cols:
        df[col + "_cat"] = df[col].apply(refined_generalize_label)
    for col in observation_cols:
        df[col + "_cat"] = "Observation"

    qid = ["person_id", "gender_concept_id", "race_concept_id", "year_decade",
            "condition_1_name_cat", "procedure_1_name_cat", "observation_1_name_cat"]
    df[qid].to_csv("data/omop_k5_final.csv", index=False)
    print("Salvato: data/omop_k5_final.csv")

if __name__ == "__main__":
    anonimizza_k5()

