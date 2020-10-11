import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('get-token')
    response = api_client.post(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_crud(authorized_client, ):
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
def test_creating_user(api_client, ):
    url = f'/api/v1/users/'
    kwargs = {'username': 'name', 'first_name': 'n', 'second_name': 'n', 'password': 'qwerty', }
    response = api_client.post(url, kwargs, format='json')
    assert response.status_code == 201
    assert response.json()['username'] == kwargs['username']


@pytest.mark.django_db
def test_user_update(api_client, create_user):
    user = create_user()
    url = f'/api/v1/users/{user.pk}/'
    api_client.force_authenticate(user=user, )
    kwargs = {'username': 'name', 'first_name': 'n', 'second_name': 'n', 'password': 'qwerty', }
    response = api_client.put(url, kwargs, follow=True, )
    assert response.status_code == 200
    assert response.json()['username'] == kwargs['username']

