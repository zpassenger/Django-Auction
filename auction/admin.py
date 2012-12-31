from django.contrib import admin
import auction.models

class AuctionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class LotAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(auction.models.Auction, AuctionAdmin)
admin.site.register(auction.models.Lot, LotAdmin)
admin.site.register(auction.models.BidBasket)
admin.site.register(auction.models.BidItem)