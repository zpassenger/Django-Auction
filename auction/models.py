from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic.polymorphic_model import PolymorphicModel
from django.contrib.auth.models import User
import auction.basemodels

class Auction(auction.basemodels.BaseAuction):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')

class Lot(auction.basemodels.BaseAuctionLot):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction lot')
        verbose_name_plural = _('Auction lots')

class BidBasket(auction.basemodels.BaseBidBasket):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid basket')
        verbose_name_plural = _('Bid baskets')

class BidItem(auction.basemodels.BaseBidItem):
    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid item')
        verbose_name_plural = _('Bid items')