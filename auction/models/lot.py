import importlib
from django.conf import settings
from auction.utils.loader import load_class

LOT_MODEL = getattr(settings, 'AUCTION_LOT_MODEL',
    'auction.models.defaults.Lot')

Lot = load_class(LOT_MODEL, 'AUCTION_LOT_MODEL')#getattr(importlib.import_module(LOT_MODEL[0]), LOT_MODEL[1])