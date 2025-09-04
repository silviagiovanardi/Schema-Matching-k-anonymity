# Schema Matching & K-Anonymity

Questo progetto contiene una pipeline completa per il matching di schemi e l'anonimizzazione k-anonima di dati sanitari sintetici basati sul modello OMOP.

Tutti i passaggi sono inclusi nel file `main.py`, che esegue l'intero flusso:

- Estrazione e arricchimento dati da BigQuery
- Anonimizzazione k-anonima (k=2,3,5)
- Matching tra schemi con metodi istanza-based e semantici
- Valutazione del trade-off privacy-utilità

Il file `my_gcp_credentials.json` necessario per accedere a BigQuery **non è stato caricato su GitHub** per motivi di sicurezza. Necessario assicurarsi di averlo localmente e di specificarne il percorso corretto nei vari script.

