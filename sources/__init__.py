# template class for creating sources
from .source import Source

# implemented sources
from .championgg import Championgg
from .probuilds import Probuilds
from .opgg import Opgg

SOURCES = [
    # temporarily disabled since championgg source needs an update to the new web site
    # Championgg(),
    Probuilds(),
    Opgg()
]
