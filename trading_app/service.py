from django.shortcuts import get_object_or_404
from trading_app.models import Trade, Offer, Inventory


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
    buyer_offer.save(update_fields=('is_active', 'quantity'))
    seller_offer.quantity -= quantity
    if seller_offer.quantity == 0:
        seller_offer.is_active = False
    seller_offer.save(update_fields=('is_active', 'quantity'))
    buyer_inventory = buyer_offer.user.inventory.get_or_create(
        item=buyer_offer.item,
        defaults={
            'quantity': 0,
            'user': buyer_offer.user,
            'reserved_quantity': 0
        }
    )
    buyer_inventory.quantity += quantity
    buyer_inventory.save(update_fields=('quantity', ))
    seller_inventory = get_object_or_404(Inventory, item=seller_offer.item, user=seller_offer.user)
    seller_inventory.quantity -= quantity
    seller_inventory.reserved_quantity -= quantity
    if seller_inventory.quantity == 0:
        seller_inventory.delete()
    else:
        seller_inventory.save()
