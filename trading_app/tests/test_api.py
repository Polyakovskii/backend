import pytest
from django.urls import reverse

#authorization test
@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('get-token')
    response = api_client.post(url)
    assert response.status_code == 400

#User CRUD tests
@pytest.mark.django_db
def test_user_list(authorized_client, ):
    url = '/api/v1/users/'
    response = authorized_client.get(url, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_retrieve(api_client, create_user):
    user = create_user()
    url = f'/api/v1/users/{user.pk}/'
    api_client.force_authenticate(user=user, )
    response = api_client.get(url, follow=True, format='json')
    assert response.status_code == 200
    assert response.json()['username'] == user.username


@pytest.mark.django_db
@pytest.mark.parametrize(
    ["user_name", "first_name", "second_name", "password", "expected"],
    [
        ("name", "n", "f", "1234", 201),
        ("", "", "", "1234", 400),
        ("", "", "", "", 400),
        ("123", "34", "3453", "", 400),
    ]
)
def test_creating_user(api_client, user_name, first_name, second_name, password, expected):
    url = f'/api/v1/users/'
    kwargs = {
        'username': user_name,
        'first_name': first_name,
        'second_name': second_name,
        'password': password,
    }
    response = api_client.post(url, kwargs, format='json')
    assert response.status_code == expected


@pytest.mark.django_db
def test_user_update(api_client, create_user):
    user = create_user()
    url = f'/api/v1/users/{user.pk}/'
    api_client.force_authenticate(user=user, )
    kwargs = {'username': 'name', 'first_name': 'n', 'second_name': 'n', 'password': 'qwerty', }
    response = api_client.put(url, kwargs, follow=True, )
    assert response.status_code == 200
    assert response.json()['username'] == kwargs['username']

# tests for currency
@pytest.mark.django_db
def test_currency_list(create_currency, authorized_client):
    url = '/api/v1/currencies/'
    currency = create_currency()
    print(currency.pk)
    response = authorized_client.get(url)
    print(response.content)
    assert response.status_code == 200
    assert response.json()[currency.pk-1]['code'] == currency.code


# tests for watchlist
@pytest.mark.django_db
def test_watchlist_list(api_client, create_watchlist):
    url = '/api/v1/watchlist/'
    watchlist = create_watchlist
    api_client.force_authenticate(user=watchlist.user)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_watchlist_retrieve(api_client, create_watchlist):
    watchlist = create_watchlist
    url = f'/api/v1/watchlist/{watchlist.item.id}/'
    api_client.force_authenticate(user=watchlist.user)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_watchlist_create(authorized_client, create_item):
    url = f'/api/v1/watchlist/'
    item = create_item()
    response = authorized_client.post(url, {'item': item.pk})
    print(response.content)
    assert response.status_code == 201


@pytest.mark.django_db
def test_watchlist_delete(api_client, create_watchlist):
    watchlist = create_watchlist
    url = f'/api/v1/watchlist/{watchlist.item.id}/'
    api_client.force_authenticate(user=watchlist.user)
    response = api_client.delete(url)
    assert response.status_code == 204


# inventory tests
@pytest.mark.django_db
def test_inventory_list(api_client, create_inventory):
    inventory = create_inventory()
    url = '/api/v1/inventory/'
    api_client.force_authenticate(user=inventory.user)
    response = api_client.get(url)
    assert response.status_code == 200


# offer tests
@pytest.mark.django_db
def test_offer_list(authorized_client):
    url = '/api/v1/offers/'
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    ["quantity", "entry_quantity", "order_type", "transaction_type", "expected"],
    [
        (10, 7, 1, 1, 201),
        (7, 10, 1, 2, 400),
        (10, 0, 1, 1, 400),
        (10, 7, 4, 2, 400),
        (10, 7, 1, 4, 400),
    ]
)
def test_offer_creation(
        api_client,
        create_inventory,
        quantity,
        entry_quantity,
        order_type,
        transaction_type,
        expected
):
    url = '/api/v1/offers/'
    inventory = create_inventory(quantity=quantity)
    api_client.force_authenticate(user=inventory.user)
    data = {
        'item': inventory.item.id,
        'entry_quantity': entry_quantity,
        'order_type': order_type,
        'transaction_type': transaction_type,
        'price': 10,
    }
    response = api_client.post(url, data)
    assert response.status_code == expected
