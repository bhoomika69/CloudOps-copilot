

def chunk_incidents(incidents):
    chunks = []

    for incident in incidents:
        metadata = {}

        # Extract incident details from the report
        for line in incident["content"].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                metadata[key] = value.strip()

        chunks.append({
            "text": incident["content"],
            "source": incident["filename"],
            "metadata": metadata
        })

    return chunks


if __name__ == "__main__":
    from ingestion import load_incidents

    incidents = load_incidents()
    chunks = chunk_incidents(incidents)

    print("Total chunks created:", len(chunks))

    for chunk in chunks:
        print("\nSource:", chunk["source"])
        print("Metadata:", chunk["metadata"])
        print("-" * 40)
