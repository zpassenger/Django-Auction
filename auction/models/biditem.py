from django.db import models
from django.utils.translation import ugettext_lazy as _
from auction.models.bases import BaseBidItem

class BidItem(BaseBidItem):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid item')
        verbose_name_plural = _('Bid items')