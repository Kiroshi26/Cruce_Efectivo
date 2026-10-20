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


def extraer_cuenta(texto):

    for linea in texto.splitlines():

        if "Nuestro" not in linea:
            continue

        cuenta_match = re.search(
            r"(\d{6,15})-\d+",
            linea
        )

        if cuenta_match:

            return (
                cuenta_match.group(1),
                linea
            )

    return "", ""


def extraer_saldo_balance(texto):
    """
    Extrae el saldo desde:

    Balance:
    6,921,690.39 C

    ignorando la naturaleza C/D.
    """

    patron = re.search(
        r"Balance:\s*([\d,]+\.\d{2})",
        texto,
        flags=re.IGNORECASE
    )

    if not patron:
        return 0.0

    return float(
        patron.group(1).replace(",", "")
    )


def extraer_cuenta_y_saldo(texto):

    cuenta, linea = extraer_cuenta(texto)

    saldo = extraer_saldo_balance(texto)

    return {
        "cuenta": cuenta,
        "saldo": saldo,
        "linea": linea
    }


def leer_pdf(ruta_pdf):

    texto = extraer_texto_pdf(ruta_pdf)

    return extraer_cuenta_y_saldo(texto)