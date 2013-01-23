import auction.models.bases
from django.test import TestCase
from django.template.defaultfilters import slugify
import datetime
import auction.utils.generic
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

class Mock(object):
    pass

class TestBaseClassMixin(object):
    model = None
    base_class = None
    def test_base_class(self):
        if self.model and self.base_class:
            self.assertEquals(self.model.__bases__[0].__name__, self.base_class)
    

class ModelTestMixin(TestBaseClassMixin):
    model = None
    attributes = []
    expected_unicode_set = None
    expected_unicode = None
    app_label = ''
    verbose_name = ''
    verbose_name_plural = ''
    
    def test_attributes(self):
        """
        Test for expected attributes.
        """
        a = self.model()
        for attr in self.attributes:
            self.assertTrue(hasattr(a, attr), 'Has attribute %s' % attr)

    def test_meta(self):
        meta = self.model.Meta
        self.assertFalse(meta.abstract)
        self.assertEquals(meta.app_label, self.app_label)
        self.assertEquals(meta.verbose_name, self.verbose_name)
        self.assertEquals(meta.verbose_name_plural, self.verbose_name_plural)

    def test_unicode(self):
        if self.expected_unicode and self.expected_unicode_set:
            a = self.model()
            for attribute,val in self.unicode_set:
                setattr(a, attribute, val)
            self.assertEqual(a.__unicode__(), self.expected_unicode)

class BaseAuctionModelTests(TestCase, ModelTestMixin):
    attributes = [
        'name',
        'slug',
        'start_date',
        'end_date',
        'active',
        'total_bids',
        'date_added',
        'last_modified',
        '__unicode__'
    ]
    model = auction.models.bases.BaseAuction
    app_label = 'auction'
    verbose_name = 'Auction'
    verbose_name_plural = 'Auctions'
    base_class = 'PolymorphicModel'
    expected_unicode = 'foo'
    unicode_set = (
        ('name', 'foo'),
    )

class BaseAuctionLotModelTests(TestCase, ModelTestMixin):
    attributes = [
        'name',
        'slug',
        'active',
        #'auction',
        'date_added',
        'last_modified',
        '__unicode__'
    ]
    model = auction.models.bases.BaseAuctionLot
    app_label = 'auction'
    verbose_name = 'Auction lot'
    verbose_name_plural = 'Auction lots'
    base_class = 'PolymorphicModel'
    expected_unicode = 'foo'
    unicode_set = (
        ('name', 'foo'),
    )

class BaseBidBasketModelTests(TestCase, ModelTestMixin):
    attributes = [
        #'user',
        'date_added',
        'last_modified',
        'add_bid',
        'update_bid',
        'delete_bid',
        'empty',
        'total_bids',
    ]
    model = auction.models.bases.BaseBidBasket
    app_label = 'auction'
    verbose_name = 'Bid basket'
    verbose_name_plural = 'Bid baskets'
    base_class = 'Model'

class BaseBidItemModelTests(TestCase, ModelTestMixin):
    attributes = [
        #'bid_basket',
        #'lot',
        'amount',
        'is_locked',
    ]
    model = auction.models.bases.BaseBidItem
    app_label = 'auction'
    verbose_name = 'Bid item'
    verbose_name_plural = 'Bid items'
    base_class = 'Model'

class AuctionModelTests(TestCase, TestBaseClassMixin):
    model = auction.models.Auction
    base_class = 'BaseAuction'

class LotModelTests(TestCase, TestBaseClassMixin):
    model = auction.models.Lot
    base_class = 'BaseAuctionLot'

class BidBasketModelTests(TestCase, TestBaseClassMixin):
    model = auction.models.BidBasket
    base_class = 'BaseBidBasket'
    
    def setUp(self):
        self.user = User.objects.create_superuser('fubar', 'fubar@example.com', 'password')
        self.user2 = User.objects.create_superuser('randomperson', 'randomperson@example.com', 'somepassword')

        now = auction.utils.generic.get_current_time()
        auction_name = 'Cool auction'
        auction_name2 = 'Awesome auction'
        self.auction,created = auction.models.Auction.objects.get_or_create(name=auction_name,
                                                         slug=slugify(auction_name),
                                                         start_date=now,
                                                         end_date=now + datetime.timedelta(365),
                                                         active=True,
                                                         total_bids=0)

        self.auction2,created = auction.models.Auction.objects.get_or_create(name=auction_name2,
                                                      slug=slugify(auction_name2),
                                                      start_date=now,
                                                      end_date=now + datetime.timedelta(365),
                                                      active=True,
                                                      total_bids=0)
        lot_name = 'Foo bar'
        lot_name2 = 'some item'
        lot_name3 = 'cool item'
        ct = ContentType.objects.get_for_model(self.auction)
        self.lot,created = auction.models.Lot.objects.get_or_create(name=lot_name,
                                                            slug=slugify(lot_name),
                                                            active=True,
                                                            content_type=ct,
                                                            object_id=self.auction.pk)

        self.lot2,created = auction.models.Lot.objects.get_or_create(name=lot_name2,
                                                            slug=slugify(lot_name2),
                                                            active=True,
                                                            content_type=ct,
                                                            object_id=self.auction.pk)

        self.lot3,created = auction.models.Lot.objects.get_or_create(name=lot_name3,
                                                            slug=slugify(lot_name3),
                                                            active=True,
                                                            content_type=ct,
                                                            object_id=self.auction2.pk)
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        
        self.request2 = Mock()
        setattr(self.request2, 'user', self.user2)
    
    def test_add_bid(self):
        """
        Test that adding a bid to the bid basket actually works.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        biditem = auction.models.BidItem.objects.filter(bid_basket=bidbasket)[0]
        self.assertEquals(biditem.lot.name, 'Foo bar')
    
    def test_update_bid(self):
        """
        Test that updating a bid works.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        biditem = auction.models.BidItem.objects.filter(bid_basket=bidbasket)[0]
        self.assertEquals(biditem.amount, Decimal('42.00'))
        
        biditem = bidbasket.update_bid(biditem.pk, '69.69')
        self.assertEquals(biditem.amount, Decimal('69.69'))
    
    def test_update_bid_with_multiple_bid_items(self):
        """
        Test that updating a bid works when a bid basket has multiple bid items.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        bidbasket.add_bid(self.lot2, '1.00')
        bidbasket.add_bid(self.lot3, '5.00')
        biditem_1 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot)
        biditem_2 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot2)
        biditem_3 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot3)
        self.assertEquals(biditem_1.amount, Decimal('42.00'))
        self.assertEquals(biditem_2.amount, Decimal('1.00'))
        self.assertEquals(biditem_3.amount, Decimal('5.00'))
        
        bidbasket.update_bid(biditem_1.pk, '40.00')
        bidbasket.update_bid(biditem_2.pk, '10.00')
        bidbasket.update_bid(biditem_3.pk, '50.00')
        biditem_1 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot)
        biditem_2 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot2)
        biditem_3 = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot3)
        self.assertEquals(biditem_1.amount, Decimal('40.00'))
        self.assertEquals(biditem_2.amount, Decimal('10.00'))
        self.assertEquals(biditem_3.amount, Decimal('50.00'))
    
    def test_delete_bid(self):
        """
        Test that deleting a bid works.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        biditem = auction.models.BidItem.objects.get(bid_basket=bidbasket)
        self.assertEquals(biditem.lot.name, 'Foo bar')
        
        bidbasket.delete_bid(biditem.pk)
        
        biditem = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertFalse(biditem)
    
    def test_delete_bid_with_multiple_bid_items(self):
        """
        Test that deleting a single bid works when there are multiple bid items in a bid basket.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        bidbasket.add_bid(self.lot2, '100.00')
        bidbasket.add_bid(self.lot3, '110.00')
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertEquals(len(biditems), 3)
        
        biditem = auction.models.BidItem.objects.get(bid_basket=bidbasket, lot=self.lot2)
        
        bidbasket.delete_bid(biditem.pk)
        
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertEquals(len(biditems), 2)
    
    def test_empty(self):
        """
        Test that calling empty on a bid basket removes all bids from it.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        bidbasket.add_bid(self.lot2, '100.00')
        bidbasket.add_bid(self.lot3, '110.00')
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertEquals(len(biditems), 3)

        bidbasket.empty()
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertFalse(biditems)
    
    def test_add_bid_with_multiple_users(self):
        """
        Test that bidbasket functions correctly when there are multiple users and
        bid baskets in the database.
        """
        bidbasket_1 = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket_2 = auction.utils.generic.get_or_create_bidbasket(self.request2)
        
        bidbasket_1.add_bid(self.lot, '5.00')
        bidbasket_1.add_bid(self.lot2, '15.00')
        bidbasket_2.add_bid(self.lot, '25.00')
        
        biditems_1 = auction.models.BidItem.objects.filter(bid_basket=bidbasket_1)
        biditems_2 = auction.models.BidItem.objects.filter(bid_basket=bidbasket_2)
        
        self.assertEqual(len(biditems_1), 2)
        self.assertEqual(len(biditems_2), 1)
        
        bidbasket_1.update_bid(biditems_1[0].pk, '55')
        biditems_1 = auction.models.BidItem.objects.filter(bid_basket=bidbasket_1)
        biditem = auction.models.BidItem.objects.get(pk=biditems_1[0].pk)
        self.assertEqual(biditem.amount, Decimal('55.00'))
        
        bidbasket_2.empty()
        biditems_1 = auction.models.BidItem.objects.filter(bid_basket=bidbasket_1)
        biditems_2 = auction.models.BidItem.objects.filter(bid_basket=bidbasket_2)
        self.assertEqual(len(biditems_1), 2)
        self.assertEqual(len(biditems_2), 0)
    
    def test_add_bid_to_inactive_lot(self):
        now = auction.utils.generic.get_current_time()
        auction_name = 'whatever auction'
        a,created = auction.models.Auction.objects.get_or_create(name=auction_name,
                                                                 slug=slugify(auction_name),
                                                                 start_date=now,
                                                                 end_date=now + datetime.timedelta(365),
                                                                 active=True,
                                                                 total_bids=0)
        
        lot_name = 'whatever'
        ct = ContentType.objects.get_for_model(a)
        lot,created = auction.models.Lot.objects.get_or_create(name=lot_name,
                                                               slug=slugify(lot_name),
                                                               active=False,
                                                               content_type=ct,
                                                               object_id=a.pk)
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        self.assertFalse(bidbasket.add_bid(lot, '42.00'))
    
    def test_update_bid_locked_biditem(self):
        """
        Test that an attempt at updating a bid when biditem is locked fails.
        """
        now = auction.utils.generic.get_current_time()
        auction_name = 'whatever auction'
        a,created = auction.models.Auction.objects.get_or_create(name=auction_name,
                                                                 slug=slugify(auction_name),
                                                                 start_date=now,
                                                                 end_date=now + datetime.timedelta(365),
                                                                 active=True,
                                                                 total_bids=0)
        
        lot_name = 'whatever'
        ct = ContentType.objects.get_for_model(a)
        lot,created = auction.models.Lot.objects.get_or_create(name=lot_name,
                                                               slug=slugify(lot_name),
                                                               active=True,
                                                               content_type=ct,
                                                               object_id=a.pk)
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(lot, '42.00')
        
        a.end_date = now - datetime.timedelta(365)
        a.save()
        
        biditem = auction.models.BidItem.objects.get(bid_basket=bidbasket)
        biditem = bidbasket.update_bid(biditem.pk, '50')
        self.assertEquals(biditem.amount, Decimal('42.00'))
    
    def test_delete_bid_locked_biditem(self):
        """
        Test that attempting to delete a bid when biditem is locked fails.
        """
        now = auction.utils.generic.get_current_time()
        auction_name = 'whatever auction'
        a,created = auction.models.Auction.objects.get_or_create(name=auction_name,
                                                                 slug=slugify(auction_name),
                                                                 start_date=now,
                                                                 end_date=now + datetime.timedelta(365),
                                                                 active=True,
                                                                 total_bids=0)

        lot_name = 'whatever'
        ct = ContentType.objects.get_for_model(a)
        lot,created = auction.models.Lot.objects.get_or_create(name=lot_name,
                                                               slug=slugify(lot_name),
                                                               active=True,
                                                               content_type=ct,
                                                               object_id=a.pk)
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(lot, '42.00')

        a.end_date = now - datetime.timedelta(365)
        a.save()

        biditem = auction.models.BidItem.objects.get(bid_basket=bidbasket)
        biditem = bidbasket.delete_bid(biditem.pk)
        self.assertTrue(biditem)
    
    def test_empty_bid_locked_biditem(self):
        """
        Test that attempting to empty a bidbasket when biditem is locked fails.
        """
        now = auction.utils.generic.get_current_time()
        auction_name = 'whatever auction'
        a,created = auction.models.Auction.objects.get_or_create(name=auction_name,
                                                                 slug=slugify(auction_name),
                                                                 start_date=now,
                                                                 end_date=now + datetime.timedelta(365),
                                                                 active=True,
                                                                 total_bids=0)

        lot_name = 'whatever'
        ct = ContentType.objects.get_for_model(a)
        lot,created = auction.models.Lot.objects.get_or_create(name=lot_name,
                                                               slug=slugify(lot_name),
                                                               active=True,
                                                               content_type=ct,
                                                               object_id=a.pk)
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(lot, '42.00')

        a.end_date = now - datetime.timedelta(365)
        a.save()

        biditem = auction.models.BidItem.objects.get(bid_basket=bidbasket)
        bidbasket.empty()
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertEqual(len(biditems), 1)
    
    def test_update_bid_deletes_at_zero(self):
        """
        Test that bids are deleted from bidbasket if amount is zero.
        """
        bidbasket = auction.utils.generic.get_or_create_bidbasket(self.request)
        bidbasket.add_bid(self.lot, '42.00')
        biditem = auction.models.BidItem.objects.filter(bid_basket=bidbasket)[0]
        self.assertEquals(biditem.amount, Decimal('42.00'))
        
        bidbasket.update_bid(biditem.pk, 'asdf')
        biditems = auction.models.BidItem.objects.filter(bid_basket=bidbasket)
        self.assertEqual(len(biditems), 0)

        

class BidItemModelTests(TestCase, TestBaseClassMixin):
    model = auction.models.BidItem
    base_class = 'BaseBidItem'