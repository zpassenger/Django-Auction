from django.conf.urls.defaults import patterns, include, url
import auction.views

urlpatterns = patterns('',
    url(r'^$', auction.views.AuctionListView.as_view(), name='auctions'),
    url(r'^bids/$', auction.views.BidListView.as_view(), name='bids'),
    url(r'^bids/delete/(?P<bid_id>\d+)/$', auction.views.BidDetailView.as_view(action="delete"), name='delete_bid'),
    url(r'^auction/(?P<slug>[0-9A-Za-z-_.]+)/$', auction.views.AuctionView.as_view(), name='auction'),
    url(r'^auction/(?P<auction_slug>[0-9A-Za-z-_.]+)/lot/(?P<slug>[0-9A-Za-z-_.//]+)/(?P<pk>\d+)/$', auction.views.LotDetailView.as_view(), name='lot'),
)