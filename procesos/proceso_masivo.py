from procesos.lector_carpetas import (
    obtener_ruta_periodo
)

from procesos.proceso_principal import ejecutar


def obtener_criterios(
    anio,
    periodo
):

    ruta = obtener_ruta_periodo(
        anio,
        periodo
    )

    criterios = set()

    for pdf in ruta.glob("*.pdf"):

        nombre = pdf.stem

        if "-" not in nombre:
            continue

        criterio = (
            nombre
            .split("-")[-1]
            .strip()
        )

        if criterio:
            criterios.add(criterio)

    return sorted(
        criterios,
        key=lambda x: (
            len(x),
            x
        )
    )


def ejecutar_masivo(
    anio,
    periodo,
    archivo_ctasbanc,
    reportar_evento=None
):

    criterios = obtener_criterios(
        anio,
        periodo
    )

    total = len(criterios)

    archivos_generados = []

    if reportar_evento:

        reportar_evento(
            "INICIO",
            (
                f"Se encontraron "
                f"{total} criterios."
            ),
            5,
        )

    for indice, criterio in enumerate(
        criterios,
        start=1
    ):

        progreso = int(
            (indice / total) * 100
        )

        if reportar_evento:

            reportar_evento(
                "PROCESANDO",
                (
                    f"[{indice}/{total}] "
                    f"Criterio {criterio}"
                ),
                progreso,
            )

        try:

            archivo = ejecutar(
                criterio=criterio,
                anio=anio,
                periodo=periodo,
                archivo_ctasbanc=archivo_ctasbanc,
                reportar_evento=reportar_evento,
            )

            if archivo:

                archivos_generados.append(
                    str(archivo)
                )

        except Exception as error:

            if reportar_evento:

                reportar_evento(
                    "ERROR",
                    (
                        f"Error en "
                        f"{criterio}: {error}"
                    ),
                    progreso,
                )

    if reportar_evento:

        reportar_evento(
            "FINALIZADO",
            (
                f"Generados "
                f"{len(archivos_generados)} "
                f"archivos."
            ),
            100,
        )

    return archivos_generados