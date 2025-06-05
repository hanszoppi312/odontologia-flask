# Imagen base oficial
FROM python:3.11

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el código
COPY . .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto
EXPOSE 5000

# Comando de inicio
CMD ["flask", "run", "--host=0.0.0.0"]
