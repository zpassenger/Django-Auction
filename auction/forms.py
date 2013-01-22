from django import forms
import auction.models
import auction.utils

class BidForm(forms.Form):
    amount = forms.DecimalField()
    lot_id = forms.IntegerField()
    
    def save_bid(self, request):
        lot_id = self.data.get('lot_id')
        amount = self.data.get('amount')
        
        lot = self.get_lot(lot_id)

        bidbasket = auction.utils.get_or_create_bidbasket(request)
        return bidbasket.add_bid(lot, amount)
    
    def get_lot(self, lot_id):
        """
        For simplified extending.
        """
        return auction.models.Lot.objects.get(pk=lot_id)