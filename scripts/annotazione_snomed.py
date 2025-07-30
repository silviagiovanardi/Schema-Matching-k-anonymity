import pandas as pd
import requests
import time
import re

def annota_colonne():

    input_csv = "data/omop_synthetic_patients_with_labels.csv"
    output_csv = "data/annotazioni_snomed.csv"
    snowstorm_api = "https://snowstorm.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/concepts"

    # Funzione per normalizzare i nomi delle colonne
    def normalize_column(col):
        col = col.replace("_name", "")
        col = re.sub(r'[_\-]+', ' ', col) 
        col = re.sub(r'\d+', '', col)    
        return col.strip()

    # Funzione di interrogazione API
    def get_snomed_concepts(term, max_results=3):
        try:
            url = f"{snowstorm_api}?term={term}&activeFilter=true&limit={max_results}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            items = response.json().get('items', [])
            results = []
            for item in items:
                results.append({
                    "Colonna originale": col,
                    "Query normalizzata": term,
                    "SNOMED Label": item['pt']['term'],
                    "SNOMED ID": item['conceptId']
                })
            return results
        except Exception as e:
            return [{
                "Colonna originale": col,
                "Query normalizzata": term,
                "SNOMED Label": f"Errore: {e}",
                "SNOMED ID": None
            }]

    # Carica intestazioni CSV
    df = pd.read_csv(input_csv, nrows=1)
    column_names = df.columns.tolist()

    # Esegui annotazione
    annotazioni = []
    for col in column_names:
        query_term = normalize_column(col)
        print(f"- {col} → '{query_term}'")
        risultati = get_snomed_concepts(query_term)
        annotazioni.extend(risultati)
        time.sleep(1)

    
    df_out = pd.DataFrame(annotazioni)
    df_out.to_csv(output_csv, index=False)
    print(f"\nAnnotazioni salvate in: {output_csv}")

if __name__ == "__main__":
    annota_colonne()