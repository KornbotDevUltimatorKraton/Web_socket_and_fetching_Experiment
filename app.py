
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import uvicorn
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/ws2", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})
@app.get("/fetching", response_class=HTMLResponse)
async def get_fetching(request: Request):
    return templates.TemplateResponse("index3.html", {"request": request})
@app.get("/ws3", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index4.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # 1. Receive incoming JSON payload
            data = await websocket.receive_text()
            payload = json.loads(data)
            print("Received payload:", payload)

            # 2. Build a feedback response (you can customize this)
            feedback = {
                "status": "ok",
                "received_keys": list(payload.keys()),
                "timestamp": __import__("time").time()
            }

            # 3. Send it back over the WebSocket
            await websocket.send_text(json.dumps(feedback))

        except Exception as e:
            print("WebSocket error:", e)
            break
@app.websocket("/ws2")
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Respond as fast as possible
            feedback = {
                "status": "ok",
                "timestamp": time.time(),
                "keys": list(payload.keys())
            }

            # Send response immediately
            await websocket.send_text(json.dumps(feedback))

    except Exception as e:
        print("WebSocket closed or errored:", e)
        await websocket.close()
#End-point fetching test function 
@app.post("/post_back_end")
async def fetching_back_end(request: Request):
        reqdat = await request.json()
        print("reqdat: ",reqdat)
        return reqdat 
@app.websocket("/optimize")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Process your data here
            print("Received:", payload)

            # Send a response
            await websocket.send_text(json.dumps({
                "status": "ok",
                "message": "Data received successfully"
            }))

            # Explicitly free memory (optional but helps in long sessions)
            del payload
            del data
    except Exception as e:
        print("WebSocket error:", e)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

