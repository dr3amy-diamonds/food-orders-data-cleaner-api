# Food Orders Data Cleaner API

Este proyecto toma un archivo CSV con datos sucios de pedidos de comida, los limpia usando Python y expone los resultados a través de una API para que puedan ser consultados de forma confiable.

##  Justificación Técnica: ¿Por qué se redondearon los resultados a 2 decimales?

1. **Por legibilidad y estándar de negocio:** En analítica de datos, mostrar 15 decimales para dinero o tiempo no aporta valor real. Nadie toma una decisión basándose en el decimal número catorce de un promedio de tiempo de entrega.
2. **Para evitar falsos positivos (Floating-point error):** Python maneja los decimales con variaciones microscópicas (ej. `32.755102040816325` vs `32.755102040816326`). Si usamos Git para comparar versiones, fallará por una diferencia irrelevante. Redondear crea una línea base estable.
3. **Problemas al renderizar en el Frontend:** Es una buena práctica que la API entregue el dato limpio y listo para consumir, evitando que el desarrollador frontend tenga que formatear números infinitamente largos para un dashboard.

##  Estructura del Proyecto

* `datos/`: Contiene el CSV original (raw) y el procesado (clean).
* `scripts/`: Scripts de Python para la limpieza de los datos.
* `repo/`: Código del servidor de la API.
* `resumen.json`: Métricas de la línea base.