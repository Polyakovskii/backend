from rest_framework.routers import SimpleRouter
from trading_app.views import UserView, CurrencyView, WatchListView

router = SimpleRouter()
router.register(r'users', UserView)
router.register(r'currencies', CurrencyView)
router.register(r'watchlist', WatchListView, basename='watchlist')
