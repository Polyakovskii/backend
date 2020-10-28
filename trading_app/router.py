from rest_framework.routers import SimpleRouter

from trading_app.views import (
    UserView,
    CurrencyView,
    WatchListView,
    InventoryView,
    OfferView,
    TradeView,
    ItemView
)

router = SimpleRouter()
router.register(r'users', UserView)
router.register(r'currencies', CurrencyView)
router.register(r'watchlist', WatchListView, basename='watchlist')
router.register(r'inventory', InventoryView, basename='inventory')
router.register(r'offers', OfferView, basename='offers')
router.register(r'trades', TradeView, basename='trades')
router.register(r'items', ItemView)
