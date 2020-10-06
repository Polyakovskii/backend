from rest_framework.routers import SimpleRouter
from trading_app.views import UserView, CurrencyView

router = SimpleRouter()
router.register(r'users', UserView, basename="users")
router.register(r'currencies', CurrencyView)
