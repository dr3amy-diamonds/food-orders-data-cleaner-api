import json
from pathlib import Path
import pandas as pd

# Path(__file__).resolve().parents[1] obtiene la RAÍZ de tu proyecto (food-orders-data-cleaner-api)
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
ruta_csv = RAIZ_PROYECTO / "datos" / "raw" / "pedidos_sucio.csv"

# Cargar el CSV
df = pd.read_csv(ruta_csv)

# 2. Parsear columnas numéricas
df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce")
df["tiempo_entrega_min"] = pd.to_numeric(
    df["tiempo_entrega_min"], errors="coerce"
)
df["total"] = df["cantidad"] * df["precio_unitario"]

# 3. Filtrar pedidos entregados
entregados = df[df["estado"] == "Entregado"]
tiempos = entregados["tiempo_entrega_min"].dropna()

# 4. Construir resumen inicial redondeado
resumen_antes = {
    "filas": int(len(df)),
    "ventas_entregado": round(float(entregados["total"].sum()), 2),
    "media_tiempo_entrega": round(float(tiempos.mean()), 2),
    "mediana_tiempo_entrega": round(float(tiempos.median()), 2),
    "desviacion_tiempo_entrega": round(float(tiempos.std()), 2),
    "duplicados_pedido_id": int(df["pedido_id"].duplicated().sum()),
}

# 5. Guardar en la raíz
Path("../resumen.json").write_text(
    json.dumps(resumen_antes, indent=2, ensure_ascii=False), encoding="utf-8"
)

print("✅ 'resumen.json' generado en la raíz del proyecto:")
print(json.dumps(resumen_antes, indent=2, ensure_ascii=False))