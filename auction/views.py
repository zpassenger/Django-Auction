from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import auction.models
import auction.forms
from auction.utils.generic import get_or_create_bidbasket

class AuctionListView(ListView):
    """
    View for displaying auctions.
    """
    
    model = auction.models.Auction

class AuctionView(DetailView):
    """
    View for displaying auction lots.
    """
    
    model = auction.models.Auction
    
    def get_context_data(self, **kwargs):
        context = super(AuctionView, self).get_context_data(**kwargs)
        object_type = ContentType.objects.get_for_model(self.object)
        context['object_list'] = auction.models.Lot.objects.filter(content_type__pk=object_type.pk,
                                                                    object_id=self.object.pk).all()
        return context

class LotDetailView(SingleObjectMixin, FormView):
    """
    View for display lot details.
    """

    model = auction.models.Lot
    form_class = auction.forms.BidForm
    
    def __init__(self, *args, **kwargs):
        self.success_url = reverse('bids')
        return super(LotDetailView, self).__init__(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super(LotDetailView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save_bid(self.request)
        return super(LotDetailView, self).form_valid(form)

class BidListView(ListView):
    """
    View for displaying bids.
    """
    
    model = auction.models.BidItem

class BidDetailView(DetailView):
    """
    View for display information about a bid.
    """
    
    model = auction.models.BidItem
    action = None
    
    def dispatch(self, request, *args, **kwargs):
        if not self.action:
            return super(BidDetailView, self).dispatch(request, *args, **kwargs)
        if self.action in self.http_method_names:
            handler = getattr(self, self.action, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        bidbasket = get_or_create_bidbasket(self.request)
        item_id = self.kwargs.get('bid_id')
        bidbasket.delete_bid(item_id)
        return HttpResponseRedirect(reverse('bids'))