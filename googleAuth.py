import os

# Imports the Google Cloud client library
from google.cloud import storage

def implicit():
    # from google.cloud import storage

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../keys/digital-curator-f02e06005c99.json"

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

implicit()