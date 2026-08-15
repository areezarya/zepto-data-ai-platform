
from fastapi import FastAPI
from graph import graph
from schemas import AskRequest, AskResponse

app = FastAPI(
    title="Zepto Policy Support Assistant"
)

@app.get("/")
def health_check():
    return {
        "status": "running"
    }

@app.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(request: AskRequest):

    result = graph.invoke(
        {
            "query": request.query
        }
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )
