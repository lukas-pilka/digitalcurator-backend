import os

# Imports the Google Cloud client library
from google.cloud import storage

def implicit():
    # from google.cloud import storage

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/lukaspilka/digitalcurator-247310-b5388c78514e.json"

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

implicit()