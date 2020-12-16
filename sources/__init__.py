# template class for creating sources
from .source import Source

# implemented sources
from .championgg import Championgg
from .probuilds import Probuilds
from .opgg import Opgg
from .metasrc import Metasrc

SOURCES = [
    Championgg(),
    Probuilds(),
    Opgg(),
    # Metasrc()
]
