import json
import asyncio
import serial
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Parking Backend")

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Arduino Seri Bağlantı
# -------------------------------
SERIAL_PORT = "COM4"   # COM değişirse sadece burayı değiştir
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"[ERROR] Arduino serial port açılamadı: {e}")
    arduino = None

# En son okunan veri
latest_data = {"parked": 0, "capacity": 10}

# WebSocket client listesi
clients: list[WebSocket] = []


async def broadcast(data: dict):
    disconnected = []
    for ws in clients:
        try:
            await ws.send_json(data)
        except Exception:
            disconnected.append(ws)

    for ws in disconnected:
        if ws in clients:
            clients.remove(ws)


async def serial_reader():
    global latest_data

    if arduino is None:
        return

    while True:
        try:
            line = arduino.readline().decode(errors="ignore").strip()
            if not line:
                await asyncio.sleep(0.05)
                continue

            data = json.loads(line)

            if "parked" in data and "capacity" in data:
                latest_data = data
                await broadcast(data)

        except json.JSONDecodeError:
            pass
        except Exception:
            pass

        await asyncio.sleep(0.05)


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(serial_reader())


# -------------------------------
# WebSocket
# -------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    await websocket.send_json(latest_data)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)


# -------------------------------
# HTTP
# -------------------------------
@app.get("/latest")
async def get_latest():
    return latest_data
