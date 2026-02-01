import time
import socket
import logging
import psutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Configuración de Logs para Vector/Loki
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="TechneNexus Enterprise API")

# Modelo de datos
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Simulación de DB en memoria
db: List[Task] = []

@app.get("/")
def read_root():
    hostname = socket.gethostname()
    logger.info(f"Petición servida por el nodo: {hostname}")
    return {
        "status": "Online",
        "node": hostname,
        "ip": socket.gethostbyname(hostname),
        "cpu_load": psutil.cpu_percent()
    }

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    db.append(task)
    logger.info(f"Tarea creada: {task.title}")
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return db

@app.get("/stress/{seconds}")
def stress_test(seconds: int):
    """Genera carga de CPU intensiva para testear monitorización"""
    logger.warning(f"⚠️ Iniciando test de estrés por {seconds} segundos en {socket.gethostname()}")
    end_time = time.time() + seconds
    while time.time() < end_time:
        _ = 1000 * 1000  # Operación inútil de CPU
    return {"message": f"Test de estrés completado en {socket.gethostname()}"}

@app.get("/error")
def trigger_error():
    """Genera un error 500 para testear alertas"""
    logger.error("❌ Error crítico simulado para pruebas de logs")
    raise HTTPException(status_code=500, detail="Error interno del servidor")