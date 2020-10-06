from django.contrib import admin
from trading_app.models import Item, WatchList, Currency
# Register your models here.

admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(Currency)
