import re
import pdfplumber


def extraer_texto_pdf(ruta_pdf):

    paginas = []

    with pdfplumber.open(ruta_pdf) as pdf:

        for pagina in pdf.pages:

            texto = pagina.extract_text()

            if texto:
                paginas.append(texto)

    return "\n".join(paginas)


def extraer_cuenta_y_saldo(texto):

    lineas = texto.splitlines()

    for linea in lineas:

        if "Nuestro" not in linea:
            continue

        cuenta_match = re.search(
            r"(\d{6,15})-\d+",
            linea
        )

        # Si no encontró cuenta, esta línea no sirve
        if not cuenta_match:
            continue

        cuenta = cuenta_match.group(1)

        numeros = re.findall(
            r"\d[\d,]*\.\d{2}",
            linea
        )

        saldo = 0.0

        if numeros:
            saldo = float(
                numeros[-1].replace(",", "")
            )

        return {
            "cuenta": cuenta,
            "saldo": saldo,
            "linea": linea
        }

    return {
        "cuenta": "",
        "saldo": 0.0,
        "linea": ""
    }


def leer_pdf(ruta_pdf):

    texto = extraer_texto_pdf(ruta_pdf)

    return extraer_cuenta_y_saldo(texto)