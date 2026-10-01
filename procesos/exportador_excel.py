from pathlib import Path
import pandas as pd

RUTA_PRUEBAS = Path(
    r"C:\Proyectos\Pruebas_Plataforma\Efectivo"
)

def exportar_excel(registros, criterio):

    RUTA_PRUEBAS.mkdir(
        parents=True,
        exist_ok=True
    )

    archivo_salida = (
        RUTA_PRUEBAS /
        f"Cruce_Efectivo_{criterio}.xlsx"
    )

    df = pd.DataFrame(registros)

    df.to_excel(
        archivo_salida,
        index=False
    )

    return archivo_salida