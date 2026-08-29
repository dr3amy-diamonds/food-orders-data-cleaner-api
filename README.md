# Food Orders Data Cleaner API

Este proyecto implementa un pipeline de análisis, limpieza y exposición de datos para una plataforma de pedidos de comida. Transforma un dataset crudo con inconsistencias en una fuente de verdad confiable y consultable a través de una API REST.

**Proyecto académico:** Curso Optativa II (8010) - Taller S04.

## Arquitectura del Proyecto

La estructura del repositorio separa claramente los datos, los scripts de procesamiento y la capa de servicio de la API:

- `datos/raw/`: Contiene el dataset original intocable (`pedidos_sucio.csv`).
- `datos/clean/`: Almacena el resultado tras aplicar las reglas de limpieza (`pedidos_limpios.csv`).
- `scripts/`: Módulos de Python encargados de la auditoría y limpieza de datos basados en reglas de negocio.
- `repo/`: Código del servidor web FastAPI (`main.py`) para el despliegue.
- `resumen.json`: Archivo de métricas base y finales.

## Justificación Técnica: Redondeo de Resultados

¿Por qué se redondearon los resultados numéricos a dos decimales?

1. **Por legibilidad y estándar de negocio:** En analítica de datos, mostrar 15 decimales para dinero o tiempo (minutos) no aporta valor real. Nadie toma una decisión de negocio basándose en el decimal número catorce de un promedio de tiempo de entrega.

2. **¿Qué problemas traería NO redondear?**
   - **Falsos positivos al comparar datos (Floating-point error):** Python y la mayoría de lenguajes manejan los decimales con pequeñas variaciones microscópicas. Un cálculo podría dar `32.755102040816325` hoy y, al recalcularlo en otro servidor, dar `32.755102040816326`. Si se usa Git para comparar si el archivo cambió, o si un sistema de testing evalúa la API, fallará por una diferencia irrelevante. Redondear permite crear una línea base estable y predecible.
   - **Problemas al renderizar en el Frontend:** Cuando se publica esta API, si el JSON envía un número infinitamente largo, el desarrollador que consume la API (por ejemplo, para hacer un dashboard interactivo o un reporte) tendrá que limpiar y formatear ese dato antes de mostrarlo en pantalla. Es una buena práctica que la API entregue el dato limpio y listo para consumir.

## Endpoints de la API

La API expone los datos limpios mediante los siguientes endpoints principales:

- `GET /`: Verifica el estado de actividad del servidor.
- `GET /resumen`: Devuelve las métricas consolidadas y las notas explicativas del procesamiento.