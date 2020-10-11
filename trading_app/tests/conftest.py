import uuid
import pytest
from django.urls import reverse
from trading_app.models import Currency, Item, WatchList

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def authorized_client(create_user, api_client, test_password):
    url = reverse('get-token')
    user = create_user()
    password = test_password
    response = api_client.post(url, {'username': user.username, 'password': password}, format='json')
    token = 'jwt ' + response.data['token']
    api_client.force_authenticate(user=user, token=token)
    return api_client


@pytest.fixture
def create_currency():
    def make_currency(**kwargs):
        if 'code' not in kwargs:
            kwargs['code'] = 'EUR'
        if 'name' not in kwargs:
            kwargs['name'] = 'Euro'
        return Currency.objects.create(**kwargs)
    return make_currency


@pytest.fixture
def create_item(create_currency):
    def make_item(**kwargs):
        item = Item.objects.create(
            code=kwargs.get('code', 'AAPL'),
            name=kwargs.get('name', 'Apple'),
            logo=kwargs.get('logo', 'www.src.com'),
            actual_price=kwargs.get('actual_price', 10),
            currency=kwargs.get('currency', create_currency()),
        )
        return item
    return make_item


@pytest.fixture
def create_watchlist(create_item, create_user):
    watchlist = WatchList.objects.create(user=create_user(), item=create_item())
    return watchlist
