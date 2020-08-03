# template class for creating sources
from .source import Source

# implemented sources
from .championgg import Championgg
from .probuilds import Probuilds
from .opgg import Opgg

SOURCES = [
    Championgg(),
    Probuilds(),
    Opgg()
]
