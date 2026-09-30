from dataclasses import dataclass

@dataclass
class RegistroExtracto:
    cuenta: str
    saldo_extracto: float
    archivo: str
    observacion: str
