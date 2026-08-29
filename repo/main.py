import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Inicializamos la aplicación
app = FastAPI(
    title="Food Orders Data Cleaner API",
    description="API para presentar métricas y resultados del pipeline de datos"
)

# Definimos la ruta para encontrar el JSON en la raíz del proyecto
ROOT = Path(__file__).resolve().parents[1]
RESUMEN_PATH = ROOT / "resumen.json"


@app.get("/")
def raiz():
    return {
        "mensaje": "El servidor está activo.",
        "rutas_disponibles": ["/resumen"]
    }


@app.get("/resumen")
def obtener_resumen():
    # Verificamos si el archivo de métricas existe antes de leerlo
    if RESUMEN_PATH.exists():
        with open(RESUMEN_PATH, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return JSONResponse(content=datos)

    return JSONResponse(
        content={"error": "El archivo resumen.json aún no ha sido generado."},
        status_code=404
    )