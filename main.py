from scripts.estrai_bigquery import estrai_dati
from scripts.aggiungi_nomi_concept import aggiungi_nomi
from scripts.annotazione_snomed import annota_colonne
from scripts.anonimizza_k2 import anonimizza_k2
from scripts.anonimizza_k3 import anonimizza_k3
from scripts.anonimizza_k5 import anonimizza_k5
from scripts.semantic_k2_anon_snomed import semantic_k2_anon_snomed
from scripts.semantic_k_anon_snomed import semantic_k_anon_snomed
from scripts.valutazione_k_anon import valuta_k3
from scripts.schema_matching_instance_based import matching_instance_based
from scripts.schema_matching_bert import matching_semantico_bert
from scripts.schema_matching_comparativo import matching_comparativo
from scripts.schema_matching_k2_confronto import schema_matching_k2_confronto
from scripts.schema_matching_k3_confronto import schema_matching_k3_confronto
from scripts.sentence_BERT import sentence_bert

if __name__ == "__main__":
    print("Inizio pipeline completa")

    estrai_dati()
    aggiungi_nomi()
    annota_colonne()

    anonimizza_k2()
    anonimizza_k3()
    anonimizza_k5()
    valuta_k3()

    semantic_k2_anon_snomed()
    semantic_k_anon_snomed()

    matching_instance_based()
    matching_semantico_bert()
    matching_comparativo()
    schema_matching_k2_confronto()
    schema_matching_k3_confronto()

    sentence_bert()

    print("Pipeline completata")
