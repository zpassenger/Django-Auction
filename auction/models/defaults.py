from django.db import models
from django.utils.translation import ugettext_lazy as _
from auction.models.bases import BaseAuctionLot
class Lot(BaseAuctionLot):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction lot')
        verbose_name_plural = _('Auction lots')