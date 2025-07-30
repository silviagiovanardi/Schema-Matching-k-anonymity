import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.generalization import generalize_year_to_decade

def semantic_k2_anon_snomed():
        
    k = 2
    input_file = "data/omop_synthetic_patients_with_labels.csv"
    output_file = "data/omop_k2_semantic.csv"

    # Mapping semantico SNOMED semplificato e più vario
    semantic_map = {
        "Hypertension": "Cardiovascular",
        "ECG": "Cardiovascular",
        "Diabetes": "Metabolic",
        "Insulin": "Metabolic",
        "Appendectomy": "Surgical",
        "Metformin": "Metabolic",
        "Asthma": "Respiratory",
        "Bronchitis": "Respiratory",
        "COPD": "Respiratory",
        "Cancer": "Oncology",
        "Neoplasm": "Oncology",
        "BMI": "VitalSign",
        "Blood pressure": "VitalSign",
        "Glucose": "Lab",
        "HbA1c": "Lab"
    }

    def generalizza_valore(valore):
        for chiave in semantic_map:
            if chiave.lower() in valore.lower():
                return semantic_map[chiave]
        return "Other"

    df = pd.read_csv(input_file)

    df["condition_1_name_cat"] = df["condition_1_name"].astype(str).apply(generalizza_valore)
    df["procedure_1_name_cat"] = df["procedure_1_name"].astype(str).apply(generalizza_valore)
    df["observation_1_name_cat"] = df["observation_1_name"].astype(str).apply(generalizza_valore)

    # Selezione colonne di quasi-identificatori generalizzati
    qid_cols = [
        "gender_concept_id",
        "race_concept_id",
        "year_decade",
        "condition_1_name_cat",
        "procedure_1_name_cat",
        "observation_1_name_cat"
    ]

    df["year_decade"] = df["year_of_birth"].apply(generalize_year_to_decade)


    # Raggruppamento per equivalenza su QID
    grouped = df.groupby(qid_cols)
    df["eq_group_size"] = grouped.transform("size")

    df_k2 = df[df["eq_group_size"] >= k].copy()
    df_k2 = df_k2.drop(columns=["eq_group_size"])

    final_cols = ["person_id"] + qid_cols
    df_k2  = df_k2 [final_cols]

    df_k2.to_csv(output_file, index=False)
    print(f"Dataset anonimizzato semanticamente salvato in {output_file} (k = {k})")

if __name__ == "__main__":
    semantic_k2_anon_snomed()