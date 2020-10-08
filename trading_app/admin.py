from django.contrib import admin
from trading_app.models import Item, WatchList, Currency, Inventory, Offer, Trade
# Register your models here.

admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(Currency)
admin.site.register(Inventory)
admin.site.register(Offer)
admin.site.register(Trade)