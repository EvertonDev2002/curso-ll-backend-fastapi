from enum import Enum as PyEnum

class AnimeStatus(str, PyEnum):
    PLANEJO_ASSISTIR = 'planejo assistir'
    ASSISTINDO = 'assistindo'
    ASSISTIDO = 'assistido'
    PARADO = 'parado'