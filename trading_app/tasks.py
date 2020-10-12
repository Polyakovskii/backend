from django.db.models import ObjectDoesNotExist
from trading_app.models import Trade, Offer, Inventory
from celery import shared_task


def make_trade(buyer_offer: Offer, seller_offer: Offer):
    if buyer_offer.quantity > seller_offer.quantity:
        quantity = seller_offer.quantity
    else:
        quantity = buyer_offer.quantity
    Trade.objects.create(
        item=buyer_offer.item,
        seller=seller_offer.user,
        buyer=buyer_offer.user,
        quantity=quantity,
        unit_price=seller_offer.price,
        trade_type=buyer_offer.order_type,
        seller_offer=seller_offer,
        buyer_offer=buyer_offer,
    )
    buyer_offer.quantity -= quantity
    if buyer_offer.quantity == 0:
        buyer_offer.is_active = False
    buyer_offer.save()
    seller_offer.quantity -= quantity
    if seller_offer.quantity == 0:
        seller_offer.is_active = False
    seller_offer.save()
    try:
        buyer_inventory = buyer_offer.user.inventory_set.get(item=buyer_offer.item)
    except ObjectDoesNotExist:
        buyer_inventory = Inventory.objects.create(
            item=buyer_offer.item,
            user=buyer_offer.user,
            quantity=0,
            reserved_quantity=0
        )
    buyer_inventory.quantity += quantity
    buyer_inventory.save()

    seller_inventory = seller_offer.user.inventory_set.get(item=seller_offer.item)
    seller_inventory.quantity -= quantity
    seller_inventory.reserved_quantity -= quantity
    if seller_inventory.quantity == 0:
        seller_inventory.delete()
    else:
        seller_inventory.save()


@shared_task
def find_trades():
    buy_offers = Offer.objects.filter(transaction_type=1)
    for buyer_offer in buy_offers:
        sell_offers = Offer.objects.filter(
            transaction_type=2,
            price__lte=buyer_offer.price,
            item=buyer_offer.item
        ).order_by('-price')
        if sell_offers.exists():
            make_trade(buyer_offer=buyer_offer, seller_offer=sell_offers[0])
