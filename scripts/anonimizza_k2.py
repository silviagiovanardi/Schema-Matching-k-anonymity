import pandas as pd
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.generalization import generalize_year_to_decade
from lib.file_utils import save_csv

def anonimizza_k2():

    # Carica il file con i concept SNOMED già etichettati
    df = pd.read_csv("data1/omop_synthetic_patients_with_labels.csv")

    df["year_decade"] = df["year_of_birth"].apply(generalize_year_to_decade)

    # Colonne da categorizzare
    condition_cols = ["condition_1_name", "condition_2_name"]
    procedure_cols = ["procedure_1_name", "procedure_2_name"]
    observation_cols = ["observation_1_name", "observation_2_name"]

    # Funzione di categorizzazione soft
    def soft_generalize_label(label):
        if pd.isna(label):
            return "Unknown"
        label = label.lower()
        if any(word in label for word in ["myocardial", "heart", "hypertension", "cardiac", "coronary"]):
            return "Cardiovascular"
        if "diabetes" in label:
            return "Diabetes"
        if any(word in label for word in ["asthma", "bronchitis", "respiratory", "copd", "pneumonia"]):
            return "Respiratory"
        if any(word in label for word in ["cancer", "neoplasm", "tumor", "malignancy"]):
            return "Cancer"
        return label  

    # Applica la categorizzazione
    for col in condition_cols + procedure_cols:
        df[col + "_softcat"] = df[col].apply(soft_generalize_label)
    for col in observation_cols:
        df[col + "_softcat"] = "Observation"

    # Scegli QID per la versione k=2
        qid = ["person_id", "gender_concept_id", "race_concept_id", "year_decade",
            "condition_1_name_softcat", "procedure_1_name_softcat", "observation_1_name_softcat"]
        df[qid].to_csv("data/omop_k2_final.csv", index=False)
        print("Salvato: data/omop_k2_final.csv")

if __name__ == "__main__":
    anonimizza_k2()
