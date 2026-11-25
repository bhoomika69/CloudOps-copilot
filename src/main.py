
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from reranker import rerank_incidents
from generation import generate_answer

app = FastAPI(
    title="CloudOps Copilot API",
    description="AI-powered cloud infrastructure troubleshooting assistant",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "CloudOps Copilot API is running!"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        query = request.question.strip()

        if not query:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        ranked_results = rerank_incidents(query)

        answer = generate_answer(query, ranked_results)

        return {
            "question": query,
            "answer": answer,
            "incidents_found": len(ranked_results)
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Troubleshooting failed: {str(error)}"
        )
