from google.cloud import bigquery
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.generalization import generalize_year_to_decade

def semantic_k_anon_snomed():
        
    #Estrai concetti SNOMED da BigQuery
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my_gcp_credentials.json"
    client = bigquery.Client()

    snomed_query = """
    SELECT concept_id, concept_name, concept_code, domain_id, vocabulary_id
    FROM `bigquery-public-data.cms_synthetic_patient_data_omop.concept`
    WHERE vocabulary_id = 'SNOMED'
    """
    snomed_df = client.query(snomed_query).to_dataframe()
    snomed_df.to_csv("data/snomed_concepts_from_bigquery.csv", index=False)
    print("Concetti SNOMED salvati in: snomed_concepts_from_bigquery.csv")



    # Carica dataset originale e dizionario SNOMED (scaricato da BigQuery)
    df_data = pd.read_csv("data/omop_synthetic_patients_with_labels.csv")
    df_snomed = pd.read_csv("data/snomed_concepts_from_bigquery.csv")

    # Mappa semantica manuale SNOMED → categoria
    semantic_map = {
        "Metformin": "Antidiabetic",
        "Insulin": "Antidiabetic",
        "Diabetes": "Metabolic",
        "Hypertension": "Cardiovascular",
        "ECG": "Cardiovascular",
        "Blood Pressure Measurement": "Cardiovascular",
        "Biopsy": "Surgical",
        "Colonoscopy": "Diagnostic",
        "Asthma": "Respiratory",
        "Dulaglutide": "Antidiabetic",
        "Carfilzomib": "Oncologic",
        "Belatacept": "Immunosuppressant",
    }

    # Funzione di generalizzazione semantica
    def map_semantic_category(concept_name):
        for key in semantic_map:
            if key.lower() in str(concept_name).lower():
                return semantic_map[key]
        return "Other"

    df_data["condition_1_name_cat"] = df_data["condition_1_name"].apply(map_semantic_category)
    df_data["procedure_1_name_cat"] = df_data["procedure_1_name"].apply(map_semantic_category)
    df_data["observation_1_name_cat"] = df_data["observation_1_name"].apply(map_semantic_category)

    df_data["year_decade"] = df_data["year_of_birth"].apply(generalize_year_to_decade)

    # QID per k-anonimato
    qid_cols = [
        "gender_concept_id",
        "race_concept_id",
        "year_decade",
        "condition_1_name_cat",
        "procedure_1_name_cat",
        "observation_1_name_cat"
    ]

    final_cols = ["person_id"] + qid_cols
    df_data = df_data[final_cols]

    k = 3
    grouped = df_data.groupby(qid_cols).size().reset_index(name="group_size")
    valid_keys = grouped[grouped["group_size"] >= k][qid_cols]
    df_data = df_data.merge(valid_keys, on=qid_cols, how="inner")

    df_data.to_csv("data/omop_k3_semantic.csv", index=False)
    print("Dataset anonimizzato semanticamente salvato in omop_k3_semantic.csv")

if __name__ == "__main__":
    semantic_k_anon_snomed()