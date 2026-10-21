import pandas as pd


def validar_columnas(df):

    columnas = {
        str(col).strip().upper()
        for col in df.columns
    }

    faltantes = []

    requeridas = [
        "CUENTA CONTABLE",
        "DESCRIPCION",
        "NOMBRE ENTIDAD",
        "MONEDA"
    ]

    for columna in requeridas:

        if columna not in columnas:
            faltantes.append(columna)

    if faltantes:

        raise ValueError(
            "El archivo no contiene las columnas requeridas: "
            + ", ".join(faltantes)
        )


def construir_diccionario(df):

    columnas = {
        str(col).strip().upper(): col
        for col in df.columns
    }

    print("\nCOLUMNAS DISPONIBLES:")
    print(columnas)

    col_cuenta = columnas["CUENTA CONTABLE"]
    col_descripcion = columnas["DESCRIPCION"]
    col_entidad = columnas["NOMBRE ENTIDAD"]
    col_moneda = columnas["MONEDA"]

    resultado = {}

    for _, fila in df.iterrows():

        valor = fila[col_cuenta]

        try:

            cuenta = str(
                int(float(valor))
            )

        except Exception:

            cuenta = str(valor).strip()

        if (
            not cuenta
            or cuenta.lower() == "nan"
        ):
            continue

        descripcion = str(
            fila[col_descripcion]
        ).strip()

        nombre_entidad = str(
            fila[col_entidad]
        ).strip()

        moneda = str(
            fila[col_moneda]
        ).strip()

        resultado[cuenta] = {
            "tipo_cuenta": descripcion,
            "nombre_entidad": nombre_entidad,
            "moneda": moneda
        }

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
            "No se encontraron las columnas DESCRIPCION y CUENTA CONTABLE."
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

    return (
        columna_cuenta,
        columna_descripcion
    )