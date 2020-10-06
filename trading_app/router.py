from rest_framework.routers import SimpleRouter
from trading_app.views import UserView

router = SimpleRouter()
router.register('users', UserView)
