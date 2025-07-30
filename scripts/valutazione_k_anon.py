import pandas as pd

def valuta_k3():

    # Sostituisci con il tuo file
    file_path = "data/omop_k3_final.csv"
    df = pd.read_csv(file_path)

    # Colonne QID da usare
    qid_cols = [
        "gender_concept_id",
        "race_concept_id",
        "year_decade",
        "condition_1_name_cat",
        "procedure_1_name_cat",
        "observation_1_name_cat"
    ]

    # Calcolo gruppi di equivalenza
    equivalence_groups = df.groupby(qid_cols).size().reset_index(name="group_size")

    # Statistiche
    summary = {
        "Totale record": len(df),
        "Numero gruppi di equivalenza": len(equivalence_groups),
        "Dimensione media gruppo": round(equivalence_groups["group_size"].mean(), 2),
        "Dimensione minima gruppo": equivalence_groups["group_size"].min(),
        "Dimensione massima gruppo": equivalence_groups["group_size"].max(),
        "Gruppi con ≥ 3 record (k=3)": len(equivalence_groups[equivalence_groups["group_size"] >= 3])
    }

    # Mostra risultato
    for k, v in summary.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    valuta_k3()