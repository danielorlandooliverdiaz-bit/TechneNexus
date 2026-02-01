from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import socket
import datetime

app = FastAPI(title="TechneNexus OS")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Obtenemos datos del sistema real
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simulación de estado de servicios (puedes ampliar esto)
    services = [
        {"name": "Docker Registry", "status": "Online", "ip": "10.2.84.60"},
        {"name": "Monitoring (Argus)", "status": "Online", "ip": "10.2.84.20"},
        {"name": "Gateway (Omni)", "status": "Active", "ip": "10.2.84.10"}
    ]

    html_content = f"""
    <html>
        <head>
            <title>TechneNexus Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1a; color: #e0e0e0; text-align: center; padding: 50px; }}
                .container {{ max-width: 800px; margin: auto; background: #2d2d2d; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
                h1 {{ color: #00ff00; font-size: 2.5em; margin-bottom: 10px; }}
                .status-card {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 30px; }}
                .card {{ background: #3d3d3d; padding: 15px; border-radius: 10px; border-bottom: 4px solid #00ff00; }}
                .footer {{ margin-top: 40px; font-size: 0.8em; color: #888; }}
                .rocket {{ font-size: 3em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="rocket">🚀</div>
                <h1>TechneNexus Operativo</h1>
                <p>Desplegado automáticamente desde <b>GitHub</b> a <b>{hostname}</b></p>
                <p>Hora del sistema: {current_time}</p>
                
                <div class="status-card">
                    {"".join([f'<div class="card"><b>{s["name"]}</b><br><span style="color:#00ff00">● {s["status"]}</span><br><small>{s["ip"]}</small></div>' for s in services])}
                </div>

                <div class="footer">
                    ID de Instancia: {socket.gethostbyname(hostname)} | Infraestructura como Código
                </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)