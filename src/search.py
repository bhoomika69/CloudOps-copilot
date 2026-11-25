
from vector_store import collection, model


def search_incidents(query, n_results=3):

    total_records = collection.count()

    if total_records == 0:
        print("No incidents found in ChromaDB.")
        return

    # Convert the user's question into an embedding
    query_embedding = model.encode([query]).tolist()

    # Search for similar incidents
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, total_records)
    )

    print("\nSearch Query:", query)
    print("\nMatching Incidents:")

    for i in range(len(results["documents"][0])):
        print("\nResult:", i + 1)
        print("Incident:", results["ids"][0][i])
        print("Source:", results["metadatas"][0][i]["source"])
        print("Distance:", results["distances"][0][i])
        print("Details:", results["documents"][0][i])
        print("-" * 50)


if __name__ == "__main__":
    question = "Why is my EC2 server running slowly?"

    search_incidents(question)
