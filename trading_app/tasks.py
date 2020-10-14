from celery import shared_task
from trading_app.models import Offer
from trading_app.service import make_trade
from trading_app.enums import TransactionTypeEnum


@shared_task
def find_trades():
    buy_offers = Offer.objects.select_related(
        'user',
        'item'
    ).filter(transaction_type=TransactionTypeEnum.purchase.value, is_active=True)

    for buyer_offer in buy_offers:
        sell_offers = Offer.objects.select_related('user', 'item').filter(
            transaction_type=TransactionTypeEnum.sale.value,
            price__lte=buyer_offer.price,
            item=buyer_offer.item,
            is_active=True,
        ).order_by('-price').exclude(user=buyer_offer.user)

        if sell_offers.exists():
            make_trade(buyer_offer=buyer_offer, seller_offer=sell_offers[0])
