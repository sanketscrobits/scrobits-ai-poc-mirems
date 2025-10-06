from fastapi import FastAPI, Request, Query, HTTPException, Response
from settings import WHATSAPP_TOKEN, PHONE_NUMBER_ID, GOOGLE_API_KEY
from src.agents.retriver_agent import create_query_agent
import httpx

VERIFICATION_TOKEN = "my_super_secret_token_987"

query_agent = create_query_agent(api_key=GOOGLE_API_KEY)

app = FastAPI()

# --- Health check ---
@app.get("/")
def root():
    return {"status": "ok"}

# --- Webhook verification (GET) ---
@app.get("/webhook")
def verify_whatsapp(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFICATION_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Invalid verification token")

# --- Webhook receiver (POST) ---
@app.post("/webhook")
async def receive_whatsapp(request: Request):
    data = await request.json()
    print("Incoming webhook:", data)  # debug log

    value = (
        data.get("entry", [{}])[0]
            .get("changes", [{}])[0]
            .get("value", {})
    )
    messages = value.get("messages")
    if not messages:
        return Response(status_code=200)  # must ACK quickly

    msg = messages[0]
    sender = msg.get("from")  # customer's phone in E.164
    message_id = msg.get("id")  # WhatsApp message ID

    # Extract text depending on message type
    text = None
    mtype = msg.get("type")

    if mtype == "text":
        text = msg.get("text", {}).get("body")
    elif mtype == "button":
        text = msg.get("button", {}).get("text")
    elif mtype == "interactive":
        itype = msg.get("interactive", {}).get("type")
        if itype == "button_reply":
            text = msg["interactive"]["button_reply"].get("title")
        elif itype == "list_reply":
            text = msg["interactive"]["list_reply"].get("title")
    elif mtype == "image":
        text = msg.get("caption")  # optional fallback

    if not text:
        await send_whatsapp_message(sender, "Please send a text message, I can't understand anything other than text messages!")
        return Response(status_code=200)

    # Mark as read + show typing indicator
    await mark_read_and_typing(message_id)

    # Call your AI agent
    try:
        result = query_agent.invoke({"input": text})
        answer = result["output"] if isinstance(result, dict) else str(result)
    except Exception as e:
        print("Agent error:", e)
        answer = "⚠️ Oops, something went wrong. Please try again."

    # Send reply back to user (this automatically dismisses typing indicator)
    await send_whatsapp_message(sender, answer)

    return Response(status_code=200)

# --- Helper: Mark as read + show typing ---
async def mark_read_and_typing(message_id: str):
    """Mark message as read and show typing indicator in one API call"""
    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
        "typing_indicator": {
            "type": "text"
        }
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(url, headers=headers, json=payload)
            print(">>> Mark read + typing response:", r.status_code)
    except Exception as e:
        print("Error setting read + typing:", e)

# --- Helper: Send WhatsApp message ---
async def send_whatsapp_message(to: str, message: str):
    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    print(">>> Using TOKEN:", WHATSAPP_TOKEN[:30], "...")  # log first 30 chars
    print(">>> Using PHONE_NUMBER_ID:", PHONE_NUMBER_ID)

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, headers=headers, json=payload)
        print(">>> Response:", r.text)
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            print("WhatsApp API error:", e.response.text)

