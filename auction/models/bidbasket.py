from django.db import models
from django.utils.translation import ugettext_lazy as _
from auction.models.bases import BaseBidBasket
class BidBasket(BaseBidBasket):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid basket')
        verbose_name_plural = _('Bid baskets')