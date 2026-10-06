from pathlib import Path


RUTA_BASE = (
    r"\\sbmdebns03\VP SERV CORP\VP_SERV_CLIE\DIR_SERV_FINAN"
    r"\GCIA_SERV_CONT\Info Actual\02_Conc_Bancaria"
    r"\09_Nego_Fidu\01_Soporte Mensual"
)


def obtener_anios_disponibles():

    ruta_base = Path(RUTA_BASE)

    anios = []

    for carpeta in ruta_base.iterdir():

        if (
            carpeta.is_dir()
            and carpeta.name.isdigit()
        ):
            anios.append(carpeta.name)

    anios.sort()

    return anios


def obtener_meses_disponibles(anio):

    ruta_anio = Path(RUTA_BASE) / anio

    meses = []

    for carpeta in ruta_anio.iterdir():

        if carpeta.is_dir():

            nombre = carpeta.name

            if (
                len(nombre) >= 2
                and nombre[:2].isdigit()
            ):
                meses.append(nombre)

    meses.sort(
        key=lambda x: int(x[:2])
    )

    return meses


def obtener_ruta_periodo(
    anio,
    periodo
):

    return (
        Path(RUTA_BASE)
        / anio
        / periodo
    )


def buscar_pdfs(
    criterio,
    anio,
    periodo
):

    ruta = obtener_ruta_periodo(
        anio,
        periodo
    )

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

        if nombre.endswith(
            f"-{criterio}".upper()
        ):
            pdfs.append(archivo)

    return sorted(pdfs)