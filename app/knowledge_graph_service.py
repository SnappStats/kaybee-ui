import json
import os
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
storage_client = storage.Client()

KNOWLEDGE_GRAPH_BUCKET = storage_client.get_bucket(
        os.environ["KNOWLEDGE_GRAPH_BUCKET"])

def fetch_knowledge_graph() -> dict:
    return json.loads(
            KNOWLEDGE_GRAPH_BUCKET.get_blob("knowledge_graph.json")\
                    .download_as_text(encoding="utf-8")
    )
