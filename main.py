import time
import socket
import logging
import psutil
import datetime
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Configuración de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="TechneNexus Live Dashboard")

# Monta un directorio para archivos estáticos (CSS, JS, etc.) si los tuvieras
# En este ejemplo, el JS está inline, pero para CSS o imágenes sería útil.
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=".") # Usamos el directorio actual para templates

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Los datos dinámicos se cargarán vía JS después
    return templates.TemplateResponse("index.html", {"request": request, "hostname": hostname, "current_time": current_time})

@app.get("/api/metrics")
async def get_metrics():
    """Retorna métricas de CPU, RAM y Disco en tiempo real."""
    cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    return {
        "cpu_usage": cpu_percent,
        "ram_usage": ram_percent,
        "disk_usage": disk_percent,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/stress/{seconds}")
async def stress_test(seconds: int):
    """Genera carga de CPU intensiva."""
    logger.warning(f"⚠️ Iniciando test de estrés por {seconds} segundos en {socket.gethostname()}")
    await asyncio.to_thread(lambda: [1000*1000 for _ in range(seconds * 100000)]) # Operación de CPU en un hilo separado
    logger.info(f"Test de estrés completado en {socket.gethostname()}")
    return {"message": f"Test de estrés completado en {socket.gethostname()}"}

@app.post("/api/error")
async def trigger_error():
    """Genera un error 500 simulado."""
    logger.error("❌ Error crítico simulado para pruebas de logs y alertas.")
    raise HTTPException(status_code=500, detail="Error interno del servidor simulado")

@app.get("/api/info")
async def get_info():
    """Retorna información básica del nodo."""
    hostname = socket.gethostname()
    return {
        "hostname": hostname,
        "ip": socket.gethostbyname(hostname),
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }