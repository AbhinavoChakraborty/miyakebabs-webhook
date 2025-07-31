from fastapi import FastAPI, HTTPException
from models import WebhookPayload
from db import insert_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🚀 Miya Kebabs Webhook is up!"}

@app.post("/webhook")
async def receive_webhook(payload: WebhookPayload):
    try:
        insert_data(payload)
        return {"message": "✅ Data received and inserted successfully!"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))