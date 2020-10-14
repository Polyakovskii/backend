from django_filters import rest_framework as filters
from trading_app.models import Offer, Trade, Inventory


TransactionType = (
    (1, "purchase"),
    (2, "sale")
)
OrderType = (
    (1, "market"),
    (2, "limit"),
    (3, "stop-loss")
)


class OfferFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    order_type = filters.ChoiceFilter(choices=OrderType)
    transaction_type = filters.ChoiceFilter(choices=TransactionType)

    class Meta:
        model = Offer
        fields = (
            'user',
            'item',
            'quantity',
            'order_type',
            'transaction_type',
            'min_price',
            'max_price'
        )


class TradeFilter(filters.FilterSet):
    min_unit_price = filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    max_unit_price = filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    min_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    trade_type = filters.ChoiceFilter(choices=OrderType)

    class Meta:
        model = Trade
        fields = (
            'item',
            'seller',
            'buyer',
            'min_quantity',
            'max_quantity',
            'trade_type',
            'min_unit_price',
            'max_unit_price'
        )


class InventoryFilter(filters.FilterSet):
    min_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='lte')

    class Meta:
        model = Inventory
        fields = ('item', 'min_quantity', 'max_quantity', )
