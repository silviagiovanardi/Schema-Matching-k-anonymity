import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def schema_matching_k3_confronto():
    file_testuale = "data/omop_k3_final.csv"
    file_semantico = "data/omop_k3_semantic.csv"

    # Descrizioni OMOP-CDM arricchite con esempi clinici
    omop_schema = {
        "gender_concept_id": "gender_concept_id Gender of the patient (e.g. male, female)",
        "race_concept_id": "race_concept_id Race or ethnicity (e.g. White, Asian, Black)",
        "year_of_birth": "year_of_birth Year of birth (e.g. 1970, 1985)",
        "condition_concept_id": "condition_concept_id Medical condition (e.g. diabetes, hypertension)",
        "procedure_concept_id": "procedure_concept_id Medical procedure (e.g. appendectomy, ECG)",
        "observation_concept_id": "observation_concept_id Clinical observation (e.g. BMI, blood pressure)"
    }

    omop_keys = list(omop_schema.keys())
    omop_texts = list(omop_schema.values())

    def preprocess_dataset(path, label):
        df = pd.read_csv(path)
        source_cols = [c for c in df.columns if c != "person_id"]
        source_texts = []

        for col in source_cols:
            values = df[col].dropna().astype(str).unique()[:20]
            col_text = col + " " + " ".join(values)
            source_texts.append(col_text)

        return source_cols, source_texts

    cols_testuale, texts_testuale = preprocess_dataset(file_testuale, "k3_classico")
    cols_semantico, texts_semantico = preprocess_dataset(file_semantico, "k3_semantico")

    all_texts = texts_testuale + texts_semantico + omop_texts
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_df=0.85)
    vectorizer.fit(all_texts)

    vec_testuale = vectorizer.transform(texts_testuale)
    vec_semantico = vectorizer.transform(texts_semantico)
    vec_target = vectorizer.transform(omop_texts)

    # Calcolo similarità
    def match_columns(source_vec, source_cols, label):
        sim_matrix = cosine_similarity(source_vec, vec_target)
        results = []

        for i, col in enumerate(source_cols):
            best_match_idx = sim_matrix[i].argmax()
            results.append({
                "Dataset": label,
                "Colonna Sorgente": col,
                "Colonna Target OMOP": omop_keys[best_match_idx],
                "Similarità": round(sim_matrix[i][best_match_idx], 3)
            })

        return pd.DataFrame(results)

    df_testuale = match_columns(vec_testuale, cols_testuale, "k3_classico")
    df_semantico = match_columns(vec_semantico, cols_semantico, "k3_semantico")

    df_finale = pd.concat([df_testuale, df_semantico], ignore_index=True)
    df_finale.to_csv("data/schema_matching_k3_confronto.csv", index=False)
    print("Matching comparativo salvato in schema_matching_k3_confronto.csv")

if __name__ == "__main__":
    schema_matching_k3_confronto()
