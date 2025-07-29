from fastapi import FastAPI, HTTPException
from models import WebhookPayload
from db import insert_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 Miya Kebabs Webhook is live and working!"}

@app.post("/webhook")
async def receive_webhook(payload: WebhookPayload):
    try:
        insert_data(payload)
        return {"message": "✅ Webhook data received and inserted successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong while inserting data.")
