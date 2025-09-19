import json
import os
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
storage_client = storage.Client()

KNOWLEDGE_GRAPH_BUCKET = storage_client.get_bucket(
        os.environ["KNOWLEDGE_GRAPH_BUCKET"])

def fetch_knowledge_graph(graph_id: str) -> dict:
    blob = KNOWLEDGE_GRAPH_BUCKET.blob(f"{graph_id}.json")
    if not blob.exists():
        return {'entities': {}, 'relationships': []}
    else:
        return json.loads(blob.download_as_text(encoding='utf-8'))

def fetch_entity(graph_id: str, entity_id: str) -> dict:
    graph = fetch_knowledge_graph(graph_id)
    return graph['entities'].get(entity_id, {})
