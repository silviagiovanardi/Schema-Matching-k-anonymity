from google.cloud import bigquery
import pandas as pd
import os

def estrai_dati():

  # Autenticazione
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./my_gcp_credentials.json"

  # Crea client BigQuery
  client = bigquery.Client()

  # Query per selezionare pazienti con 2 condition, 2 procedure, 2 observation
  query = """
  WITH
    condition_counts AS (
      SELECT person_id,
            ARRAY_AGG(DISTINCT condition_concept_id ORDER BY condition_concept_id LIMIT 2) AS conditions
      FROM `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`
      GROUP BY person_id
      HAVING COUNT(DISTINCT condition_concept_id) = 2
    ),
    procedure_counts AS (
      SELECT person_id,
            ARRAY_AGG(DISTINCT procedure_concept_id ORDER BY procedure_concept_id LIMIT 2) AS procedures
      FROM `bigquery-public-data.cms_synthetic_patient_data_omop.procedure_occurrence`
      GROUP BY person_id
      HAVING COUNT(DISTINCT procedure_concept_id) = 2
    ),
    observation_counts AS (
      SELECT person_id,
            ARRAY_AGG(DISTINCT observation_concept_id ORDER BY observation_concept_id LIMIT 2) AS observations
      FROM `bigquery-public-data.cms_synthetic_patient_data_omop.observation`
      GROUP BY person_id
      HAVING COUNT(DISTINCT observation_concept_id) = 2
    )
  SELECT
    p.person_id,
    p.gender_concept_id,
    p.race_concept_id,
    p.year_of_birth,
    c.conditions[OFFSET(0)] AS condition_1,
    c.conditions[OFFSET(1)] AS condition_2,
    o.observations[OFFSET(0)] AS observation_1,
    o.observations[OFFSET(1)] AS observation_2,
    pr.procedures[OFFSET(0)] AS procedure_1,
    pr.procedures[OFFSET(1)] AS procedure_2
  FROM
    condition_counts c
  JOIN
    procedure_counts pr ON c.person_id = pr.person_id
  JOIN
    observation_counts o ON c.person_id = o.person_id
  JOIN
    `bigquery-public-data.cms_synthetic_patient_data_omop.person` p ON p.person_id = c.person_id
  LIMIT 1000
  """

  # Esegui la query
  df = client.query(query).to_dataframe()

  # Salva in CSV
  df.to_csv("data/omop_synthetic_patients.csv", index=False)
  print("CSV salvato: omop_synthetic_patients.csv")

if __name__ == "__main__":
    estrai_dati()