from django.db import models
from django.utils.translation import ugettext_lazy as _

from auction.models.bases import BaseAuction

class Auction(BaseAuction):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')