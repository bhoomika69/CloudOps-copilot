

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

MODEL_NAME =  "gemini-3.6-flash"


def generate_answer(query, ranked_results):

    # Prepare retrieved incident context
    context = ""

    for incident in ranked_results:
        context += f"""
Incident ID: {incident['id']}
Date: {incident['date']}
Source: {incident['source']}
Incident Details:
{incident['text']}

"""

    if not context:
        context = "No historical incidents were retrieved."

    # Build the RAG prompt
    prompt = f"""
You are CloudOps Copilot, an AI assistant for cloud
infrastructure troubleshooting.

User's Question:
{query}

Retrieved Historical Incidents:
{context}

Instructions:
1. Use the retrieved incidents as historical evidence.
2. Do not invent causes or fixes and present them as past incidents.
3. Explain relevant historical findings clearly.
4. If historical evidence is insufficient, say so.
5. You may suggest additional diagnostic steps, but label
   them clearly as AI-generated suggestions.
6. Never claim that an unverified suggestion is a confirmed fix.
7. Give the response in simple, structured language.

Provide:
- Likely cause
- Supporting historical evidence
- Recommended troubleshooting steps
- Whether the recommendation is historical or AI-generated
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    from reranker import rerank_incidents

    query = "Why am I getting Access Denied when accessing my S3 bucket?"

    print("\nSearching historical incidents...")

    ranked_results = rerank_incidents(query)

    print("\nGenerating answer using Gemini...")

    answer = generate_answer(query, ranked_results)

    print("\n========== CLOUDOPS COPILOT ==========")
    print(answer)
    print("======================================")
