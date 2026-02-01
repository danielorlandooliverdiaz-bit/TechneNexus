# Etapa 1: Constructor (instala dependencias)
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Ejecución (imagen final ligera con solo lo necesario)
FROM python:3.11-slim
WORKDIR /app
# Copia las libs instaladas en la etapa de builder
COPY --from=builder /root/.local /root/.local

# Copia tu aplicación y plantilla
COPY main.py .
COPY index.html .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]