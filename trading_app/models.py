from django.db import models
from django.contrib.auth.models import User


# Create your models here.
TransactionType = {
    1: "purchase",
    2: "sale"
}
OrderType = {
    1: "market",
    2: "limit",
    3: "stop-loss"
}


class Currency(models.Model):

    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128, unique=True)

    is_active = models.BooleanField(default=True)


class Item(models.Model):

    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=8, unique=True)
    logo = models.URLField(max_length=200)

    actual_price = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)

    details = models.TextField(blank=True, null=True)


class WatchList(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('user', 'item')


class Price(models.Model):

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)

    price = models.DecimalField(max_digits=7, decimal_places=2)

    buy = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sell = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)


class Offer(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    entry_quantity = models.IntegerField()
    quantity = models.IntegerField()

    order_type = models.PositiveSmallIntegerField(choices=OrderType.items())
    transaction_type = models.PositiveSmallIntegerField(choices=TransactionType.items())

    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    is_active = models.BooleanField(default=True)


class Trade(models.Model):

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade'
    )
    buyer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade'
    )

    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)

    trade_type = models.PositiveSmallIntegerField(choices=OrderType.items())

    description = models.TextField(blank=True, null=True)

    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='offer_trade',
        related_query_name='offer_trade',
    )


class Inventory(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='inventory')

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    quantity = models.IntegerField()
    reserved_quantity = models.IntegerField()

    class Meta:
        db_table = 'inventory'
        unique_together = ('user', 'item')
