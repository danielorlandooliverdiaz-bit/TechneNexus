# Usamos una imagen ligera de Python
FROM python:3.11-slim

WORKDIR /app

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir fastapi uvicorn

# Copiamos el código
COPY main.py .

# Exponemos el puerto 80
EXPOSE 80

# Comando para arrancar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]