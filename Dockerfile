# Receta para la nube: Render la construye; usted no necesita Docker en su equipo.
FROM python:3.12-slim

# Usuario sin privilegios: la app no necesita ser administradora.
RUN useradd -m -u 1000 usuario
USER usuario
ENV PATH=/home/usuario/.local/bin:$PATH
WORKDIR /home/usuario/app

# Primero las dependencias (con versiones fijas), después el código.
COPY --chown=usuario requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=usuario . .

# Solara usa el puerto que fija la nube en $PORT (8765 si no hay).
EXPOSE 8765
CMD ["solara", "run", "app.py", "--host=0.0.0.0", "--production"]
