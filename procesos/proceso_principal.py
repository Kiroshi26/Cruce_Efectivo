from procesos.lector_carpetas import (
    buscar_pdfs,
    obtener_anios_disponibles,
    obtener_meses_disponibles
)

from procesos.cuentas_bancarias import (
    leer_archivo_ctasbanc
)

from procesos.extractor_pdf import leer_pdf
from procesos.exportador_excel import exportar_excel
from datetime import datetime

MESES_CARPETA = {
    1: "01_ENE",
    2: "02_FEB",
    3: "03_MAR",
    4: "04_ABR",
    5: "05_MAY",
    6: "06_JUN",
    7: "07_JUL",
    8: "08_AGO",
    9: "09_SEP",
    10: "10_OCT",
    11: "11_NOV",
    12: "12_DIC",
}

def seleccionar_anio():

    anios = obtener_anios_disponibles()

    print("\nAños disponibles:\n")

    for i, anio in enumerate(
        anios,
        start=1
    ):
        print(f"{i}. {anio}")

    ultimo = len(anios)

    opcion = input(
        f"\nSeleccione año "
        f"[Enter = {anios[-1]}]: "
    ).strip()

    if not opcion:
        return anios[-1]

    return anios[int(opcion) - 1]


def seleccionar_mes(anio):

    meses = obtener_meses_disponibles(
        anio
    )

    print("\nMeses disponibles:\n")

    for i, mes in enumerate(
        meses,
        start=1
    ):
        print(f"{i}. {mes}")

        opcion = input(
        f"\nSeleccione período "
        f"[Enter = {meses[-1]}]: "
    ).strip()

    if not opcion:
        return meses[-1]

    return meses[int(opcion) - 1]


def ejecutar(
    criterio=None,
    anio=None,
    periodo=None,
    archivo_ctasbanc=None,
    reportar_evento=None
):

    if criterio is None:

     criterio = input(
        "\nIngrese criterio: "
    ).strip()

    if not criterio:

     print(
        "Debe ingresar un criterio."
    )

     return
 
    
    if not anio:
      anio = seleccionar_anio()

    if not periodo:
      periodo = seleccionar_mes(anio)
      
      diccionario_cuentas = {}

    if archivo_ctasbanc:

      diccionario_cuentas = (
        leer_archivo_ctasbanc(
            archivo_ctasbanc
        )
    )

    pdfs = buscar_pdfs(
        criterio,
        anio,
        periodo
    )

    print("\nPDF encontrados:")
    print("-" * 80)

    for pdf in pdfs:
        print(pdf.name)

    print("-" * 80)
    print(
        f"Total encontrados: {len(pdfs)}"
    )

    if not pdfs:
        return

    print("\nResultados:\n")

    registros = []

    for pdf in pdfs:

        resultado = leer_pdf(pdf)

        cuenta = str(
            resultado["cuenta"]
        ).strip()

        tipo_cuenta = (
            diccionario_cuentas.get(
                cuenta,
                ""
           )
        )

        registros.append(
    {
        "Cuenta": cuenta,
        "Tipo Cuenta": tipo_cuenta,
        "Saldo Extracto": float(
            resultado["saldo"]
        ),
        "Archivo": pdf.name
    }
)

        print(
            f"Archivo : {pdf.name}"
        )

        print(
            f"Cuenta  : "
            f"{resultado['cuenta']}"
        )

        print(
            f"Saldo   : "
            f"{resultado['saldo']}"
        )

        print("-" * 80)

    archivo = exportar_excel(
        registros,
        criterio
        )

    print("\n" + "=" * 80)
    print("ARCHIVO GENERADO")
    print(archivo)
    print("=" * 80)