from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    print("✅ Received payload:")
    print(json.dumps(payload, indent=2))
    return {"status": "received"}
