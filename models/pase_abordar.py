from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PaseAbordar:
    id_pase: Optional[int]
    id_reservacion: int
    hora_abordaje: datetime
    qr_data: Optional[str] = None
