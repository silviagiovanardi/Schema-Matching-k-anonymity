from google.cloud import bigquery
import pandas as pd
import os

def aggiungi_nomi():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my_gcp_credentials.json"
    client = bigquery.Client()

    df = pd.read_csv("data/omop_synthetic_patients.csv")

    # Colonne da convertire in nomi
    id_columns = [
        "gender_concept_id",
        "race_concept_id",
        "condition_1",
        "condition_2",
        "observation_1",
        "observation_2",
        "procedure_1",
        "procedure_2"
    ]

    all_concept_ids = set()
    for col in id_columns:
        all_concept_ids.update(df[col].dropna().astype(int).tolist())

    # Converti tutto in int "puro" (no np.int64)
    all_concept_ids = [int(x) for x in all_concept_ids]

    query = f"""
        SELECT concept_id, concept_name
        FROM `bigquery-public-data.cms_synthetic_patient_data_omop.concept`
        WHERE concept_id IN UNNEST({all_concept_ids})
    """

    concept_df = client.query(query).to_dataframe()

    # Crea un dizionario {concept_id: concept_name}
    concept_dict = dict(zip(concept_df["concept_id"], concept_df["concept_name"]))

    # Aggiungi le colonne *_name
    for col in id_columns:
        name_col = col + "_name"
        df[name_col] = df[col].map(concept_dict)

    df.to_csv("data/omop_synthetic_patients_with_labels.csv", index=False)
    print("File salvato: data/omop_synthetic_patients_with_labels.csv")


if __name__ == "__main__":
    aggiungi_nomi()
