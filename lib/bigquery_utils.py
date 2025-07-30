def get_bigquery_client():
    import os
    from google.cloud import bigquery
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my_gcp_credentials.json"
    return bigquery.Client()