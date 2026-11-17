
def chunk_incidents(incidents):
    chunks = []

    for incident in incidents:
        chunks.append({
            "text": incident["content"],
            "source": incident["filename"]
        })

    return chunks


if __name__ == "__main__":
    from ingestion import load_incidents

    incidents = load_incidents()
    chunks = chunk_incidents(incidents)

    print("Total chunks created:", len(chunks))

    for chunk in chunks:
        print("\nSource:", chunk["source"])
        print(chunk["text"])
        print("-" * 40)
