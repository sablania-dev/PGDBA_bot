from fastapi import FastAPI, Query
from bot.qa_engine_v0 import QABot

app = FastAPI()
qa = QABot()

@app.get("/chat")
def chat(query: str = Query(...)):
    answer, confidence = qa.search(query)
    if answer:
        return {"answer": answer, "confidence": confidence}
    return {"answer": "❌ Sorry, I don't have info on that. Please check the official PGDBA website.", 
            "confidence": confidence}
