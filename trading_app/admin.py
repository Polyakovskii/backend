from django.contrib import admin
from trading_app.models import Item, WatchList, Currency, Inventory
# Register your models here.

admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(Currency)
admin.site.register(Inventory)