from datetime import datetime
from pathlib import Path


RUTA_BASE = (
    r"\\sbmdebns03\VP SERV CORP\VP_SERV_CLIE\DIR_SERV_FINAN"
    r"\GCIA_SERV_CONT\Info Actual\02_Conc_Bancaria"
    r"\09_Nego_Fidu\01_Soporte Mensual"
)


def obtener_ruta_periodo() -> Path:
    """
    Obtiene la última carpeta de mes disponible
    dentro del año actual.
    """

    anio_actual = str(datetime.now().year)

    ruta_anio = Path(RUTA_BASE) / anio_actual

    if not ruta_anio.exists():
        raise FileNotFoundError(
            f"No existe la carpeta del año:\n{ruta_anio}"
        )

    carpetas_mes = []

    for carpeta in ruta_anio.iterdir():

        if not carpeta.is_dir():
            continue

        nombre = carpeta.name

        # Solo carpetas tipo 01_Ene, 02_Feb, etc
        if len(nombre) >= 2 and nombre[:2].isdigit():
            carpetas_mes.append(carpeta)

    if not carpetas_mes:
        raise FileNotFoundError(
            f"No existen carpetas de meses en:\n{ruta_anio}"
        )

    carpetas_mes.sort(
        key=lambda x: int(x.name[:2])
    )

    return carpetas_mes[-1]


def buscar_pdfs(criterio: str):

    ruta = obtener_ruta_periodo()

    print("\nCarpeta encontrada:")
    print(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe la ruta:\n{ruta}"
        )

    pdfs = []

    criterio = criterio.strip()

    for archivo in ruta.glob("*.pdf"):

        nombre = archivo.stem.upper()

        # Solo archivos que TERMINAN exactamente
        # con -criterio

        if nombre.endswith(f"-{criterio}".upper()):
            pdfs.append(archivo)

    return sorted(pdfs)