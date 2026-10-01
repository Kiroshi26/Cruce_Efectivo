from procesos.lector_carpetas import buscar_pdfs
from procesos.extractor_pdf import leer_pdf
from procesos.exportador_excel import exportar_excel


def ejecutar():

    criterio = input(
        "\nIngrese criterio: "
    ).strip()

    if not criterio:
        print("Debe ingresar un criterio.")
        return

    pdfs = buscar_pdfs(criterio)

    print("\nPDF encontrados:")
    print("-" * 80)

    for pdf in pdfs:
        print(pdf.name)

    print("-" * 80)
    print(f"Total encontrados: {len(pdfs)}")

    if not pdfs:
        return

    print("\nResultados:\n")

    registros = []

    for pdf in pdfs:

        resultado = leer_pdf(pdf)

        registros.append(
            {
                "Cuenta": resultado["cuenta"],
                "Saldo Extracto": resultado["saldo"],
                "Archivo": pdf.name
            }
        )

        print(f"Archivo : {pdf.name}")
        print(f"Cuenta  : {resultado['cuenta']}")
        print(f"Saldo   : {resultado['saldo']}")
        print("-" * 80)  

    archivo = exportar_excel(
        registros,
        criterio
    )

    print("\n" + "=" * 80)
    print("ARCHIVO GENERADO")
    print(archivo)
    print("=" * 80)