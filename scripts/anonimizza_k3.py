import pandas as pd
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.generalization import generalize_year_to_decade

def anonimizza_k3():

    df = pd.read_csv("data1/omop_synthetic_patients_with_labels.csv")

    df["year_decade"] = df["year_of_birth"].apply(generalize_year_to_decade)

    condition_cols = ["condition_1_name", "condition_2_name"]
    procedure_cols = ["procedure_1_name", "procedure_2_name"]
    observation_cols = ["observation_1_name", "observation_2_name"]

    def refined_generalize_label(label):
        if pd.isna(label):
            return "Unknown"
        label = label.lower()
        
        if any(word in label for word in ["diabetes", "hyperglycemia", "obesity", "lipid"]):
            return "Metabolic"
        if any(word in label for word in ["myocardial", "heart", "hypertension", "cardiac", "coronary"]):
            return "Cardiovascular"
        if any(word in label for word in ["depression", "anxiety", "bipolar", "mental", "schizophrenia"]):
            return "Mental Health"
        if any(word in label for word in ["asthma", "bronchitis", "respiratory", "copd", "pneumonia"]):
            return "Respiratory"
        if any(word in label for word in ["vaccine", "vaccination", "influenza", "immunization"]):
            return "Vaccination"
        if any(word in label for word in ["cancer", "neoplasm", "tumor", "malignancy"]):
            return "Neoplastic"
        if any(word in label for word in ["fracture", "injury", "accident", "trauma"]):
            return "Trauma"
        if any(word in label for word in ["surgery", "appendectomy", "operation", "bypass"]):
            return "Surgical"
        if any(word in label for word in ["eye", "vision", "hearing", "dental"]):
            return "Sensory"
        if any(word in label for word in ["infection", "viral", "bacterial", "fever"]):
            return "Infectious"

        return "Other"

    for col in condition_cols + procedure_cols:
        df[col + "_cat"] = df[col].apply(refined_generalize_label)

    for col in observation_cols:
        df[col + "_cat"] = "Observation"

    qid_cols_final = [
        "person_id",
        "gender_concept_id",
        "race_concept_id",
        "year_decade",
        "condition_1_name_cat",
        "procedure_1_name_cat",
        "observation_1_name_cat"
    ]

    df[qid_cols_final].to_csv("data/omop_k3_final.csv", index=False)
    print("File salvato: omop_generalized.csv")

if __name__ == "__main__":
    anonimizza_k3()