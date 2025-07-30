import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def matching_comparativo():
        
    datasets = {
        "labels": "data/omop_synthetic_patients_with_labels.csv",
        "k2": "data/omop_k2_final.csv",
        "k3": "data/omop_k3_final.csv"
    }

    # OMOP-CDM Target Schema arricchito con esempi
    target_schema = {
        "gender_concept_id": "Gender of the person (e.g. male, female)",
        "race_concept_id": "Race or ethnicity (e.g. White, Asian, Black)",
        "year_of_birth": "Year of birth (e.g. 1970, 1985)",
        "condition_concept_id": "Medical condition diagnosis (e.g. diabetes, hypertension)",
        "procedure_concept_id": "Medical procedure code (e.g. appendectomy, ECG)",
        "observation_concept_id": "Clinical observation or measurement (e.g. BMI, blood pressure)"
    }

    target_keys = list(target_schema.keys())
    target_texts = [f"{k} {v}" for k, v in target_schema.items()]

    def compute_matching(dataset_path, dataset_label):
        df = pd.read_csv(dataset_path)
        source_cols = [col for col in df.columns if col != "person_id"]
        source_texts = []

        for col in source_cols:
            sample_values = df[col].dropna().astype(str).unique()[:18]
            sample_text = " ".join(sample_values)
            full_text = col + " " + sample_text
            source_texts.append(full_text)

        # TF-IDF potenziato
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_df=0.85
        ).fit(source_texts + target_texts)

        source_vecs = vectorizer.transform(source_texts)
        target_vecs = vectorizer.transform(target_texts)
        sim_matrix = cosine_similarity(source_vecs, target_vecs)

        matches = []
        for i, s_col in enumerate(source_cols):
            best_j = sim_matrix[i].argmax()
            matches.append({
                "Dataset": dataset_label,
                "Colonna Sorgente": s_col,
                "Colonna Target OMOP": target_keys[best_j],
                "Descrizione Target": target_schema[target_keys[best_j]],
                "Similarità": round(sim_matrix[i][best_j], 3)
            })

        return pd.DataFrame(matches)

    all_matches = pd.concat(
        [compute_matching(path, label) for label, path in datasets.items()],
        ignore_index=True
    )

    # Salvataggio risultati
    all_matches.to_csv("data/schema_matching_confronto.csv", index=False)
    print("File salvato: schema_matching_confronto.csv")


if __name__ == "__main__":
    matching_comparativo()
