
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

from ingestion import load_incidents
from chunking import chunk_incidents


# Set up ChromaDB storage
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="cloud_incidents"
)


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def store_incidents(chunks):
    if not chunks:
        print("No incident chunks found.")
        return

    documents = [chunk["text"] for chunk in chunks]

    metadatas = []

    for chunk in chunks:
        metadata = chunk["metadata"].copy()
        metadata["source"] = chunk["source"]
        metadatas.append(metadata)

    ids = [chunk["source"] for chunk in chunks]

    # Generate embeddings
    embeddings = model.encode(documents).tolist()

    # Store incidents in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Incidents stored successfully:", len(documents))
    print("Total records in ChromaDB:", collection.count())


if __name__ == "__main__":
    incidents = load_incidents()
    chunks = chunk_incidents(incidents)

    store_incidents(chunks)
