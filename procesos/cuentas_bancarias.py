import pandas as pd


def validar_columnas(df):

    columnas = {
        str(col).strip().upper()
        for col in df.columns
    }

    faltantes = []

    if "DESCRIPCION" not in columnas:
        faltantes.append("DESCRIPCION")

    if "CUENTA CONTABLE" not in columnas:
        faltantes.append("CUENTA CONTABLE")

    if faltantes:

        raise ValueError(
            "El archivo no contiene las columnas requeridas: "
            + ", ".join(faltantes)
        )


def construir_diccionario(df):

    col_cuenta, col_descripcion = (
        detectar_columnas(df)
    )

    if not col_cuenta:

        raise ValueError(
            "No fue posible identificar la columna de cuentas."
        )

    if not col_descripcion:

        raise ValueError(
            "No fue posible identificar la columna de descripción."
        )

    resultado = {}

    for _, fila in df.iterrows():

     valor = fila[col_cuenta]

    try:
           cuenta = str(
           int(float(valor))
    ).strip()
            
            
    except Exception:
           cuenta = str(valor).strip() 

    descripcion = str(
        fila[col_descripcion]
        ).strip()

    if cuenta:

     resultado[cuenta] = descripcion

    print(
        "[CTASBANC]",
        cuenta,
        "=>",
        descripcion
    )

    return resultado


def leer_archivo_ctasbanc(ruta_archivo):

    df_raw = pd.read_excel(
        ruta_archivo,
        engine="openpyxl",
        header=None
    )

    fila_encabezado = None

    for indice, fila in df_raw.iterrows():

        valores = [
            str(valor).strip().upper()
            for valor in fila
        ]

        if (
            "DESCRIPCION" in valores
            and "CUENTA CONTABLE" in valores
        ):
            fila_encabezado = indice
            break

    if fila_encabezado is None:

        raise ValueError(
            "No se encontraron las columnas DESCRIPCION y CUENTA CONTABLE en el archivo."
        )

    df = pd.read_excel(
        ruta_archivo,
        engine="openpyxl",
        header=fila_encabezado
    )

    validar_columnas(df)

    return construir_diccionario(df)

def detectar_columnas(df):

    columna_cuenta = None
    columna_descripcion = None

    for columna in df.columns:

        serie = (
            df[columna]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # columna cuenta
        cantidad_cuentas = (
            serie.str.fullmatch(r"\d{8,20}")
            .fillna(False)
            .sum()
        )

        if cantidad_cuentas > 5:
            columna_cuenta = columna

        texto = " ".join(
            serie.head(100)
        ).upper()

        if (
            "AHORRO" in texto
            or "CORRIENTE" in texto
            or "FIDU" in texto
        ):
            columna_descripcion = columna

    return columna_cuenta, columna_descripcion