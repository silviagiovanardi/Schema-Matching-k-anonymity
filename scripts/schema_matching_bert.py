import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"


def matching_semantico_bert():
        
    datasets = {
        "original": "data/omop_synthetic_patients_with_labels.csv",
        "k2": "data/omop_k2_final.csv",
        "k3": "data/omop_k3_final.csv"
    }

    target_schema = {
        "gender_concept_id": "Gender of the person",
        "race_concept_id": "Race or ethnicity of the person",
        "year_of_birth": "Year the person was born",
        "condition_concept_id": "Code identifying a condition diagnosis",
        "procedure_concept_id": "Code identifying a medical procedure",
        "observation_concept_id": "Clinical observation or finding"
    }

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    target_keys = list(target_schema.keys())
    target_texts = [f"{k} {v}" for k, v in target_schema.items()]
    target_embeddings = model.encode(target_texts, convert_to_tensor=True)

    all_matches = []

    for dataset_label, dataset_path in datasets.items():
        df = pd.read_csv(dataset_path)
        source_cols = [col for col in df.columns if col != "person_id"]

        for col in source_cols:
            sample_vals = df[col].dropna().astype(str).unique()[:10]
            combined_text = col + " " + " ".join(sample_vals)

            source_embedding = model.encode(combined_text, convert_to_tensor=True)
            cosine_scores = util.cos_sim(source_embedding, target_embeddings)[0]

            best_match_idx = int(cosine_scores.argmax())
            best_score = float(cosine_scores[best_match_idx])

            all_matches.append({
                "Dataset": dataset_label,
                "Colonna Sorgente": col,
                "Colonna Target OMOP": target_keys[best_match_idx],
                "Descrizione Target": target_schema[target_keys[best_match_idx]],
                "Similarità": round(best_score, 3)
            })

    df_out = pd.DataFrame(all_matches)
    output_path = "data/schema_matching_bert.csv"
    df_out.to_csv(output_path, index=False)
    print(f"Matching semantico completato. Risultato salvato in: {output_path}")

if __name__ == "__main__":
    matching_semantico_bert()
