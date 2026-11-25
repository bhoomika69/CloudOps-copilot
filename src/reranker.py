

from sentence_transformers import CrossEncoder
from vector_store import collection
from datetime import datetime
import math


# Load the reranking model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_incidents(query, n_results=5):

    total_records = collection.count()

    if total_records == 0:
        print("No incidents available.")
        return []

    # Retrieve incidents from ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, total_records)
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    ids = results["ids"][0]

    # Calculate relevance scores
    pairs = [[query, document] for document in documents]
    relevance_scores = reranker.predict(pairs)

    # Normalize relevance scores between 0 and 1
    min_score = min(relevance_scores)
    max_score = max(relevance_scores)

    ranked_results = []

    for i in range(len(documents)):

        if max_score == min_score:
            relevance = 1.0
        else:
            relevance = (
                float(relevance_scores[i]) - min_score
            ) / (max_score - min_score)

        # Calculate recency score
        incident_date = datetime.strptime(
            metadata[i]["date"], "%Y-%m-%d"
        ).date()

        today = datetime.now().date()
        age_days = max((today - incident_date).days, 0)

        recency = math.exp(-age_days / 30)

        # Combine relevance and recency
        final_score = (0.8 * relevance) + (0.2 * recency)

        ranked_results.append({
            "id": ids[i],
            "source": metadata[i]["source"],
            "date": str(incident_date),
            "relevance_score": round(relevance, 4),
            "recency_score": round(recency, 4),
            "final_score": round(final_score, 4),
            "text": documents[i]
        })

    # Sort by final score
    ranked_results.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    return ranked_results


if __name__ == "__main__":

    question = "Why is my EC2 server running slowly?"

    results = rerank_incidents(question)

    print("\nFinal Reranked Incidents:")

    for result in results:
        print("\nIncident:", result["id"])
        print("Date:", result["date"])
        print("Relevance:", result["relevance_score"])
        print("Recency:", result["recency_score"])
        print("Final Score:", result["final_score"])
        print("Details:", result["text"])
        print("-" * 50)
