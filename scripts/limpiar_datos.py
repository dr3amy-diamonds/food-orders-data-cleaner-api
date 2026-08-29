from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "datos" / "raw" / "pedidos_sucio.csv"
OUTPUT_DIR = ROOT / "datos" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "pedidos_limpios.csv"
REPORT_PATH = OUTPUT_DIR / "reporte_calidad.txt"


def limpiar_pedidos(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    pedidos = pd.read_csv(input_path, skipinitialspace=True)
    pedidos.columns = pedidos.columns.str.strip()

    columnas_texto = pedidos.select_dtypes(include="object").columns
    pedidos[columnas_texto] = pedidos[columnas_texto].apply(
        lambda columna: columna.str.strip()
    )
    pedidos = pedidos.replace(r"^\s*$", pd.NA, regex=True)

    pedidos["fecha"] = pd.to_datetime(pedidos["fecha"], errors="coerce")
    pedidos["cantidad"] = pd.to_numeric(pedidos["cantidad"], errors="coerce").astype("Int64")
    pedidos.loc[pedidos["cantidad"] < 0, "cantidad"] = pd.NA
    pedidos["precio_unitario"] = pd.to_numeric(
        pedidos["precio_unitario"], errors="coerce"
    )
    pedidos["tiempo_entrega_min"] = pd.to_numeric(
        pedidos["tiempo_entrega_min"], errors="coerce"
    )
    pedidos.loc[pedidos["tiempo_entrega_min"] < 0, "tiempo_entrega_min"] = pd.NA

    pedidos["metodo_pago"] = (
        pedidos["metodo_pago"].str.lower().str.replace("é", "e", regex=False)
    )
    pedidos["metodo_pago"] = pedidos["metodo_pago"].replace(
        {"tarjeta": "Tarjeta", "efectivo": "Efectivo", "transferencia": "Transferencia"}
    )
    pedidos["estado"] = pedidos["estado"].str.capitalize()

    pedidos = pedidos.drop_duplicates(subset="pedido_id", keep="first")
    tiempos_validos = pedidos.loc[
        pedidos["tiempo_entrega_min"].between(0, 100), "tiempo_entrega_min"
    ]
    mediana_global = tiempos_validos.median()
    medianas_por_producto = pedidos.loc[
        pedidos["tiempo_entrega_min"].between(0, 100)
    ].groupby("producto")["tiempo_entrega_min"].median()
    tiempos_excesivos = pedidos["tiempo_entrega_min"] > 100
    pedidos.loc[tiempos_excesivos, "tiempo_entrega_min"] = pedidos.loc[
        tiempos_excesivos, "producto"
    ].map(medianas_por_producto).fillna(mediana_global)
    pedidos = pedidos.sort_values("pedido_id").reset_index(drop=True)
    return pedidos


def generar_reporte(pedidos: pd.DataFrame, filas_originales: int) -> str:
    faltantes = pedidos.isna().sum()
    lineas = [
        "Reporte de calidad de pedidos",
        f"Filas originales: {filas_originales}",
        f"Filas finales: {len(pedidos)}",
        f"Duplicados eliminados: {filas_originales - len(pedidos)}",
        "",
        "Valores faltantes por columna:",
    ]
    lineas.extend(f"- {columna}: {cantidad}" for columna, cantidad in faltantes.items())
    return "\n".join(lineas) + "\n"


def main() -> None:
    filas_originales = len(pd.read_csv(INPUT_PATH, skipinitialspace=True))
    pedidos = limpiar_pedidos()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pedidos.to_csv(
        OUTPUT_PATH, index=False, date_format="%Y-%m-%d", na_rep="null"
    )
    REPORT_PATH.write_text(
        generar_reporte(pedidos, filas_originales), encoding="utf-8"
    )
    print(f"Archivo limpio: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Reporte: {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()