import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def matching_instance_based():

    source_file = "data/omop_synthetic_patients_with_labels.csv"  # oppure omop_k2_final.csv, omop_k3_final.csv

    # Target schema OMOP-CDM simulato
    target_schema = {
        "gender_concept_id": "Gender of the person",
        "race_concept_id": "Race or ethnicity of the person",
        "year_of_birth": "Year the person was born",
        "condition_concept_id": "Code identifying a condition diagnosis",
        "procedure_concept_id": "Code identifying a medical procedure",
        "observation_concept_id": "Clinical observation or finding"
    }

    df = pd.read_csv(source_file)
    source_cols = [col for col in df.columns if col != "person_id"]

    source_texts = []
    for col in source_cols:
        sample_values = df[col].dropna().astype(str).unique()[:10]
        sample_text = " ".join(sample_values)
        full_text = col + " " + sample_text
        source_texts.append(full_text)

    target_keys = list(target_schema.keys())
    target_texts = [f"{key} {desc}" for key, desc in target_schema.items()]

    # TF-IDF + cosine similarity
    vectorizer = TfidfVectorizer().fit(source_texts + target_texts)
    source_vecs = vectorizer.transform(source_texts)
    target_vecs = vectorizer.transform(target_texts)
    similarity_matrix = cosine_similarity(source_vecs, target_vecs)

    matches = []
    for i, s_col in enumerate(source_cols):
        for j, t_col in enumerate(target_keys):
            matches.append({
                "Colonna Sorgente": s_col,
                "Colonna Target OMOP": t_col,
                "Descrizione Target": target_schema[t_col],
                "Similarità": round(similarity_matrix[i, j], 3)
            })

    match_df = pd.DataFrame(matches).sort_values(by="Similarità", ascending=False)

    best_matches = match_df.sort_values(by=["Colonna Sorgente", "Similarità"], ascending=[True, False]) \
                        .groupby("Colonna Sorgente").head(1)

    match_df.to_csv("data/schema_matching_completo.csv", index=False)
    best_matches.to_csv("data/schema_matching_migliori.csv", index=False)
    print("Matching completato. File salvati:")
    print("- schema_matching_completo.csv")
    print("- schema_matching_migliori.csv")


if __name__ == "__main__":
    matching_instance_based()