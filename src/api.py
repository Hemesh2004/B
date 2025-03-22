from fastapi import FastAPI, Request
from data_preprocessing import load_and_clean_data
from analytics import cancellation_rate
from rag_qa import create_embeddings, search

app = FastAPI()

# Load and preprocess data on startup
df = load_and_clean_data('data/hotel_bookings.csv')
index, docs = create_embeddings(df)

@app.post("/analytics")
def analytics():
  from fastapi import FastAPI
from analytics import get_analytics

app = FastAPI()

@app.post("/analytics")
def analytics():
    return get_analytics()


@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    query = data.get("query", "")

    if not query:
        return {"error": "No query provided."}

    results = search(query, index, docs)
    return {"results": results}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
